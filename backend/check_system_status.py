#!/usr/bin/env python3
"""
Agent Learning Platform 系统状态检查脚本
用于快速验证前后端服务状态
"""

import requests
import time
import sys
from datetime import datetime

def check_backend():
    """检查后端服务状态"""
    print("🔍 检查后端服务...")
    
    endpoints = [
        ("健康检查", "http://localhost:8004/health"),
        ("Agent列表", "http://localhost:8004/api/v1/agents"),
        ("API文档", "http://localhost:8004/docs"),
    ]
    
    all_ok = True
    for name, url in endpoints:
        try:
            if name == "API文档":
                # 对于文档页面，只需要检查是否能访问
                response = requests.get(url, timeout=5)
                status = "✅" if response.status_code == 200 else "❌"
                print(f"  {status} {name}: {url} (状态码: {response.status_code})")
            else:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if name == "健康检查":
                        print(f"  ✅ {name}: {url} - {data.get('status', 'unknown')}")
                    elif name == "Agent列表":
                        print(f"  ✅ {name}: {url} - 找到 {len(data)} 个Agent")
                        for agent in data[:3]:  # 只显示前3个
                            print(f"    • {agent.get('name', '未知')}: {agent.get('status', '未知')}")
                else:
                    print(f"  ❌ {name}: {url} (状态码: {response.status_code})")
                    all_ok = False
        except requests.exceptions.RequestException as e:
            print(f"  ❌ {name}: {url} (错误: {e})")
            all_ok = False
    
    return all_ok

def check_frontend():
    """检查前端服务状态"""
    print("\n🔍 检查前端服务...")
    
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
                print(f"  ✅ 前端服务运行在: {url}")
                break
        except:
            continue
    
    if not frontend_url:
        print("  ❌ 未找到运行中的前端服务")
        return False
    
    # 检查前端代理
    endpoints = [
        ("前端代理健康检查", f"{frontend_url}/api/health"),
        ("前端代理Agent列表", f"{frontend_url}/api/v1/agents"),
    ]
    
    all_ok = True
    for name, url in endpoints:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if "health" in url:
                    print(f"  ✅ {name}: {data.get('status', 'unknown')}")
                else:
                    print(f"  ✅ {name}: 找到 {len(data)} 个Agent")
            else:
                print(f"  ❌ {name}: 状态码 {response.status_code}")
                all_ok = False
        except requests.exceptions.RequestException as e:
            print(f"  ❌ {name}: 错误 {e}")
            all_ok = False
    
    return all_ok, frontend_url

def check_functionality(frontend_url):
    """检查核心功能"""
    print("\n🔍 检查核心功能...")
    
    try:
        # 获取Agent列表
        response = requests.get(f"{frontend_url}/api/v1/agents", timeout=5)
        if response.status_code != 200:
            print("  ❌ 无法获取Agent列表")
            return False
        
        agents = response.json()
        if not agents:
            print("  ⚠️ 没有找到Agent")
            return True  # 没有Agent不是错误，只是警告
        
        agent = agents[0]  # 使用第一个Agent测试
        agent_id = agent['id']
        agent_name = agent['name']
        current_status = agent['status']
        
        print(f"  📋 测试Agent: {agent_name} (ID: {agent_id[:15]}..., 状态: {current_status})")
        
        # 根据当前状态测试启动或停止
        if current_status == 'stopped':
            # 测试启动
            print("  🚀 测试启动功能...")
            start_response = requests.post(f"{frontend_url}/api/v1/agents/{agent_id}/start", timeout=10)
            if start_response.status_code == 200:
                print(f"    ✅ 启动成功: {start_response.json().get('message', '成功')}")
                
                # 等待并验证状态
                time.sleep(2)
                updated = requests.get(f"{frontend_url}/api/v1/agents", timeout=5).json()
                updated_agent = next((a for a in updated if a['id'] == agent_id), None)
                if updated_agent and updated_agent['status'] == 'running':
                    print(f"    ✅ 状态已更新: {updated_agent['status']}")
                    
                    # 测试停止
                    print("  🛑 测试停止功能...")
                    stop_response = requests.post(f"{frontend_url}/api/v1/agents/{agent_id}/stop", timeout=10)
                    if stop_response.status_code == 200:
                        print(f"    ✅ 停止成功: {stop_response.json().get('message', '成功')}")
                        
                        # 等待并验证状态
                        time.sleep(2)
                        final = requests.get(f"{frontend_url}/api/v1/agents", timeout=5).json()
                        final_agent = next((a for a in final if a['id'] == agent_id), None)
                        if final_agent and final_agent['status'] == 'stopped':
                            print(f"    ✅ 状态已更新: {final_agent['status']}")
                            return True
                        else:
                            print(f"    ❌ 停止后状态未更新")
                            return False
                    else:
                        print(f"    ❌ 停止失败: {stop_response.status_code}")
                        return False
                else:
                    print(f"    ❌ 启动后状态未更新")
                    return False
            else:
                print(f"    ❌ 启动失败: {start_response.status_code}")
                return False
        else:
            # 当前是running状态，测试停止
            print("  🛑 测试停止功能...")
            stop_response = requests.post(f"{frontend_url}/api/v1/agents/{agent_id}/stop", timeout=10)
            if stop_response.status_code == 200:
                print(f"    ✅ 停止成功: {stop_response.json().get('message', '成功')}")
                
                # 等待并验证状态
                time.sleep(2)
                updated = requests.get(f"{frontend_url}/api/v1/agents", timeout=5).json()
                updated_agent = next((a for a in updated if a['id'] == agent_id), None)
                if updated_agent and updated_agent['status'] == 'stopped':
                    print(f"    ✅ 状态已更新: {updated_agent['status']}")
                    return True
                else:
                    print(f"    ❌ 停止后状态未更新")
                    return False
            else:
                print(f"    ❌ 停止失败: {stop_response.status_code}")
                return False
                
    except Exception as e:
        print(f"  ❌ 功能测试异常: {e}")
        return False

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
    
    # 检查功能
    functionality_ok = False
    if frontend_ok and frontend_url:
        functionality_ok = check_functionality(frontend_url)
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 检查结果总结")
    print("=" * 60)
    
    status_icons = {
        True: "✅",
        False: "❌"
    }
    
    print(f"{status_icons[backend_ok]} 后端服务: {'正常' if backend_ok else '异常'}")
    print(f"{status_icons[frontend_ok]} 前端服务: {'正常' if frontend_ok else '异常'}")
    print(f"{status_icons[functionality_ok]} 核心功能: {'正常' if functionality_ok else '异常'}")
    
    if frontend_url:
        print(f"\n🔗 访问地址:")
        print(f"   前端: {frontend_url}/agent")
        print(f"   后端API文档: http://localhost:8004/docs")
        print(f"   状态报告: {frontend_url}/final-system-status.html")
    
    print(f"\n⏰ 检查完成时间: {datetime.now().strftime('%H:%M:%S')}")
    
    # 返回退出码
    if backend_ok and frontend_ok and functionality_ok:
        print("\n🎉 所有检查通过！系统运行正常。")
        return 0
    else:
        print("\n⚠️  系统存在异常，请检查相关服务。")
        return 1

if __name__ == "__main__":
    sys.exit(main())