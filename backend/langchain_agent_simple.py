"""
简化的LangChain Agent模块
兼容LangChain 1.x版本
"""
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

# 尝试导入LangChain组件
try:
    from langchain_openai import ChatOpenAI
    from langchain.agents import AgentExecutor, create_openai_tools_agent
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain.agents import Tool
    from langchain.memory import ConversationBufferMemory
    from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
    LANGCHAIN_AVAILABLE = True
except ImportError as e:
    print(f"LangChain导入失败: {e}")
    print("使用模拟模式运行...")
    LANGCHAIN_AVAILABLE = False

# 加载环境变量
load_dotenv()

class LangChainAgentManager:
    """LangChain Agent管理器"""
    
    def __init__(self):
        self.agents: Dict[str, Any] = {}
        self.conversations: Dict[str, List[Dict]] = {}
        
    def create_agent(self, agent_config: Dict[str, Any]) -> Dict[str, Any]:
        """创建新的Agent"""
        agent_id = f"agent_{datetime.now().timestamp()}"
        
        if LANGCHAIN_AVAILABLE:
            try:
                # 配置LLM
                llm = ChatOpenAI(
                    model=agent_config.get("model", "gpt-3.5-turbo"),
                    temperature=agent_config.get("temperature", 0.7),
                    max_tokens=agent_config.get("max_tokens", 2000),
                    api_key=os.getenv("OPENAI_API_KEY", "sk-test-key-1234567890")
                )
                
                # 定义工具
                tools = self._create_tools(agent_config.get("tools", []))
                
                # 创建提示模板
                prompt = ChatPromptTemplate.from_messages([
                    SystemMessage(content=agent_config.get("system_prompt", "你是一个有帮助的AI助手。")),
                    MessagesPlaceholder(variable_name="chat_history"),
                    HumanMessage(content="{input}"),
                    MessagesPlaceholder(variable_name="agent_scratchpad")
                ])
                
                # 创建Agent
                agent = create_openai_tools_agent(llm, tools, prompt)
                
                # 创建执行器
                memory = ConversationBufferMemory(
                    memory_key="chat_history",
                    return_messages=True
                ) if agent_config.get("memory", False) else None
                
                agent_executor = AgentExecutor(
                    agent=agent,
                    tools=tools,
                    memory=memory,
                    verbose=True,
                    handle_parsing_errors=True
                )
                
                executor = agent_executor
            except Exception as e:
                print(f"创建真实Agent失败，使用模拟模式: {e}")
                executor = None
        else:
            executor = None
        
        # 保存Agent
        self.agents[agent_id] = {
            "id": agent_id,
            "name": agent_config.get("name", "未命名Agent"),
            "description": agent_config.get("description", ""),
            "type": agent_config.get("type", "conversational"),
            "config": agent_config,
            "executor": executor,
            "created_at": datetime.now().isoformat(),
            "status": "stopped",
            "run_count": 0
        }
        
        # 初始化对话历史
        self.conversations[agent_id] = []
        
        return self.agents[agent_id]
    
    def _create_tools(self, tool_names: List[str]) -> List:
        """根据工具名称创建工具"""
        if not LANGCHAIN_AVAILABLE:
            return []
            
        tools = []
        
        # 网页搜索工具
        if "web-search" in tool_names:
            from langchain.agents import Tool
            tools.append(Tool(
                name="web_search",
                func=self._web_search,
                description="搜索网页获取最新信息"
            ))
        
        # 计算器工具
        if "calculator" in tool_names:
            from langchain.agents import Tool
            tools.append(Tool(
                name="calculator",
                func=self._calculator,
                description="执行数学计算"
            ))
        
        return tools
    
    def _web_search(self, query: str) -> str:
        """网页搜索工具（模拟）"""
        return f"搜索 '{query}' 的结果：\n1. 相关结果1\n2. 相关结果2\n3. 相关结果3"
    
    def _calculator(self, expression: str) -> str:
        """计算器工具（模拟）"""
        try:
            # 安全地计算表达式
            allowed_chars = "0123456789+-*/(). "
            if all(c in allowed_chars for c in expression):
                result = eval(expression)
                return f"{expression} = {result}"
            else:
                return "错误：表达式包含不安全字符"
        except Exception as e:
            return f"计算错误：{str(e)}"
    
    def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """获取Agent信息"""
        return self.agents.get(agent_id)
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """列出所有Agent"""
        return list(self.agents.values())
    
    def update_agent(self, agent_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """更新Agent配置"""
        if agent_id not in self.agents:
            return None
        
        agent = self.agents[agent_id]
        
        # 更新配置
        for key, value in updates.items():
            if key in ["name", "description", "type"]:
                agent[key] = value
            elif key == "config":
                agent["config"].update(value)
        
        agent["updated_at"] = datetime.now().isoformat()
        return agent
    
    def delete_agent(self, agent_id: str) -> bool:
        """删除Agent"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            if agent_id in self.conversations:
                del self.conversations[agent_id]
            return True
        return False
    
    def start_agent(self, agent_id: str) -> bool:
        """启动Agent"""
        if agent_id not in self.agents:
            return False
        
        self.agents[agent_id]["status"] = "running"
        self.agents[agent_id]["started_at"] = datetime.now().isoformat()
        return True
    
    def stop_agent(self, agent_id: str) -> bool:
        """停止Agent"""
        if agent_id not in self.agents:
            return False
        
        self.agents[agent_id]["status"] = "stopped"
        return True
    
    def interact_with_agent(self, agent_id: str, message: str) -> Dict[str, Any]:
        """与Agent交互"""
        if agent_id not in self.agents:
            return {"error": "Agent not found"}
        
        agent = self.agents[agent_id]
        
        if agent["status"] != "running":
            return {"error": "Agent is not running"}
        
        try:
            # 如果有真实的executor，使用它
            if agent["executor"] is not None and LANGCHAIN_AVAILABLE:
                executor = agent["executor"]
                response = executor.invoke({"input": message})
                agent_response = response.get("output", "没有响应")
            else:
                # 模拟响应
                agent_response = f"模拟响应（LangChain未启用）: 你说了 '{message}'。这是一个模拟的Agent回复。"
            
            # 记录对话
            conversation_entry = {
                "timestamp": datetime.now().isoformat(),
                "user": message,
                "agent": agent_response,
                "intermediate_steps": []
            }
            
            self.conversations[agent_id].append(conversation_entry)
            agent["run_count"] += 1
            
            return {
                "success": True,
                "response": agent_response,
                "conversation_id": len(self.conversations[agent_id]) - 1
            }
            
        except Exception as e:
            return {"error": f"Agent interaction failed: {str(e)}"}
    
    def get_conversation_history(self, agent_id: str, limit: int = 10) -> List[Dict]:
        """获取对话历史"""
        if agent_id not in self.conversations:
            return []
        
        return self.conversations[agent_id][-limit:]
    
    def clear_conversation_history(self, agent_id: str) -> bool:
        """清空对话历史"""
        if agent_id in self.conversations:
            self.conversations[agent_id] = []
            return True
        return False

# 全局Agent管理器实例
agent_manager = LangChainAgentManager()

# 创建一些示例Agent
def initialize_sample_agents():
    """初始化示例Agent"""
    
    # 文档分析助手
    agent_manager.create_agent({
        "name": "文档分析助手",
        "description": "使用LangChain分析文档内容，提取关键信息",
        "type": "tool-calling",
        "model": "gpt-3.5-turbo",
        "temperature": 0.7,
        "max_tokens": 2000,
        "memory": True,
        "tools": ["web-search"],
        "system_prompt": "你是一个专业的文档分析助手。请帮助用户分析文档内容，提取关键信息，并提供总结和建议。"
    })
    
    # 代码审查助手
    agent_manager.create_agent({
        "name": "代码审查助手",
        "description": "自动审查代码质量，提供改进建议",
        "type": "conversational",
        "model": "gpt-3.5-turbo",
        "temperature": 0.3,
        "max_tokens": 1000,
        "memory": False,
        "tools": [],
        "system_prompt": "你是一个专业的代码审查助手。请仔细审查用户提供的代码，指出潜在问题，并提供改进建议。"
    })
    
    # 数据分析助手
    agent_manager.create_agent({
        "name": "数据分析助手",
        "description": "处理和分析结构化数据，生成可视化报告",
        "type": "planning",
        "model": "gpt-4",
        "temperature": 0.5,
        "max_tokens": 4000,
        "memory": True,
        "tools": ["calculator"],
        "system_prompt": "你是一个专业的数据分析助手。请帮助用户分析数据，提供洞察，并生成报告。"
    })

# 初始化示例Agent
initialize_sample_agents()

print(f"LangChain可用: {LANGCHAIN_AVAILABLE}")
print(f"已初始化 {len(agent_manager.list_agents())} 个Agent")