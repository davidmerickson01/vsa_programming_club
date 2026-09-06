<?php
require __DIR__ . '/lib.php';

$data = read_json_body();
require_admin((string)($data['token'] ?? ''));

$sid = (string)($data['session'] ?? '');
$status = (string)($data['status'] ?? '');

if (!preg_match(SESSION_ID_RE, $sid) || !in_array($status, ['active', 'archived'], true)) {
    json_response(400, ['error' => 'invalid request']);
}

$found = false;
update_json_file(SESSIONS_FILE, function ($sessions) use ($sid, $status, &$found) {
    if (isset($sessions[$sid])) {
        $found = true;
        $sessions[$sid]['status'] = $status;
    }
    return $sessions;
});

if (!$found) {
    json_response(404, ['error' => 'session not found']);
}

json_response(200, ['ok' => true]);
