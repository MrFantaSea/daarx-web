/* Atlas: local procedural light, static sculpture first. No dependencies. */
(() => {
  'use strict';
  const doc = document, reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const style = doc.createElement('style');
  // Zero-specificity mechanics: the shared stylesheet owns all visual design.
  style.textContent = `
:where(.atlas-engine-stage){position:relative;perspective:1100px;overflow:hidden;touch-action:pan-y}
:where(.atlas-engine-svg){transform-origin:50% 49%}
:where(.atlas-engine .is-muted){opacity:.55}
:where(.atlas-engine [data-atlas-canvas]){position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
`;
  doc.head.append(style);
  const roles = {
    daarx: ['DAARX / Private ownership', 'Private payment amounts, one-time destination keys and full-chain membership proofs protect the person behind a balance.', '#79f5b0'],
    l10n: ['L10N / Everyday circulation', 'Private everyday money with its own balances and monetary rules. Offline exchange and later settlement are part of the engineering work.', '#f3cc79'],
    open: ['OPEN / Bounded authority', 'Distinct Human, Institution and Agent accounts. Mandates bound delegated spending; delegation cannot multiply the allowance.', '#77e5f5'],
    nexus: ['NXXXS / Evidence-backed services', 'The Nexus / NXXXS lineage connects chosen services to evidence and collateral. Ordinary sibling-chain transfers carry no automatic NXXXS toll.', '#c8a4ff']
  };
  let paused = doc.documentElement.classList.contains('motion-paused') || doc.body.classList.contains('motion-paused');
  const instances = [];
  doc.querySelectorAll('.atlas-engine').forEach(figure => {
    const stage = figure.querySelector('.atlas-engine-stage'), svg = figure.querySelector('svg');
    const canvas = figure.querySelector('[data-atlas-canvas]');
    let ctx = null;
    try { ctx = canvas?.getContext('2d'); } catch (_) { /* SVG remains complete. */ }
    let visible = !('IntersectionObserver' in window), raf = 0, last = 0, elapsed = 0, frames = 0;
    let width = 0, height = 0, x = 0, y = 0, targetX = 0, targetY = 0;
    let selected = 'daarx';
    figure.dataset.atlasEnhanced = '';
    function resize() {
      if (!ctx) return;
      const rect = stage.getBoundingClientRect();
      width = rect.width; height = rect.height;
      const dpr = Math.min(devicePixelRatio || 1, 1.5, 1600 / Math.max(width, 1));
      canvas.width = Math.round(width * dpr); canvas.height = Math.round(height * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    function allowed() { return !!ctx && visible && !doc.hidden && !paused && !reduced.matches && width > 0; }
    function stop() {
      cancelAnimationFrame(raf); raf = 0; last = 0;
      figure.dataset.atlasActive = 'false';
      svg.style.transform = '';
      ctx?.clearRect(0, 0, width, height);
    }
    function reconcile() {
      if (!allowed()) { stop(); return; }
      if (!raf) { figure.dataset.atlasActive = 'true'; raf = requestAnimationFrame(draw); }
    }
    function draw(time) {
      raf = 0;
      if (!allowed()) { stop(); return; }
      if (last && time - last < 33.3) { raf = requestAnimationFrame(draw); return; }
      elapsed += last ? Math.min(time-last, 60) : 0; last = time;
      x += (targetX-x)*.07; y += (targetY-y)*.07;
      svg.style.transform = `rotateX(${y.toFixed(2)}deg) rotateY(${x.toFixed(2)}deg)`;
      ctx.clearRect(0, 0, width, height);
      ctx.save(); ctx.scale(width/960, height/720);
      // Fine travelling caustics only; underlying SVG is always visible.
      ctx.strokeStyle = roles[selected][2]; ctx.lineWidth = .8;
      for (let n=0;n<18;n++) {
        const t = elapsed*.000095+n*Math.PI*2/18;
        const r = 254/Math.pow(Math.pow(Math.abs(Math.cos(t)),1.3)+Math.pow(Math.abs(Math.sin(t)),1.3),1/1.3);
        const phase = 3*t+Object.keys(roles).indexOf(selected)*Math.PI/2;
        const radial = r+43*Math.cos(phase)+19;
        const yy=radial*Math.sin(t)*.88-64*Math.sin(phase)*.475;
        const zz=radial*Math.sin(t)*.475+64*Math.sin(phase)*.88;
        const s=980/(980-zz), px=480+(radial*Math.cos(t)*1.18+zz*.13)*s, py=350+yy*s;
        ctx.globalAlpha=.12+.3*(.5+.5*Math.sin(t+elapsed*.0003));
        ctx.beginPath();ctx.moveTo(px-3,py);ctx.lineTo(px+3,py);ctx.moveTo(px,py-3);ctx.lineTo(px,py+3);ctx.stroke();
      }
      ctx.restore(); frames++; figure.dataset.atlasFrames = String(frames);
      raf = requestAnimationFrame(draw);
    }
    figure.querySelectorAll('[data-atlas-coin]').forEach(button => button.addEventListener('click', () => {
      const key = button.dataset.atlasCoin;
      if (!roles[key]) return;
      selected = key; figure.dataset.atlasSelected = key;
      figure.querySelectorAll('[data-atlas-strand]').forEach(path => {
        path.classList.toggle('is-selected', path.dataset.atlasStrand === key);
        path.classList.toggle('is-muted', path.dataset.atlasStrand !== key);
      });
      figure.style.setProperty('--atlas-selected', roles[key][2]);
      figure.querySelectorAll('[data-atlas-coin]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
      figure.querySelector('[data-atlas-title]').textContent = roles[key][0];
      figure.querySelector('[data-atlas-description]').textContent = roles[key][1];
    }));
    stage.addEventListener('pointermove', event => {
      if (reduced.matches || paused) return;
      if (event.pointerType === 'touch' && !event.buttons) return;
      const r = stage.getBoundingClientRect();
      targetX = ((event.clientX-r.left)/r.width-.5)*5;
      targetY = -((event.clientY-r.top)/r.height-.5)*4;
    }, {passive:true});
    ['pointerleave','pointerup','pointercancel'].forEach(type => stage.addEventListener(type, () => {targetX=targetY=0;}, {passive:true}));
    if ('ResizeObserver' in window) new ResizeObserver(() => {resize();reconcile();}).observe(stage);
    else window.addEventListener('resize', () => {resize();reconcile();}, {passive:true});
    if ('IntersectionObserver' in window) new IntersectionObserver(entries => {
      visible = entries[0].isIntersecting; reconcile();
    }, {threshold:0}).observe(stage);
    instances.push({reconcile}); resize(); reconcile();
  });
  const reconcileAll = () => instances.forEach(item => item.reconcile());
  doc.addEventListener('daarx:motion', event => {paused=!!event.detail?.paused;reconcileAll();});
  doc.addEventListener('visibilitychange', reconcileAll);
  reduced.addEventListener('change', reconcileAll);
  // Navigation and reading position have no dependency on the artwork/canvas.
  const progress = doc.querySelector('[data-reading-progress]');
  let progressPending = false;
  function updateProgress() {
    progressPending = false;
    if (!progress) return;
    const max = doc.documentElement.scrollHeight-innerHeight;
    const fraction = max > 0 ? Math.max(0,Math.min(1,scrollY/max)) : 0;
    progress.style.setProperty('--reading-progress', String(fraction));
    progress.style.transformOrigin = 'left'; progress.style.transform = `scaleX(${fraction})`;
    if (progress.getAttribute('role') === 'progressbar') progress.setAttribute('aria-valuenow', String(Math.round(fraction*100)));
  }
  window.addEventListener('scroll', () => {if(!progressPending){progressPending=true;requestAnimationFrame(updateProgress);}}, {passive:true});
  window.addEventListener('resize', updateProgress, {passive:true}); updateProgress();
  if ('IntersectionObserver' in window) {
    const links = [...doc.querySelectorAll('.atlas-chapters a[href^="#"]')];
    const sections = links.map(a => {try{return doc.getElementById(decodeURIComponent(a.hash.slice(1)));}catch(_){return null;}}).filter(Boolean);
    const seen = new Map();
    const observer = new IntersectionObserver(entries => {
      entries.forEach(e => seen.set(e.target, e.isIntersecting));
      const current = sections.filter(s => seen.get(s)).sort((a,b) => Math.abs(a.getBoundingClientRect().top)-Math.abs(b.getBoundingClientRect().top))[0];
      if (!current) return;
      links.forEach(a => {if(a.hash === '#'+current.id){a.setAttribute('aria-current','location');a.classList.add('is-active');}else{a.removeAttribute('aria-current');a.classList.remove('is-active');}});
    }, {rootMargin:'-10% 0px -40% 0px'});
    sections.forEach(s => observer.observe(s));
    // Content starts visible; a small Web Animation is strictly decorative.
    const reveal = new IntersectionObserver(entries => entries.forEach(e => {
      if (!e.isIntersecting) return;
      reveal.unobserve(e.target);
      if (!reduced.matches && !paused && e.target.animate) e.target.animate([{transform:'translateY(10px)'},{transform:'translateY(0)'}], {duration:550,easing:'cubic-bezier(.2,.7,.2,1)'});
    }), {threshold:.08});
    doc.querySelectorAll('.atlas-reveal').forEach(el => reveal.observe(el));
  }
})();
