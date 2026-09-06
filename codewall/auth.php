<?php
require __DIR__ . '/lib.php';

$data = read_json_body();
$username = (string)($data['username'] ?? '');
$password = (string)($data['password'] ?? '');

$result = authenticate($username, $password);
if (isset($result['error'])) {
    json_response(401, ['error' => $result['error']]);
}

json_response(200, [
    'ok'       => true,
    'token'    => $result['token'],
    'username' => $result['username'],
    'isAdmin'  => $result['isAdmin'],
]);
