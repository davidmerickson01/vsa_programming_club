(function () {
  'use strict';

  const TOKEN_KEY = 'vsa_admin_token';

  const EYE_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z"/><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>';
  const EYE_OFF_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88"/></svg>';

  const loginOverlay = document.getElementById('loginOverlay');
  const loginForm = document.getElementById('loginForm');
  const passwordInput = document.getElementById('passwordInput');
  const loginError = document.getElementById('loginError');

  const adminRoot = document.getElementById('adminRoot');
  const logoutBtn = document.getElementById('logoutBtn');

  const newSessionForm = document.getElementById('newSessionForm');
  const newSessionName = document.getElementById('newSessionName');
  const newSessionError = document.getElementById('newSessionError');
  const newSessionLink = document.getElementById('newSessionLink');
  const sessionsBody = document.getElementById('sessionsTableBody');
  const sessionsEmpty = document.getElementById('sessionsEmpty');
  const usersBody = document.getElementById('usersTableBody');
  const usersEmpty = document.getElementById('usersEmpty');

  let token = localStorage.getItem(TOKEN_KEY) || null;

  function sessionLinkFor(id) {
    const base = location.pathname.replace(/admin\.php$/, 'index.php');
    return `${location.origin}${base}?s=${encodeURIComponent(id)}`;
  }

  function fmtDate(ts) {
    if (!ts) return '—';
    return new Date(ts * 1000).toLocaleString();
  }

  function slugify(input) {
    return input
      .trim()
      .toLowerCase()
      .replace(/[^a-z0-9_-]+/g, '-')
      .replace(/^-+|-+$/g, '')
      .slice(0, 64);
  }

  document.querySelectorAll('.toggle-password-btn').forEach((btn) => {
    const input = document.getElementById(btn.dataset.toggleFor);
    if (!input) return;
    btn.innerHTML = EYE_ICON;
    btn.addEventListener('click', () => {
      const showing = input.type === 'text';
      input.type = showing ? 'password' : 'text';
      btn.innerHTML = showing ? EYE_ICON : EYE_OFF_ICON;
      btn.setAttribute('aria-label', showing ? 'Show password' : 'Hide password');
    });
  });

  function showLogin() {
    loginOverlay.classList.remove('hidden');
    adminRoot.classList.add('hidden');
    passwordInput.value = '';
    passwordInput.focus();
  }

  function showAdmin() {
    loginOverlay.classList.add('hidden');
    adminRoot.classList.remove('hidden');
    loadData();
  }

  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    loginError.classList.add('hidden');
    const submitButton = loginForm.querySelector('button[type="submit"]');
    submitButton.disabled = true;
    try {
      const res = await fetch('auth.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: 'admin', password: passwordInput.value }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data.error || 'Login failed');
      if (!data.isAdmin) throw new Error('That account is not the admin account.');
      token = data.token;
      localStorage.setItem(TOKEN_KEY, token);
      showAdmin();
    } catch (err) {
      loginError.textContent = err.message;
      loginError.classList.remove('hidden');
    } finally {
      submitButton.disabled = false;
    }
  });

  logoutBtn.addEventListener('click', () => {
    localStorage.removeItem(TOKEN_KEY);
    token = null;
    showLogin();
  });

  async function loadData() {
    const res = await fetch(`admin_data.php?token=${encodeURIComponent(token)}`);
    if (res.status === 403) {
      localStorage.removeItem(TOKEN_KEY);
      token = null;
      showLogin();
      return;
    }
    if (!res.ok) return;
    const data = await res.json();
    renderSessions(data.sessions || []);
    renderUsers(data.users || []);
  }

  function renderSessions(sessions) {
    sessionsBody.innerHTML = '';
    sessionsEmpty.classList.toggle('hidden', sessions.length > 0);

    sessions.forEach((s) => {
      const tr = document.createElement('tr');
      tr.className = 'border-b last:border-0';

      const link = sessionLinkFor(s.id);
      const nextStatus = s.status === 'active' ? 'archived' : 'active';
      const badgeClass = s.status === 'active'
        ? 'bg-emerald-100 text-emerald-700'
        : 'bg-amber-100 text-amber-700';

      tr.innerHTML = `
        <td class="py-2 pr-3 font-mono">
          <a href="${link}" target="_blank" class="text-indigo-600 hover:underline">${s.id}</a>
        </td>
        <td class="py-2 pr-3">
          <span class="px-2 py-0.5 rounded text-xs font-bold ${badgeClass}">${s.status}</span>
        </td>
        <td class="py-2 pr-3 text-slate-500">${fmtDate(s.createdAt)}</td>
        <td class="py-2 text-right whitespace-nowrap space-x-2">
          <button data-id="${s.id}" data-status="${nextStatus}"
            class="toggle-session-btn px-3 py-1 bg-slate-200 hover:bg-slate-300 rounded-lg text-xs font-semibold">
            Mark ${s.status === 'active' ? 'read-only' : 'active'}
          </button>
          <button data-id="${s.id}"
            class="delete-session-btn px-3 py-1 bg-red-100 hover:bg-red-200 text-red-700 rounded-lg text-xs font-semibold">
            Delete session
          </button>
        </td>
      `;
      sessionsBody.appendChild(tr);
    });

    sessionsBody.querySelectorAll('.toggle-session-btn').forEach((btn) => {
      btn.addEventListener('click', async () => {
        await fetch('admin_set_session_status.php', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ token, session: btn.dataset.id, status: btn.dataset.status }),
        });
        loadData();
      });
    });

    sessionsBody.querySelectorAll('.delete-session-btn').forEach((btn) => {
      btn.addEventListener('click', async () => {
        if (!confirm(`Delete session "${btn.dataset.id}" and all code submitted in it? This can't be undone.`)) {
          return;
        }
        await fetch('admin_delete_session.php', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ token, session: btn.dataset.id }),
        });
        loadData();
      });
    });
  }

  function renderUsers(users) {
    usersBody.innerHTML = '';
    usersEmpty.classList.toggle('hidden', users.length > 0);

    users.forEach((u) => {
      const tr = document.createElement('tr');
      tr.className = 'border-b last:border-0';
      const pwCell = u.hasPassword
        ? 'Yes'
        : '<span class="text-amber-600 font-semibold">No (can set on next login)</span>';

      tr.innerHTML = `
        <td class="py-2 pr-3">${u.username}</td>
        <td class="py-2 pr-3">${pwCell}</td>
        <td class="py-2 pr-3 text-slate-500">${fmtDate(u.createdAt)}</td>
        <td class="py-2 text-right whitespace-nowrap space-x-2">
          <button data-username="${u.username}"
            class="clear-pw-btn px-3 py-1 bg-slate-200 hover:bg-slate-300 rounded-lg text-xs font-semibold">
            Clear password
          </button>
          <button data-username="${u.username}"
            class="delete-user-btn px-3 py-1 bg-red-100 hover:bg-red-200 text-red-700 rounded-lg text-xs font-semibold">
            Delete account
          </button>
        </td>
      `;
      usersBody.appendChild(tr);
    });

    usersBody.querySelectorAll('.clear-pw-btn').forEach((btn) => {
      btn.addEventListener('click', async () => {
        if (!confirm(`Clear the password for "${btn.dataset.username}"? They'll be able to set a new one with no verification.`)) {
          return;
        }
        await fetch('admin_clear_password.php', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ token, username: btn.dataset.username }),
        });
        loadData();
      });
    });

    usersBody.querySelectorAll('.delete-user-btn').forEach((btn) => {
      btn.addEventListener('click', async () => {
        if (!confirm(`Delete the account "${btn.dataset.username}" and all of their submitted code? This can't be undone.`)) {
          return;
        }
        await fetch('admin_delete_user.php', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ token, username: btn.dataset.username }),
        });
        loadData();
      });
    });
  }

  newSessionForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    newSessionError.classList.add('hidden');
    newSessionLink.classList.add('hidden');

    const name = slugify(newSessionName.value);
    if (name === '') {
      newSessionError.textContent = 'Enter a name using letters, numbers, underscore, or hyphen.';
      newSessionError.classList.remove('hidden');
      return;
    }

    const res = await fetch('admin_new_session.php', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token, name }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      newSessionError.textContent = data.error || 'Could not create session.';
      newSessionError.classList.remove('hidden');
      return;
    }

    newSessionName.value = '';
    const link = sessionLinkFor(data.id);
    newSessionLink.innerHTML = `New session created: <a href="${link}" target="_blank" class="font-mono underline">${link}</a>`;
    newSessionLink.classList.remove('hidden');
    loadData();
  });

  // ── Boot ───────────────────────────────────────────────────────────────

  if (token) {
    showAdmin();
  } else {
    showLogin();
  }
})();
