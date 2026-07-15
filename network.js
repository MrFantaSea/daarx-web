(function () {
  'use strict';

  var doc = document;
  var body = doc.body;
  if (!body || !body.classList.contains('network-home')) return;

  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var nav = doc.getElementById('nav');
  if (nav) {
    var updateNav = function () {
      nav.classList.toggle('scrolled', (window.scrollY || 0) > 24);
    };
    updateNav();
    window.addEventListener('scroll', updateNav, { passive: true });
  }

  var menu = doc.querySelector('.nd');
  if (menu) {
    doc.addEventListener('click', function (event) {
      if (menu.open && !menu.contains(event.target)) menu.open = false;
    });
    doc.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && menu.open) {
        menu.open = false;
        var summary = menu.querySelector('summary');
        if (summary) summary.focus();
      }
    });
  }

  var reveals = Array.prototype.slice.call(doc.querySelectorAll('.reveal'));
  if (reduce || !('IntersectionObserver' in window)) {
    reveals.forEach(function (element) { element.classList.add('in'); });
  } else {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('in');
        observer.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

    reveals.forEach(function (element) {
      if (element.getBoundingClientRect().top < window.innerHeight * 0.95) element.classList.add('in');
      else observer.observe(element);
    });
    body.classList.add('reveal-ready');

    window.setTimeout(function () {
      reveals.forEach(function (element) { element.classList.add('in'); });
    }, 2200);
  }

  var switchyard = doc.querySelector('.switchyard');
  var tabs = Array.prototype.slice.call(doc.querySelectorAll('[role="tab"][data-protocol]'));
  var panels = Array.prototype.slice.call(doc.querySelectorAll('[role="tabpanel"].protocol-panel'));
  var live = doc.getElementById('protocol-live');

  function activateProtocol(protocol, announce) {
    tabs.forEach(function (tab) {
      var active = tab.getAttribute('data-protocol') === protocol;
      tab.setAttribute('aria-selected', String(active));
      tab.setAttribute('tabindex', active ? '0' : '-1');
    });
    panels.forEach(function (panel) {
      var active = panel.id === 'panel-' + protocol;
      panel.hidden = !active;
      panel.classList.toggle('is-active', active);
    });
    if (switchyard) switchyard.setAttribute('data-active', protocol);
    if (announce && live) live.textContent = protocol.toUpperCase() + ' protocol details selected.';
  }

  tabs.forEach(function (tab, index) {
    tab.addEventListener('click', function () {
      activateProtocol(tab.getAttribute('data-protocol'), true);
    });
    tab.addEventListener('keydown', function (event) {
      var targetIndex = index;
      if (event.key === 'ArrowRight' || event.key === 'ArrowDown') targetIndex = (index + 1) % tabs.length;
      else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') targetIndex = (index - 1 + tabs.length) % tabs.length;
      else if (event.key === 'Home') targetIndex = 0;
      else if (event.key === 'End') targetIndex = tabs.length - 1;
      else return;
      event.preventDefault();
      tabs[targetIndex].focus();
      activateProtocol(tabs[targetIndex].getAttribute('data-protocol'), true);
    });
  });
  if (tabs.length) activateProtocol('daarx', false);

  var comparison = doc.querySelector('.ledger-comparison');
  var comparisonButtons = Array.prototype.slice.call(doc.querySelectorAll('.comparison-button[data-view]'));
  var publicPanel = doc.querySelector('.comparison-panel.public-panel');
  var privatePanel = doc.querySelector('.comparison-panel.private-panel');

  function activateComparison(view) {
    if (comparison) comparison.setAttribute('data-ledger-view', view);
    comparisonButtons.forEach(function (button) {
      var active = button.getAttribute('data-view') === view;
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', String(active));
    });
    if (publicPanel) publicPanel.hidden = view !== 'public';
    if (privatePanel) privatePanel.hidden = view !== 'private';
  }

  comparisonButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      activateComparison(button.getAttribute('data-view'));
    });
  });
  if (comparisonButtons.length) activateComparison('public');

  var hero = doc.querySelector('.network-hero');
  var finePointer = window.matchMedia && window.matchMedia('(pointer: fine)').matches;
  if (hero && !reduce && finePointer) {
    hero.addEventListener('pointermove', function (event) {
      var box = hero.getBoundingClientRect();
      var x = ((event.clientX - box.left) / box.width - 0.5) * -12;
      var y = ((event.clientY - box.top) / box.height - 0.5) * -8;
      hero.style.setProperty('--hero-x', x.toFixed(2));
      hero.style.setProperty('--hero-y', y.toFixed(2));
    }, { passive: true });
    hero.addEventListener('pointerleave', function () {
      hero.style.setProperty('--hero-x', '0');
      hero.style.setProperty('--hero-y', '0');
    }, { passive: true });
  }
})();
