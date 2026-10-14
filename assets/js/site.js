(function () {
  var root = document.documentElement, WA = document.body.getAttribute('data-wa');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* theme toggle (initial theme is set by the inline script in <head>) */
  var tt = document.getElementById('tt');
  function icon() { tt.textContent = root.getAttribute('data-theme') === 'dark' ? '\u2600' : '\u263E'; }
  icon();
  tt.addEventListener('click', function () {
    var n = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', n); icon();
    try { localStorage.setItem('theme', n); } catch (e) {}
  });

  /* mobile menu */
  var m = document.getElementById('menu'), nav = document.getElementById('nav');
  m.addEventListener('click', function () { m.setAttribute('aria-expanded', nav.classList.toggle('open')); });

  /* WhatsApp forms */
  document.querySelectorAll('[data-wa-form]').forEach(function (f) {
    var out = f.querySelector('[data-wa-send]');
    function up() {
      var v = function (n) { var e = f.querySelector('[name=' + n + ']'); return e ? e.value.trim() : ''; };
      var txt = "Hi Mujahid, I'm " + (v('name') || 'a potential client') + '. Project type: ' + v('type') +
        (v('budget') ? '. Budget: ' + v('budget') : '') + '. ' + (v('msg') || "I'd like to discuss a project.");
      out.href = 'https://wa.me/' + WA + '?text=' + encodeURIComponent(txt);
    }
    f.addEventListener('input', up); f.addEventListener('change', up); up();
  });

  /* scroll reveal */
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: .12 });
    document.querySelectorAll('.head,.bento,.mkts,.case,.steps,.trio,.faq,.posts,.cta,.sr,.two,.ab,.stk').forEach(function (el) {
      if (el.getBoundingClientRect().top > innerHeight * .9) { el.classList.add('rv'); io.observe(el); }
    });
  }

  /* card spotlight */
  document.querySelectorAll('.bx,.post').forEach(function (c) {
    c.addEventListener('pointermove', function (e) {
      var r = c.getBoundingClientRect();
      c.style.setProperty('--mx', (e.clientX - r.left) + 'px'); c.style.setProperty('--my', (e.clientY - r.top) + 'px');
    });
  });

  /* typewriter */
  var tw = document.querySelector('.tw');
  if (tw && !reduce) {
    var words = JSON.parse(tw.getAttribute('data-words')), wi = 0, ci = words[0].length, del = true;
    (function tick() {
      var w = words[wi];
      if (del) { ci--; if (ci <= 0) { del = false; wi = (wi + 1) % words.length; } }
      else { ci++; if (ci >= words[wi].length) { del = true; tw.textContent = words[wi]; return setTimeout(tick, 2200); } }
      tw.textContent = words[wi].slice(0, Math.max(ci, 0));
      setTimeout(tick, del ? 38 : 70);
    })();
    setTimeout(function () {}, 0);
  }

  /* particle network */
  var cv = document.getElementById('fx');
  if (cv && !reduce) {
    var ctx = cv.getContext('2d'), W, H, dpr = Math.min(devicePixelRatio || 1, 2), pts = [], mouse = { x: -999, y: -999 }, col = '127,160,255';
    function size() {
      W = innerWidth; H = innerHeight; cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Math.min(70, Math.round(W * H / 18000)); pts = [];
      for (var i = 0; i < n; i++) pts.push({ x: Math.random() * W, y: Math.random() * H, vx: (Math.random() - .5) * .35, vy: (Math.random() - .5) * .35 });
    }
    size(); addEventListener('resize', size);
    addEventListener('pointermove', function (e) { mouse.x = e.clientX; mouse.y = e.clientY; });
    (function draw() {
      if (!document.hidden) {
        col = root.getAttribute('data-theme') === 'dark' ? '127,160,255' : '20,71,230';
        ctx.clearRect(0, 0, W, H);
        for (var i = 0; i < pts.length; i++) {
          var p = pts[i]; p.x += p.vx; p.y += p.vy;
          if (p.x < 0 || p.x > W) p.vx *= -1; if (p.y < 0 || p.y > H) p.vy *= -1;
          ctx.fillStyle = 'rgba(' + col + ',.55)'; ctx.beginPath(); ctx.arc(p.x, p.y, 1.6, 0, 6.283); ctx.fill();
          for (var j = i + 1; j < pts.length; j++) {
            var q = pts[j], dx = p.x - q.x, dy = p.y - q.y, d = dx * dx + dy * dy;
            if (d < 14400) { ctx.strokeStyle = 'rgba(' + col + ',' + (.22 * (1 - d / 14400)) + ')'; ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(q.x, q.y); ctx.stroke(); }
          }
          var mx = p.x - mouse.x, my = p.y - mouse.y, md = mx * mx + my * my;
          if (md < 19600) { ctx.strokeStyle = 'rgba(198,244,50,' + (.35 * (1 - md / 19600)) + ')'; ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(mouse.x, mouse.y); ctx.stroke(); }
        }
      }
      requestAnimationFrame(draw);
    })();
  }
})();
