#!/usr/bin/env python3
"""
生产环境配置
关闭 debug 模式，启用日志记录
"""

from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import db, User, Script, Assignment
from database import init_db, import_users_from_excel, import_scripts, auto_assign_scripts, validate_filename, get_dashboard_stats
from datetime import datetime
import os
import zipfile
import io
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'production-secret-key-2026-change-me'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dialect_demo.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB

# 生产环境日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ==================== 认证路由 ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form.get('phone')
        password = request.form.get('password')
        user = User.query.filter_by(phone=phone).first()
        
        if user and (user.password_hash == password or check_password_hash(user.password_hash, password)):
            login_user(user)
            user.last_login_at = datetime.now()
            db.session.commit()
            app.logger.info(f'用户登录成功：{phone}')
            return redirect(url_for('dashboard'))
        else:
            app.logger.warning(f'用户登录失败：{phone}')
            flash('手机号或密码错误', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ==================== 主看板 ====================

@app.route('/')
@login_required
def dashboard():
    stats = get_dashboard_stats()
    return render_template('dashboard.html', stats=stats)

# ==================== 员工管理 ====================

@app.route('/users/import', methods=['GET', 'POST'])
@login_required
def import_users():
    if current_user.role not in ['admin', 'supervisor']:
        flash('权限不足', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('未选择文件', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('未选择文件', 'error')
            return redirect(request.url)
        
        temp_path = f'/tmp/{file.filename}'
        file.save(temp_path)
        
        created, skipped = import_users_from_excel(temp_path)
        os.remove(temp_path)
        
        app.logger.info(f'导入员工：成功{created}人，跳过{skipped}人')
        flash(f'✅ 成功导入 {created} 人，跳过 {skipped} 人（重复）', 'success')
        return redirect(url_for('user_list'))
    
    return render_template('import_users.html')

@app.route('/users')
@login_required
def user_list():
    users = User.query.filter_by(role='employee').all()
    return render_template('user_list.html', users=users)

# ==================== 话术管理 ====================

@app.route('/scripts/import', methods=['GET', 'POST'])
@login_required
def import_scripts_view():
    if current_user.role not in ['admin', 'supervisor']:
        flash('权限不足', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        script_text = request.form.get('script_text')
        dialect_type = request.form.get('dialect_type')
        
        if not script_text or not dialect_type:
            flash('请填写话术内容和方言类型', 'error')
            return redirect(request.url)
        
        scripts = [s.strip() for s in script_text.split('\n') if s.strip()]
        count = import_scripts(scripts, dialect_type)
        assigned = auto_assign_scripts()
        
        app.logger.info(f'导入话术：{count}条，分配：{assigned}条')
        flash(f'✅ 导入 {count} 条话术，已自动分配 {assigned} 条任务', 'success')
        return redirect(url_for('script_list'))
    
    return render_template('import_scripts.html')

@app.route('/scripts')
@login_required
def script_list():
    scripts = Script.query.order_by(Script.created_at.desc()).all()
    return render_template('script_list.html', scripts=scripts)

# ==================== 任务管理 ====================

@app.route('/assignments')
@login_required
def assignment_list():
    if current_user.role == 'employee':
        assignments = Assignment.query.filter_by(employee_id=current_user.id).all()
    else:
        assignments = Assignment.query.all()
    return render_template('assignment_list.html', assignments=assignments)

@app.route('/assignments/<int:id>/upload', methods=['GET', 'POST'])
@login_required
def upload_recording(id):
    assignment = Assignment.query.get_or_404(id)
    
    if assignment.employee_id != current_user.id:
        flash('无权操作此任务', 'error')
        return redirect(url_for('assignment_list'))
    
    if request.method == 'POST':
        if 'recording' not in request.files:
            flash('未选择文件', 'error')
            return redirect(request.url)
        
        file = request.files['recording']
        if file.filename == '':
            flash('未选择文件', 'error')
            return redirect(request.url)
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(filepath)
        
        assignment.recording_filename = filename
        assignment.recording_url = f'/static/uploads/{filename}'
        assignment.record_status = 'submitted'
        assignment.submitted_at = datetime.now()
        db.session.commit()
        
        app.logger.info(f'录音上传：{filename}')
        flash('✅ 录音上传成功', 'success')
        return redirect(url_for('assignment_list'))
    
    return render_template('upload_recording.html', assignment=assignment)

# ==================== 审核管理 ====================

@app.route('/review')
@login_required
def review_list():
    if current_user.role not in ['admin', 'supervisor', 'reviewer']:
        flash('权限不足', 'error')
        return redirect(url_for('dashboard'))
    
    assignments = Assignment.query.filter_by(record_status='submitted').all()
    return render_template('review_list.html', assignments=assignments)

@app.route('/review/<int:id>', methods=['GET', 'POST'])
@login_required
def review_assignment(id):
    if current_user.role not in ['admin', 'supervisor', 'reviewer']:
        flash('权限不足', 'error')
        return redirect(url_for('dashboard'))
    
    assignment = Assignment.query.get_or_404(id)
    
    if request.method == 'POST':
        result = request.form.get('result')
        reject_reason = request.form.get('reject_reason', '')
        
        assignment.review_result = result
        assignment.reviewed_at = datetime.now()
        assignment.reviewer_id = current_user.id
        
        if result == 'approved':
            assignment.record_status = 'approved'
            assignment.script.status = 'completed'
        else:
            assignment.record_status = 'rejected'
            assignment.reject_reason = reject_reason
            assignment.script.status = 'assigned'
        
        db.session.commit()
        app.logger.info(f'审核完成：{assignment.recording_filename} - {result}')
        flash('✅ 审核完成', 'success')
        return redirect(url_for('review_list'))
    
    is_valid, message = validate_filename(
        assignment.recording_filename,
        assignment.employee.name,
        assignment.script.id
    )
    
    return render_template('review_detail.html', assignment=assignment, is_valid=is_valid, message=message)

# ==================== 下载管理 ====================

@app.route('/download')
@login_required
def download_list():
    if current_user.role not in ['admin', 'supervisor']:
        flash('权限不足', 'error')
        return redirect(url_for('dashboard'))
    
    assignments = Assignment.query.filter_by(record_status='approved').all()
    return render_template('download_list.html', assignments=assignments)

@app.route('/download/batch')
@login_required
def download_batch():
    if current_user.role not in ['admin', 'supervisor']:
        flash('权限不足', 'error')
        return redirect(url_for('dashboard'))
    
    assignments = Assignment.query.filter_by(record_status='approved').all()
    
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for assignment in assignments:
            if assignment.recording_url:
                filepath = os.path.join('static/uploads', os.path.basename(assignment.recording_url))
                if os.path.exists(filepath):
                    zf.write(filepath, assignment.recording_filename)
    
    memory_file.seek(0)
    app.logger.info(f'批量下载：{len(assignments)}个录音文件')
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f'recordings_{datetime.now().strftime("%Y%m%d")}.zip'
    )

@app.route('/delete-downloaded', methods=['POST'])
@login_required
def delete_downloaded():
    if current_user.role not in ['admin', 'supervisor']:
        flash('权限不足', 'error')
        return redirect(url_for('dashboard'))
    
    assignments = Assignment.query.filter_by(record_status='approved').all()
    deleted_count = 0
    
    for assignment in assignments:
        if assignment.recording_url:
            filepath = os.path.join('static/uploads', os.path.basename(assignment.recording_url))
            if os.path.exists(filepath):
                os.remove(filepath)
                deleted_count += 1
            assignment.recording_url = None
    
    db.session.commit()
    app.logger.info(f'删除录音文件：{deleted_count}个')
    flash(f'✅ 已删除 {deleted_count} 个录音文件', 'success')
    return redirect(url_for('download_list'))

if __name__ == '__main__':
    # 创建日志目录
    os.makedirs('logs', exist_ok=True)
    os.makedirs('static/uploads', exist_ok=True)
    os.makedirs('instance', exist_ok=True)
    
    init_db(app)
    # 生产环境：debug=False
    app.run(debug=False, host='0.0.0.0', port=5001)
