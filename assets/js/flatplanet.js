/* ==========================================================================
   FlatPlanet — Runtime
   Small, dependency-free behaviours for the static component library.
   ========================================================================== */
(function () {
  'use strict';

  /* --------------------------------------------------------------------
     Theme toggle — persists to localStorage
     ------------------------------------------------------------------ */
  var THEME_KEY = 'flatplanet-theme';
  var root = document.documentElement;
  var themeIcon = document.getElementById('themeIcon');

  var SUN = '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>';
  var MOON = '<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>';

  function applyTheme(theme) {
    root.setAttribute('data-theme', theme);
    if (themeIcon) themeIcon.innerHTML = theme === 'dark' ? MOON : SUN;
  }

  var saved = null;
  try { saved = localStorage.getItem(THEME_KEY); } catch (e) { /* private mode */ }
  applyTheme(saved || 'light');

  var toggle = document.getElementById('themeToggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      applyTheme(next);
      try { localStorage.setItem(THEME_KEY, next); } catch (e) { /* ignore */ }
    });
  }

  /* --------------------------------------------------------------------
     Tabs — aria-selected + is-active class
     ------------------------------------------------------------------ */
  function initTabs(scope) {
    (scope || document).querySelectorAll('[role="tablist"]').forEach(function (tablist) {
      var tabs = Array.prototype.slice.call(tablist.querySelectorAll('[role="tab"]'));
      tabs.forEach(function (tab) {
        tab.addEventListener('click', function () {
          tabs.forEach(function (t) {
            t.setAttribute('aria-selected', 'false');
            t.classList.remove('is-active');
          });
          tab.setAttribute('aria-selected', 'true');
          tab.classList.add('is-active');
        });
      });
    });
  }

  /* --------------------------------------------------------------------
     Segmented control + chips
     ------------------------------------------------------------------ */
  function initSegments(scope) {
    (scope || document).querySelectorAll('.fp-segment').forEach(function (seg) {
      var items = seg.querySelectorAll('.fp-segment__item');
      items.forEach(function (item) {
        item.addEventListener('click', function () {
          items.forEach(function (i) {
            i.classList.remove('is-active');
            i.setAttribute('aria-pressed', 'false');
          });
          item.classList.add('is-active');
          item.setAttribute('aria-pressed', 'true');
        });
      });
    });
    (scope || document).querySelectorAll('.fp-chip[aria-pressed]').forEach(function (chip) {
      chip.addEventListener('click', function () {
        var on = chip.getAttribute('aria-pressed') === 'true';
        chip.setAttribute('aria-pressed', on ? 'false' : 'true');
      });
    });
  }

  /* --------------------------------------------------------------------
     Modal
     ------------------------------------------------------------------ */
  var openModals = [];

  function openModal(id) {
    var m = document.getElementById(id);
    if (!m) return;
    m.classList.add('is-open');
    openModals.push(m);
    document.body.style.overflow = 'hidden';
    var focusable = m.querySelector('button, [href], input, select, textarea');
    if (focusable) focusable.focus();
  }

  function closeModal(modal) {
    if (!modal) return;
    modal.classList.remove('is-open');
    openModals = openModals.filter(function (m) { return m !== modal; });
    if (!openModals.length) document.body.style.overflow = '';
  }

  document.addEventListener('click', function (e) {
    var opener = e.target.closest('[data-modal-open]');
    if (opener) { openModal(opener.getAttribute('data-modal-open')); return; }

    var closer = e.target.closest('[data-modal-close]');
    if (closer) {
      var backdrop = closer.closest('.fp-modal-backdrop');
      if (backdrop) closeModal(backdrop);
      return;
    }
    // Click on the scrim (but not the dialog) closes it
    if (e.target.classList && e.target.classList.contains('fp-modal-backdrop')) {
      closeModal(e.target);
    }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      if (openModals.length) closeModal(openModals[openModals.length - 1]);
      closeDrawer();
    }
  });

  /* --------------------------------------------------------------------
     Drawer
     ------------------------------------------------------------------ */
  function openDrawer() {
    var drawer = document.getElementById('demoDrawerPanel');
    var scrim = document.getElementById('demoDrawer');
    if (!drawer) return;
    drawer.classList.add('is-open');
    if (scrim) scrim.classList.add('is-open');
    document.body.style.overflow = 'hidden';
  }

  function closeDrawer() {
    var drawer = document.getElementById('demoDrawerPanel');
    var scrim = document.getElementById('demoDrawer');
    if (drawer) drawer.classList.remove('is-open');
    if (scrim) scrim.classList.remove('is-open');
    if (!openModals.length) document.body.style.overflow = '';
  }

  document.addEventListener('click', function (e) {
    if (e.target.closest('[data-drawer-open]')) { openDrawer(); return; }
    if (e.target.closest('[data-drawer-close]')) { closeDrawer(); return; }
    if (e.target.classList && e.target.classList.contains('fp-drawer-backdrop')) closeDrawer();
  });

  /* --------------------------------------------------------------------
     Toast
     ------------------------------------------------------------------ */
  var ICONS = {
    success: '<path d="M20 6L9 17l-5-5"/>',
    danger: '<circle cx="12" cy="12" r="9"/><path d="M15 9l-6 6M9 9l6 6"/>',
    warning: '<path d="M12 9v4M12 17h.01M10.3 3.9L1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/>',
    info: '<circle cx="12" cy="12" r="9"/><path d="M12 16v-4M12 8h.01"/>'
  };

  function toast(message, type, title) {
    var region = document.getElementById('toastRegion');
    if (!region) return;
    type = type || 'info';
    var el = document.createElement('div');
    el.className = 'fp-toast fp-toast--' + type;
    el.setAttribute('role', 'status');
    el.innerHTML =
      '<span class="fp-toast__icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">' +
      (ICONS[type] || ICONS.info) + '</svg></span>' +
      '<div class="fp-toast__content">' +
      (title ? '<div class="fp-toast__title">' + title + '</div>' : '') +
      '<div>' + message + '</div></div>' +
      '<button class="fp-toast__close" aria-label="Dismiss">' +
      '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"><path d="M18 6L6 18M6 6l12 12"/></svg></button>';
    region.appendChild(el);

    var timer = setTimeout(function () { dismiss(el); }, 4000);
    el.querySelector('.fp-toast__close').addEventListener('click', function () {
      clearTimeout(timer);
      dismiss(el);
    });
  }

  function dismiss(el) {
    el.classList.add('is-leaving');
    setTimeout(function () { el.remove(); }, 220);
  }

  window.FlatPlanet = window.FlatPlanet || {};
  window.FlatPlanet.toast = toast;

  /* --------------------------------------------------------------------
     Palette swatches — rendered from the same token values used in CSS
     ------------------------------------------------------------------ */
  var PALETTE = [
    ['--fp-blue', 'BLP Blue', '#007bff'],
    ['--fp-blue-deep', 'BLP Deep Blue', '#005bdd'],
    ['--fp-blue-ultra-deep', 'BLP Ultra Deep Blue', '#0026a3'],
    ['--fp-blue-soft', 'BLP Soft Blue', '#7fbcff'],
    ['--fp-blue-light', 'BLP Light Blue', '#dbedff'],
    ['--fp-blue-light-deep', 'BLP Light Deep Blue', '#bdcbdb'],
    ['--fp-blue-light-ultra-deep', 'BLP Light Ultra Deep Blue', '#8598ad'],
    ['--fp-blue-neon', 'BLP Neon Blue', '#00ddff'],
    ['--fp-blue-neon-plus', 'BLP Neon Blue Plus', '#00f2ff'],
    ['--fp-blue-cli-accent', 'BLP CLI Accent Blue', '#2fc2ff'],
    ['--fp-blue-logo-sky', 'BLP Logo Sky Blue', '#00afff'],
    ['--fp-blue-logo-dark', 'BLP Logo Dark Blue', '#006dbd'],
    ['--fp-blue-paper', 'BLP Paper Blue', '#f4f8fc'],
    ['--fp-blue-bg', 'BLP BG Blue', '#eef5fc'],

    ['--fp-red', 'BLP Red', '#ff0505'],
    ['--fp-red-deep', 'BLP Deep Red', '#db0000'],
    ['--fp-red-ultra-deep', 'BLP Ultra Deep Red', '#a30000'],
    ['--fp-red-soft', 'BLP Soft Red', '#ff7f7f'],
    ['--fp-red-light', 'BLP Light Red', '#ffdbdb'],
    ['--fp-red-light-deep', 'BLP Light Deep Red', '#dbbdbd'],
    ['--fp-red-light-ultra-deep', 'BLP Light Ultra Deep Red', '#ad8585'],
    ['--fp-red-neon', 'BLP Neon Red', '#ff3f4a'],

    ['--fp-yellow', 'BLP Yellow', '#ffea00'],
    ['--fp-yellow-deep', 'BLP Deep Yellow', '#ebd700'],
    ['--fp-yellow-ultra-deep', 'BLP Ultra Deep Yellow', '#b2a400'],
    ['--fp-yellow-soft', 'BLP Soft Yellow', '#ffeb7f'],
    ['--fp-yellow-light', 'BLP Light Yellow', '#fff9bd'],
    ['--fp-yellow-light-deep', 'BLP Light Deep Yellow', '#dbd9bd'],
    ['--fp-yellow-light-ultra-deep', 'BLP Light Ultra Deep Yellow', '#adaa85'],
    ['--fp-yellow-neon', 'BLP Neon Yellow', '#fcff00'],

    ['--fp-green', 'BLP Green', '#00d620'],
    ['--fp-green-deep', 'BLP Deep Green', '#00b21b'],
    ['--fp-green-ultra-deep', 'BLP Ultra Deep Green', '#007512'],
    ['--fp-green-soft', 'BLP Soft Green', '#6bd67b'],
    ['--fp-green-light', 'BLP Light Green', '#ccffd4'],
    ['--fp-green-light-deep', 'BLP Light Deep Green', '#bddbc1'],
    ['--fp-green-light-ultra-deep', 'BLP Light Ultra Deep Green', '#85ad8b'],
    ['--fp-green-neon', 'BLP Neon Green', '#00ff0e'],
    ['--fp-green-paper', 'BLP Paper Green', '#eaf7ef'],
    ['--fp-green-bg', 'BLP BG Green', '#b8e1d8'],

    ['--fp-purple', 'BLP Purple', '#ae00ff'],
    ['--fp-purple-deep', 'BLP Deep Purple', '#9200d6'],
    ['--fp-purple-ultra-deep', 'BLP Ultra Deep Purple', '#650094'],
    ['--fp-purple-soft', 'BLP Soft Purple', '#d67fff'],
    ['--fp-purple-light', 'BLP Light Purple', '#f4dbff'],
    ['--fp-purple-light-deep', 'BLP Light Deep Purple', '#d2bddb'],
    ['--fp-purple-light-ultra-deep', 'BLP Light Ultra Deep Purple', '#a085ad'],
    ['--fp-purple-neon', 'BLP Neon Purple', '#fa00ff'],
    ['--fp-purple-paper', 'BLP Paper Purple', '#f1f0f5'],
    ['--fp-purple-bg', 'BLP BG Purple', '#d9b8e1'],

    ['--fp-dark', 'BLP Dark', '#00193d'],
    ['--fp-dark-deep', 'BLP Deep Dark', '#000a19'],
    ['--fp-dark-ultra-deep', 'BLP Ultra Deep Dark', '#000309'],
    ['--fp-dark-soft', 'BLP Soft Dark', '#1e2b3d'],
    ['--fp-dark-light', 'BLP Light Dark', '#d4dce8'],
    ['--fp-dark-light-deep', 'BLP Light Deep Dark', '#c7cbd1'],
    ['--fp-dark-light-ultra-deep', 'BLP Light Ultra Deep Dark', '#94989e'],
    ['--fp-sub-dark', 'BLP Sub Dark', '#3e4d5f'],

    ['--fp-white', 'BLP White', '#fefeff'],
    ['--fp-white-deep', 'BLP Deep White', '#fafcff'],
    ['--fp-paper-orange', 'BLP Paper Orange', '#f9f1e5'],
    ['--fp-paper-pink', 'BLP Paper Pink', '#f1e8ec'],
    ['--fp-paper-lime', 'BLP Paper Lime', '#f2f6ed'],
    ['--fp-bg-orange', 'BLP BG Orange', '#fcf5ee'],
    ['--fp-bg-gray', 'BLP BG Gray', '#f5f5f5'],
    ['--fp-bg-brown', 'BLP BG Brown', '#d09c7b']
  ];

  var swatchHost = document.getElementById('swatches');
  if (swatchHost) {
    var html = '';
    PALETTE.forEach(function (c) {
      html +=
        '<div class="fp-swatch">' +
          '<div class="fp-swatch__chip" style="background: ' + c[2] + '"></div>' +
          '<div class="fp-swatch__body">' +
            '<span class="fp-swatch__name">' + c[1] + '</span>' +
            '<span class="fp-swatch__hex">' + c[2] + '</span>' +
            '<span class="fp-swatch__token">' + c[0] + '</span>' +
          '</div>' +
        '</div>';
    });
    swatchHost.innerHTML = html;
  }

  /* --------------------------------------------------------------------
     Scroll spy for the docs TOC (if present)
     ------------------------------------------------------------------ */
  function initScrollSpy() {
    var links = document.querySelectorAll('.fp-toc__item[href^="#"]');
    if (!links.length) return;
    var targets = Array.prototype.map.call(links, function (l) {
      return document.querySelector(l.getAttribute('href'));
    }).filter(Boolean);

    function onScroll() {
      var current = null;
      targets.forEach(function (t) {
        if (t.getBoundingClientRect().top <= 140) current = t.id;
      });
      links.forEach(function (l) {
        l.classList.toggle('is-active', l.getAttribute('href') === '#' + current);
      });
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* --------------------------------------------------------------------
     Boot
     ------------------------------------------------------------------ */
  initTabs();
  initSegments();
  initScrollSpy();
})();
