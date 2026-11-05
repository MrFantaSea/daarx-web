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
        status.textContent = 'Thanks. Your hardware enquiry is in. We’ll follow up by email.';
        status.focus();
      } catch (_) {
        submit.disabled = false;
        submit.innerHTML = original;
        status.classList.add('error');
        status.textContent = 'That didn’t send. Your entries are still here. Try again later.';
        status.focus();
      }
    });
  }

  function applyMotion() {
    doc.body.classList.toggle('motion-paused', paused);
    doc.documentElement.classList.toggle('motion-paused', paused);
    doc.querySelectorAll('[data-motion]').forEach(function (button) {
      button.setAttribute('aria-pressed', String(paused));
      button.textContent = paused ? 'Resume motion ▷' : 'Pause motion Ⅱ';
    });
    doc.dispatchEvent(new CustomEvent('daarx:motion', { detail: { paused } }));
  }
  doc.querySelectorAll('[data-motion]').forEach(function (button) {
    button.addEventListener('click', function () { paused = !paused; applyMotion(); });
  });
  if (reduced.addEventListener) reduced.addEventListener('change', function (event) { paused = event.matches; applyMotion(); });
  applyMotion();
}());
