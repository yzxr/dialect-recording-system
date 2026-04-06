<?php
/**
 * 用户注册 API
 * 请求方式：POST
 * 请求参数：name, phone, company, employee_id, email, password
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
$name = trim($data['name'] ?? '');
$phone = trim($data['phone'] ?? '');
$company = trim($data['company'] ?? '');
$employee_id = trim($data['employee_id'] ?? '');
$email = trim($data['email'] ?? '');
$password = $data['password'] ?? '';

// 验证必填字段
$errors = [];
if (empty($name)) $errors[] = '姓名不能为空';
if (empty($phone)) $errors[] = '手机号不能为空';
if (empty($company)) $errors[] = '公司不能为空';
if (empty($employee_id)) $errors[] = '工号不能为空';
if (empty($email)) $errors[] = '邮箱不能为空';
if (empty($password)) $errors[] = '密码不能为空';

if (!empty($errors)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => implode('，', $errors)]);
    exit;
}

// 验证手机号格式
if (!preg_match('/^1[3-9]\d{9}$/', $phone)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => '手机号格式不正确']);
    exit;
}

// 验证邮箱格式
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => '邮箱格式不正确']);
    exit;
}

// 验证密码长度
if (strlen($password) < 6) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => '密码至少 6 位']);
    exit;
}

try {
    $pdo = getDbConnection();
    
    // 检查手机号是否已注册
    $stmt = $pdo->prepare("SELECT id FROM users WHERE phone = ?");
    $stmt->execute([$phone]);
    if ($stmt->fetch()) {
        http_response_code(409);
        echo json_encode(['success' => false, 'message' => '该手机号已注册']);
        exit;
    }
    
    // 加密密码
    $hashed_password = password_hash($password, PASSWORD_DEFAULT);
    
    // 插入用户
    $stmt = $pdo->prepare("
        INSERT INTO users (name, phone, company, employee_id, email, password) 
        VALUES (?, ?, ?, ?, ?, ?)
    ");
    $stmt->execute([$name, $phone, $company, $employee_id, $email, $hashed_password]);
    
    $user_id = $pdo->lastInsertId();
    
    echo json_encode([
        'success' => true,
        'message' => '注册成功',
        'data' => [
            'user_id' => $user_id,
            'phone' => $phone,
            'name' => $name
        ]
    ]);
    
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => '注册失败：' . $e->getMessage()]);
}
?>
