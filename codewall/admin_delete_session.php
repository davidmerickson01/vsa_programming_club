<?php
require __DIR__ . '/lib.php';

$data = read_json_body();
require_admin((string)($data['token'] ?? ''));

$sid = (string)($data['session'] ?? '');
if (!preg_match(SESSION_ID_RE, $sid)) {
    json_response(400, ['error' => 'invalid session id']);
}

$existed = false;
update_json_file(SESSIONS_FILE, function ($sessions) use ($sid, &$existed) {
    if (isset($sessions[$sid])) {
        $existed = true;
        unset($sessions[$sid]);
    }
    return $sessions;
});

if (!$existed) {
    json_response(404, ['error' => 'session not found']);
}

$dir = session_dir($sid);
if (is_dir($dir)) {
    foreach (glob($dir . '/*.txt') as $file) {
        unlink($file);
    }
    rmdir($dir);
}

json_response(200, ['ok' => true]);
