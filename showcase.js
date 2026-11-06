/* Enhancements to the original showcase: native controls and exact monetary study. */
(function(){'use strict';const doc=document,names=['daarx','l10n','open','nexus'];
const root=doc.documentElement;root.classList.add('js');
const menu=doc.querySelector('.nd');
if(menu){doc.addEventListener('click',e=>{if(menu.open&&!menu.contains(e.target))menu.open=false;});doc.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu.open){menu.open=false;menu.querySelector('summary').focus();}});}
const nav=doc.getElementById('nav');if(nav){const update=()=>nav.classList.toggle('scrolled',scrollY>24);update();addEventListener('scroll',update,{passive:true});}
const pref=matchMedia('(prefers-reduced-motion:reduce)');let paused=pref.matches;
function motion(value){paused=value;root.classList.toggle('motion-paused',paused);doc.querySelectorAll('[data-showcase-motion]').forEach(b=>{b.setAttribute('aria-pressed',String(paused));b.setAttribute('aria-label',paused?'Resume visual motion':'Pause visual motion');b.textContent=paused?'▷':'Ⅱ';});doc.dispatchEvent(new CustomEvent('daarx:motion',{detail:{paused}}));}
motion(paused);doc.querySelectorAll('[data-showcase-motion]').forEach(b=>b.addEventListener('click',()=>motion(!paused)));pref.addEventListener('change',e=>motion(e.matches));
  const emission = doc.querySelector('[data-emission]');
  if (emission) {
    const range = doc.getElementById('time-range');
    const display = doc.getElementById('time-output');
    const plots = Array.from(emission.querySelectorAll('[data-schedule-plot]'));
    const announcement = emission.querySelector('[data-schedule-announcement]');
    let data = null, loading = null, announcementTimer = 0;
    function update() {
      if (!data) return;
      const year = Number(range.value);
      const index = Math.max(0, Math.min(data.coins.daarx.rewards.length-1, Math.round(year / data.step_years)));
      display.value = year.toFixed(2);
      range.setAttribute('aria-valuetext', year.toFixed(2) + ' target years');
      const x = 56 + year / data.years * 904;
      plots.forEach(plot=>{
        const id=plot.dataset.schedulePlot,reward=Number(data.coins[id].rewards[index]),y=190-170*reward/Number(plot.dataset.ymax);
        const cursor=plot.querySelector('[data-schedule-cursor]'),marker=plot.querySelector('[data-schedule-marker]');
        cursor.setAttribute('x1',x);cursor.setAttribute('x2',x);marker.setAttribute('cx',x);marker.setAttribute('cy',y);
      });
      names.forEach(id => {
        const value = Number(data.coins[id].rewards[index]);
        emission.querySelector('[data-reward="' + id + '"]').value = value.toLocaleString('en-US', { maximumFractionDigits: value > 0 && value < .000001 ? 12 : value < 1 ? 6 : 3 });
      });
      emission.dataset.year = year.toFixed(2);
    }
    function announce() {
      clearTimeout(announcementTimer);
      announcementTimer = setTimeout(() => {
        const words=names.map(id => {
          const value=emission.querySelector('[data-reward="'+id+'"]').value;
          return (id==='nexus'?'NXXXS':id.toUpperCase())+' '+value+' '+(id==='daarx'?'DIAM':id==='nexus'?'NXXXS':id.toUpperCase())+' per block';
        });
        announcement.textContent='At '+Number(range.value).toFixed(2)+' target years: '+words.join('; ')+'.';
      },220);
    }
    function loadStudy() {
      if (loading) return loading;
      loading=fetch(emission.dataset.src,{credentials:'same-origin',cache:'force-cache'}).then(response => {
        if (!response.ok) throw new Error('Study data unavailable');
        return response.json();
      }).then(value => {
        data=value; range.disabled=false; emission.dataset.state='interactive';update();
      }).catch(() => { emission.dataset.state='snapshot'; });
      return loading;
    }
    range.addEventListener('input',update);
    range.addEventListener('change',announce);
    emission.addEventListener('focusin',loadStudy,{once:true});
    emission.querySelectorAll('.emission-chart').forEach(chart=>chart.addEventListener('pointerdown', async event => {
      await loadStudy();if (!data) return;
      const box=chart.getBoundingClientRect();
      const ratio=((event.clientX-box.left)/box.width*1000-56)/904;
      range.value=Math.max(.01,Math.min(data.years,ratio*data.years)).toFixed(2);update();announce();
    }));
    if ('IntersectionObserver' in window) {
      const observer=new IntersectionObserver(entries => { if(entries.some(entry=>entry.isIntersecting)){loadStudy();observer.disconnect();} },{rootMargin:'600px 0px'});
      observer.observe(emission);
    } else loadStudy();
  }

  doc.querySelectorAll('[data-inspect]').forEach(button => {
    button.closest('[data-proof-scene]').querySelectorAll('[data-proof-description]').forEach(detail => { detail.hidden=true; });
    button.addEventListener('click', () => {
      const scene = button.closest('[data-proof-scene]');
      const active = scene.classList.toggle('inspected');
      scene.querySelectorAll('[data-proof-description]').forEach(detail => { detail.hidden = !active; });
      button.setAttribute('aria-pressed', String(active));
      button.setAttribute('aria-expanded', String(active));
      button.innerHTML = active ? 'Close inspection <span aria-hidden="true">−</span>' : 'Inspect the structure <span aria-hidden="true">＋</span>';
    });
  });

  doc.querySelectorAll('[data-prism-scene]').forEach(figure=>{
    const stages=JSON.parse(figure.dataset.prismContent);
    figure.querySelectorAll('[data-prism-step]').forEach(button=>button.addEventListener('click',()=>{
      const n=Number(button.dataset.prismStep),stage=stages[n];
      figure.querySelector('[data-prism-title]').textContent=stage[0];
      figure.querySelector('[data-prism-copy]').textContent=stage[1];
      figure.querySelector('[data-prism-index]').textContent=String(n+1);
    }));
  });

  doc.querySelectorAll('[data-coin-curve]').forEach(curve=>{
    const points=JSON.parse(curve.dataset.curvePoints);
    curve.querySelectorAll('[data-curve-step]').forEach(button=>button.addEventListener('click',()=>{
      const point=points[Number(button.dataset.curveStep)];
      curve.querySelectorAll('[data-curve-step]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
      const marker=curve.querySelector('.supply-marker');marker.setAttribute('cx',point.x);marker.setAttribute('cy',point.y);
      curve.querySelector('[data-curve-reward]').value=Number(point.value).toLocaleString('en-US',{maximumFractionDigits:point.value>0&&point.value<.000001?12:point.value<1?6:3});
    }));
  });

  const topics=doc.querySelector('[data-prism-scene="questions"]');
  if(topics){topics.querySelectorAll('[data-prism-step]').forEach(button=>button.addEventListener('click',()=>{
    const search=doc.getElementById('faq-query');if(search){search.value=['','mining','service'][Number(button.dataset.prismStep)];search.dispatchEvent(new Event('input',{bubbles:true}));}
  }));}
  const hardware=doc.querySelector('[data-prism-scene="hardware"]');
  if(hardware){['tab-node','tab-compact','tab-rig','tab-scale'].forEach((id,index)=>{
    const tab=doc.getElementById(id);if(tab)tab.addEventListener('click',()=>{const n=Math.min(2,index);if(hardware.dataset.prismState!==String(n))hardware.querySelector('[data-prism-step="'+n+'"]').click();});
  });}
})();
