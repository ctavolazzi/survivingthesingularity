(function () {
  var views = ['people', 'map', 'drive', 'scene', 'later', 'beats', 'shape', 'rhymes', 'arcs', 'fixes', 'method'];
  var jump = document.getElementById('jump');
  var jumpwrap = document.getElementById('jumpwrap');

  function show(name) {
    if (views.indexOf(name) < 0) name = 'people';
    views.forEach(function (v) {
      document.getElementById('view-' + v).hidden = v !== name;
      var tab = document.getElementById('tab-' + v);
      if (v === name) tab.setAttribute('aria-current', 'page');
      else tab.removeAttribute('aria-current');
    });
    jumpwrap.hidden = name !== 'people';
    return name;
  }

  function fromHash(scroll) {
    show((location.hash || '').slice(1));
    if (scroll) window.scrollTo(0, 0);
  }

  function goTo(id) {
    var el = document.getElementById(id);
    if (!el) return;
    show('people');
    el.scrollIntoView({ block: 'start' });
  }

  window.addEventListener('hashchange', function () { fromHash(true); });
  jump.addEventListener('change', function () {
    if (jump.value) goTo(jump.value);
    jump.value = '';
  });
  document.addEventListener('click', function (e) {
    var b = e.target.closest ? e.target.closest('[data-jump]') : null;
    if (b) goTo(b.getAttribute('data-jump'));
    var s = e.target.closest ? e.target.closest('[data-scroll]') : null;
    if (s) {
      var t = document.getElementById(s.getAttribute('data-scroll'));
      if (t) t.scrollIntoView({ block: 'start' });
    }
  });

  fromHash(false);
})();

(function () {
  var holder = document.getElementById('shape-data');
  var fig = document.getElementById('shape-chart');
  if (!holder || !fig) return;
  var d = JSON.parse(holder.textContent);
  var svg = document.getElementById('shape-svg');
  var hair = document.getElementById('shape-hair');
  var cur = document.getElementById('shape-cur');
  var tip = document.getElementById('shape-tip');
  var hit = document.getElementById('shape-hit');
  var at = 14;

  function xOf(i) { return d.L + i * d.PW / 39; }
  function yOf(v) { return d.T + (5 - v) * d.PH / 10; }

  function show(i) {
    at = Math.max(0, Math.min(39, i));
    var r = d.rows[at];
    var x = xOf(at);
    hair.setAttribute('x1', x); hair.setAttribute('x2', x);
    hair.setAttribute('visibility', 'visible');
    if (r.v === null) { cur.setAttribute('visibility', 'hidden'); }
    else {
      cur.setAttribute('cx', x); cur.setAttribute('cy', yOf(r.v));
      cur.setAttribute('visibility', 'visible');
    }
    tip.textContent = '';
    var a = document.createElement('strong');
    a.textContent = r.v === null ? 'not in it' : (r.v > 0 ? '+' + r.v : String(r.v));
    var b = document.createElement('span');
    b.textContent = 'Ch ' + r.c + ' \u00b7 ' + r.t;
    var c = document.createElement('span');
    c.className = 'tipnote';
    c.textContent = r.n;
    tip.appendChild(a); tip.appendChild(b); tip.appendChild(c);
    tip.hidden = false;
    var box = svg.getBoundingClientRect();
    var figBox = fig.getBoundingClientRect();
    var px = box.left - figBox.left + x * box.width / d.W;
    var w = tip.offsetWidth;
    var left = Math.max(6, Math.min(figBox.width - w - 6, px - w / 2));
    tip.style.left = left + 'px';
    tip.style.top = (box.top - figBox.top + 4) + 'px';
  }
  function hide() {
    hair.setAttribute('visibility', 'hidden');
    cur.setAttribute('visibility', 'hidden');
    tip.hidden = true;
  }
  function fromPointer(e) {
    var box = svg.getBoundingClientRect();
    var x = (e.clientX - box.left) * d.W / box.width;
    show(Math.round((x - d.L) * 39 / d.PW));
  }
  hit.addEventListener('pointermove', fromPointer);
  hit.addEventListener('pointerdown', fromPointer);
  hit.addEventListener('pointerleave', function (e) { if (e.pointerType === 'mouse') hide(); });
  fig.addEventListener('focus', function () { show(at); });
  fig.addEventListener('blur', hide);
  fig.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') { show(at - 1); e.preventDefault(); }
    else if (e.key === 'ArrowRight') { show(at + 1); e.preventDefault(); }
    else if (e.key === 'Escape') { hide(); }
  });
})();
