/**
 * Agent Learning Platform - Cloudflare Worker API
 */

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // CORS 头
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };
    
    // 处理 OPTIONS 预检请求
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: corsHeaders,
      });
    }
    
    // API 路由
    if (url.pathname.startsWith('/api/')) {
      return handleAPI(request, url, corsHeaders);
    }
    
    // 前端静态文件（由 GitHub Pages 处理）
    return fetch(`https://${env.GITHUB_USER}.github.io/${env.REPO_NAME}${url.pathname}`);
  },
};

async function handleAPI(request, url, corsHeaders) {
  const path = url.pathname;
  
  // 健康检查
  if (path === '/api/health' || path === '/api/health/') {
    const healthData = {
      status: 'healthy',
      service: 'Agent Learning Platform API',
      version: '1.0.0',
      timestamp: new Date().toISOString(),
      environment: 'cloudflare-worker',
    };
    
    return new Response(JSON.stringify(healthData, null, 2), {
      headers: {
        'Content-Type': 'application/json',
        ...corsHeaders,
      },
    });
  }
  
  // 状态检查
  if (path === '/api/status' || path === '/api/status/') {
    const statusData = {
      status: 'running',
      uptime: '24/7',
      endpoints: [
        '/api/health',
        '/api/status',
        '/api/agents',
        '/api/learning',
        '/api/tasks',
      ],
      limits: {
        requests_per_day: 100000,
        cpu_time_ms: 10,
        memory_mb: 128,
      },
    };
    
    return new Response(JSON.stringify(statusData, null, 2), {
      headers: {
        'Content-Type': 'application/json',
        ...corsHeaders,
      },
    });
  }
  
  // 代理列表
  if (path === '/api/agents' || path === '/api/agents/') {
    if (request.method === 'GET') {
      const agents = [
        {
          id: 'agent_001',
          name: 'Learning Agent',
          type: 'educational',
          status: 'active',
          created_at: '2026-04-15T10:30:00Z',
        },
        {
          id: 'agent_002',
          name: 'Code Review Agent',
          type: 'technical',
          status: 'active',
          created_at: '2026-04-16T14:20:00Z',
        },
        {
          id: 'agent_003',
          name: 'Documentation Agent',
          type: 'assistant',
          status: 'idle',
          created_at: '2026-04-17T09:00:00Z',
        },
      ];
      
      return new Response(JSON.stringify({ agents }, null, 2), {
        headers: {
          'Content-Type': 'application/json',
          ...corsHeaders,
        },
      });
    }
    
    if (request.method === 'POST') {
      try {
        const data = await request.json();
        
        const newAgent = {
          id: `agent_${Date.now().toString(36)}`,
          name: data.name || 'Unnamed Agent',
          type: data.type || 'general',
          status: 'created',
          created_at: new Date().toISOString(),
          config: data.config || {},
        };
        
        // 这里可以保存到 KV 存储
        // await env.AGENTS_KV.put(newAgent.id, JSON.stringify(newAgent));
        
        return new Response(JSON.stringify({
          message: 'Agent created successfully',
          agent: newAgent,
        }, null, 2), {
          status: 201,
          headers: {
            'Content-Type': 'application/json',
            ...corsHeaders,
          },
        });
      } catch (error) {
        return new Response(JSON.stringify({
          error: 'Invalid JSON data',
          details: error.message,
        }, null, 2), {
          status: 400,
          headers: {
            'Content-Type': 'application/json',
            ...corsHeaders,
          },
        });
      }
    }
  }
  
  // 学习进度
  if (path === '/api/learning' || path === '/api/learning/') {
    const learningData = {
      progress: {
        completed: 42,
        total: 100,
        percentage: 42,
      },
      modules: [
        { id: 'module_1', name: 'Introduction', completed: true },
        { id: 'module_2', name: 'Basic Concepts', completed: true },
        { id: 'module_3', name: 'Advanced Techniques', completed: false },
        { id: 'module_4', name: 'Real Projects', completed: false },
      ],
      achievements: [
        'First Agent Created',
        'Basic Training Completed',
        'API Integration Mastered',
      ],
    };
    
    return new Response(JSON.stringify(learningData, null, 2), {
      headers: {
        'Content-Type': 'application/json',
        ...corsHeaders,
      },
    });
  }
  
  // 任务管理
  if (path === '/api/tasks' || path === '/api/tasks/') {
    const tasks = [
      {
        id: 'task_001',
        title: 'Setup Development Environment',
        description: 'Install and configure all necessary tools',
        status: 'completed',
        priority: 'high',
        due_date: '2026-04-10',
      },
      {
        id: 'task_002',
        title: 'Implement Core API',
        description: 'Create basic REST endpoints for agent management',
        status: 'in_progress',
        priority: 'high',
        due_date: '2026-04-20',
      },
      {
        id: 'task_003',
        title: 'Design User Interface',
        description: 'Create intuitive dashboard for agent monitoring',
        status: 'pending',
        priority: 'medium',
        due_date: '2026-04-25',
      },
    ];
    
    return new Response(JSON.stringify({ tasks }, null, 2), {
      headers: {
        'Content-Type': 'application/json',
        ...corsHeaders,
      },
    });
  }
  
  // 404 - API 端点不存在
  return new Response(JSON.stringify({
    error: 'API endpoint not found',
    available_endpoints: [
      '/api/health',
      '/api/status',
      '/api/agents',
      '/api/learning',
      '/api/tasks',
    ],
  }, null, 2), {
    status: 404,
    headers: {
      'Content-Type': 'application/json',
      ...corsHeaders,
    },
  });
}