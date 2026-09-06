<?php
require __DIR__ . '/lib.php';
?>
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Admin — VSA Programming Club Code Wall</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-100 text-slate-900 min-h-screen">

  <!-- ── Admin login overlay ── -->
  <div id="loginOverlay" class="fixed inset-0 z-50 bg-slate-900/80 flex items-center justify-center p-6">
    <div class="bg-white rounded-2xl shadow-xl p-8 w-full max-w-sm">
      <h1 class="text-xl font-black text-indigo-700">Admin Login</h1>
      <p class="text-slate-500 text-sm mt-1">Sign in as the admin account.</p>

      <form id="loginForm" class="mt-6 space-y-4">
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
        <p id="loginError" class="text-red-600 text-sm hidden"></p>
        <button type="submit"
          class="w-full px-4 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl shadow transition">
          Sign in
        </button>
      </form>
      <p class="text-slate-400 text-xs mt-3">
        First time? Any password you enter here becomes the admin password.
      </p>
    </div>
  </div>

  <!-- ── Admin dashboard ── -->
  <div id="adminRoot" class="hidden max-w-5xl mx-auto p-6">
    <header class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-black text-indigo-700">Admin — Code Wall</h1>
      <button id="logoutBtn"
        class="px-3 py-1.5 text-sm bg-slate-200 hover:bg-slate-300 rounded-lg font-semibold text-slate-700 transition">
        Log out
      </button>
    </header>

    <section class="bg-white rounded-xl shadow p-5 mb-8">
      <h2 class="font-bold text-slate-700 mb-3">Sessions</h2>

      <form id="newSessionForm" class="flex flex-wrap items-start gap-2 mb-2">
        <div class="flex-1 min-w-[200px]">
          <input id="newSessionName" type="text" required maxlength="64"
            placeholder="e.g. week-3-warmup"
            class="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>
        <button type="submit"
          class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl shadow transition text-sm">
          + New session
        </button>
      </form>
      <p id="newSessionError" class="text-red-600 text-sm mb-3 hidden"></p>
      <p id="newSessionLink" class="text-sm mb-3 hidden bg-emerald-50 text-emerald-800 rounded-lg px-3 py-2"></p>

      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="text-left text-slate-500 border-b">
              <th class="py-2 pr-3">Session</th>
              <th class="py-2 pr-3">Status</th>
              <th class="py-2 pr-3">Created</th>
              <th class="py-2"></th>
            </tr>
          </thead>
          <tbody id="sessionsTableBody"></tbody>
        </table>
      </div>
      <p id="sessionsEmpty" class="text-slate-400 text-sm mt-2 hidden">No sessions yet.</p>
    </section>

    <section class="bg-white rounded-xl shadow p-5">
      <h2 class="font-bold text-slate-700 mb-3">Users</h2>
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="text-left text-slate-500 border-b">
              <th class="py-2 pr-3">Username</th>
              <th class="py-2 pr-3">Password set?</th>
              <th class="py-2 pr-3">Created</th>
              <th class="py-2"></th>
            </tr>
          </thead>
          <tbody id="usersTableBody"></tbody>
        </table>
      </div>
      <p id="usersEmpty" class="text-slate-400 text-sm mt-2 hidden">No users yet.</p>
    </section>
  </div>

  <script src="admin.js"></script>
</body>
</html>
