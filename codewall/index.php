<?php
require __DIR__ . '/lib.php';

$sid = (string)($_GET['s'] ?? '');
$sessionMeta = get_session_meta($sid);

if ($sessionMeta === null) {
    http_response_code(404);
    ?>
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width,initial-scale=1" />
      <title>Session not found — VSA Programming Club Code Wall</title>
      <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-100 text-slate-900 min-h-screen flex items-center justify-center p-6">
      <div class="bg-white rounded-2xl shadow-xl p-8 max-w-md text-center">
        <h1 class="text-xl font-black text-indigo-700">Session not found</h1>
        <p class="text-slate-500 mt-2">
          This isn't a valid coding session. Ask your admin for a session link.
        </p>
        <a href="admin.php"
          class="inline-block mt-6 px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl shadow transition">
          I'm the admin — sign in to create one
        </a>
      </div>
    </body>
    </html>
    <?php
    exit;
}
?>
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>VSA Programming Club - Code Wall</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
  <link rel="stylesheet" href="app.css" />
</head>
<body class="bg-slate-100 text-slate-900 min-h-screen">

  <!-- ── Login overlay ── -->
  <div id="loginOverlay" class="fixed inset-0 z-50 bg-slate-900/80 flex items-center justify-center p-6">
    <div class="bg-white rounded-2xl shadow-xl p-8 w-full max-w-sm">
      <h1 class="text-xl font-black text-indigo-700">Join Coding Session</h1>
      <p class="text-slate-500 text-sm mt-1">
        New username? Your password will be set the first time you sign in.
      </p>

      <form id="loginForm" class="mt-6 space-y-4">
        <div>
          <label class="block text-sm font-bold text-slate-700 mb-1" for="usernameInput">Username</label>
          <input
            id="usernameInput" type="text" required maxlength="32" placeholder="e.g. alex"
            pattern="[A-Za-z0-9_-]{1,32}"
            title="Letters, numbers, underscore, and hyphen only"
            class="w-full border border-slate-300 rounded-lg px-4 py-2 text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
        <div>
          <label class="block text-sm font-bold text-slate-700 mb-1" for="passwordInput">Password</label>
          <div class="relative">
            <input
              id="passwordInput" type="password" required maxlength="200"
              class="w-full border border-slate-300 rounded-lg px-4 py-2 pr-10 text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
            <button type="button" data-toggle-for="passwordInput" aria-label="Show password"
              class="toggle-password-btn absolute inset-y-0 right-0 flex items-center px-3 text-slate-400 hover:text-slate-600"></button>
          </div>
        </div>
        <div id="confirmPasswordWrap" class="hidden">
          <label class="block text-sm font-bold text-slate-700 mb-1" for="confirmPasswordInput">Confirm password</label>
          <div class="relative">
            <input
              id="confirmPasswordInput" type="password" maxlength="200"
              class="w-full border border-slate-300 rounded-lg px-4 py-2 pr-10 text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
            <button type="button" data-toggle-for="confirmPasswordInput" aria-label="Show password"
              class="toggle-password-btn absolute inset-y-0 right-0 flex items-center px-3 text-slate-400 hover:text-slate-600"></button>
          </div>
          <p class="text-slate-400 text-xs mt-1">New username — enter your password twice.</p>
        </div>
        <p id="loginError" class="text-red-600 text-sm hidden"></p>
        <button type="submit"
          class="w-full px-4 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl shadow transition">
          Join
        </button>
      </form>
    </div>
  </div>

  <!-- ── Main app (hidden until logged in) ── -->
  <div id="appRoot" class="hidden">
    <header class="sticky top-0 z-40 backdrop-blur bg-white/80 shadow-sm">
      <div class="max-w-6xl mx-auto flex flex-wrap items-center justify-between gap-3 p-4">
        <div>
          <div class="font-bold text-indigo-700">VSA Programming Club - Code Wall</div>
          <div class="text-xs text-slate-500">
            Session: <code id="sessionIdLabel" class="font-mono bg-slate-100 px-1.5 py-0.5 rounded"></code>
            &nbsp;•&nbsp; Signed in as <span id="usernameLabel" class="font-semibold"></span>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <button id="copyLinkBtn"
            class="px-3 py-1.5 text-sm bg-slate-200 hover:bg-slate-300 rounded-lg font-semibold text-slate-700 transition">
            Copy session link
          </button>
          <button id="switchUserBtn"
            class="px-3 py-1.5 text-sm bg-slate-200 hover:bg-slate-300 rounded-lg font-semibold text-slate-700 transition">
            Log out
          </button>
        </div>
      </div>
    </header>

    <div id="archivedBanner" class="hidden max-w-6xl mx-auto px-6 pt-4">
      <div class="bg-amber-100 text-amber-800 text-sm font-semibold rounded-lg px-4 py-2">
        This session is archived (read-only) — new submissions are disabled.
      </div>
    </div>

    <main class="max-w-6xl mx-auto p-6">

      <!-- ── Editor ── -->
      <section class="bg-white rounded-xl shadow p-5">
        <div class="flex items-center justify-between mb-2">
          <h2 class="font-bold text-slate-700">Your code</h2>
          <span id="submitStatus" class="text-sm text-slate-400"></span>
        </div>
        <div class="code-editor-wrap relative w-full h-56 sm:h-64 border border-slate-300 rounded-lg focus-within:ring-2 focus-within:ring-indigo-500">
          <pre id="codeHighlightLayer" class="code-editor-layer code-editor-highlight" aria-hidden="true"><code class="hljs language-python"></code></pre>
          <textarea
            id="codeInput"
            spellcheck="false"
            placeholder="Write or paste your Python code here…"
            class="code-editor-layer code-editor-textarea"
          ></textarea>
        </div>
        <div class="mt-3 flex justify-end">
          <button id="submitBtn"
            class="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl shadow transition">
            Submit
          </button>
        </div>
      </section>

      <!-- ── All submissions ── -->
      <section class="mt-8">
        <h2 class="font-bold text-slate-700 mb-3">Everyone's Code</h2>
        <div id="panelsGrid" class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- panels injected by app.js -->
        </div>
        <p id="panelsEmpty" class="text-slate-400 text-sm mt-2 hidden">
          No one has submitted code in this session yet.
        </p>
      </section>

    </main>
  </div>

  <script>window.SESSION_ID = <?= json_encode($sid) ?>;</script>
  <script src="app.js"></script>
</body>
</html>
