#!/usr/bin/env python3
"""
方言采集系统 - 快速测试脚本
用于演示完整流程
"""

import requests
from requests.sessions import Session

BASE_URL = 'http://localhost:5001'

def test_login():
    """测试登录"""
    print("\n=== 1️⃣ 测试登录 ===")
    session = Session()
    
    # 管理员登录
    resp = session.post(f'{BASE_URL}/login', data={
        'phone': '13800000000',
        'password': '123456'
    }, allow_redirects=False)
    
    if resp.status_code == 302:
        print("✅ 管理员登录成功")
        return session
    else:
        print("❌ 登录失败")
        return None

def test_dashboard(session):
    """测试看板"""
    print("\n=== 2️⃣ 测试数据看板 ===")
    resp = session.get(f'{BASE_URL}/')
    if resp.status_code == 200:
        print("✅ 看板页面加载成功")
        # 提取统计数据
        if '总话术数' in resp.text:
            print("📊 看板包含统计数据")
    else:
        print("❌ 看板加载失败")

def test_import_scripts(session):
    """测试导入话术"""
    print("\n=== 3️⃣ 测试导入话术 ===")
    test_scripts = """你好，欢迎来咨询
我们这个效果很好的
很多客户都反馈不错
今天有优惠活动
您想了解哪方面呢"""
    
    resp = session.post(f'{BASE_URL}/scripts/import', data={
        'dialect_type': '闽南语',
        'script_text': test_scripts
    }, allow_redirects=False)
    
    if resp.status_code == 302:
        print("✅ 话术导入成功（5 条闽南语话术）")
    else:
        print("❌ 话术导入失败")

def test_user_list(session):
    """测试用户列表"""
    print("\n=== 4️⃣ 测试员工列表 ===")
    resp = session.get(f'{BASE_URL}/users')
    if resp.status_code == 200:
        print("✅ 员工列表页面加载成功")
    else:
        print("❌ 员工列表加载失败")

def test_assignments(session):
    """测试任务分配"""
    print("\n=== 5️⃣ 测试任务列表 ===")
    resp = session.get(f'{BASE_URL}/assignments')
    if resp.status_code == 200:
        print("✅ 任务列表页面加载成功")
        if 'pending' in resp.text.lower() or '待录制' in resp.text:
            print("📋 已有待录制任务")
    else:
        print("❌ 任务列表加载失败")

def main():
    print("🎙️ 方言采集系统 - 自动化测试")
    print("=" * 50)
    
    session = test_login()
    if not session:
        print("\n❌ 测试终止：登录失败")
        return
    
    test_dashboard(session)
    test_import_scripts(session)
    test_user_list(session)
    test_assignments(session)
    
    print("\n" + "=" * 50)
    print("✅ 测试完成！")
    print("\n📱 访问地址：http://localhost:5000")
    print("👤 管理员账号：13800000000 / 123456")
    print("\n💡 下一步：")
    print("1. 手动导入员工（使用 CSV 模板）")
    print("2. 导入话术（已自动测试导入 5 条）")
    print("3. 员工登录并上传录音")
    print("4. 管理员审核并下载")

if __name__ == '__main__':
    try:
        import requests
        main()
    except ImportError:
        print("❌ 需要安装 requests 库：pip3 install requests")
    except Exception as e:
        print(f"❌ 测试出错：{e}")
