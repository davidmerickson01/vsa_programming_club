<?php
require __DIR__ . '/lib.php';

$token = $_GET['token'] ?? '';
$sid   = $_GET['s']     ?? '';

$username = resolve_token((string)$token);
if ($username === null) {
    json_response(401, ['error' => 'not logged in']);
}

$sessionMeta = get_session_meta((string)$sid);
if ($sessionMeta === null) {
    json_response(404, ['error' => 'session not found']);
}

json_response(200, [
    'submissions' => load_submissions(session_dir((string)$sid)),
    'since'       => time(),
    'status'      => $sessionMeta['status'],
]);
