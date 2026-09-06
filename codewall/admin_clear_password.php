<?php
require __DIR__ . '/lib.php';

$data = read_json_body();
require_admin((string)($data['token'] ?? ''));

$target = normalize_username((string)($data['username'] ?? ''));
if ($target === ADMIN_USERNAME || !preg_match(USERNAME_RE, $target)) {
    json_response(400, ['error' => 'invalid username']);
}

$found = false;
update_json_file(USERS_FILE, function ($users) use ($target, &$found) {
    if (isset($users[$target])) {
        $found = true;
        $users[$target]['passwordHash'] = null;
    }
    return $users;
});

if (!$found) {
    json_response(404, ['error' => 'user not found']);
}

// Existing tokens still work; the account simply has no password until they set one.
json_response(200, ['ok' => true]);
