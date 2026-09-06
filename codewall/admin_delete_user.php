<?php
require __DIR__ . '/lib.php';

$data = read_json_body();
require_admin((string)($data['token'] ?? ''));

$target = normalize_username((string)($data['username'] ?? ''));
if ($target === ADMIN_USERNAME || !preg_match(USERNAME_RE, $target)) {
    json_response(400, ['error' => 'invalid username']);
}

$existed = false;
update_json_file(USERS_FILE, function ($users) use ($target, &$existed) {
    if (isset($users[$target])) {
        $existed = true;
        unset($users[$target]);
    }
    return $users;
});

if (!$existed) {
    json_response(404, ['error' => 'user not found']);
}

purge_tokens_for_user($target);

// Remove all of their submitted code across every session.
foreach (glob(__DIR__ . '/sessions/*', GLOB_ONLYDIR) as $dir) {
    $file = $dir . '/' . $target . '.txt';
    if (is_file($file)) {
        unlink($file);
    }
}

json_response(200, ['ok' => true]);
