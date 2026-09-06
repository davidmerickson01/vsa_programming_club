(function () {
  'use strict';

  const USERNAME_RE = /^[a-z0-9_-]{1,32}$/;
  const AUTH_KEY = 'vsa_collab_auth'; // JSON: { username, token }

  const EYE_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z"/><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>';
  const EYE_OFF_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88"/></svg>';
  const COPY_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M15.666 3.888A2.25 2.25 0 0013.5 2.25h-3a2.25 2.25 0 00-2.166 1.638m7.332 0c.055.194.084.4.084.612a.75.75 0 01-.75.75H9a.75.75 0 01-.75-.75c0-.212.03-.418.084-.612m7.332 0c.646.049 1.288.11 1.927.184 1.1.128 1.907 1.077 1.907 2.185V19.5a2.25 2.25 0 01-2.25 2.25H6.75A2.25 2.25 0 014.5 19.5V6.257c0-1.108.806-2.057 1.907-2.185a48.208 48.208 0 011.927-.184"/></svg>';
  const CHECK_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5"/></svg>';

  const sessionId = window.SESSION_ID;

  const loginOverlay = document.getElementById('loginOverlay');
  const loginForm = document.getElementById('loginForm');
  const usernameInput = document.getElementById('usernameInput');
  const passwordInput = document.getElementById('passwordInput');
  const confirmPasswordWrap = document.getElementById('confirmPasswordWrap');
  const confirmPasswordInput = document.getElementById('confirmPasswordInput');
  const loginError = document.getElementById('loginError');

  const appRoot = document.getElementById('appRoot');
  const sessionIdLabel = document.getElementById('sessionIdLabel');
  const usernameLabel = document.getElementById('usernameLabel');
  const copyLinkBtn = document.getElementById('copyLinkBtn');
  const switchUserBtn = document.getElementById('switchUserBtn');
  const archivedBanner = document.getElementById('archivedBanner');

  const codeInput = document.getElementById('codeInput');
  const codeHighlightLayer = document.getElementById('codeHighlightLayer');
  const codeHighlightCode = codeHighlightLayer ? codeHighlightLayer.querySelector('code') : null;
  const submitBtn = document.getElementById('submitBtn');
  const submitStatus = document.getElementById('submitStatus');

  const panelsGrid = document.getElementById('panelsGrid');
  const panelsEmpty = document.getElementById('panelsEmpty');

  let username = null;
  let token = null;
  let isArchived = false;
  let pollGeneration = 0; // bumped to stop a stale polling loop after logging out

  sessionIdLabel.textContent = sessionId;

  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  function getSavedAuth() {
    try {
      const raw = localStorage.getItem(AUTH_KEY);
      if (!raw) return null;
      const parsed = JSON.parse(raw);
      if (parsed && typeof parsed.username === 'string' && typeof parsed.token === 'string') {
        return parsed;
      }
    } catch (err) {
      // fall through
    }
    return null;
  }

  function saveAuth(name, tok) {
    localStorage.setItem(AUTH_KEY, JSON.stringify({ username: name, token: tok }));
  }

  function clearAuth() {
    localStorage.removeItem(AUTH_KEY);
  }

  // ── Password visibility toggles ────────────────────────────────────────

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

  // ── New-username detection (require password twice only for new accounts) ──

  async function usernameNeedsConfirm(name) {
    if (!USERNAME_RE.test(name)) return false;
    try {
      const res = await fetch(`check_username.php?username=${encodeURIComponent(name)}`);
      if (!res.ok) return false;
      const data = await res.json();
      return !data.exists || !data.hasPassword;
    } catch (err) {
      return false;
    }
  }

  function setConfirmVisible(visible) {
    confirmPasswordWrap.classList.toggle('hidden', !visible);
    confirmPasswordInput.required = visible;
    if (!visible) confirmPasswordInput.value = '';
  }

  let usernameCheckTimer = null;
  usernameInput.addEventListener('input', () => {
    clearTimeout(usernameCheckTimer);
    const name = usernameInput.value.trim().toLowerCase();
    usernameCheckTimer = setTimeout(() => {
      usernameNeedsConfirm(name).then(setConfirmVisible);
    }, 350);
  });

  // ── Login ──────────────────────────────────────────────────────────────

  function showLogin() {
    pollGeneration++; // stop any in-flight polling loop
    loginOverlay.classList.remove('hidden');
    appRoot.classList.add('hidden');
    passwordInput.value = '';
    setConfirmVisible(false);
    const saved = getSavedAuth();
    usernameInput.value = saved ? saved.username : '';
    usernameInput.focus();
    if (usernameInput.value) {
      usernameNeedsConfirm(usernameInput.value).then(setConfirmVisible);
    }
  }

  function setArchived(archived) {
    isArchived = archived;
    archivedBanner.classList.toggle('hidden', !archived);
    codeInput.disabled = archived;
    submitBtn.disabled = archived;
  }

  function startApp(name, tok) {
    username = name;
    token = tok;
    saveAuth(name, tok);
    usernameLabel.textContent = name;
    loginOverlay.classList.add('hidden');
    appRoot.classList.remove('hidden');

    const myGeneration = ++pollGeneration;
    initialLoadAndPoll(myGeneration);
  }

  async function login(name, password) {
    const res = await fetch('auth.php', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: name, password }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      throw new Error(data.error || `Login failed (${res.status})`);
    }
    return data;
  }

  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = usernameInput.value.trim().toLowerCase();
    const password = passwordInput.value;

    if (!USERNAME_RE.test(name)) {
      loginError.textContent = 'Use 1-32 letters, numbers, underscore, or hyphen only.';
      loginError.classList.remove('hidden');
      return;
    }

    loginError.classList.add('hidden');
    const submitButton = loginForm.querySelector('button[type="submit"]');
    submitButton.disabled = true;
    try {
      const needsConfirm = await usernameNeedsConfirm(name);
      setConfirmVisible(needsConfirm);
      if (needsConfirm && password !== confirmPasswordInput.value) {
        loginError.textContent = 'Passwords do not match.';
        loginError.classList.remove('hidden');
        return;
      }
      const data = await login(name, password);
      startApp(data.username, data.token);
    } catch (err) {
      loginError.textContent = err.message;
      loginError.classList.remove('hidden');
    } finally {
      submitButton.disabled = false;
    }
  });

  switchUserBtn.addEventListener('click', () => {
    clearAuth();
    showLogin();
  });

  copyLinkBtn.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(location.href);
      const original = copyLinkBtn.textContent;
      copyLinkBtn.textContent = 'Copied!';
      setTimeout(() => { copyLinkBtn.textContent = original; }, 1500);
    } catch (err) {
      prompt('Copy this link:', location.href);
    }
  });

  // ── Submitting code ────────────────────────────────────────────────────

  async function submitCode() {
    if (isArchived) return;
    submitBtn.disabled = true;
    submitStatus.textContent = 'Submitting…';
    try {
      const res = await fetch('submit.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token, session: sessionId, code: codeInput.value }),
      });
      const data = await res.json().catch(() => ({}));
      if (res.status === 401) {
        clearAuth();
        showLogin();
        return;
      }
      if (!res.ok) {
        throw new Error(data.error || `Request failed (${res.status})`);
      }
      submitStatus.textContent = 'Saved ✓';
      setTimeout(() => { submitStatus.textContent = ''; }, 2000);
    } catch (err) {
      submitStatus.textContent = `Error: ${err.message}`;
    } finally {
      submitBtn.disabled = isArchived;
    }
  }

  submitBtn.addEventListener('click', submitCode);
  codeInput.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
      e.preventDefault();
      submitCode();
    }
  });

  // ── Read-only panels ───────────────────────────────────────────────────

  const HIGHLIGHT_LANGS = ['python', 'javascript', 'java', 'cpp', 'c', 'bash', 'html', 'json', 'plaintext'];

  // ── Live syntax highlighting for "Your code" ───────────────────────────
  // A transparent textarea sits on top of a highlighted <pre><code> layer
  // showing the same text, so it's still a real, fully-editable textarea.

  function updateCodeHighlight() {
    if (!codeHighlightCode || !window.hljs) return;
    try {
      codeHighlightCode.innerHTML = window.hljs.highlightAuto(codeInput.value, HIGHLIGHT_LANGS).value;
    } catch (err) {
      codeHighlightCode.textContent = codeInput.value;
    }
  }

  codeInput.addEventListener('input', updateCodeHighlight);
  codeInput.addEventListener('scroll', () => {
    codeHighlightLayer.scrollTop = codeInput.scrollTop;
    codeHighlightLayer.scrollLeft = codeInput.scrollLeft;
  });

  function timeAgo(unixSeconds) {
    const diff = Math.max(0, Date.now() / 1000 - unixSeconds);
    if (diff < 5) return 'just now';
    if (diff < 60) return `${Math.floor(diff)}s ago`;
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
    return `${Math.floor(diff / 86400)}d ago`;
  }

  function renderPanel(sub) {
    const panel = document.createElement('div');
    panel.className = 'panel';

    const header = document.createElement('div');
    header.className = 'panel-header';

    const meta = document.createElement('div');
    meta.className = 'panel-meta';

    const nameEl = document.createElement('span');
    nameEl.className = 'panel-username';
    nameEl.textContent = sub.username === username ? `${sub.username} (you)` : sub.username;

    const timeEl = document.createElement('span');
    timeEl.className = 'panel-time';
    timeEl.dataset.updatedAt = String(sub.updatedAt);
    timeEl.textContent = timeAgo(sub.updatedAt);

    meta.appendChild(nameEl);
    meta.appendChild(timeEl);

    const copyBtn = document.createElement('button');
    copyBtn.type = 'button';
    copyBtn.className = 'panel-copy-btn';
    copyBtn.title = 'Copy to clipboard';
    copyBtn.setAttribute('aria-label', 'Copy code to clipboard');
    copyBtn.innerHTML = COPY_ICON;
    copyBtn.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(sub.code);
        copyBtn.innerHTML = CHECK_ICON;
        setTimeout(() => { copyBtn.innerHTML = COPY_ICON; }, 1200);
      } catch (err) {
        prompt('Copy this code:', sub.code);
      }
    });

    header.appendChild(meta);
    header.appendChild(copyBtn);

    const pre = document.createElement('pre');
    pre.className = 'panel-body';
    const codeEl = document.createElement('code');
    codeEl.textContent = sub.code;
    pre.appendChild(codeEl);

    panel.appendChild(header);
    panel.appendChild(pre);

    if (window.hljs) {
      try {
        const result = window.hljs.highlightAuto(sub.code, HIGHLIGHT_LANGS);
        codeEl.innerHTML = result.value;
        codeEl.classList.add('hljs');
      } catch (err) {
        // fall back to plain escaped text already set via textContent
      }
    }

    return panel;
  }

  function renderSubmissions(submissions) {
    panelsGrid.innerHTML = '';
    submissions.forEach((sub) => panelsGrid.appendChild(renderPanel(sub)));
    panelsEmpty.classList.toggle('hidden', submissions.length > 0);
  }

  // Keep "Xs ago" labels fresh without re-fetching.
  setInterval(() => {
    document.querySelectorAll('.panel-time[data-updated-at]').forEach((el) => {
      el.textContent = timeAgo(Number(el.dataset.updatedAt));
    });
  }, 5000);

  // ── Live updates via short-interval polling ────────────────────────────
  // Each request returns immediately (no server-side blocking), so this
  // stays responsive even behind a single-threaded dev server handling
  // multiple connected clients at once. We just re-fetch on a short,
  // fixed interval and re-render.

  const POLL_INTERVAL_MS = 1200;

  async function refreshOnce() {
    const res = await fetch(
      `submissions.php?s=${encodeURIComponent(sessionId)}&token=${encodeURIComponent(token)}`
    );
    if (res.status === 401) {
      clearAuth();
      showLogin();
      return null;
    }
    if (!res.ok) return null;
    const data = await res.json();
    setArchived(data.status === 'archived');
    const submissions = data.submissions || [];
    renderSubmissions(submissions);
    return submissions;
  }

  async function initialLoadAndPoll(myGeneration) {
    try {
      const submissions = await refreshOnce();
      const mine = submissions && submissions.find((sub) => sub.username === username);
      codeInput.value = mine ? mine.code : '';
      updateCodeHighlight();
    } catch (err) {
      // First load failed; the polling loop below will retry.
    }

    while (pollGeneration === myGeneration) {
      await sleep(POLL_INTERVAL_MS);
      if (pollGeneration !== myGeneration) break;
      try {
        await refreshOnce();
      } catch (err) {
        // Network hiccup; just try again next tick.
      }
    }
  }

  // ── Boot ───────────────────────────────────────────────────────────────

  const saved = getSavedAuth();
  if (saved) {
    startApp(saved.username, saved.token);
  } else {
    showLogin();
  }
})();
