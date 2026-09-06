<?php
require __DIR__ . '/lib.php';

$data = read_json_body();
require_admin((string)($data['token'] ?? ''));

$name = trim((string)($data['name'] ?? ''));
if ($name === '' || !preg_match(SESSION_ID_RE, $name)) {
    json_response(400, [
        'error' => 'Session name must be 1-64 characters: letters, numbers, underscore, or hyphen.',
    ]);
}

$created = true;
update_json_file(SESSIONS_FILE, function ($sessions) use ($name, &$created) {
    if (isset($sessions[$name])) {
        $created = false;
        return $sessions;
    }
    $sessions[$name] = ['status' => 'active', 'createdAt' => time()];
    return $sessions;
});

if (!$created) {
    json_response(409, ['error' => 'A session with that name already exists.']);
}

json_response(200, ['ok' => true, 'id' => $name]);
