<?php
require __DIR__ . '/lib.php';

require_admin((string)($_GET['token'] ?? ''));

$users = read_json_file(USERS_FILE);
$userList = [];
foreach ($users as $uname => $info) {
    if ($uname === ADMIN_USERNAME) {
        continue;
    }
    $userList[] = [
        'username'    => $uname,
        'hasPassword' => !empty($info['passwordHash']),
        'createdAt'   => $info['createdAt'] ?? null,
    ];
}
usort($userList, fn($a, $b) => strcasecmp($a['username'], $b['username']));

$sessions = read_json_file(SESSIONS_FILE);
$sessionList = [];
foreach ($sessions as $sid => $info) {
    $sessionList[] = [
        'id'        => $sid,
        'status'    => $info['status'] ?? 'active',
        'createdAt' => $info['createdAt'] ?? null,
    ];
}
usort($sessionList, fn($a, $b) => ($b['createdAt'] ?? 0) <=> ($a['createdAt'] ?? 0));

json_response(200, ['users' => $userList, 'sessions' => $sessionList]);
