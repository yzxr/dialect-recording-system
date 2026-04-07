from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """用户表"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100))
    age = db.Column(db.Integer)
    dialect_tags = db.Column(db.String(200))  # JSON 字符串：["闽南语","粤语"]
    team_id = db.Column(db.Integer, default=1)
    role = db.Column(db.String(20), default='employee')  # admin/supervisor/reviewer/employee
    status = db.Column(db.String(20), default='normal')
    created_at = db.Column(db.DateTime, default=datetime.now)
    last_login_at = db.Column(db.DateTime)

class Script(db.Model):
    """话术表"""
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, default=1)
    content = db.Column(db.Text, nullable=False)
    dialect_type = db.Column(db.String(20), nullable=False)  # 闽南语/客家话/粤语
    status = db.Column(db.String(20), default='pending')  # pending/assigned/completed/recycled
    target_date = db.Column(db.Date)
    deadline = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.now)
    recycle_count = db.Column(db.Integer, default=0)

class Assignment(db.Model):
    """分配记录表"""
    id = db.Column(db.Integer, primary_key=True)
    script_id = db.Column(db.Integer, db.ForeignKey('script.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    team_id = db.Column(db.Integer, default=1)
    assigned_at = db.Column(db.DateTime, default=datetime.now)
    deadline = db.Column(db.DateTime)
    recycled_at = db.Column(db.DateTime)
    reassigned_at = db.Column(db.DateTime)
    submitted_at = db.Column(db.DateTime)
    reviewed_at = db.Column(db.DateTime)
    recording_filename = db.Column(db.String(200))
    recording_url = db.Column(db.String(500))
    record_status = db.Column(db.String(20), default='pending')  # pending/submitted/approved/rejected
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    review_result = db.Column(db.String(20))  # approved/rejected
    reject_reason = db.Column(db.String(200))
    recycle_count = db.Column(db.Integer, default=0)
    
    script = db.relationship('Script', backref='assignments')
    employee = db.relationship('User', foreign_keys=[employee_id])
    reviewer = db.relationship('User', foreign_keys=[reviewer_id])
