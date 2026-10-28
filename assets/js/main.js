/* 付钟浩 Alex · 个人网站脚本：主题切换、出现动画、卡片高光、进度轨、复制、终端、筛选、时钟。零依赖。 */
(function () {
  'use strict';
  var root = document.documentElement;
  root.classList.remove('no-js');
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 主题 ---------- */
  function setTheme(t) {
    root.setAttribute('data-theme', t);
    try { localStorage.setItem('theme', t); } catch (e) {}
  }
  function toggleTheme() {
    setTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
    return root.getAttribute('data-theme');
  }
  document.querySelectorAll('[data-theme-toggle]').forEach(function (b) {
    b.addEventListener('click', toggleTheme);
  });

  /* ---------- 出现动画 ---------- */
  var reveals = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window) || reduceMotion) {
    reveals.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
    reveals.forEach(function (el, i) {
      el.style.transitionDelay = Math.min((i % 6) * 40, 200) + 'ms';
      io.observe(el);
    });
  }

  /* ---------- 卡片高光 ---------- */
  if (!reduceMotion) {
    document.querySelectorAll('.gx').forEach(function (el) {
      if (!el.querySelector(':scope > .spot')) {
        var s = document.createElement('span');
        s.className = 'spot';
        el.insertBefore(s, el.firstChild);
      }
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        el.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        el.style.setProperty('--my', (e.clientY - r.top) + 'px');
      });
    });
  }

  /* ---------- 右侧进度轨 ---------- */
  var railTargets = document.querySelectorAll('[data-rail]');
  if (railTargets.length > 1 && 'IntersectionObserver' in window) {
    var rail = document.createElement('nav');
    rail.className = 'rail';
    rail.setAttribute('aria-label', '页面进度');
    var links = [];
    railTargets.forEach(function (sec) {
      var a = document.createElement('a');
      a.href = '#' + sec.id;
      a.innerHTML = '<span class="lbl"></span><span class="dot"></span>';
      a.querySelector('.lbl').textContent = sec.getAttribute('data-rail');
      rail.appendChild(a);
      links.push({ a: a, sec: sec });
    });
    document.body.appendChild(rail);
    var current = null;
    var ro = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) current = en.target;
      });
      links.forEach(function (l) { l.a.classList.toggle('on', l.sec === current); });
    }, { rootMargin: '-45% 0px -50% 0px' });
    railTargets.forEach(function (s) { ro.observe(s); });
  }

  /* ---------- 复制 ---------- */
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
    return new Promise(function (resolve, reject) {
      var ta = document.createElement('textarea');
      ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy') ? resolve() : reject(); } catch (e) { reject(e); }
      document.body.removeChild(ta);
    });
  }
  document.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      copyText(btn.getAttribute('data-copy')).then(function () {
        btn.classList.add('done');
        setTimeout(function () { btn.classList.remove('done'); }, 1400);
      }, function () {});
    });
  });

  /* ---------- 项目筛选 ---------- */
  var filterBar = document.querySelector('.filters');
  if (filterBar) {
    filterBar.addEventListener('click', function (e) {
      var b = e.target.closest('button[data-filter]');
      if (!b) return;
      var f = b.getAttribute('data-filter');
      filterBar.querySelectorAll('button').forEach(function (x) { x.classList.toggle('on', x === b); });
      document.querySelectorAll('[data-kind]').forEach(function (card) {
        card.classList.toggle('is-hidden', f !== 'all' && card.getAttribute('data-kind') !== f);
      });
    });
  }

  /* ---------- 页脚时钟（北京时间） ---------- */
  var clock = document.querySelector('[data-clock]');
  if (clock) {
    var fmt = function () {
      try {
        return new Intl.DateTimeFormat('zh-CN', { timeZone: 'Asia/Shanghai', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false }).format(new Date());
      } catch (e) { return new Date().toTimeString().slice(0, 8); }
    };
    var tick = function () { clock.textContent = fmt(); };
    tick(); setInterval(tick, 1000);
  }

  /* ---------- 文章目录高亮 ---------- */
  var tocLinks = document.querySelectorAll('.toc a[href^="#"]');
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var to = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          tocLinks.forEach(function (a) { a.classList.remove('on'); });
          var a = map[en.target.id];
          if (a) a.classList.add('on');
        }
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    Object.keys(map).forEach(function (id) { var h = document.getElementById(id); if (h) to.observe(h); });
  }

  /* ---------- 终端 ---------- */
  var term = document.getElementById('term');
  var dataEl = document.getElementById('term-data');
  if (term && dataEl) {
    var data = JSON.parse(dataEl.textContent);
    var out = term.querySelector('.term-out');
    var input = term.querySelector('input');
    var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
    var print = function (html, cls) {
      var d = document.createElement('div');
      d.className = 'line' + (cls ? ' ' + cls : '');
      d.innerHTML = html;
      out.appendChild(d);
      out.scrollTop = out.scrollHeight;
    };
    var commands = {
      help: function () {
        return '可用命令：\n' + data.commands.map(function (c) { return '  <b>' + esc(c[0]) + '</b>  ' + esc(c[1]); }).join('\n');
      },
      whoami: function () { return esc(data.whoami); },
      skills: function () {
        return data.skills.map(function (g) { return '<b>' + esc(g[0]) + '</b>\n  ' + g[1].map(esc).join(' · '); }).join('\n');
      },
      courses: function () {
        return data.courses.map(function (c) { return '• <b>' + esc(c[0]) + '</b>  <span class="muted">' + esc(c[1]) + '</span>'; }).join('\n');
      },
      projects: function () {
        return data.projects.map(function (p) {
          return '• <a href="' + esc(p[2]) + '">' + esc(p[0]) + '</a>  <span class="muted">' + esc(p[1]) + '</span>';
        }).join('\n');
      },
      sites: function () {
        return data.sites.map(function (s) {
          return '• <a href="' + esc(s[1]) + '" target="_blank" rel="noopener">' + esc(s[0]) + '</a>';
        }).join('\n');
      },
      contact: function () {
        return data.contact.map(function (c) { return '<b>' + esc(c[0]) + '</b>  ' + esc(c[1]); }).join('\n');
      },
      theme: function () { return '已切换到' + (toggleTheme() === 'dark' ? '深色' : '浅色') + '主题。'; },
      clear: function () { out.innerHTML = ''; return null; }
    };
    var run = function (raw) {
      var cmd = String(raw || '').trim().toLowerCase();
      if (!cmd) return;
      print(esc(cmd), 'cmd');
      var fn = commands[cmd];
      var res = fn ? fn() : '没有这个命令：' + esc(cmd) + '。输入 <b>help</b> 看看有哪些。';
      if (res !== null) print(res);
    };
    term.querySelectorAll('.chip[data-cmd]').forEach(function (c) {
      c.addEventListener('click', function () { run(c.getAttribute('data-cmd')); });
    });
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { run(input.value); input.value = ''; }
    });
  }
  /* ---------- 现场：视频进入视野才加载和播放；点开看大图，左右键翻页 ---------- */
  var tiles = Array.prototype.slice.call(document.querySelectorAll('.tile'));
  if (tiles.length) {
    var tileVideos = document.querySelectorAll('.tile video[data-src]');
    if (!reduceMotion && 'IntersectionObserver' in window) {
      var vo = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          var v = en.target;
          if (en.isIntersecting) {
            if (!v.getAttribute('src')) v.src = v.getAttribute('data-src');
            var pr = v.play();
            if (pr && pr.catch) pr.catch(function () {});
          } else {
            v.pause();
          }
        });
      }, { threshold: 0.5 });
      tileVideos.forEach(function (v) { vo.observe(v); });
    }
    var dlg = document.querySelector('.lightbox');
    if (dlg && typeof dlg.showModal === 'function') {
      var lbImg = dlg.querySelector('.lb-img'), lbVid = dlg.querySelector('.lb-video');
      var lbCap = dlg.querySelector('.lb-cap'), lbCnt = dlg.querySelector('.lb-count');
      var lbList = [], lbCur = 0;
      var lbShow = function (i) {
        lbCur = (i + lbList.length) % lbList.length;
        var t = lbList[lbCur], isVideo = t.getAttribute('data-type') === 'video';
        lbImg.hidden = isVideo;
        lbVid.hidden = !isVideo;
        if (isVideo) {
          lbImg.removeAttribute('src');
          lbVid.poster = t.getAttribute('data-poster');
          lbVid.src = t.getAttribute('data-full');
          var pr = lbVid.play();
          if (pr && pr.catch) pr.catch(function () {});
        } else {
          lbVid.pause();
          lbVid.removeAttribute('src');
          lbImg.src = t.getAttribute('data-full');
          lbImg.alt = t.getAttribute('data-cap');
        }
        lbCap.textContent = t.getAttribute('data-cap');
        lbCnt.textContent = (lbCur + 1) + ' / ' + lbList.length;
      };
      tiles.forEach(function (t) {
        t.addEventListener('click', function () {
          lbList = tiles.filter(function (x) { return x.offsetParent !== null; });
          lbShow(Math.max(0, lbList.indexOf(t)));
          dlg.showModal();
        });
      });
      dlg.querySelector('.lb-prev').addEventListener('click', function () { lbShow(lbCur - 1); });
      dlg.querySelector('.lb-next').addEventListener('click', function () { lbShow(lbCur + 1); });
      dlg.querySelector('.lb-close').addEventListener('click', function () { dlg.close(); });
      dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
      dlg.addEventListener('close', function () { lbVid.pause(); });
      document.addEventListener('keydown', function (e) {
        if (!dlg.open) return;
        if (e.key === 'ArrowLeft') lbShow(lbCur - 1);
        if (e.key === 'ArrowRight') lbShow(lbCur + 1);
      });
    } else {
      // 不支持 dialog 的老浏览器：直接新窗口打开原图或视频
      tiles.forEach(function (t) {
        t.addEventListener('click', function () { window.open(t.getAttribute('data-full'), '_blank'); });
      });
    }
  }
})();
