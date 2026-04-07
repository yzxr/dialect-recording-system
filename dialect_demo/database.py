from models import db, User, Script, Assignment
from datetime import datetime, timedelta
import pandas as pd
import os

def init_db(app):
    """初始化数据库"""
    with app.app_context():
        db.create_all()
        # 创建默认管理员账号（密码：123456）
        admin = User.query.filter_by(phone='13800000000').first()
        if not admin:
            # 简单哈希，仅用于 Demo
            admin = User(
                name='系统管理员',
                phone='13800000000',
                password_hash='123456',  # Demo 版直接用明文
                email='admin@example.com',
                age=35,
                role='admin',
                team_id=1
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ 默认管理员账号已创建：13800000000 / 123456")

def import_users_from_excel(file_path, team_id=1):
    """从 Excel 批量导入用户"""
    df = pd.read_excel(file_path)
    created_count = 0
    skipped_count = 0
    error_count = 0
    
    for _, row in df.iterrows():
        # 必填字段验证
        phone = str(row.get('手机号', '')).strip()
        name = str(row.get('姓名', '')).strip()
        password = str(row.get('密码', '')).strip()
        
        # 检查必填字段
        if not phone or not name or not password:
            error_count += 1
            continue
        
        # 检查手机号是否重复
        existing = User.query.filter_by(phone=phone).first()
        if existing:
            skipped_count += 1
            continue
        
        # 可选字段
        age = row.get('年龄')
        if pd.isna(age):
            age = 30  # 默认年龄
        else:
            age = int(age)
        
        dialect_tags = row.get('方言能力', '')
        if pd.isna(dialect_tags):
            dialect_tags = ''
        
        remark = row.get('备注', '')
        if pd.isna(remark):
            remark = ''
        
        user = User(
            name=name,
            phone=phone,
            password_hash=password,
            email='',  # 新版不强制要求邮箱
            age=age,
            dialect_tags=dialect_tags,
            team_id=team_id,
            role='employee'
        )
        db.session.add(user)
        created_count += 1
    
    db.session.commit()
    return created_count, skipped_count, error_count

def import_scripts(script_texts, dialect_type, team_id=1):
    """批量导入话术（文本粘贴方式）"""
    created_count = 0
    for text in script_texts:
        if not text.strip():
            continue
        script = Script(
            team_id=team_id,
            content=text.strip(),
            dialect_type=dialect_type,
            target_date=datetime.now().date(),
            deadline=datetime.now().replace(hour=23, minute=59, second=59)
        )
        db.session.add(script)
        created_count += 1
    db.session.commit()
    return created_count

def import_scripts_from_excel(file_path, team_id=1):
    """从 Excel 批量导入话术（三列格式：序号 | 方言文本 | 普通话文本）"""
    df = pd.read_excel(file_path)
    created_count = 0
    duplicate_count = 0
    error_count = 0
    
    # 获取今天的话术用于去重
    today = datetime.now().date()
    today_scripts = Script.query.filter(
        Script.team_id == team_id,
        db.func.date(Script.created_at) == today
    ).all()
    today_contents = set(s.content for s in today_scripts)
    
    for _, row in df.iterrows():
        # 必填字段验证
        script_id = str(row.get('序号', '')).strip()
        dialect_text = str(row.get('方言文本', '')).strip()
        mandarin_text = str(row.get('普通话文本', '')).strip()
        
        # 检查必填字段
        if not script_id or not dialect_text or not mandarin_text:
            error_count += 1
            continue
        
        # 组合话术内容（方言 + 普通话对照）
        content = f"{dialect_text}\n（普通话：{mandarin_text}）"
        
        # 去重检查
        if content in today_contents:
            duplicate_count += 1
            continue
        
        # 可选字段
        difficulty = row.get('难度等级')
        if pd.isna(difficulty):
            difficulty = 1
        else:
            difficulty = int(difficulty)
        
        remark = row.get('备注', '')
        if pd.isna(remark):
            remark = ''
        
        script = Script(
            team_id=team_id,
            content=content,
            dialect_type='闽南语',  # 默认值
            target_date=datetime.now().date(),
            deadline=datetime.now().replace(hour=23, minute=59, second=59),
            difficulty_level=difficulty
        )
        db.session.add(script)
        created_count += 1
        today_contents.add(content)  # 添加到去重集合
    
    db.session.commit()
    return created_count, duplicate_count, error_count

def delete_old_scripts(days=3):
    """删除超过指定天数的旧话术"""
    from datetime import timedelta
    cutoff_date = datetime.now() - timedelta(days=days)
    
    old_scripts = Script.query.filter(Script.created_at < cutoff_date).all()
    deleted_count = len(old_scripts)
    
    for script in old_scripts:
        db.session.delete(script)
    
    db.session.commit()
    return deleted_count

def auto_assign_scripts():
    """自动分配话术给员工"""
    pending_scripts = Script.query.filter_by(status='pending').all()
    employees = User.query.filter_by(role='employee', status='normal').all()
    
    if not employees:
        return 0
    
    assigned_count = 0
    for script in pending_scripts:
        # 简单轮询分配
        employee = employees[assigned_count % len(employees)]
        assignment = Assignment(
            script_id=script.id,
            employee_id=employee.id,
            team_id=script.team_id,
            deadline=script.deadline,
            record_status='pending'
        )
        db.session.add(assignment)
        script.status = 'assigned'
        assigned_count += 1
    
    db.session.commit()
    return assigned_count

def validate_filename(filename, employee_name, script_id):
    """校验文件名格式"""
    import re
    pattern = r'^(闽南语 | 客家话 | 粤语)_(.+)_(S\d+)_(\d{12})\.wav$'
    match = re.match(pattern, filename)
    
    if not match:
        return False, "格式错误（应为：方言类型_姓名_话术编号_时间戳.wav）"
    
    dialect, name, script_no, timestamp = match.groups()
    
    if name != employee_name:
        return False, f"员工姓名不匹配（期望：{employee_name}，实际：{name}）"
    
    expected_script_id = f"S{script_id}"
    if script_no != expected_script_id:
        return False, f"话术编号不匹配（期望：{expected_script_id}，实际：{script_no}）"
    
    return True, "校验通过"

def get_dashboard_stats():
    """获取看板统计数据"""
    total_scripts = Script.query.count()
    pending_scripts = Script.query.filter_by(status='pending').count()
    assigned_scripts = Script.query.filter_by(status='assigned').count()
    completed_scripts = Script.query.filter_by(status='completed').count()
    
    total_assignments = Assignment.query.count()
    pending_assignments = Assignment.query.filter_by(record_status='pending').count()
    submitted_assignments = Assignment.query.filter_by(record_status='submitted').count()
    approved_assignments = Assignment.query.filter_by(record_status='approved').count()
    
    return {
        'total_scripts': total_scripts,
        'pending_scripts': pending_scripts,
        'assigned_scripts': assigned_scripts,
        'completed_scripts': completed_scripts,
        'total_assignments': total_assignments,
        'pending_assignments': pending_assignments,
        'submitted_assignments': submitted_assignments,
        'approved_assignments': approved_assignments
    }
