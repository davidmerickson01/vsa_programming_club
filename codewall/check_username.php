<?php
require __DIR__ . '/lib.php';

$username = normalize_username((string)($_GET['username'] ?? ''));

if (!preg_match(USERNAME_RE, $username)) {
    json_response(200, ['exists' => false, 'hasPassword' => false]);
}

$users = read_json_file(USERS_FILE);
$entry = $users[$username] ?? null;

json_response(200, [
    'exists'      => $entry !== null,
    'hasPassword' => $entry !== null && !empty($entry['passwordHash']),
]);
