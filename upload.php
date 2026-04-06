<?php
/**
 * 录音文件上传 API
 * 接收录音文件并保存为 WAV 格式
 */

require_once 'config.php';

header('Content-Type: application/json; charset=utf-8');

// 只接受 POST 请求
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => '请求方法错误']);
    exit;
}

// 检查是否有上传文件
if (!isset($_FILES['audio']) || $_FILES['audio']['error'] !== UPLOAD_ERR_OK) {
    http_response_code(400);
    $error_messages = [
        UPLOAD_ERR_INI_SIZE => '文件超过 php.ini 中 upload_max_filesize 限制',
        UPLOAD_ERR_FORM_SIZE => '文件超过表单 MAX_FILE_SIZE 限制',
        UPLOAD_ERR_PARTIAL => '文件只有部分被上传',
        UPLOAD_ERR_NO_FILE => '没有文件被上传',
        UPLOAD_ERR_NO_TMP_DIR => '找不到临时文件夹',
        UPLOAD_ERR_CANT_WRITE => '文件写入失败',
        UPLOAD_ERR_EXTENSION => 'PHP 扩展阻止了文件上传'
    ];
    $error_code = isset($_FILES['audio']) ? $_FILES['audio']['error'] : UPLOAD_ERR_NO_FILE;
    $message = isset($error_messages[$error_code]) ? $error_messages[$error_code] : '文件上传失败';
    echo json_encode(['success' => false, 'message' => $message]);
    exit;
}

// 获取用户信息
$user_id = $_POST['user_id'] ?? '';
$phone = $_POST['phone'] ?? '';

if (empty($phone)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => '缺少用户信息']);
    exit;
}

// 创建上传目录
$upload_dir = __DIR__ . '/../uploads/';
if (!is_dir($upload_dir)) {
    mkdir($upload_dir, 0755, true);
}

// 按日期创建子目录
$date_dir = $upload_dir . date('Y-m-d') . '/';
if (!is_dir($date_dir)) {
    mkdir($date_dir, 0755, true);
}

// 生成文件名
$custom_name = $_POST['custom_filename'] ?? '';
if (!empty($custom_name)) {
    // 使用自定义文件名
    $ext = pathinfo($_FILES['audio']['name'], PATHINFO_EXTENSION);
    $filename = $custom_name . '.' . $ext;
} else {
    // 自动生成文件名
    $filename = 'recording_' . $phone . '_' . time() . '_' . uniqid() . '.wav';
}
$filepath = $date_dir . $filename;

// 移动上传文件
if (move_uploaded_file($_FILES['audio']['tmp_name'], $filepath)) {
    // 保存到数据库
    try {
        $pdo = getDbConnection();
        
        // 获取用户 ID
        if (empty($user_id)) {
            $stmt = $pdo->prepare("SELECT id FROM users WHERE phone = ?");
            $stmt->execute([$phone]);
            $user = $stmt->fetch();
            $user_id = $user ? $user['id'] : 0;
        }
        
        // 获取存储链接
        $storage_link = $_POST['storage_link'] ?? '';
        
        // 插入录音记录
        $stmt = $pdo->prepare("
            INSERT INTO recordings (user_id, audio_file, storage_link, duration, status, created_at) 
            VALUES (?, ?, ?, 0, 0, NOW())
        ");
        $stmt->execute([$user_id, $filepath, $storage_link]);
        
        $recording_id = $pdo->lastInsertId();
        
        echo json_encode([
            'success' => true,
            'message' => '上传成功',
            'filename' => $filename,
            'filepath' => $date_dir,
            'recording_id' => $recording_id
        ]);
        
    } catch (PDOException $e) {
        // 数据库错误，但文件已保存
        error_log('Database error: ' . $e->getMessage());
        echo json_encode([
            'success' => true,
            'message' => '文件已保存，但数据库记录失败',
            'filename' => $filename,
            'filepath' => $date_dir
        ]);
    }
} else {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => '文件保存失败']);
}
?>
