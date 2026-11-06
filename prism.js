/* Decorative projected geometry. No network, storage, telemetry or protocol simulation. */
(function () {
  'use strict';
  const doc = document;
  const tau = Math.PI * 2;
  const palette = ['#38ff9c', '#ffc54f', '#37eaff', '#b176ff'];
  const routes = ['daarx', 'l10n', 'open', 'nexus', 'development', 'testnet', 'security', 'hardware', 'questions', 'privacy', 'family'];
  const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
  const forcedColors = window.matchMedia('(forced-colors: active)');
  let classPaused = doc.documentElement.classList.contains('motion-paused');
  let explicitMotion = null;
  let paused = classPaused || doc.body.classList.contains('motion-paused') || motionPreference.matches;
  const scenes = [];
  const clamp = (n, lo, hi) => Math.max(lo, Math.min(hi, n));

  doc.querySelectorAll('figure[data-prism-scene]').forEach(function (figure) {
    const canvas = figure.querySelector('[data-prism-canvas]');
    if (!canvas) return;
    const type = routes.includes(figure.dataset.prismScene) ? figure.dataset.prismScene : 'family';
    const buttons = Array.from(figure.querySelectorAll('button[data-prism-step]'));
    const colorIndex = type === 'l10n' || type === 'hardware' ? 1 : type === 'open' || type === 'testnet' || type === 'questions' ? 2 : type === 'nexus' || type === 'security' ? 3 : 0;
    const accent = palette[colorIndex];
    let ctx;
    try { ctx = canvas.getContext('2d', { alpha: true }); } catch (_) { ctx = null; }
    let stage = clamp(Number(figure.dataset.prismState) || 0, 0, 2);
    let frame = 0, last = -1000, frames = 0, elapsed = 0;
    let width = 0, height = 0, visible = false, failed = !ctx;
    let yaw = -.32, pitch = -.12, targetYaw = yaw, targetPitch = pitch;
    let pointerId = null, origin = null;
    let sy = 0, cy = 1, sx = 0, cx = 1, sculptureScale = 1;
    figure.dataset.prismRenderer = 'svg';
    figure.dataset.prismFrames = '0';
    figure.dataset.prismState = String(stage);
    figure.dataset.prismYaw = yaw.toFixed(4);
    figure.dataset.prismPitch = pitch.toFixed(4);

    function stop() {
      if (frame) cancelAnimationFrame(frame);
      frame = 0;
      last = -1000;
    }
    function runnable() { return !failed && !paused && visible && !doc.hidden && !forcedColors.matches; }
    function project(p) {
      const x = p[0] * cy + p[2] * sy;
      const z0 = p[2] * cy - p[0] * sy;
      const y = p[1] * cx - z0 * sx;
      const z = z0 * cx + p[1] * sx;
      const perspective = 4.5 / (4.5 - z);
      const scale = sculptureScale * perspective;
      return [width * .5 + x * scale * 1.07, height * .49 + y * scale, perspective];
    }
    function line(points, color, alpha, thickness, glow) {
      if (points.length < 2) return;
      const projected = points.map(project);
      const depth = projected.reduce((sum, p) => sum + p[2], 0) / projected.length;
      ctx.beginPath();
      projected.forEach(function (q, i) {
        if (i) ctx.lineTo(q[0], q[1]); else ctx.moveTo(q[0], q[1]);
      });
      ctx.globalAlpha = Math.min(.96, alpha * (1.04 + depth * .22));
      if (points.length > 20 && alpha > .2) {
        const a=projected[0], b=projected[Math.floor(projected.length*.46)];
        const spectrum=ctx.createLinearGradient(a[0],a[1],b[0]+1,b[1]+1);
        spectrum.addColorStop(0,color);spectrum.addColorStop(.34,palette[(colorIndex+1)%4]);
        spectrum.addColorStop(.65,palette[(colorIndex+3)%4]);spectrum.addColorStop(1,color);
        ctx.strokeStyle=spectrum;
      } else ctx.strokeStyle = color;
      ctx.lineWidth = (thickness || .75) * (.72+depth*.32);
      ctx.shadowColor = color;
      ctx.shadowBlur = glow || 0;
      ctx.stroke();
      ctx.shadowBlur = 0;
    }
    function path(fn, steps, color, alpha, thickness, glow) {
      const pts = [];
      for (let i = 0; i <= steps; i++) pts.push(fn(i / steps));
      line(pts, color, alpha, thickness, glow);
    }
    function node(p, color, radius) {
      const q = project(p);
      ctx.globalAlpha = .95;
      ctx.fillStyle = color;
      ctx.shadowColor = color;
      ctx.shadowBlur = 16;
      const r=(radius||2.2)*1.16;
      ctx.beginPath(); ctx.arc(q[0], q[1], r, 0, tau); ctx.fill();
      ctx.shadowBlur = 0;
      ctx.fillStyle='#efffff';ctx.beginPath();ctx.arc(q[0]-.3,q[1]-.4,r*.4,0,tau);ctx.fill();
      ctx.globalAlpha=.6;ctx.strokeStyle=color;ctx.lineWidth=.6;
      ctx.beginPath();ctx.moveTo(q[0]-r*3,q[1]);ctx.lineTo(q[0]+r*3,q[1]);
      ctx.moveTo(q[0],q[1]-r*3);ctx.lineTo(q[0],q[1]+r*3);ctx.stroke();
    }
    // Translucent caustic strips provide an optical surface between wire contours.
    // Quads are sorted back-to-front; specular edges remain separately legible.
    function ribbon(fn, spread, color, alpha) {
      const samples=70, left=[],right=[],quads=[];
      for(let i=0;i<=samples;i++) {
        const u=i/samples,p=fn(u),next=fn(Math.min(1,u+.003)),prev=fn(Math.max(0,u-.003));
        const dx=next[0]-prev[0],dy=next[1]-prev[1],len=Math.hypot(dx,dy)||1;
        const band=spread*(.65+.35*Math.sin(u*Math.PI));
        left.push([p[0]-dy/len*band,p[1]+dx/len*band,p[2]+band*.28]);
        right.push([p[0]+dy/len*band,p[1]-dx/len*band,p[2]-band*.28]);
      }
      for(let i=0;i<samples;i++) {
        const p=[left[i],right[i],right[i+1],left[i+1]].map(project);
        quads.push({p,depth:p.reduce((s,v)=>s+v[2],0)/4,index:i});
      }
      const p0=project(fn(.1)),p1=project(fn(.62));
      const gradient=ctx.createLinearGradient(p0[0],p0[1],p1[0]+1,p1[1]+1);
      gradient.addColorStop(0,color);gradient.addColorStop(.27,palette[1]);
      gradient.addColorStop(.52,palette[3]);gradient.addColorStop(.78,palette[2]);gradient.addColorStop(1,color);
      ctx.fillStyle=gradient;
      quads.sort((a,b)=>a.depth-b.depth).forEach(q=>{
        ctx.globalAlpha=alpha*(.5+q.depth*.5)*(.7+.3*Math.sin(q.index*.44));
        ctx.beginPath();q.p.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.closePath();ctx.fill();
      });
      line(left,color,.69,.85,2);line(right,palette[(colorIndex+2)%4],.53,.65);
    }
    function opticalSurfaces(time) {
      const seed=routes.indexOf(type),shift=time*.055+stage*.24;
      if(type==='family'||type==='development') {
        for(let j=0;j<4;j++)ribbon(u=>{const a=u*tau*(1.15+stage*.28)+j/4*tau+shift;return [Math.cos(a)*.77,(u-.5)*1.94,Math.sin(a)*.67];},.06,palette[j],.16);
      }else if(type==='l10n'){
        for(let j=0;j<3;j++)ribbon(u=>{const a=u*tau+j*.035;return [Math.sin(a)*1.12,Math.sin(a*2)*.48,Math.cos(a)*(.36+j*.07)];},.065,palette[j],.16);
      }else if(type==='privacy'){
        for(let j=0;j<4;j++)ribbon(u=>{const a=u*tau,r=(.72+j*.045)*(.8+.22*Math.cos(a*(5+stage)+shift));return [Math.cos(a)*r,Math.sin(a)*r,Math.cos(a*3+shift)*.27+j*.06];},.045,palette[j],.2);
      }else if(type==='daarx'){
        for(let j=0;j<4;j++)ribbon(u=>{const a=u*tau+j*.09;return [Math.cos(a)*(.88+j*.04),Math.sin(a)*.27,Math.sin(a)*.66];},.047,palette[j],.17);
        const vertices=[];
        for(let j=0;j<8;j++){const a=j/8*tau+stage*.23+time*.08;vertices.push([Math.cos(a)*.8,Math.sin(a*2)*.13,Math.sin(a)*.8]);}
        vertices.forEach((v,i)=>{const p=[[0,-1.02,0],v,vertices[(i+1)%8]].map(project);ctx.globalAlpha=.035+(i%3)*.018;ctx.fillStyle=palette[i%4];ctx.beginPath();p.forEach((q,k)=>k?ctx.lineTo(q[0],q[1]):ctx.moveTo(q[0],q[1]));ctx.closePath();ctx.fill();});
      }else{
        for(let j=0;j<3;j++)ribbon(u=>{
          const a=u*tau, r=.78+j*.095,warp=.045*Math.sin(a*(8+stage)+shift);
          if(type==='open')return [Math.cos(a)*r,Math.sin(a)*r,(j-1)*.56+warp];
          if(type==='hardware')return [Math.cos(a)*r*1.11,Math.sin(a)*r*.77,Math.sin(a*8+shift)*.1+(j-1)*.2];
          if(type==='security')return [Math.sin(a)*r,(-Math.cos(a)*.82-Math.pow(Math.max(0,Math.cos(a)),4)*.17)*r,(j-1)*.35+warp];
          if(type==='questions')return [Math.cos(a)*r*.88,-.1+Math.sin(a)*r*.75,Math.sin(a*3)*.23+(j-1)*.15];
          return [Math.cos(a)*r,Math.sin(a)*r*.8,Math.sin(a+j*1.1)*.48];
        },.035+stage*.007,palette[(j+seed)%4],.14);
      }
      // Fine orbital engraving, deliberately coherent rather than a particle field.
      for(let j=0;j<12;j++){
        const band=j%4,phase=Math.floor(j/4)*.045;
        path(u=>{const a=u*tau+shift*.4,r=1.01+phase+.025*Math.sin(a*(9+stage)+seed);return [Math.cos(a)*r,Math.sin(a)*(.38+band*.15),Math.sin(a+band*.7)*.38];},100,palette[band],j%4===0?.35:.19,j%4===0?.85:.5);
      }
      for(let j=0;j<4;j++){
        const a=j/4*tau+shift*.55+seed*.16;
        node([Math.cos(a)*1.04,Math.sin(a)*.68,Math.sin(a+j*.7)*.42],palette[j],1.7);
      }
    }
    function square(size, z, angle, color, alpha, thick) {
      const c = Math.cos(angle), s = Math.sin(angle);
      line([[-1,-1],[1,-1],[1,1],[-1,1],[-1,-1]].map(p => [(p[0]*c-p[1]*s)*size,(p[0]*s+p[1]*c)*size,z]), color, alpha, thick);
    }
    function crystal(time, bloom) {
      const twist = stage * .23 + time * .08;
      for (let j = 0; j < 25 + stage * 7; j++) {
        const a = j / (24 + stage * 7) * tau;
        const radius = .72 + .15 * Math.cos(a * 4 + twist);
        const top = [0,-1.02,0], bottom = [0,1.02,0];
        const side = [Math.cos(a+twist)*radius,Math.sin(a*2)*.16,Math.sin(a+twist)*radius];
        line([top,side,bottom], palette[j%4], j % 5 === 0 ? .86 : .35, j % 5 === 0 ? 1.3 : .65, j % 5 === 0 ? 5 : 0);
      }
      for (let j = 0; j < 21; j++) {
        const y = -1 + j / 10;
        const r = (1-Math.abs(y)) * .86 + .025;
        path(u => [Math.cos(u*tau+twist)*r,y,Math.sin(u*tau+twist)*r], 80, palette[j%4], .4, .7);
      }
      for (let j = 0; j < 13 + stage*3; j++) {
        const z = -.8 + j*.105;
        path(u => { const x=(u-.5)*2.7; return [x,Math.sin(x*3+z*5+time*.2)*.15 + .36*Math.cos(x*1.1),z]; }, 90, bloom ? palette[3] : palette[2], .16, .65);
      }
    }
    function cash(time) {
      const count = 19 + stage*6;
      for (let j=0;j<count;j++) {
        const offset=(j/(count-1)-.5)*.44;
        path(u => { const a=u*tau; return [Math.sin(a)*1.16,Math.sin(a*2)*.48+offset*Math.cos(a*2+time*.13),Math.cos(a)*.38+offset*Math.sin(a*3+stage*.3)]; }, 150, j%6===0 ? palette[0] : palette[1], j%6===0 ? .8 : .37, j%6===0 ? 1.3 : .65, j%6===0 ? 4 : 0);
      }
      for (let j=0;j<16;j++) {
        const a=j/16*tau;
        line([[Math.sin(a)*1.16,Math.sin(a*2)*.48-.19,Math.cos(a)*.38],[Math.sin(a)*1.16,Math.sin(a*2)*.48+.19,Math.cos(a)*.38]], palette[2], .3, .6);
      }
    }
    function gates(time) {
      for (let j=0;j<15+stage*5;j++) {
        const d=j/(14+stage*5);
        square(.94-d*.3,-.95+d*1.9,Math.sin(time*.13)*.025+stage*.06*(d-.5),j%4===0?palette[3]:palette[2],j%4===0?.8:.25,j%4===0?1.4:.7);
      }
      for(let k=0;k<4;k++) {
        const a=Math.PI/4+k*Math.PI/2;
        line([[Math.cos(a)*1.32,Math.sin(a)*1.32,-.95],[Math.cos(a)*.91,Math.sin(a)*.91,.95]],palette[1],.85,1,4);
      }
      for(let j=0;j<13;j++) {
        const d=(j-6)*.13;
        line([[-.94,d,-.95],[.94,d,-.95]],palette[0],.19,.6);
        line([[d,-.94,-.95],[d,.94,-.95]],palette[0],.19,.6);
      }
      node([0,0,1.02],palette[2],3.4);
    }
    function tension(time) {
      const n=4+stage, points=[];
      for(let i=0;i<n;i++) {const a=i/n*tau+time*.04;points.push([Math.cos(a),Math.sin(a)*.85,(i%2-.5)*.85]);}
      for(let i=0;i<n;i++) for(let j=i+1;j<n;j++) {
        const a=points[i],b=points[j];
        for(let k=-2;k<=2;k++) path(u=>{const v=1-u, bow=Math.sin(u*Math.PI)*k*.055;return [a[0]*v+b[0]*u,a[1]*v+b[1]*u+bow,a[2]*v+b[2]*u+Math.sin(u*Math.PI)*(.18+stage*.08)];},48,k===0?palette[3]:palette[2],k===0?.82:.21,k===0?1.1:.6,k===0?3:0);
      }
      points.forEach((p,i)=>{node(p,palette[i%4],3);for(let j=0;j<3;j++)path(u=>[p[0]+Math.cos(u*tau)*(.055+j*.025),p[1]+Math.sin(u*tau)*(.055+j*.025),p[2]],32,palette[3],.5,.6);});
    }
    function braid(time, family) {
      const strands=family?4:3;
      for(let j=0;j<strands;j++) for(let k=0;k<15+stage*3;k++) {
        const offset=(k-(14+stage*3)/2)*.017;
        path(u=>{const a=u*tau*(1.15+stage*.28)+j/strands*tau+time*.1;return [Math.cos(a)*(.77+offset), (u-.5)*1.94, Math.sin(a)*(.67+offset)];},120,palette[family?j:(j+stage)%4],k%4===0?.8:.36,k%4===0?1.1:.65,k%4===0?3:0);
      }
      for(let j=0;j<13;j++) {
        const u=j/12,a=u*tau*(1.15+stage*.28)+time*.1;
        path(v=>[Math.cos(a+v*tau)*.78,(u-.5)*1.94,Math.sin(a+v*tau)*.68],70,palette[j%4],.4,.7);
      }
    }
    function constellation(time) {
      for(let j=0;j<8+stage*4;j++) {
        const angle=j/(8+stage*4)*Math.PI;
        path(u=>{const a=u*tau;return [Math.cos(a)*Math.cos(angle),Math.sin(a)*.88,Math.cos(a)*Math.sin(angle)];},100,j%3===0?palette[0]:palette[2],j%3===0?.72:.25,j%3===0?1.1:.65);
      }
      for(let j=0;j<5;j++) {
        const lat=(j-2)*.32,r=Math.sqrt(1-lat*lat);
        path(u=>[Math.cos(u*tau)*r,lat,Math.sin(u*tau)*r],100,palette[3],.45,.7);
      }
      for(let j=0;j<12;j++){const a=j/12*tau+time*.04;node([Math.cos(a),Math.sin(a)*.64,Math.sin(a*3)*.45],palette[j%4],2.4);}
    }
    function shield(time) {
      for(let j=0;j<30+stage*8;j++) {
        const s=.25+j/(29+stage*8)*.75, z=(s-.6)*.8;
        path(u=>{const a=u*tau;return [Math.sin(a)*s*.9,(-Math.cos(a)*.82+Math.pow(Math.max(0,Math.cos(a)),4)*-.17)*s, z+Math.sin(a*2+time*.12)*.12];},100,j%6===0?palette[1]:palette[3],j%6===0?.78:.27,j%6===0?1.2:.6,j%6===0?3:0);
      }
      for(let j=0;j<14;j++){const x=(j-6.5)*.115;path(u=>[x,(u-.5)*1.45,Math.sin(u*Math.PI)*.3-.3],60,palette[2],.25,.65);}
    }
    function chip(time) {
      for(let j=0;j<13;j++) square(.52+j*.012,(j-6)*.035,0,j%4===0?palette[1]:palette[0],j%4===0?.8:.28,j%4===0?1.15:.6);
      for(let side=0;side<4;side++) for(let j=0;j<11;j++) {
        const p=(j-5)*.112,a=side*Math.PI/2,c=Math.cos(a),s=Math.sin(a);
        line([[p*c-.7*s,p*s+.7*c,0],[p*c-.99*s,p*s+.99*c,-.06]],palette[1],.75,1);
      }
      for(let j=0;j<17+stage*5;j++) {
        const r=.82+j*.025;
        path(u=>{const a=u*tau;return [Math.cos(a)*r,Math.sin(a)*r*.78,Math.sin(a*8+time*.2)*(j*.008+stage*.025)];},125,j%5===0?palette[2]:palette[1],j%5===0?.6:.2,j%5===0?1:.6);
      }
      for(let j=0;j<9;j++){const p=(j-4)*.11;line([[-.5,p,.28],[.5,p,.28]],palette[0],.3,.6);line([[p,-.5,.28],[p,.5,.28]],palette[0],.3,.6);}
    }
    function query(time) {
      function branch(a,b,depth,index) {
        for(let k=-2;k<=2;k++) path(u=>{const v=1-u;return [a[0]*v+b[0]*u+Math.sin(u*Math.PI)*k*.026,a[1]*v+b[1]*u,a[2]*v+b[2]*u+Math.sin(u*Math.PI)*.15];},40,palette[index%4],k===0?.85:.25,k===0?1.1:.6);
        if(depth===0){node(b,palette[2],2.4);return;}
        const spread=.52/(4-depth);
        [-1,1].forEach((dir,i)=>branch(b,[b[0]+dir*spread,b[1]-.46,b[2]+Math.sin(index+i+time*.07)*.28],depth-1,index*2+i));
      }
      branch([0,1.02,0],[0,.48,0],2+Math.min(stage,1),1);
      for(let j=0;j<12+stage*3;j++){const r=.22+j*.018;path(u=>[Math.cos(u*tau)*r,1.02+Math.sin(u*tau)*r*.3,Math.sin(u*tau)*r],60,palette[3],.32,.65);}
    }
    function bloom(time) {
      for(let j=0;j<34+stage*8;j++) {
        const v=j/(33+stage*8);
        path(u=>{const a=u*tau,petal=.75+.25*Math.cos(a*(5+stage)+v*2);const r=(.25+v*.8)*petal;return [Math.cos(a)*r,Math.sin(a)*r,Math.sin(v*Math.PI)*.5+Math.cos(a*3+time*.1)*.12];},135,j%7===0?palette[2]:palette[0],j%7===0?.8:.25,j%7===0?1.15:.6,j%7===0?4:0);
      }
      for(let j=0;j<8;j++) {const a=j/8*tau;line([[0,0,.65],[Math.cos(a)*.22,Math.sin(a)*.22,.1],[0,0,-.2]],palette[1],.65,.8);}
    }
    function frameMarks() {
      ctx.globalAlpha = .3; ctx.strokeStyle = '#a6e6cd'; ctx.lineWidth = .65;
      ctx.beginPath();
      for(let i=0;i<13;i++){const x=width*.13+i*width*.74/12;ctx.moveTo(x,height*.91);ctx.lineTo(x,height*.91+(i%3===0?5:2));}
      ctx.moveTo(width*.1,height*.5);ctx.lineTo(width*.14,height*.5);
      ctx.moveTo(width*.86,height*.5);ctx.lineTo(width*.9,height*.5);ctx.stroke();
    }
    function render(time, count) {
      if (failed || !ctx || !width || !height || forcedColors.matches) return;
      try {
        sy=Math.sin(yaw);cy=Math.cos(yaw);sx=Math.sin(pitch);cx=Math.cos(pitch);
        sculptureScale=Math.min(width*.39,height*.45);
        ctx.clearRect(0,0,width,height);
        const glow=ctx.createRadialGradient(width*.5,height*.48,2,width*.5,height*.48,Math.min(width,height)*.55);
        glow.addColorStop(0,'#33ffbd12');glow.addColorStop(.45,'#a16eff0b');glow.addColorStop(.76,'#29dfff05');glow.addColorStop(1,'#81ffbf00');
        ctx.globalAlpha=1;ctx.fillStyle=glow;ctx.fillRect(0,0,width,height);
        ctx.globalCompositeOperation='lighter';
        const t=time*.001;
        opticalSurfaces(t);
        if(type==='daarx')crystal(t,false);
        else if(type==='l10n')cash(t);
        else if(type==='open')gates(t);
        else if(type==='nexus')tension(t);
        else if(type==='development')braid(t,false);
        else if(type==='testnet')constellation(t);
        else if(type==='security')shield(t);
        else if(type==='hardware')chip(t);
        else if(type==='questions')query(t);
        else if(type==='privacy')bloom(t);
        else braid(t,true);
        ctx.globalCompositeOperation='source-over';frameMarks();ctx.globalAlpha=1;
        figure.dataset.prismRenderer='canvas';
        if(count){frames++;figure.dataset.prismFrames=String(frames);}
      } catch (_) { failed=true;stop();figure.dataset.prismRenderer='svg'; }
    }
    function tick(now) {
      frame=0;
      if(!runnable())return;
      if(now-last>=1000/30){
        const delta=last<0?0:Math.min(now-last,100);
        elapsed+=delta;
        yaw+=(targetYaw-yaw)*.12;pitch+=(targetPitch-pitch)*.12;
        figure.dataset.prismYaw=yaw.toFixed(4);figure.dataset.prismPitch=pitch.toFixed(4);
        render(elapsed,true);last=now;
      }
      if(runnable())frame=requestAnimationFrame(tick);
    }
    function start(){if(!frame&&runnable())frame=requestAnimationFrame(tick);}
    function measure(){
      if(failed)return;
      const box=canvas.getBoundingClientRect();
      if(!box.width||!box.height)return;
      width=box.width;height=box.height;
      const ratio=Math.min(window.devicePixelRatio||1,1.5,1100/width,900/height);
      canvas.width=Math.max(1,Math.round(width*ratio));canvas.height=Math.max(1,Math.round(height*ratio));
      ctx.setTransform(ratio,0,0,ratio,0,0);
      if(visible&&!doc.hidden)render(elapsed,false);
      start();
    }
    function select(next, announce){
      stage=clamp(Number(next)||0,0,2);
      figure.dataset.prismState=String(stage);
      buttons.forEach(button=>button.setAttribute('aria-pressed',String(Number(button.dataset.prismStep)===stage)));
      const selected=buttons.find(button=>Number(button.dataset.prismStep)===stage);
      const status=figure.querySelector('[data-prism-status]');
      if(status&&announce&&selected)status.textContent=selected.dataset.prismLabel||selected.textContent.trim();
      if(visible&&!doc.hidden)render(elapsed,false);
    }
    buttons.forEach(button=>button.addEventListener('click',()=>select(button.dataset.prismStep,true)));
    canvas.addEventListener('pointerdown',event=>{
      if(event.button!==0||failed)return;
      pointerId=event.pointerId;origin=[event.clientX,event.clientY,targetYaw,targetPitch];
      figure.dataset.prismDragging='true';
      try{canvas.setPointerCapture(pointerId);}catch(_){}
    });
    canvas.addEventListener('pointermove',event=>{
      if(event.pointerId!==pointerId||!origin)return;
      targetYaw=clamp(origin[2]+(event.clientX-origin[0])/Math.max(width,1)*2.8,-1.45,1.45);
      targetPitch=clamp(origin[3]+(event.clientY-origin[1])/Math.max(height,1)*1.6,-.8,.8);
      figure.dataset.prismYaw=targetYaw.toFixed(4);figure.dataset.prismPitch=targetPitch.toFixed(4);
      if(paused){yaw=targetYaw;pitch=targetPitch;if(visible&&!doc.hidden)render(elapsed,false);}
      start();
    });
    function release(event){if(event.pointerId!==pointerId)return;pointerId=null;origin=null;figure.dataset.prismDragging='false';}
    canvas.addEventListener('pointerup',release);canvas.addEventListener('pointercancel',release);canvas.addEventListener('lostpointercapture',release);
    canvas.addEventListener('contextlost',event=>{
      event.preventDefault();failed=true;stop();figure.dataset.prismRenderer='svg';
    });
    canvas.addEventListener('contextrestored',()=>{
      try{ctx=canvas.getContext('2d',{alpha:true});}catch(_){ctx=null;}
      failed=!ctx;if(!failed)measure();
    });
    if('IntersectionObserver' in window){
      new IntersectionObserver(entries=>{
        visible=entries[0].isIntersecting;
        if(visible){if(!width)measure();render(elapsed,false);start();}else stop();
      },{threshold:0}).observe(figure);
    }else{
      function check(){const r=figure.getBoundingClientRect();visible=r.bottom>0&&r.top<window.innerHeight;if(visible){render(elapsed,false);start();}else stop();}
      window.addEventListener('scroll',check,{passive:true});check();
    }
    if('ResizeObserver' in window)new ResizeObserver(measure).observe(canvas);
    else window.addEventListener('resize',measure,{passive:true});
    scenes.push({refresh:function(){stop();if(visible&&!doc.hidden){if(!width)measure();render(elapsed,false);start();}}});
    select(stage,false);measure();
  });
  function refresh(){scenes.forEach(scene=>scene.refresh());}
  doc.addEventListener('daarx:motion',event=>{
    if(!event.detail||typeof event.detail.paused!=='boolean')return;
    explicitMotion=event.detail.paused;paused=explicitMotion;refresh();
  });
  new MutationObserver(()=>{
    const next=doc.documentElement.classList.contains('motion-paused');
    if(next===classPaused)return;
    classPaused=next;explicitMotion=next;paused=next;refresh();
  }).observe(doc.documentElement,{attributes:true,attributeFilter:['class']});
  function preferenceChange(){if(explicitMotion===null){paused=motionPreference.matches||classPaused;refresh();}}
  if(motionPreference.addEventListener)motionPreference.addEventListener('change',preferenceChange);
  if(forcedColors.addEventListener)forcedColors.addEventListener('change',refresh);
  doc.addEventListener('visibilitychange',refresh);
}());
