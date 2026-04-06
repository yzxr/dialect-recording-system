-- 录音收集平台数据库表结构
-- 创建时间：2026-04-05

-- 创建数据库
CREATE DATABASE IF NOT EXISTS `luyin_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE `luyin_db`;

-- 用户表
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
    `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '用户 ID',
    `name` VARCHAR(50) NOT NULL COMMENT '姓名',
    `phone` VARCHAR(20) NOT NULL UNIQUE COMMENT '手机号（登录账号）',
    `company` VARCHAR(100) NOT NULL COMMENT '公司',
    `employee_id` VARCHAR(50) NOT NULL COMMENT '工号',
    `email` VARCHAR(100) NOT NULL COMMENT '邮箱',
    `password` VARCHAR(255) NOT NULL COMMENT '密码（加密存储）',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `last_login` TIMESTAMP NULL COMMENT '最后登录时间',
    `status` TINYINT DEFAULT 1 COMMENT '状态：1=正常，0=禁用',
    
    INDEX `idx_phone` (`phone`),
    INDEX `idx_employee_id` (`employee_id`),
    INDEX `idx_company` (`company`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 录音记录表（预留）
DROP TABLE IF EXISTS `recordings`;
CREATE TABLE `recordings` (
    `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '记录 ID',
    `user_id` INT UNSIGNED NOT NULL COMMENT '用户 ID',
    `dialect` VARCHAR(50) COMMENT '方言类型',
    `audio_file` VARCHAR(255) NOT NULL COMMENT '音频文件路径',
    `duration` INT COMMENT '时长（秒）',
    `status` TINYINT DEFAULT 0 COMMENT '状态：0=待审核，1=已审核，2= rejected',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '上传时间',
    
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='录音记录表';
