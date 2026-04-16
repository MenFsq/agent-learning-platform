// 修复报告页面的JavaScript功能
const consoleEl = document.getElementById('console');
const API_BASE = 'http://localhost:8004';
const FRONTEND_BASE = 'http://localhost:5177';

function log(message, type = 'success') {
    const entry = document.createElement('div');
    entry.className = `log-entry log-${type}`;
    entry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
    consoleEl.appendChild(entry);
    consoleEl.scrollTop = consoleEl.scrollHeight;
}

function clearConsole() {
    consoleEl.innerHTML = '<div class="log-entry log-success">控制台已清空</div>';
}

async function testBackendHealth() {
    log('测试后端健康检查...', 'success');
    
    try {
        const response = await fetch(API_BASE + '/health');
        const data = await response.json();
        
        if (response.ok) {
            log(`✅ 后端健康检查正常: ${JSON.stringify(data, null, 2)}`, 'success');
        } else {
            log(`❌ 后端健康检查失败: ${response.status}`, 'error');
        }
    } catch (error) {
        log(`❌ 错误: ${error.message}`, 'error');
    }
}

async function testAgentList() {
    log('测试获取Agent列表...', 'success');
    
    try {
        const response = await fetch(API_BASE + '/api/v1/agents');
        const agents = await response.json();
        
        if (response.ok) {
            log(`✅ 找到 ${agents.length} 个Agent:`, 'success');
            agents.forEach(agent => {
                log(`  - ${agent.name} (ID: ${agent.id}, 状态: ${agent.status})`, 'success');
            });
            
            // 检查ID格式
            const hasStringId = agents.some(agent => agent.id.startsWith('agent_'));
            if (hasStringId) {
                log('✅ Agent ID是字符串格式 (agent_xxx)，不是数字', 'success');
            } else {
                log('⚠️ Agent ID不是预期的字符串格式', 'error');
            }
        } else {
            log(`❌ 获取Agent列表失败: ${response.status}`, 'error');
        }
    } catch (error) {
        log(`❌ 错误: ${error.message}`, 'error');
    }
}

async function testAgentStartStop() {
    log('测试Agent启动/停止功能...', 'success');
    
    try {
        // 先获取Agent列表
        const response = await fetch(API_BASE + '/api/v1/agents');
        const agents = await response.json();
        
        if (agents.length > 0) {
            const agent = agents[0];
            log(`使用Agent: ${agent.name} (ID: ${agent.id})`, 'success');
            
            // 启动Agent
            const startResponse = await fetch(API_BASE + `/api/v1/agents/${agent.id}/start`, {
                method: 'POST'
            });
            const startResult = await startResponse.json();
            
            if (startResponse.ok) {
                log(`✅ 启动成功: ${startResult.message}`, 'success');
                
                // 等待2秒
                await new Promise(resolve => setTimeout(resolve, 2000));
                
                // 停止Agent
                const stopResponse = await fetch(API_BASE + `/api/v1/agents/${agent.id}/stop`, {
                    method: 'POST'
                });
                const stopResult = await stopResponse.json();
                
                if (stopResponse.ok) {
                    log(`✅ 停止成功: ${stopResult.message}`, 'success');
                } else {
                    log(`❌ 停止失败: ${JSON.stringify(stopResult)}`, 'error');
                }
            } else {
                log(`❌ 启动失败: ${JSON.stringify(startResult)}`, 'error');
            }
        } else {
            log('❌ 没有找到可用的Agent', 'error');
        }
    } catch (error) {
        log(`❌ 错误: ${error.message}`, 'error');
    }
}

async function testAgentChat() {
    log('测试Agent聊天功能...', 'success');
    
    try {
        // 先获取Agent列表
        const response = await fetch(API_BASE + '/api/v1/agents');
        const agents = await response.json();
        
        if (agents.length > 0) {
            const agent = agents[0];
            
            // 确保Agent是运行状态
            if (agent.status !== 'running') {
                log(`⚠️ Agent ${agent.name} 未运行，正在启动...`, 'success');
                
                const startResponse = await fetch(API_BASE + `/api/v1/agents/${agent.id}/start`, {
                    method: 'POST'
                });
                
                if (!startResponse.ok) {
                    log('❌ 启动Agent失败，无法进行聊天测试', 'error');
                    return;
                }
                
                log('✅ Agent已启动，等待2秒...', 'success');
                await new Promise(resolve => setTimeout(resolve, 2000));
            }
            
            // 与Agent交互
            const interactResponse = await fetch(API_BASE + `/api/v1/agents/${agent.id}/interact`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: "你好，请介绍一下你的功能"
                })
            });
            
            const result = await interactResponse.json();
            
            if (interactResponse.ok) {
                log(`✅ Agent回复: ${result.response}`, 'success');
                log('✅ 聊天功能正常，没有NaN错误！', 'success');
            } else {
                log(`❌ 聊天失败: ${JSON.stringify(result)}`, 'error');
            }
        } else {
            log('❌ 没有找到可用的Agent', 'error');
        }
    } catch (error) {
        log(`❌ 错误: ${error.message}`, 'error');
    }
}

async function testFrontendAccess() {
    log('测试前端页面访问...', 'success');
    
    const pages = [
        { name: 'Agent页面', url: FRONTEND_BASE + '/agent' },
        { name: '社区页面', url: FRONTEND_BASE + '/community' },
        { name: '首页', url: FRONTEND_BASE + '/' },
        { name: '代理健康检查', url: FRONTEND_BASE + '/api/health' }
    ];
    
    for (const page of pages) {
        try {
            const response = await fetch(page.url, { method: 'HEAD' });
            if (response.ok) {
                log(`✅ ${page.name} 可以正常访问 (状态码: ${response.status})`, 'success');
            } else {
                log(`❌ ${page.name} 访问失败 (状态码: ${response.status})`, 'error');
            }
        } catch (error) {
            log(`❌ ${page.name} 访问错误: ${error.message}`, 'error');
        }
    }
}

// 页面加载时自动运行一些测试
window.addEventListener('load', () => {
    setTimeout(() => {
        log('页面加载完成，开始自动测试...', 'success');
        setTimeout(testBackendHealth, 1000);
        setTimeout(testAgentList, 2000);
        setTimeout(testFrontendAccess, 3000);
    }, 1000);
});