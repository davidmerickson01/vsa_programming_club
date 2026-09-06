# Collaborative Code Sharing

A shared coding session where everyone can paste code and see each other's
latest submission update live.

## Run it

This is plain PHP with no dependencies. Point any PHP-capable local server
(e.g. the club's `webserver.py`) at the repo root (so both the main club
site and this `codewall/` folder are served together), then open
`codewall/admin.php` or `codewall/index.php?s=...`.

- **Admin**: go to `admin.php`, sign in (the first password you enter
  becomes the admin password), and click "+ New session" to get a
  shareable link like `index.php?s=a1b2c3d4`.
- **Everyone else**: open the session link an admin gave you, then pick a
  username and password (the first time you use a username, that password
  becomes its password).

Only sessions created from the admin panel are valid — there's no way to
land on a fresh session by guessing a URL.

## How it works

- Each session is identified by the `s` parameter in its URL, and must
  exist in the admin-managed session registry.
- Usernames are always lower-cased. The first time a username is used, the
  given password is stored (hashed) as its password; after that, the
  correct password is required to use that username again. There's no
  self-service password reset or account deletion — only the admin can do
  that.
- Login issues a bearer token (stored in the browser's localStorage) that's
  sent with every request instead of a cookie, so this doesn't depend on
  the serving webserver forwarding `Cookie` headers.
- The textbox at the top is your own code; "Submit" POSTs it to
  `submit.php`, which saves it to `sessions/<session-id>/<username>.py`.
  On page load, your own most recent submission (if any) pre-fills the box.
- Everyone's latest submission — including your own — shows up below in
  read-only, syntax-highlighted panels (yours is labeled "(you)"). When
  anyone submits, those panels update for every connected client within a
  couple seconds — your own textbox is never touched.
- Live updates use short-interval polling (`app.js` re-fetches
  `submissions.php` every ~1.2s). Each request returns immediately with no
  server-side blocking, so this stays responsive with multiple connected
  clients even behind a single-threaded dev server.

## Admin interface (`admin.php`)

Sign in as `admin` (same login mechanism as everyone else, just a reserved
username). From the dashboard:

- **Sessions**: create new sessions, and mark any session `active`
  (read/write) or `archived` (read-only — submissions are rejected).
- **Users**: see every account, **clear a password** (the user can then
  set a new one on their next login with no verification), or **delete an
  account** entirely (removes the account and deletes all of that user's
  submitted code across every session).

## Notes

- `sessions/` (submitted code) and `data/` (accounts, tokens, session
  registry — all with password hashes, so keep this private) are both
  gitignored runtime data.
- Auth tokens don't expire; deleting a user's account is what invalidates
  their tokens.
