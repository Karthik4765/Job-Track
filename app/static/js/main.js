/* ============================================================
   JOBTRACK – GLOBAL JAVASCRIPT
   Theme toggle, sidebar, flash messages, utilities
   ============================================================ */

(function () {
  'use strict';

  // ── Theme ─────────────────────────────────────────────────
  const THEME_KEY = 'jt_theme';

  function getTheme() {
    return localStorage.getItem(THEME_KEY) ||
      document.documentElement.getAttribute('data-theme') || 'dark';
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(THEME_KEY, theme);
    const icons = document.querySelectorAll('.theme-icon');
    icons.forEach(icon => {
      icon.textContent = theme === 'dark' ? '☀️' : '🌙';
    });
    const toggles = document.querySelectorAll('.theme-toggle-btn');
    toggles.forEach(btn => btn.setAttribute('data-theme', theme));
  }

  function toggleTheme() {
    const current = getTheme();
    const next = current === 'dark' ? 'light' : 'dark';
    applyTheme(next);
    // Persist to server
    fetch('/settings/theme', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: `theme=${next}`
    }).catch(() => {});
  }

  // Init theme
  applyTheme(getTheme());

  // ── Flash Messages ─────────────────────────────────────────
  function initFlashes() {
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(flash => {
      const closeBtn = flash.querySelector('.flash-close');
      if (closeBtn) {
        closeBtn.addEventListener('click', () => dismissFlash(flash));
      }
      setTimeout(() => dismissFlash(flash), 5000);
    });
  }

  function dismissFlash(el) {
    el.style.animation = 'slideInRight 0.3s ease reverse';
    setTimeout(() => el.remove(), 300);
  }

  // ── Sidebar ────────────────────────────────────────────────
  function initSidebar() {
    const hamburger = document.getElementById('hamburger');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');

    if (!hamburger || !sidebar) return;

    hamburger.addEventListener('click', () => {
      sidebar.classList.toggle('mobile-open');
      overlay?.classList.toggle('active');
    });

    overlay?.addEventListener('click', () => {
      sidebar.classList.remove('mobile-open');
      overlay.classList.remove('active');
    });
  }

  // ── Delete Confirmations ────────────────────────────────────
  function initDeleteForms() {
    document.querySelectorAll('[data-confirm]').forEach(el => {
      el.addEventListener('submit', function (e) {
        const msg = this.getAttribute('data-confirm') || 'Are you sure?';
        if (!confirm(msg)) e.preventDefault();
      });
      el.addEventListener('click', function (e) {
        if (this.tagName !== 'FORM') {
          const msg = this.getAttribute('data-confirm') || 'Are you sure?';
          if (!confirm(msg)) e.preventDefault();
        }
      });
    });
  }

  // ── Modal ──────────────────────────────────────────────────
  window.openModal = function (id) {
    const overlay = document.getElementById(id);
    if (overlay) {
      overlay.classList.add('active');
      document.body.style.overflow = 'hidden';
    }
  };

  window.closeModal = function (id) {
    const overlay = document.getElementById(id);
    if (overlay) {
      overlay.classList.remove('active');
      document.body.style.overflow = '';
    }
  };

  function initModals() {
    // Close on overlay click
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
      overlay.addEventListener('click', function (e) {
        if (e.target === this) {
          this.classList.remove('active');
          document.body.style.overflow = '';
        }
      });
    });

    // Close on Escape key
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        document.querySelectorAll('.modal-overlay.active').forEach(overlay => {
          overlay.classList.remove('active');
          document.body.style.overflow = '';
        });
      }
    });
  }

  // ── View Toggle (Table/Card) ────────────────────────────────
  window.setView = function (view) {
    const tableView = document.getElementById('table-view');
    const cardView = document.getElementById('card-view');
    const tableBtnEl = document.getElementById('btn-table');
    const cardBtnEl = document.getElementById('btn-card');

    if (view === 'table') {
      tableView?.classList.remove('hidden');
      cardView?.classList.add('hidden');
      tableBtnEl?.classList.add('active');
      cardBtnEl?.classList.remove('active');
    } else {
      tableView?.classList.add('hidden');
      cardView?.classList.remove('hidden');
      cardBtnEl?.classList.add('active');
      tableBtnEl?.classList.remove('active');
    }
    localStorage.setItem('jt_view', view);
    // Update URL param without reload
    const url = new URL(window.location);
    url.searchParams.set('view', view);
    window.history.replaceState({}, '', url);
  };

  // ── Animate on scroll ──────────────────────────────────────
  function initAnimations() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.animationPlayState = 'running';
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });

    document.querySelectorAll('.animate-in').forEach(el => {
      el.style.animationPlayState = 'paused';
      observer.observe(el);
    });
  }

  // ── Tooltip ────────────────────────────────────────────────
  function initTooltips() {
    document.querySelectorAll('[data-tooltip]').forEach(el => {
      el.addEventListener('mouseenter', function () {
        const tip = document.createElement('div');
        tip.className = 'tooltip-popup';
        tip.textContent = this.getAttribute('data-tooltip');
        tip.style.cssText = `
          position: fixed; z-index: 9999;
          background: var(--bg-tertiary); color: var(--text-primary);
          font-size: 11px; padding: 5px 9px; border-radius: 5px;
          border: 1px solid var(--border); pointer-events: none;
          white-space: nowrap; box-shadow: var(--shadow);
        `;
        document.body.appendChild(tip);
        const rect = this.getBoundingClientRect();
        tip.style.top = (rect.top - 32) + 'px';
        tip.style.left = (rect.left + rect.width / 2 - tip.offsetWidth / 2) + 'px';
        this._tooltip = tip;
      });
      el.addEventListener('mouseleave', function () {
        this._tooltip?.remove();
      });
    });
  }

  // ── Format dates relative ──────────────────────────────────
  window.timeAgo = function (dateStr) {
    const date = new Date(dateStr);
    const now = new Date();
    const diff = Math.floor((now - date) / 1000);

    if (diff < 60) return 'just now';
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
    if (diff < 604800) return `${Math.floor(diff / 86400)}d ago`;
    return date.toLocaleDateString('en-IN', { month: 'short', day: 'numeric' });
  };

  // ── Number counter animation ────────────────────────────────
  function animateCounters() {
    document.querySelectorAll('.stat-value[data-count]').forEach(el => {
      const target = parseInt(el.getAttribute('data-count'));
      let current = 0;
      const step = Math.max(1, Math.ceil(target / 30));
      const timer = setInterval(() => {
        current = Math.min(current + step, target);
        el.textContent = current;
        if (current >= target) clearInterval(timer);
      }, 30);
    });
  }

  // ── Init ──────────────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', function () {
    initFlashes();
    initSidebar();
    initDeleteForms();
    initModals();
    initAnimations();
    initTooltips();
    animateCounters();

    // Theme toggle buttons
    document.querySelectorAll('.theme-toggle-btn').forEach(btn => {
      btn.addEventListener('click', toggleTheme);
    });
  });

})();
