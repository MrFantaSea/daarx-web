(function () {
  'use strict';
  const doc = document;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  let paused = reduced.matches;
  doc.documentElement.classList.add('js-ready');

  doc.querySelectorAll('[data-tabs]').forEach(function (group) {
    const tabs = Array.from(group.querySelectorAll('[role="tab"]'));
    const panels = Array.from(group.querySelectorAll('[role="tabpanel"]'));
    function activate(tab, focus) {
      tabs.forEach(function (item) {
        const active = item === tab;
        item.setAttribute('aria-selected', String(active));
        item.tabIndex = active ? 0 : -1;
      });
      panels.forEach(function (panel) { panel.hidden = panel.id !== tab.getAttribute('aria-controls'); });
      if (focus) tab.focus();
      const coin = tab.id.replace('coin-tab-', '');
      if (tab.id.startsWith('coin-tab-')) doc.documentElement.dataset.coin = coin;
    }
    tabs.forEach(function (tab, index) {
      tab.addEventListener('click', function () { activate(tab, false); });
      tab.addEventListener('keydown', function (event) {
        let next = index;
        if (event.key === 'ArrowRight' || event.key === 'ArrowDown') next = (index + 1) % tabs.length;
        else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = (index - 1 + tabs.length) % tabs.length;
        else if (event.key === 'Home') next = 0;
        else if (event.key === 'End') next = tabs.length - 1;
        else return;
        event.preventDefault();
        activate(tabs[next], true);
      });
    });
    if (tabs.length) activate(tabs[0], false);
  });

  const menu = doc.querySelector('.site-menu');
  if (menu) {
    doc.addEventListener('click', function (event) { if (menu.open && !menu.contains(event.target)) menu.open = false; });
    doc.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && menu.open) {
        menu.open = false;
        menu.querySelector('summary').focus();
      }
    });
  }

  const query = doc.getElementById('faq-query');
  if (query) {
    const records = Array.from(doc.querySelectorAll('.faq-list .qa'));
    const result = doc.getElementById('faq-results');
    const empty = doc.querySelector('.no-results');
    function filter() {
      const term = query.value.trim().toLowerCase();
      let visible = 0;
      records.forEach(function (record) {
        const match = !term || record.textContent.toLowerCase().includes(term);
        record.hidden = !match;
        if (match) visible += 1;
      });
      result.textContent = visible + (visible === 1 ? ' answer' : ' answers') + (term ? ' found' : '');
      empty.hidden = visible > 0;
    }
    query.addEventListener('input', filter);
    query.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') { query.value = ''; filter(); }
    });
  }

  doc.querySelectorAll('[data-sku]').forEach(function (link) {
    link.addEventListener('click', function () {
      const select = doc.getElementById('f-product');
      if (!select) return;
      const option = Array.from(select.options).find(function (item) { return item.value === link.dataset.sku || item.text === link.dataset.sku; });
      if (option) { select.value = option.value; select.dispatchEvent(new Event('change', { bubbles: true })); }
    });
  });
  doc.querySelectorAll('[data-acc]').forEach(function (link) {
    link.addEventListener('click', function () {
      const input = Array.from(doc.querySelectorAll('input[type="checkbox"]')).find(function (item) { return item.name === link.dataset.acc; });
      if (input) input.checked = true;
    });
  });
  const form = doc.querySelector('form.pre');
  if (form) {
    form.addEventListener('submit', async function (event) {
      event.preventDefault();
      const submit = form.querySelector('button[type="submit"]');
      if (submit.disabled) return;
      const status = doc.getElementById('f-status');
      const original = submit.innerHTML;
      submit.disabled = true;
      submit.textContent = 'Sending…';
      status.classList.remove('error');
      status.textContent = '';
      try {
        const response = await window.fetch(form.action, { method: 'POST', headers: { Accept: 'application/json' }, body: new FormData(form) });
        const result = await response.json();
        if (!response.ok || !result.success) throw new Error('Submission was not accepted');
        form.hidden = true;
        status.textContent = 'Your hardware interest was recorded. No order, payment, priority or Testnet signup was created. We’ll contact you only if a relevant compliant offer or material update becomes available.';
        status.focus();
      } catch (_) {
        submit.disabled = false;
        submit.innerHTML = original;
        status.classList.add('error');
        status.textContent = 'That didn’t send. Your entries are still here. Please try again later.';
        status.focus();
      }
    });
  }

  /* A procedural spectral torus, not network data. No requests or storage. */
  const canvas = doc.querySelector('[data-spectrum]');
  const ctx = canvas && canvas.getContext('2d');
  let width = 0;
  let height = 0;
  let frame = 0;
  let visible = true;
  let pointerX = 0;
  let pointerY = 0;
  let last = 0;
  const colors = ['134,243,177', '232,199,109', '131,217,228', '182,154,245'];

  function draw(time) {
    if (!ctx || !width) return;
    ctx.clearRect(0, 0, width, height);
    const size = Math.min(width, height);
    const centerX = width * .5 + pointerX * 9;
    const centerY = height * .5 + pointerY * 7;
    const radius = size * .267;
    const t = time * .000085;
    ctx.globalCompositeOperation = 'lighter';
    for (let band = 0; band < 86; band += 1) {
      const b = band / 86 * Math.PI * 2;
      const color = colors[Math.floor(band / 21.5)];
      const alpha = .20 + Math.pow(Math.sin(b * 1.4 + t), 2) * .32;
      ctx.strokeStyle = 'rgba(' + color + ',' + alpha.toFixed(3) + ')';
      ctx.lineWidth = band % 5 === 0 ? 1.15 : .65;
      ctx.shadowColor = 'rgba(' + color + ',.48)';
      ctx.shadowBlur = band % 7 === 0 ? 14 : 0;
      ctx.beginPath();
      for (let step = 0; step <= 170; step += 1) {
        const a = step / 170 * Math.PI * 2;
        const swell = Math.cos(b * 3 + a * 2 + t * 2) * .065;
        const tube = radius * (.26 + swell);
        const ring = radius + tube * Math.cos(b + a * .6 + t);
        const x = Math.cos(a) * ring;
        const y = Math.sin(a) * ring;
        const z = tube * Math.sin(b + a * .6 + t);
        const warp = Math.sin(a * 4 - b * 2 + t * .7) * size * .012;
        const dx = x * .88 - y * .36;
        const dy = x * .27 + y * .60 + z * .9 + warp;
        const px = centerX + dx;
        const py = centerY + dy;
        if (!step) ctx.moveTo(px, py); else ctx.lineTo(px, py);
      }
      ctx.closePath();
      ctx.stroke();
    }
    ctx.shadowBlur = 0;
    ctx.globalCompositeOperation = 'source-over';
  }
  function resize() {
    if (!ctx) return;
    const box = canvas.getBoundingClientRect();
    const ratio = Math.min(window.devicePixelRatio || 1, 1.75);
    width = box.width;
    height = box.height;
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    draw(3500);
  }
  function tick(time) {
    frame = 0;
    if (paused || !visible || doc.hidden || !ctx) return;
    if (time - last > 42) { draw(time); last = time; }
    frame = window.requestAnimationFrame(tick);
  }
  function start() { if (!frame && ctx && !paused && visible && !doc.hidden) frame = window.requestAnimationFrame(tick); }
  function stop() { if (frame) window.cancelAnimationFrame(frame); frame = 0; }
  function applyMotion() {
    doc.body.classList.toggle('motion-paused', paused);
    doc.querySelectorAll('[data-motion]').forEach(function (button) {
      button.setAttribute('aria-pressed', String(paused));
      button.textContent = paused ? 'Resume motion ▷' : 'Pause motion Ⅱ';
    });
    if (paused) { stop(); draw(3500); } else start();
  }
  doc.querySelectorAll('[data-motion]').forEach(function (button) { button.addEventListener('click', function () { paused = !paused; applyMotion(); }); });
  if (reduced.addEventListener) reduced.addEventListener('change', function (event) { paused = event.matches; applyMotion(); });
  if (ctx) {
    resize();
    if ('ResizeObserver' in window) new ResizeObserver(resize).observe(canvas);
    else window.addEventListener('resize', resize, { passive: true });
    const lens = canvas.parentElement;
    lens.addEventListener('pointermove', function (event) {
      if (paused || event.pointerType === 'touch') return;
      const box = lens.getBoundingClientRect();
      pointerX = (event.clientX - box.left) / box.width - .5;
      pointerY = (event.clientY - box.top) / box.height - .5;
    }, { passive: true });
    lens.addEventListener('pointerleave', function () { pointerX = 0; pointerY = 0; }, { passive: true });
    if ('IntersectionObserver' in window) new IntersectionObserver(function (entries) { visible = entries[0].isIntersecting; if (visible) start(); else stop(); }).observe(lens);
    doc.addEventListener('visibilitychange', function () { if (doc.hidden) stop(); else start(); });
  }
  applyMotion();
}());
