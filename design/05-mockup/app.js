/* Surviving the Singularity: mockup behavior, v0.0.1
   Three jobs and no more: the precedent tabs, the header state, and honest
   inert handlers for the two things this demo deliberately does not do. */

(function () {
  "use strict";

  /* ---------- 1. precedent tabs ---------- */

  var tabs = Array.prototype.slice.call(document.querySelectorAll(".tab"));
  var panels = Array.prototype.slice.call(document.querySelectorAll(".panel"));

  function selectTab(tab) {
    tabs.forEach(function (t) {
      var on = t === tab;
      t.classList.toggle("is-active", on);
      t.setAttribute("aria-selected", on ? "true" : "false");
      t.tabIndex = on ? 0 : -1;
    });
    panels.forEach(function (p) {
      var on = p.id === tab.getAttribute("aria-controls");
      p.classList.toggle("is-active", on);
      p.hidden = !on;
    });
  }

  tabs.forEach(function (tab, i) {
    tab.tabIndex = i === 0 ? 0 : -1;
    tab.addEventListener("click", function () {
      selectTab(tab);
    });
    // Arrow-key navigation is what makes a tablist a tablist rather than three
    // buttons that happen to be next to each other.
    tab.addEventListener("keydown", function (e) {
      var delta = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
      if (!delta) return;
      e.preventDefault();
      var next = tabs[(tabs.indexOf(tab) + delta + tabs.length) % tabs.length];
      selectTab(next);
      next.focus();
    });
  });

  /* ---------- 2. header state ---------- */

  // The header buy button appears only once the hero has scrolled past. A
  // sentinel beats a scroll listener: no layout reads, no rAF throttling.
  var head = document.getElementById("siteHead");
  var hero = document.querySelector(".hero");

  if (head && hero && "IntersectionObserver" in window) {
    var sentinel = document.createElement("div");
    sentinel.setAttribute("aria-hidden", "true");
    sentinel.style.cssText = "position:absolute;height:1px;width:1px;";
    hero.style.position = "relative";
    hero.appendChild(sentinel);

    new IntersectionObserver(
      function (entries) {
        head.classList.toggle("is-stuck", !entries[0].isIntersecting);
      },
      { rootMargin: "-70px 0px 0px 0px" }
    ).observe(sentinel);
  }

  /* ---------- 3. the two inert handlers ---------- */

  var toast = document.getElementById("toast");
  var toastTimer = null;

  function say(message) {
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add("is-on");
    window.clearTimeout(toastTimer);
    toastTimer = window.setTimeout(function () {
      toast.classList.remove("is-on");
    }, 5200);
  }

  // Every buy button. Wiring a demo to a real Stripe key is how test charges
  // end up in a real ledger, so this one says what it is and stops.
  document.querySelectorAll("[data-buy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      say("Demo build. Checkout is not wired, on purpose. In production this opens Stripe at $5.00.");
    });
  });

  // The email field validates and reports. It stores nothing, because a demo
  // with no privacy policy behind it has no business holding an address.
  var form = document.getElementById("signup");
  var note = document.getElementById("signupNote");
  var input = document.getElementById("email");

  if (form && note && input) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var value = input.value.trim();
      var looksValid = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value);

      note.classList.remove("is-ok", "is-bad");

      if (!value) {
        note.textContent = "Enter an email address first.";
        note.classList.add("is-bad");
        input.setAttribute("aria-invalid", "true");
        input.focus();
        return;
      }

      if (!looksValid) {
        note.textContent = "That does not look like a valid address.";
        note.classList.add("is-bad");
        input.setAttribute("aria-invalid", "true");
        input.focus();
        return;
      }

      input.removeAttribute("aria-invalid");
      note.textContent =
        "Valid. In production this would be stored and confirmed. This demo stored nothing.";
      note.classList.add("is-ok");
    });

    input.addEventListener("input", function () {
      input.removeAttribute("aria-invalid");
    });
  }

  /* ---------- 4. explore, with a focus move ---------- */

  // Smooth scroll is handled in CSS. What CSS cannot do is move keyboard focus,
  // and an anchor that moves the viewport without moving focus strands anyone
  // navigating by keyboard.
  var explore = document.querySelector("[data-explore]");
  var target = document.getElementById("precedent");

  if (explore && target) {
    explore.addEventListener("click", function () {
      window.setTimeout(function () {
        var firstTab = target.querySelector(".tab");
        if (firstTab) firstTab.focus({ preventScroll: true });
      }, 500);
    });
  }
})();
