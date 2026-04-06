<?php
/**
 * 录音文件自动清理脚本
 * 删除 24 小时前的录音文件
 * 
 * 使用方法：
 * 1. 添加到宝塔面板计划任务（每天执行一次）
 * 2. 或通过命令行执行：php clean_old_recordings.php
 */

require_once 'config.php';

// 设置执行时间和内存限制
set_time_limit(300);
ini_set('memory_limit', '512M');

echo "========================================\n";
echo "录音文件自动清理脚本\n";
echo "执行时间：" . date('Y-m-d H:i:s') . "\n";
echo "========================================\n\n";

try {
    $pdo = getDbConnection();
    
    // 计算 24 小时前的时间戳
    $cutoff_time = date('Y-m-d H:i:s', strtotime('-24 hours'));
    
    echo "清理策略：删除 24 小时前的录音文件\n";
    echo "截止时间：" . $cutoff_time . "\n\n";
    
    // 查询需要删除的录音记录
    $stmt = $pdo->prepare("
        SELECT id, audio_file, created_at 
        FROM recordings 
        WHERE created_at < ?
        ORDER BY created_at ASC
    ");
    $stmt->execute([$cutoff_time]);
    $recordings = $stmt->fetchAll();
    
    if (empty($recordings)) {
        echo "✓ 没有需要清理的录音文件\n";
        exit(0);
    }
    
    echo "找到 " . count($recordings) . " 条需要清理的录音记录\n\n";
    
    $deleted_count = 0;
    $failed_count = 0;
    $total_size = 0;
    
    foreach ($recordings as $recording) {
        $file_path = $recording['audio_file'];
        
        // 检查文件是否存在
        if (file_exists($file_path)) {
            // 获取文件大小
            $file_size = filesize($file_path);
            $total_size += $file_size;
            
            // 删除文件
            if (unlink($file_path)) {
                echo "✓ 已删除文件：" . basename($file_path) . " (" . round($file_size / 1024, 2) . " KB)\n";
                $deleted_count++;
                
                // 从数据库删除记录
                $delete_stmt = $pdo->prepare("DELETE FROM recordings WHERE id = ?");
                $delete_stmt->execute([$recording['id']]);
            } else {
                echo "✗ 删除失败：" . basename($file_path) . "\n";
                $failed_count++;
            }
        } else {
            // 文件已不存在，只删除数据库记录
            $delete_stmt = $pdo->prepare("DELETE FROM recordings WHERE id = ?");
            $delete_stmt->execute([$recording['id']]);
            echo "✓ 文件已不存在，已删除数据库记录：ID " . $recording['id'] . "\n";
            $deleted_count++;
        }
    }
    
    echo "\n========================================\n";
    echo "清理完成统计\n";
    echo "========================================\n";
    echo "成功删除：" . $deleted_count . " 个文件\n";
    echo "删除失败：" . $failed_count . " 个文件\n";
    echo "释放空间：" . round($total_size / 1024 / 1024, 2) . " MB\n";
    echo "执行时间：" . date('Y-m-d H:i:s') . "\n";
    echo "========================================\n";
    
} catch (PDOException $e) {
    echo "数据库错误：" . $e->getMessage() . "\n";
    exit(1);
} catch (Exception $e) {
    echo "错误：" . $e->getMessage() . "\n";
    exit(1);
}
?>
