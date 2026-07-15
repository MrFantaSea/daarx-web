(function () {
  'use strict';

  var doc = document;
  var body = doc.body;
  if (!body || !body.classList.contains('protocol-page')) return;

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

  function activateInspection(consoleElement, tab, announce) {
    var tabs = Array.prototype.slice.call(consoleElement.querySelectorAll('[role="tab"][data-inspection-tab]'));
    var panels = Array.prototype.slice.call(consoleElement.querySelectorAll('[role="tabpanel"]'));
    var target = tab.getAttribute('aria-controls');

    tabs.forEach(function (candidate) {
      var active = candidate === tab;
      candidate.setAttribute('aria-selected', String(active));
      candidate.setAttribute('tabindex', active ? '0' : '-1');
    });

    panels.forEach(function (panel) {
      var active = panel.id === target;
      panel.hidden = !active;
      panel.classList.toggle('is-active', active);
    });

    var live = consoleElement.querySelector('[aria-live]');
    if (announce && live) live.textContent = tab.textContent.trim() + ' inspection layer selected.';
  }

  Array.prototype.slice.call(doc.querySelectorAll('[data-inspection]')).forEach(function (consoleElement) {
    var tabs = Array.prototype.slice.call(consoleElement.querySelectorAll('[role="tab"][data-inspection-tab]'));
    tabs.forEach(function (tab, index) {
      tab.addEventListener('click', function () { activateInspection(consoleElement, tab, true); });
      tab.addEventListener('keydown', function (event) {
        var targetIndex = index;
        if (event.key === 'ArrowRight' || event.key === 'ArrowDown') targetIndex = (index + 1) % tabs.length;
        else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') targetIndex = (index - 1 + tabs.length) % tabs.length;
        else if (event.key === 'Home') targetIndex = 0;
        else if (event.key === 'End') targetIndex = tabs.length - 1;
        else return;
        event.preventDefault();
        tabs[targetIndex].focus();
        activateInspection(consoleElement, tabs[targetIndex], true);
      });
    });
    if (tabs.length) activateInspection(consoleElement, tabs[0], false);
  });

  body.classList.add('protocol-ready');

  var hero = doc.querySelector('.protocol-hero');
  var visual = doc.querySelector('.protocol-hero-visual');
  var finePointer = window.matchMedia && window.matchMedia('(pointer: fine)').matches;
  if (hero && visual && !reduce && finePointer) {
    hero.addEventListener('pointermove', function (event) {
      var box = hero.getBoundingClientRect();
      var x = ((event.clientX - box.left) / box.width - 0.5) * -14;
      var y = ((event.clientY - box.top) / box.height - 0.5) * -9;
      visual.style.setProperty('--module-x', x.toFixed(2));
      visual.style.setProperty('--module-y', y.toFixed(2));
    }, { passive: true });
    hero.addEventListener('pointerleave', function () {
      visual.style.setProperty('--module-x', '0');
      visual.style.setProperty('--module-y', '0');
    }, { passive: true });
  }
})();
