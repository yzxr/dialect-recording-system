<?php
/**
 * 用户登录 API
 * 请求方式：POST
 * 请求参数：phone, password
 */

require_once 'config.php';

// 只接受 POST 请求
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => '请求方法错误']);
    exit;
}

// 获取 POST 数据
$input = file_get_contents('php://input');
$data = json_decode($input, true);

if (!$data) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => '无效的请求数据']);
    exit;
}

// 提取字段
$phone = trim($data['phone'] ?? '');
$password = $data['password'] ?? '';

// 验证必填字段
if (empty($phone) || empty($password)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => '手机号和密码不能为空']);
    exit;
}

try {
    $pdo = getDbConnection();
    
    // 查询用户
    $stmt = $pdo->prepare("SELECT id, name, phone, company, employee_id, email, password, status, last_login FROM users WHERE phone = ?");
    $stmt->execute([$phone]);
    $user = $stmt->fetch();
    
    if (!$user) {
        http_response_code(401);
        echo json_encode(['success' => false, 'message' => '用户不存在']);
        exit;
    }
    
    // 验证密码
    if (!password_verify($password, $user['password'])) {
        http_response_code(401);
        echo json_encode(['success' => false, 'message' => '密码错误']);
        exit;
    }
    
    // 检查账号状态
    if ($user['status'] == 0) {
        http_response_code(403);
        echo json_encode(['success' => false, 'message' => '账号已被禁用']);
        exit;
    }
    
    // 更新最后登录时间
    $update_stmt = $pdo->prepare("UPDATE users SET last_login = NOW() WHERE id = ?");
    $update_stmt->execute([$user['id']]);
    
    // 返回用户信息（不返回密码）
    echo json_encode([
        'success' => true,
        'message' => '登录成功',
        'data' => [
            'user_id' => $user['id'],
            'name' => $user['name'],
            'phone' => $user['phone'],
            'company' => $user['company'],
            'employee_id' => $user['employee_id'],
            'email' => $user['email']
        ]
    ]);
    
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => '登录失败：' . $e->getMessage()]);
}
?>
