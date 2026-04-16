#!/usr/bin/env python3
"""
Agent Learning Platform 系统状态检查脚本（简化版）
"""

import requests
import time
import sys
from datetime import datetime

def check_backend():
    """检查后端服务状态"""
    print("检查后端服务...")
    
    endpoints = [
        ("健康检查", "http://localhost:8004/health"),
        ("Agent列表", "http://localhost:8004/api/v1/agents"),
    ]
    
    all_ok = True
    for name, url in endpoints:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if name == "健康检查":
                    print(f"  [OK] {name}: {data.get('status', 'unknown')}")
                elif name == "Agent列表":
                    print(f"  [OK] {name}: 找到 {len(data)} 个Agent")
            else:
                print(f"  [ERROR] {name}: 状态码 {response.status_code}")
                all_ok = False
        except Exception as e:
            print(f"  [ERROR] {name}: {e}")
            all_ok = False
    
    return all_ok

def check_frontend():
    """检查前端服务状态"""
    print("\n检查前端服务...")
    
    # 前端运行在动态端口，需要检测当前端口
    base_port = 5174
    max_port = 5185
    frontend_url = None
    
    # 尝试找到运行中的前端
    for port in range(base_port, max_port + 1):
        url = f"http://localhost:{port}"
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                frontend_url = url
                print(f"  [OK] 前端服务运行在: {url}")
                break
        except:
            continue
    
    if not frontend_url:
        print("  [ERROR] 未找到运行中的前端服务")
        return False, None
    
    # 检查前端代理
    try:
        response = requests.get(f"{frontend_url}/api/v1/agents", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  [OK] 前端代理正常: 找到 {len(data)} 个Agent")
            return True, frontend_url
        else:
            print(f"  [ERROR] 前端代理异常: 状态码 {response.status_code}")
            return False, frontend_url
    except Exception as e:
        print(f"  [ERROR] 前端代理异常: {e}")
        return False, frontend_url

def main():
    """主函数"""
    print("=" * 60)
    print("Agent Learning Platform 系统状态检查")
    print("=" * 60)
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 检查后端
    backend_ok = check_backend()
    
    # 检查前端
    frontend_ok, frontend_url = check_frontend()
    
    # 总结
    print("\n" + "=" * 60)
    print("检查结果总结")
    print("=" * 60)
    
    print(f"后端服务: {'[OK] 正常' if backend_ok else '[ERROR] 异常'}")
    print(f"前端服务: {'[OK] 正常' if frontend_ok else '[ERROR] 异常'}")
    
    if frontend_url:
        print(f"\n访问地址:")
        print(f"  前端: {frontend_url}/agent")
        print(f"  后端API文档: http://localhost:8004/docs")
        print(f"  状态报告: {frontend_url}/final-system-status.html")
    
    print(f"\n检查完成时间: {datetime.now().strftime('%H:%M:%S')}")
    
    # 返回退出码
    if backend_ok and frontend_ok:
        print("\n[SUCCESS] 所有检查通过！系统运行正常。")
        return 0
    else:
        print("\n[WARNING] 系统存在异常，请检查相关服务。")
        return 1

if __name__ == "__main__":
    sys.exit(main())