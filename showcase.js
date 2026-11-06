/* Enhancements to the original showcase: native controls and exact monetary study. */
(function(){'use strict';const doc=document,names=['daarx','l10n','open','nexus'];
const root=doc.documentElement;root.classList.add('js');
const pref=matchMedia('(prefers-reduced-motion:reduce)');let paused=pref.matches;
function motion(value){paused=value;root.classList.toggle('motion-paused',paused);doc.querySelectorAll('[data-showcase-motion]').forEach(b=>{b.setAttribute('aria-pressed',String(paused));b.setAttribute('aria-label',paused?'Resume visual motion':'Pause visual motion');b.textContent=paused?'▷':'Ⅱ';});}
motion(paused);doc.querySelectorAll('[data-showcase-motion]').forEach(b=>b.addEventListener('click',()=>motion(!paused)));pref.addEventListener('change',e=>motion(e.matches));
  const emission = doc.querySelector('[data-emission]');
  if (emission) {
    const range = doc.getElementById('time-range');
    const display = doc.getElementById('time-output');
    const cursor = emission.querySelector('.time-cursor');
    const announcement = emission.querySelector('[data-schedule-announcement]');
    let data = null, loading = null, announcementTimer = 0;
    function update() {
      if (!data) return;
      const year = Number(range.value);
      const index = Math.max(0, Math.min(data.coins.daarx.rewards.length-1, Math.round(year / data.step_years)));
      display.value = year.toFixed(2);
      range.setAttribute('aria-valuetext', year.toFixed(2) + ' target years');
      const x = 56 + year / data.years * 1088;
      cursor.setAttribute('x1', x.toFixed(3));
      cursor.setAttribute('x2', x.toFixed(3));
      names.forEach(id => {
        const value = Number(data.coins[id].rewards[index]);
        emission.querySelector('[data-reward="' + id + '"]').value = value.toLocaleString('en-US', { maximumFractionDigits: value < 1 ? 6 : 3 });
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
    const chart=emission.querySelector('.emission-chart');
    chart.addEventListener('pointerdown', async event => {
      await loadStudy();if (!data) return;
      const box=chart.getBoundingClientRect();
      const ratio=((event.clientX-box.left)/box.width*1200-56)/1088;
      range.value=Math.max(.01,Math.min(data.years,ratio*data.years)).toFixed(2);update();announce();
    });
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

})();
