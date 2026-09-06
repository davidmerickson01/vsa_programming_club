<?php
// Shared helpers for the collaborative code session endpoints.

const SESSION_ID_RE = '/^[A-Za-z0-9_-]{1,64}$/';
const USERNAME_RE   = '/^[a-z0-9_-]{1,32}$/'; // usernames are always normalized to lowercase
const MAX_CODE_LEN  = 10000; // 10KB per submission; longer code is truncated
const ADMIN_USERNAME = 'admin';

const DATA_DIR       = __DIR__ . '/data';
const USERS_FILE     = DATA_DIR . '/users.json';
const TOKENS_FILE    = DATA_DIR . '/tokens.json';
const SESSIONS_FILE  = DATA_DIR . '/sessions.json';
const USER_WHITELIST_FILE = __DIR__ . '/user_whitelist.txt';

function session_dir(string $sessionId): string {
    return __DIR__ . '/sessions/' . $sessionId;
}

function normalize_username(string $username): string {
    return strtolower(trim($username));
}

/** Case-insensitive check against user_whitelist.txt (one username per line). */
function is_username_whitelisted(string $username): bool {
    if (!is_file(USER_WHITELIST_FILE)) {
        return false;
    }
    $lines = file(USER_WHITELIST_FILE, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    foreach ($lines as $line) {
        if (normalize_username($line) === $username) {
            return true;
        }
    }
    return false;
}

// ── Small JSON key-value stores (users, tokens, sessions) ─────────────────

function read_json_file(string $path): array {
    if (!is_file($path)) {
        return [];
    }
    $raw = file_get_contents($path);
    $data = $raw !== false ? json_decode($raw, true) : null;
    return is_array($data) ? $data : [];
}

/** Read-modify-write a JSON file under an exclusive lock to avoid races. */
function update_json_file(string $path, callable $mutator): array {
    $dir = dirname($path);
    if (!is_dir($dir)) {
        mkdir($dir, 0777, true);
    }
    $fp = fopen($path, 'c+');
    flock($fp, LOCK_EX);

    $size = filesize($path);
    $raw = $size > 0 ? fread($fp, $size) : '';
    $data = $raw !== '' ? json_decode($raw, true) : [];
    if (!is_array($data)) {
        $data = [];
    }

    $data = $mutator($data);

    ftruncate($fp, 0);
    rewind($fp);
    fwrite($fp, json_encode($data, JSON_PRETTY_PRINT));
    fflush($fp);
    flock($fp, LOCK_UN);
    fclose($fp);

    return $data;
}

// ── Accounts (username/password) ───────────────────────────────────────────

/**
 * Log in or sign up a user. Returns ['username'=>..., 'token'=>..., 'isAdmin'=>bool]
 * on success, or ['error'=>string] on failure.
 */
function authenticate(string $username, string $password): array {
    $username = normalize_username($username);
    if (!preg_match(USERNAME_RE, $username)) {
        return ['error' => 'Username must be 1-32 letters, numbers, underscore, or hyphen.'];
    }
    if ($password === '' || strlen($password) > 200) {
        return ['error' => 'Password is required.'];
    }

    $users = read_json_file(USERS_FILE);
    $existing = $users[$username] ?? null;

    if ($existing === null) {
        if (!is_username_whitelisted($username)) {
            return ['error' => 'That username is not on the club whitelist. Ask your admin to add you.'];
        }
        // Brand-new account: this password becomes their password.
        update_json_file(USERS_FILE, function ($data) use ($username, $password) {
            $data[$username] = [
                'passwordHash' => password_hash($password, PASSWORD_DEFAULT),
                'createdAt'    => time(),
            ];
            return $data;
        });
    } elseif (empty($existing['passwordHash'])) {
        // Admin cleared this account's password: accept a fresh one, no verification.
        update_json_file(USERS_FILE, function ($data) use ($username, $password) {
            $data[$username]['passwordHash'] = password_hash($password, PASSWORD_DEFAULT);
            return $data;
        });
    } else {
        if (!password_verify($password, $existing['passwordHash'])) {
            return ['error' => 'Incorrect password.'];
        }
    }

    $token = issue_token($username);
    return ['username' => $username, 'token' => $token, 'isAdmin' => $username === ADMIN_USERNAME];
}

// ── Tokens ──────────────────────────────────────────────────────────────────
// Auth is token-based (not cookies): the token travels in the request body /
// query string and is looked up server-side. This keeps everything working
// regardless of whether the serving webserver forwards Cookie headers.

function issue_token(string $username): string {
    $token = bin2hex(random_bytes(24));
    update_json_file(TOKENS_FILE, function ($data) use ($token, $username) {
        $data[$token] = ['username' => $username, 'createdAt' => time()];
        return $data;
    });
    return $token;
}

/** Resolve a token to a still-valid username, or null. */
function resolve_token(string $token): ?string {
    if ($token === '') {
        return null;
    }
    $tokens = read_json_file(TOKENS_FILE);
    $username = $tokens[$token]['username'] ?? null;
    if ($username === null) {
        return null;
    }
    $users = read_json_file(USERS_FILE);
    if (!isset($users[$username])) {
        return null; // account was deleted since the token was issued
    }
    return $username;
}

function purge_tokens_for_user(string $username): void {
    update_json_file(TOKENS_FILE, function ($data) use ($username) {
        foreach ($data as $tok => $info) {
            if (($info['username'] ?? null) === $username) {
                unset($data[$tok]);
            }
        }
        return $data;
    });
}

// ── Session registry ────────────────────────────────────────────────────────
// Only sessions present here (created via the admin panel) are valid.

/** @return array{status:string, createdAt:int}|null */
function get_session_meta(string $sessionId): ?array {
    if (!preg_match(SESSION_ID_RE, $sessionId)) {
        return null;
    }
    $sessions = read_json_file(SESSIONS_FILE);
    return $sessions[$sessionId] ?? null;
}

// ── Code submissions ─────────────────────────────────────────────────────────

/** @return array<int, array{username:string, code:string, updatedAt:int}> */
function load_submissions(string $dir): array {
    $results = [];
    if (is_dir($dir)) {
        foreach (glob($dir . '/*.py') as $file) {
            $username = basename($file, '.py');
            $code = file_get_contents($file);
            if ($code === false) {
                continue;
            }
            $results[] = [
                'username'  => $username,
                'code'      => $code,
                'updatedAt' => filemtime($file),
            ];
        }
    }
    usort($results, fn($a, $b) => strcasecmp($a['username'], $b['username']));
    return $results;
}

// ── HTTP helpers ──────────────────────────────────────────────────────────

function json_response(int $status, array $data): void {
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    echo json_encode($data);
    exit;
}

function read_json_body(): array {
    $raw = file_get_contents('php://input');
    $data = $raw !== false ? json_decode($raw, true) : null;
    return is_array($data) ? $data : [];
}

/** For admin-only endpoints: resolves the token and enforces admin, or exits with an error. */
function require_admin(string $token): string {
    $username = resolve_token($token);
    if ($username !== ADMIN_USERNAME) {
        json_response(403, ['error' => 'admin access required']);
    }
    return $username;
}
