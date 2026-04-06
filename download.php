<?php
/**
 * ZIP 文件下载 API
 */

require_once 'config.php';

// 只接受 GET 请求
if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    http_response_code(405);
    exit;
}

$filename = $_GET['file'] ?? '';
$filepath = $_GET['path'] ?? '';

if (empty($filename) || empty($filepath)) {
    http_response_code(400);
    exit;
}

// 安全检查：确保路径在临时目录
if (strpos($filepath, sys_get_temp_dir()) !== 0) {
    http_response_code(403);
    exit;
}

if (!file_exists($filepath)) {
    http_response_code(404);
    exit;
}

// 设置下载头
header('Content-Type: application/zip');
header('Content-Disposition: attachment; filename="' . $filename . '"');
header('Content-Length: ' . filesize($filepath));
header('Cache-Control: no-cache, must-revalidate');
header('Pragma: no-cache');

// 输出文件
readfile($filepath);

// 删除临时文件
unlink($filepath);
exit;
?>
