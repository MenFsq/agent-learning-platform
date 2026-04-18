/**
 * 前端模拟API服务器
 * 在没有真实后端服务器时使用
 */

// 模拟数据库
const mockDatabase = {
  agents: [
    {
      id: 'agent_001',
      name: 'Learning Agent',
      type: 'educational',
      status: 'active',
      created_at: '2026-04-15T10:30:00Z',
      config: {
        learning_rate: 0.01,
        memory_size: 1000,
        skills: ['vue', 'python', 'openclaw']
      }
    },
    {
      id: 'agent_002',
      name: 'Code Review Agent',
      type: 'technical',
      status: 'active',
      created_at: '2026-04-16T14:20:00Z',
      config: {
        languages: ['javascript', 'typescript', 'python'],
        rules: ['best-practices', 'security', 'performance']
      }
    }
  ],
  
  learning: {
    progress: 42,
    modules: [
      { id: 'module_1', name: 'Introduction', completed: true },
      { id: 'module_2', name: 'Basic Concepts', completed: true },
      { id: 'module_3', name: 'Advanced Techniques', completed: false },
      { id: 'module_4', name: 'Real Projects', completed: false }
    ],
    achievements: [
      'First Agent Created',
      'Basic Training Completed',
      'API Integration Mastered'
    ]
  },
  
  tasks: [
    {
      id: 'task_001',
      title: 'Setup Development Environment',
      description: 'Install and configure all necessary tools',
      status: 'completed',
      priority: 'high',
      due_date: '2026-04-10'
    },
    {
      id: 'task_002',
      title: 'Implement Core API',
      description: 'Create basic REST endpoints for agent management',
      status: 'in_progress',
      priority: 'high',
      due_date: '2026-04-20'
    }
  ]
};

// 模拟延迟
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// API 模拟器
class MockAPIServer {
  constructor() {
    this.db = JSON.parse(JSON.stringify(mockDatabase)); // 深拷贝
    this.requestCount = 0;
  }
  
  // 健康检查
  async health() {
    await delay(100);
    return {
      status: 'healthy',
      service: 'Mock API Server',
      version: '1.0.0',
      timestamp: new Date().toISOString(),
      requests_served: this.requestCount++,
      mode: 'frontend-mock'
    };
  }
  
  // 获取所有代理
  async getAgents() {
    await delay(200);
    return {
      agents: this.db.agents,
      count: this.db.agents.length,
      timestamp: new Date().toISOString()
    };
  }
  
  // 创建新代理
  async createAgent(agentData) {
    await delay(300);
    
    const newAgent = {
      id: `agent_${Date.now().toString(36)}`,
      name: agentData.name || 'Unnamed Agent',
      type: agentData.type || 'general',
      status: 'created',
      created_at: new Date().toISOString(),
      config: agentData.config || {}
    };
    
    this.db.agents.push(newAgent);
    
    return {
      message: 'Agent created successfully',
      agent: newAgent,
      total_agents: this.db.agents.length
    };
  }
  
  // 获取学习进度
  async getLearningProgress() {
    await delay(150);
    return {
      ...this.db.learning,
      timestamp: new Date().toISOString(),
      estimated_completion: '2026-05-01'
    };
  }
  
  // 更新学习进度
  async updateLearningProgress(moduleId) {
    await delay(250);
    
    const module = this.db.learning.modules.find(m => m.id === moduleId);
    if (module) {
      module.completed = true;
      this.db.learning.progress = Math.floor(
        (this.db.learning.modules.filter(m => m.completed).length / 
         this.db.learning.modules.length) * 100
      );
      
      // 添加成就
      if (this.db.learning.progress >= 50 && !this.db.learning.achievements.includes('Halfway There')) {
        this.db.learning.achievements.push('Halfway There');
      }
      
      return {
        success: true,
        module: module,
        progress: this.db.learning.progress,
        achievements: this.db.learning.achievements
      };
    }
    
    return {
      success: false,
      error: 'Module not found'
    };
  }
  
  // 获取任务列表
  async getTasks() {
    await delay(180);
    return {
      tasks: this.db.tasks,
      count: this.db.tasks.length,
      completed: this.db.tasks.filter(t => t.status === 'completed').length,
      pending: this.db.tasks.filter(t => t.status !== 'completed').length
    };
  }
  
  // 创建新任务
  async createTask(taskData) {
    await delay(350);
    
    const newTask = {
      id: `task_${Date.now().toString(36)}`,
      title: taskData.title || 'New Task',
      description: taskData.description || '',
      status: 'pending',
      priority: taskData.priority || 'medium',
      due_date: taskData.due_date || new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      created_at: new Date().toISOString()
    };
    
    this.db.tasks.push(newTask);
    
    return {
      message: 'Task created successfully',
      task: newTask,
      total_tasks: this.db.tasks.length
    };
  }
  
  // 更新任务状态
  async updateTask(taskId, updates) {
    await delay(220);
    
    const taskIndex = this.db.tasks.findIndex(t => t.id === taskId);
    if (taskIndex !== -1) {
      this.db.tasks[taskIndex] = {
        ...this.db.tasks[taskIndex],
        ...updates,
        updated_at: new Date().toISOString()
      };
      
      return {
        success: true,
        task: this.db.tasks[taskIndex],
        message: 'Task updated successfully'
      };
    }
    
    return {
      success: false,
      error: 'Task not found'
    };
  }
  
  // 获取系统统计
  async getStats() {
    await delay(120);
    
    const now = new Date();
    const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
    
    return {
      agents: {
        total: this.db.agents.length,
        active: this.db.agents.filter(a => a.status === 'active').length,
        by_type: this.db.agents.reduce((acc, agent) => {
          acc[agent.type] = (acc[agent.type] || 0) + 1;
          return acc;
        }, {})
      },
      learning: {
        progress: this.db.learning.progress,
        completed_modules: this.db.learning.modules.filter(m => m.completed).length,
        total_modules: this.db.learning.modules.length,
        achievements: this.db.learning.achievements.length
      },
      tasks: {
        total: this.db.tasks.length,
        completed: this.db.tasks.filter(t => t.status === 'completed').length,
        in_progress: this.db.tasks.filter(t => t.status === 'in_progress').length,
        pending: this.db.tasks.filter(t => t.status === 'pending').length
      },
      system: {
        uptime: '24/7',
        requests_served: this.requestCount,
        last_updated: now.toISOString(),
        data_size: JSON.stringify(this.db).length
      }
    };
  }
}

// 创建单例实例
const mockServer = new MockAPIServer();

// 导出API函数
export const mockAPI = {
  // 健康检查
  health: () => mockServer.health(),
  
  // 代理管理
  getAgents: () => mockServer.getAgents(),
  createAgent: (agentData) => mockServer.createAgent(agentData),
  
  // 学习管理
  getLearningProgress: () => mockServer.getLearningProgress(),
  updateLearningProgress: (moduleId) => mockServer.updateLearningProgress(moduleId),
  
  // 任务管理
  getTasks: () => mockServer.getTasks(),
  createTask: (taskData) => mockServer.createTask(taskData),
  updateTask: (taskId, updates) => mockServer.updateTask(taskId, updates),
  
  // 系统统计
  getStats: () => mockServer.getStats(),
  
  // 工具函数
  resetDatabase: () => {
    mockServer.db = JSON.parse(JSON.stringify(mockDatabase));
    mockServer.requestCount = 0;
    return { message: 'Database reset successfully' };
  },
  
  exportData: () => ({
    data: mockServer.db,
    timestamp: new Date().toISOString(),
    version: '1.0.0'
  })
};

// 默认导出
export default mockAPI;