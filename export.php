<?php
/**
 * 录音文件导出 API
 * 导出指定日期的录音文件为 ZIP 压缩包
 */

require_once 'config.php';

// 只接受 GET 请求
if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => '请求方法错误']);
    exit;
}

// 获取用户信息
$user_id = $_GET['user_id'] ?? '';
$phone = $_GET['phone'] ?? '';
$date = $_GET['date'] ?? date('Y-m-d');

if (empty($phone)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => '缺少用户信息']);
    exit;
}

try {
    $pdo = getDbConnection();
    
    // 获取用户 ID
    if (empty($user_id)) {
        $stmt = $pdo->prepare("SELECT id FROM users WHERE phone = ?");
        $stmt->execute([$phone]);
        $user = $stmt->fetch();
        $user_id = $user ? $user['id'] : 0;
    }
    
    // 获取指定日期的录音记录
    $stmt = $pdo->prepare("
        SELECT id, audio_file, created_at 
        FROM recordings 
        WHERE user_id = ? 
        AND DATE(created_at) = ?
        ORDER BY created_at DESC
    ");
    $stmt->execute([$user_id, $date]);
    $recordings = $stmt->fetchAll();
    
    if (empty($recordings)) {
        http_response_code(404);
        echo json_encode(['success' => false, 'message' => '今天还没有录音记录']);
        exit;
    }
    
    // 创建 ZIP 文件
    $zip = new ZipArchive();
    $zip_filename = 'recordings_' . $phone . '_' . $date . '_' . time() . '.zip';
    $zip_filepath = sys_get_temp_dir() . '/' . $zip_filename;
    
    if ($zip->open($zip_filepath, ZipArchive::CREATE) !== TRUE) {
        http_response_code(500);
        echo json_encode(['success' => false, 'message' => '无法创建压缩包']);
        exit;
    }
    
    // 添加文件到 ZIP
    $file_list = [];
    foreach ($recordings as $recording) {
        if (file_exists($recording['audio_file'])) {
            $filename = basename($recording['audio_file']);
            $zip->addFile($recording['audio_file'], $filename);
            $file_list[] = [
                'filename' => $filename,
                'time' => $recording['created_at']
            ];
        }
    }
    
    $zip->close();
    
    // 检查 ZIP 文件是否创建成功
    if (!file_exists($zip_filepath)) {
        http_response_code(500);
        echo json_encode(['success' => false, 'message' => '压缩包创建失败']);
        exit;
    }
    
    // 返回下载信息
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode([
        'success' => true,
        'message' => '导出成功',
        'count' => count($recordings),
        'zip_filename' => $zip_filename,
        'zip_filepath' => $zip_filepath,
        'files' => $file_list
    ]);
    
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => '数据库错误：' . $e->getMessage()]);
}
?>
