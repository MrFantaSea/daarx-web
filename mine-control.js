(function () {
  "use strict";

  var d = document;
  var root = d.documentElement;
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  root.classList.add("js");

  /* Hardware-scale controller. Without JavaScript every panel remains visible. */
  var tabs = Array.prototype.slice.call(d.querySelectorAll("[data-bay-tab]"));
  var panels = Array.prototype.slice.call(d.querySelectorAll("[data-bay-panel]"));

  function activateTab(tab, moveFocus) {
    var target = tab && tab.getAttribute("data-bay-tab");
    tabs.forEach(function (item) {
      var active = item === tab;
      item.setAttribute("aria-selected", String(active));
      item.tabIndex = active ? 0 : -1;
    });
    panels.forEach(function (panel) {
      panel.hidden = panel.getAttribute("data-bay-panel") !== target;
    });
    if (moveFocus && tab) tab.focus();
  }

  if (tabs.length && panels.length) {
    activateTab(tabs[0], false);
    tabs.forEach(function (tab, index) {
      tab.addEventListener("click", function () { activateTab(tab, false); });
      tab.addEventListener("keydown", function (event) {
        var next = index;
        if (event.key === "ArrowRight" || event.key === "ArrowDown") next = (index + 1) % tabs.length;
        else if (event.key === "ArrowLeft" || event.key === "ArrowUp") next = (index - 1 + tabs.length) % tabs.length;
        else if (event.key === "Home") next = 0;
        else if (event.key === "End") next = tabs.length - 1;
        else return;
        event.preventDefault();
        activateTab(tabs[next], true);
      });
    });
  }

  /* Concept selection prefills the existing Web3Forms payload. */
  d.querySelectorAll("a[data-sku]").forEach(function (row) {
    row.addEventListener("click", function () {
      var sku = row.getAttribute("data-sku");
      var select = d.getElementById("f-product");
      if (!select) return;
      for (var index = 0; index < select.options.length; index += 1) {
        if (select.options[index].value === sku || select.options[index].text === sku) {
          select.selectedIndex = index;
          break;
        }
      }
    });
  });

  d.querySelectorAll("a[data-acc]").forEach(function (row) {
    row.addEventListener("click", function () {
      var checkbox = d.querySelector('input[name="' + row.getAttribute("data-acc") + '"]');
      if (checkbox) checkbox.checked = true;
    });
  });

  /* Submit without leaving the page while retaining the native POST fallback. */
  var form = d.querySelector("form.pre");
  if (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var button = form.querySelector("button");
      var original = button.textContent;
      var status = d.getElementById("f-status");
      button.textContent = "TRANSMITTING…";
      button.disabled = true;
      window.fetch("https://api.web3forms.com/submit", {
        method: "POST",
        headers: { Accept: "application/json" },
        body: new FormData(form)
      }).then(function (response) {
        return response.json();
      }).then(function (result) {
        if (result.success) {
          form.hidden = true;
          status.style.color = "var(--bay-green)";
          status.textContent = "Your non-binding interest was recorded. No order, priority, or payment was created. We'll contact you only if a compliant offer becomes available.";
          status.focus();
          return;
        }
        button.textContent = original;
        button.disabled = false;
        status.style.color = "var(--bay-red)";
        status.textContent = "Sorry — that didn't send. Please try again in a moment.";
      }).catch(function () {
        button.textContent = original;
        button.disabled = false;
        status.style.color = "var(--bay-red)";
        status.textContent = "Sorry — that didn't send. Please try again in a moment.";
      });
    });
  }

  /* Reveal only when motion is welcome; content is visible in every fallback. */
  var reveals = Array.prototype.slice.call(d.querySelectorAll(".reveal"));
  if (reduce || !("IntersectionObserver" in window)) {
    reveals.forEach(function (element) { element.classList.add("in"); });
  } else {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          observer.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (element) {
      if (element.getBoundingClientRect().top < window.innerHeight * 0.94) element.classList.add("in");
      else observer.observe(element);
    });
  }

  var nav = d.getElementById("nav");
  if (nav) {
    var updateNav = function () { nav.classList.toggle("scrolled", (window.scrollY || 0) > 24); };
    updateNav();
    window.addEventListener("scroll", updateNav, { passive: true });
  }

  var menu = d.querySelector(".nd");
  if (menu) {
    d.addEventListener("click", function (event) {
      if (menu.open && !menu.contains(event.target)) menu.open = false;
    });
  }
}());
