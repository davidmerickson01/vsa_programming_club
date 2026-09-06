<?php
require __DIR__ . '/lib.php';

$data = read_json_body();

$token = (string)($data['token']   ?? '');
$sid   = (string)($data['session'] ?? '');
$code  = $data['code'] ?? '';

$username = resolve_token($token);
if ($username === null) {
    json_response(401, ['error' => 'not logged in']);
}

$sessionMeta = get_session_meta($sid);
if ($sessionMeta === null) {
    json_response(404, ['error' => 'session not found']);
}
if ($sessionMeta['status'] !== 'active') {
    json_response(403, ['error' => 'this session is archived (read-only)']);
}
if (!is_string($code)) {
    json_response(400, ['error' => 'code missing']);
}
if (strlen($code) > MAX_CODE_LEN) {
    $code = substr($code, 0, MAX_CODE_LEN);
}

$dir = session_dir($sid);
if (!is_dir($dir)) {
    mkdir($dir, 0777, true);
}
file_put_contents($dir . '/' . $username . '.txt', $code, LOCK_EX);

json_response(200, ['ok' => true]);
