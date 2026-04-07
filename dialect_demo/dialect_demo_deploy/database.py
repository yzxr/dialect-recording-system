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
    
    for _, row in df.iterrows():
        phone = str(row['手机号'])
        existing = User.query.filter_by(phone=phone).first()
        if existing:
            skipped_count += 1
            continue
        
        user = User(
            name=row['姓名'],
            phone=phone,
            password_hash=row.get('密码', '123456'),
            email=row.get('邮箱', ''),
            age=int(row.get('年龄', 30)),
            dialect_tags=row.get('方言能力', ''),
            team_id=team_id,
            role='employee'
        )
        db.session.add(user)
        created_count += 1
    
    db.session.commit()
    return created_count, skipped_count

def import_scripts(script_texts, dialect_type, team_id=1):
    """批量导入话术"""
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
