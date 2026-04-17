"""
LangChain Agent 模块 - 修复版本
兼容最新LangChain版本
"""
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from dotenv import load_dotenv
import json

# 尝试不同的导入方式
try:
    # 新版本LangChain导入方式
    from langchain_openai import ChatOpenAI
    from langchain.agents import AgentExecutor, create_openai_tools_agent
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain.agents import Tool
    from langchain.memory import ConversationBufferMemory
    from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
    LANGCHAIN_AVAILABLE = True
    LANGCHAIN_VERSION = "new"
except ImportError as e:
    print(f"LangChain导入错误: {e}")
    # 尝试备用导入
    try:
        from langchain.chat_models import ChatOpenAI
        from langchain.agents import initialize_agent, AgentType
        from langchain.memory import ConversationBufferMemory
        from langchain.prompts import MessagesPlaceholder
        from langchain.schema import SystemMessage, HumanMessage, AIMessage
        LANGCHAIN_AVAILABLE = True
        LANGCHAIN_VERSION = "old"
    except ImportError:
        LANGCHAIN_AVAILABLE = False
        LANGCHAIN_VERSION = "none"

# 加载环境变量
load_dotenv()

class LangChainAgentManager:
    """LangChain Agent管理器 - 兼容版本"""
    
    def __init__(self):
        """初始化Agent管理器"""
        if not LANGCHAIN_AVAILABLE:
            print("警告: LangChain不可用，将使用模拟模式")
            self.mock_mode = True
            return
        
        self.mock_mode = False
        self.agents = {}
        self.initialize_agents()
    
    def initialize_agents(self):
        """初始化预定义的Agent"""
        if self.mock_mode:
            # 模拟模式
            self.agents = {
                "agent_1776365387.509348": {
                    "id": "agent_1776365387.509348",
                    "name": "智能文档助手",
                    "description": "专业的文档处理和分析助手",
                    "status": "stopped",
                    "tools": ["文档解析", "文本摘要", "关键词提取"],
                    "model": "gpt-3.5-turbo"
                },
                "agent_1776365388.123456": {
                    "id": "agent_1776365388.123456",
                    "name": "代码审查专家",
                    "description": "专业的代码审查和质量分析助手",
                    "status": "stopped",
                    "tools": ["代码分析", "漏洞检测", "最佳实践建议"],
                    "model": "gpt-4"
                },
                "agent_1776365389.789012": {
                    "id": "agent_1776365389.789012",
                    "name": "学习进度跟踪",
                    "description": "学习进度跟踪和个性化推荐助手",
                    "status": "stopped",
                    "tools": ["进度分析", "个性化推荐", "学习计划"],
                    "model": "gpt-3.5-turbo"
                }
            }
            return
        
        try:
            # 创建模拟工具
            def document_analyzer(query: str) -> str:
                """文档分析工具"""
                return f"已分析文档: {query}\n分析结果: 文档结构良好，包含重要信息。"
            
            def code_reviewer(code: str) -> str:
                """代码审查工具"""
                return f"代码审查结果: {code[:50]}...\n建议: 代码结构清晰，建议添加更多注释。"
            
            def learning_tracker(progress: str) -> str:
                """学习进度跟踪工具"""
                return f"学习进度分析: {progress}\n建议: 保持当前学习节奏，建议复习重点内容。"
            
            # 创建工具列表
            tools = []
            
            if LANGCHAIN_VERSION == "new":
                # 新版本工具创建
                tools = [
                    Tool(
                        name="document_analyzer",
                        func=document_analyzer,
                        description="分析文档内容和结构"
                    ),
                    Tool(
                        name="code_reviewer",
                        func=code_reviewer,
                        description="审查代码质量和最佳实践"
                    ),
                    Tool(
                        name="learning_tracker",
                        func=learning_tracker,
                        description="跟踪学习进度并提供建议"
                    )
                ]
            else:
                # 旧版本工具创建
                from langchain.tools import Tool
                tools = [
                    Tool(
                        name="document_analyzer",
                        func=document_analyzer,
                        description="分析文档内容和结构"
                    ),
                    Tool(
                        name="code_reviewer",
                        func=code_reviewer,
                        description="审查代码质量和最佳实践"
                    ),
                    Tool(
                        name="learning_tracker",
                        func=learning_tracker,
                        description="跟踪学习进度并提供建议"
                    )
                ]
            
            # 创建Agent
            agent1 = self.create_agent(
                agent_id="agent_1776365387.509348",
                name="智能文档助手",
                description="专业的文档处理和分析助手",
                tools=[tools[0]],
                model="gpt-3.5-turbo"
            )
            
            agent2 = self.create_agent(
                agent_id="agent_1776365388.123456",
                name="代码审查专家",
                description="专业的代码审查和质量分析助手",
                tools=[tools[1]],
                model="gpt-4"
            )
            
            agent3 = self.create_agent(
                agent_id="agent_1776365389.789012",
                name="学习进度跟踪",
                description="学习进度跟踪和个性化推荐助手",
                tools=[tools[2]],
                model="gpt-3.5-turbo"
            )
            
            self.agents = {
                agent1["id"]: agent1,
                agent2["id"]: agent2,
                agent3["id"]: agent3
            }
            
            print(f"成功初始化 {len(self.agents)} 个LangChain Agent")
            
        except Exception as e:
            print(f"初始化Agent时出错: {e}")
            print("将使用模拟模式")
            self.mock_mode = True
            self.initialize_agents()  # 递归调用模拟模式
    
    def create_agent(self, agent_id: str, name: str, description: str, tools: list, model: str = "gpt-3.5-turbo"):
        """创建Agent"""
        if self.mock_mode:
            return {
                "id": agent_id,
                "name": name,
                "description": description,
                "status": "stopped",
                "tools": [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools],
                "model": model,
                "chain": None
            }
        
        try:
            # 创建LLM
            llm = ChatOpenAI(
                temperature=0.7,
                model_name=model,
                openai_api_key=os.getenv("OPENAI_API_KEY", "sk-demo")
            )
            
            # 创建提示模板
            prompt = ChatPromptTemplate.from_messages([
                ("system", f"你是一个{name}，{description}"),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ])
            
            # 创建记忆
            memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
            
            if LANGCHAIN_VERSION == "new":
                # 新版本Agent创建
                agent = create_openai_tools_agent(llm, tools, prompt)
                agent_executor = AgentExecutor(
                    agent=agent,
                    tools=tools,
                    memory=memory,
                    verbose=True,
                    handle_parsing_errors=True
                )
            else:
                # 旧版本Agent创建
                agent_executor = initialize_agent(
                    tools=tools,
                    llm=llm,
                    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
                    memory=memory,
                    verbose=True,
                    handle_parsing_errors=True
                )
            
            return {
                "id": agent_id,
                "name": name,
                "description": description,
                "status": "stopped",
                "tools": [tool.name for tool in tools],
                "model": model,
                "chain": agent_executor,
                "memory": memory
            }
            
        except Exception as e:
            print(f"创建Agent {name} 时出错: {e}")
            # 返回模拟Agent
            return {
                "id": agent_id,
                "name": name,
                "description": description,
                "status": "stopped",
                "tools": [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools],
                "model": model,
                "chain": None
            }
    
    def get_agents(self) -> List[Dict]:
        """获取所有Agent"""
        return list(self.agents.values())
    
    def get_agent(self, agent_id: str) -> Optional[Dict]:
        """获取特定Agent"""
        return self.agents.get(agent_id)
    
    def start_agent(self, agent_id: str) -> bool:
        """启动Agent"""
        agent = self.get_agent(agent_id)
        if not agent:
            return False
        
        agent["status"] = "running"
        print(f"Agent {agent['name']} 已启动")
        return True
    
    def stop_agent(self, agent_id: str) -> bool:
        """停止Agent"""
        agent = self.get_agent(agent_id)
        if not agent:
            return False
        
        agent["status"] = "stopped"
        print(f"Agent {agent['name']} 已停止")
        return True
    
    def interact_with_agent(self, agent_id: str, message: str) -> str:
        """与Agent交互"""
        agent = self.get_agent(agent_id)
        if not agent:
            return "Agent未找到"
        
        if agent["status"] != "running":
            return f"Agent {agent['name']} 未运行，请先启动Agent"
        
        if self.mock_mode or agent.get("chain") is None:
            # 模拟响应
            responses = {
                "agent_1776365387.509348": f"智能文档助手: 已收到您的文档查询: '{message}'。我会帮您分析文档内容。",
                "agent_1776365388.123456": f"代码审查专家: 已收到您的代码: '{message[:50]}...'。我会进行代码审查。",
                "agent_1776365389.789012": f"学习进度跟踪: 已记录您的学习进度: '{message}'。我会为您提供个性化建议。"
            }
            return responses.get(agent_id, f"Agent响应: {message}")
        
        try:
            # 实际LangChain调用
            response = agent["chain"].run(input=message)
            return response
        except Exception as e:
            print(f"与Agent交互时出错: {e}")
            return f"Agent响应时出错: {str(e)}"

# 全局Agent管理器实例
agent_manager = LangChainAgentManager()