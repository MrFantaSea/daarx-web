(function () {
  'use strict';
  const style = document.createElement('style');
  document.head.appendChild(style);
  document.querySelectorAll('[data-paper]').forEach(function (button) {
    button.addEventListener('click', function () {
      const a4 = button.dataset.paper === 'a4';
      document.body.classList.toggle('a4', a4);
      style.textContent = '@page{size:' + (a4 ? 'A4' : 'letter') + ';margin:0}';
      document.querySelectorAll('[data-paper]').forEach(function (item) { item.setAttribute('aria-pressed', String(item === button)); });
    });
  });
  document.querySelector('[data-print]').addEventListener('click', function () { window.print(); });
}());
