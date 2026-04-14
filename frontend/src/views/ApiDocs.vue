<template>
  <div class="api-docs">
    <!-- 页面头部 -->
    <div class="docs-header">
      <div class="header-content">
        <h1 class="docs-title">
          <i class="header-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="16" y1="13" x2="8" y2="13"></line>
              <line x1="16" y1="17" x2="8" y2="17"></line>
              <polyline points="10 9 9 9 8 9"></polyline>
            </svg>
          </i>
          API 文档
        </h1>
        <p class="docs-subtitle">
          Agent Learning Platform 后端API完整文档，基于FastAPI自动生成
        </p>
      </div>
      
      <div class="header-actions">
        <el-button type="primary" @click="openSwaggerUI">
          <template #icon>
            <i class="action-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                <polyline points="15 3 21 3 21 9"></polyline>
                <line x1="10" y1="14" x2="21" y2="3"></line>
              </svg>
            </i>
          </template>
          打开 Swagger UI
        </el-button>
        
        <el-button @click="openReDoc">
          <template #icon>
            <i class="action-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
                <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
              </svg>
            </i>
          </template>
          打开 ReDoc
        </el-button>
        
        <el-button @click="copyApiUrl" :disabled="copyLoading">
          <template #icon>
            <i class="action-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
              </svg>
            </i>
          </template>
          {{ copyLoading ? '已复制' : '复制API地址' }}
        </el-button>
      </div>
    </div>

    <!-- API状态卡片 -->
    <div class="status-cards">
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="status-card" shadow="hover">
            <div class="card-content">
              <div class="card-icon success">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                  <polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
              </div>
              <div class="card-info">
                <h3 class="card-title">API状态</h3>
                <p class="card-value">{{ apiStatus }}</p>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="status-card" shadow="hover">
            <div class="card-content">
              <div class="card-icon primary">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                  <circle cx="9" cy="7" r="4"></circle>
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                  <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                </svg>
              </div>
              <div class="card-info">
                <h3 class="card-title">端点数量</h3>
                <p class="card-value">{{ endpoints.length }}</p>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="status-card" shadow="hover">
            <div class="card-content">
              <div class="card-icon warning">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" y1="8" x2="12" y2="12"></line>
                  <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
              </div>
              <div class="card-info">
                <h3 class="card-title">版本</h3>
                <p class="card-value">{{ apiVersion }}</p>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="status-card" shadow="hover">
            <div class="card-content">
              <div class="card-icon info">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
                </svg>
              </div>
              <div class="card-info">
                <h3 class="card-title">响应时间</h3>
                <p class="card-value">{{ responseTime }}ms</p>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- API端点列表 -->
    <div class="endpoints-section">
      <div class="section-header">
        <h2 class="section-title">
          <i class="section-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
            </svg>
          </i>
          API 端点
        </h2>
        <div class="section-actions">
          <el-input
            v-model="searchQuery"
            placeholder="搜索端点..."
            clearable
            class="search-input"
            @input="filterEndpoints"
          >
            <template #prefix>
              <el-icon>
                <Search />
              </el-icon>
            </template>
          </el-input>
          
          <el-select
            v-model="selectedCategory"
            placeholder="筛选分类"
            clearable
            class="category-select"
            @change="filterEndpoints"
          >
            <el-option label="全部" value="all" />
            <el-option label="认证" value="auth" />
            <el-option label="项目" value="projects" />
            <el-option label="系统" value="system" />
          </el-select>
        </div>
      </div>

      <div class="endpoints-list">
        <el-table
          :data="filteredEndpoints"
          style="width: 100%"
          :row-class-name="tableRowClassName"
          @row-click="handleRowClick"
        >
          <el-table-column prop="method" label="方法" width="100">
            <template #default="scope">
              <el-tag
                :type="getMethodType(scope.row.method)"
                effect="dark"
                class="method-tag"
              >
                {{ scope.row.method }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column prop="path" label="路径">
            <template #default="scope">
              <code class="path-code">{{ scope.row.path }}</code>
            </template>
          </el-table-column>
          
          <el-table-column prop="name" label="名称" width="200" />
          
          <el-table-column prop="category" label="分类" width="120">
            <template #default="scope">
              <el-tag
                :type="getCategoryType(scope.row.category)"
                size="small"
              >
                {{ scope.row.category }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column prop="requiresAuth" label="认证" width="80">
            <template #default="scope">
              <el-tag
                v-if="scope.row.requiresAuth"
                type="danger"
                size="small"
              >
                需要
              </el-tag>
              <el-tag
                v-else
                type="success"
                size="small"
              >
                公开
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column label="操作" width="120">
            <template #default="scope">
              <el-button
                type="primary"
                link
                @click.stop="testEndpoint(scope.row)"
              >
                测试
              </el-button>
              <el-button
                type="info"
                link
                @click.stop="viewDetails(scope.row)"
              >
                详情
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>

    <!-- API测试面板 -->
    <div class="test-panel" v-if="selectedEndpoint">
      <div class="panel-header">
        <h3 class="panel-title">
          <i class="panel-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="16 18 22 12 16 6"></polyline>
              <polyline points="8 6 2 12 8 18"></polyline>
            </svg>
          </i>
          测试端点: {{ selectedEndpoint.name }}
        </h3>
        <el-button type="text" @click="selectedEndpoint = null">
          关闭
        </el-button>
      </div>
      
      <div class="panel-content">
        <div class="endpoint-info">
          <div class="info-row">
            <span class="info-label">方法:</span>
            <el-tag :type="getMethodType(selectedEndpoint.method)" effect="dark">
              {{ selectedEndpoint.method }}
            </el-tag>
          </div>
          <div class="info-row">
            <span class="info-label">路径:</span>
            <code class="full-path">{{ apiBaseUrl }}{{ selectedEndpoint.path }}</code>
          </div>
          <div class="info-row">
            <span class="info-label">描述:</span>
            <span class="info-value">{{ selectedEndpoint.description }}</span>
          </div>
        </div>
        
        <div class="test-form">
          <h4 class="form-title">请求参数</h4>
          <el-form
            ref="testFormRef"
            :model="testForm"
            label-width="100px"
            class="demo-form"
          >
            <el-form-item
              v-for="param in selectedEndpoint.parameters"
              :key="param.name"
              :label="param.name"
              :prop="param.name"
            >
              <el-input
                v-model="testForm[param.name]"
                :placeholder="`请输入${param.name} (${param.type})`"
                clearable
              />
              <span class="param-hint">{{ param.description }}</span>
            </el-form-item>
            
            <el-form-item>
              <el-button
                type="primary"
                :loading="testing"
                @click="sendTestRequest"
              >
                发送请求
              </el-button>
              <el-button @click="resetTestForm">
                重置
              </el-button>
            </el-form-item>
          </el-form>
        </div>
        
        <div class="response-section" v-if="testResponse">
          <h4 class="response-title">响应结果</h4>
          <div class="response-info">
            <div class="response-status">
              <span class="status-label">状态码:</span>
              <el-tag :type="testResponse.status >= 400 ? 'danger' : 'success'">
                {{ testResponse.status }}
              </el-tag>
            </div>
            <div class="response-time">
              <span class="time-label">响应时间:</span>
              <span class="time-value">{{ testResponse.time }}ms</span>
            </div>
          </div>
          
          <div class="response-content">
            <el-tabs v-model="responseView" class="response-tabs">
              <el-tab-pane label="格式化" name="formatted">
                <pre class="response-pre">{{ formattedResponse }}</pre>
              </el-tab-pane>
              <el-tab-pane label="原始数据" name="raw">
                <pre class="response-pre">{{ rawResponse }}</pre>
              </el-tab-pane>
            </el-tabs>
          </div>
        </div>
      </div>
    </div>

    <!-- 快速链接 -->
    <div class="quick-links">
      <h3 class="links-title">快速链接</h3>
      <div class="links-grid">
        <el-card
          v-for="link in quickLinks"
          :key="link.title"
          class="link-card"
          shadow="hover"
          @click="openLink(link.url)"
        >
          <div class="link-content">
            <div class="link-icon" :class="link.type">
              <component :is="link.icon" />
            </div>
            <div class="link-info">
              <h4 class="link-title">{{ link.title }}</h4>
              <p class="link-desc">{{ link.description }}</p>
            </div>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import type { FormInstance } from 'element-plus'

// API配置 - 使用相对路径通过Vite代理
const apiBaseUrl = import.meta.env.DEV ? '' : (import.meta.env.VITE_API_BASE_URL || '/api')

// 响应式数据
const apiStatus = ref('检查中...')
const apiVersion = ref('1.0.0')
const responseTime = ref(0)
const copyLoading = ref(false)
const searchQuery = ref('')
const selectedCategory = ref('all')
const selectedEndpoint = ref<any>(null)
const testing = ref(false)
const testResponse = ref<any>(null)
const responseView = ref('formatted')

// API端点数据
const endpoints = ref([
  {
    method: 'GET',
    path: '/',
    name: '根端点',
    category: 'system',
    description: '获取系统基本信息',
    requiresAuth: false,
    parameters: []
  },
  {
    method: 'GET',
    path: '/health',
    name: '健康检查',
    category: 'system',
    description: '检查API服务健康状态',
    requiresAuth: false,
    parameters: []
  },
  {
    method: 'GET',
    path: '/info',
    name: '应用信息',
    category: 'system',
    description: '获取应用详细信息',
    requiresAuth: false,
    parameters: []
  },
  {
    method: 'POST',
    path: '/api/v1/auth/test',
    name: '认证测试',
    category: 'auth',
    description: '测试认证API功能',
    requiresAuth: false,
    parameters: []
  },
  {
    method: 'GET',
    path: '/api/v1/projects',
    name: '项目列表',
    category: 'projects',
    description: '获取所有项目列表',
    requiresAuth: true,
    parameters: []
  },
  {
    method: 'GET',
    path: '/docs',
    name: 'Swagger UI',
    category: 'system',
    description: 'Swagger API文档界面',
    requiresAuth: false,
    parameters: []
  },
  {
    method: 'GET',
    path: '/redoc',
    name: 'ReDoc',
    category: 'system',
    description: 'ReDoc API文档界面',
    requiresAuth: false,
    parameters: []
  }
])

// 测试表单
const testForm = ref<Record<string, string>>({})
const testFormRef = ref<FormInstance>()

// 快速链接
const quickLinks = ref([
  {
    title: 'Swagger UI',
    description: '交互式API文档和测试工具',
    url: `/api/docs`,
    type: 'primary',
    icon: 'Document'
  },
  {
    title: 'ReDoc',
    description: '美观的API文档展示',
    url: `/api/redoc`,
    type: 'success',
    icon: 'Reading'
  },
  {
    title: '健康检查',
    description: '检查API服务状态',
    url: `/api/health`,
    type: 'warning',
    icon: 'Monitor'
  },
  {
    title: '应用信息',
    description: '查看应用版本和功能',
    url: `/api/info`,
    type: 'info',
    icon: 'InfoFilled'
  }
])

// 计算属性
const filteredEndpoints = computed(() => {
  let filtered = endpoints.value
  
  // 搜索过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(endpoint =>
      endpoint.name.toLowerCase().includes(query) ||
      endpoint.path.toLowerCase().includes(query) ||
      endpoint.description.toLowerCase().includes(query)
    )
  }
  
  // 分类过滤
  if (selectedCategory.value && selectedCategory.value !== 'all') {
    filtered = filtered.filter(endpoint => endpoint.category === selectedCategory.value)
  }
  
  return filtered
})

const formattedResponse = computed(() => {
  if (!testResponse.value) return ''
  try {
    return JSON.stringify(testResponse.value.data, null, 2)
  } catch {
    return testResponse.value.data
  }
})

const rawResponse = computed(() => {
  if (!testResponse.value) return ''
  return JSON.stringify(testResponse.value, null, 2)
})

// 方法
const getMethodType = (method: string) => {
  const types: Record<string, string> = {
    GET: 'success',
    POST: 'primary',
    PUT: 'warning',
    DELETE: 'danger',
    PATCH: 'info'
  }
  return types[method] || 'default'
}

const getCategoryType = (category: string) => {
  const types: Record<string, string> = {
    auth: 'danger',
    projects: 'primary',
    system: 'info',
    learning: 'success'
  }
  return types[category] || 'default'
}

const tableRowClassName = ({ row }: { row: any }) => {
  return row.requiresAuth ? 'auth-required-row' : ''
}

const handleRowClick = (row: any) => {
  selectedEndpoint.value = row
  // 初始化测试表单
  testForm.value = {}
  testResponse.value = null
}

const openSwaggerUI = () => {
  window.open(`/api/docs`, '_blank')
}

const openReDoc = () => {
  window.open(`/api/redoc`, '_blank')
}

const copyApiUrl = async () => {
  try {
    await navigator.clipboard.writeText(apiBaseUrl)
    copyLoading.value = true
    ElMessage.success('API地址已复制到剪贴板')
    setTimeout(() => {
      copyLoading.value = false
    }, 2000)
  } catch (err) {
    ElMessage.error('复制失败，请手动复制')
  }
}

const testEndpoint = (endpoint: any) => {
  selectedEndpoint.value = endpoint
  testForm.value = {}
  testResponse.value = null
}

const viewDetails = (endpoint: any) => {
  ElMessageBox.alert(
    `<div style="text-align: left;">
      <h3 style="margin-top: 0;">${endpoint.name}</h3>
      <p><strong>路径:</strong> <code>${apiBaseUrl}${endpoint.path}</code></p>
      <p><strong>方法:</strong> <span style="color: var(--el-color-primary)">${endpoint.method}</span></p>
      <p><strong>描述:</strong> ${endpoint.description}</p>
      <p><strong>认证:</strong> ${endpoint.requiresAuth ? '需要认证' : '公开访问'}</p>
      <p><strong>分类:</strong> ${endpoint.category}</p>
    </div>`,
    '端点详情',
    {
      dangerouslyUseHTMLString: true,
      confirmButtonText: '关闭'
    }
  )
}

const sendTestRequest = async () => {
  if (!selectedEndpoint.value) return
  
  testing.value = true
  testResponse.value = null
  
  try {
    const startTime = Date.now()
    
    // 构建请求URL
    let url = `${apiBaseUrl}${selectedEndpoint.value.path}`
    
    // 构建请求配置
    const config: RequestInit = {
      method: selectedEndpoint.value.method,
      headers: {
        'Content-Type': 'application/json'
      }
    }
    
    // 如果是需要认证的端点，添加token
    if (selectedEndpoint.value.requiresAuth) {
      const token = localStorage.getItem('token')
      if (token) {
        config.headers = {
          ...config.headers,
          'Authorization': `Bearer ${token}`
        }
      } else {
        ElMessage.warning('此端点需要认证，请先登录')
        testing.value = false
        return
      }
    }
    
    // 如果是POST/PUT/PATCH请求，添加请求体
    if (['POST', 'PUT', 'PATCH'].includes(selectedEndpoint.value.method)) {
      config.body = JSON.stringify(testForm.value)
    }
    
    // 发送请求
    const response = await fetch(url, config)
    const endTime = Date.now()
    
    const data = await response.json().catch(() => ({ error: '响应不是有效的JSON' }))
    
    testResponse.value = {
      status: response.status,
      statusText: response.statusText,
      time: endTime - startTime,
      data: data,
      headers: Object.fromEntries(response.headers.entries())
    }
    
    if (response.ok) {
      ElMessage.success('请求成功')
    } else {
      ElMessage.error(`请求失败: ${response.status} ${response.statusText}`)
    }
  } catch (error: any) {
    ElMessage.error(`请求错误: ${error.message}`)
    testResponse.value = {
      status: 0,
      statusText: 'Network Error',
      time: 0,
      data: { error: error.message },
      headers: {}
    }
  } finally {
    testing.value = false
  }
}

const resetTestForm = () => {
  if (testFormRef.value) {
    testFormRef.value.resetFields()
  }
  testResponse.value = null
}

const filterEndpoints = () => {
  // 搜索和过滤逻辑已在计算属性中处理
}

const openLink = (url: string) => {
  window.open(url, '_blank')
}

const checkApiStatus = async () => {
  try {
    const startTime = Date.now()
    const response = await fetch(`/api/health`)
    const endTime = Date.now()
    
    responseTime.value = endTime - startTime
    
    if (response.ok) {
      const data = await response.json()
      apiStatus.value = '运行正常'
      apiVersion.value = data.version || '1.0.0'
    } else {
      apiStatus.value = '运行异常'
    }
  } catch (error) {
    apiStatus.value = '无法连接'
    responseTime.value = 0
  }
}

// 生命周期
onMounted(() => {
  checkApiStatus()
  
  // 每30秒检查一次API状态
  setInterval(checkApiStatus, 30000)
})
</script>

<style scoped lang="scss">

.api-docs {
  position: relative;
  z-index: 1;
  margin: 40px auto 40px auto;
  max-width: 980px;
  border-radius: 22px;
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.10), 0 1.5px 8px 0 rgba(31,38,135,0.04);
  background: rgba(255,255,255,0.55);
  color: var(--el-text-color-primary);
  padding: 40px 36px 36px 36px;
  overflow: hidden;
  min-height: 80vh;
  transition: background 0.3s, color 0.3s;
}
.api-docs::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;
  border-radius: 18px;
  background: linear-gradient(180deg, rgba(255,255,255,0.18) 60%, rgba(255,255,255,0.32) 100%);
  backdrop-filter: blur(18px) saturate(1.2);
  -webkit-backdrop-filter: blur(18px) saturate(1.2);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.12);
  transition: background 0.3s;
}
.api-docs > * {
  position: relative;
  z-index: 1;
}

[data-theme='dark'] .api-docs {
  background: rgba(30,32,38,0.72);
  color: #f3f6fa;
  box-shadow: 0 8px 32px 0 rgba(0,0,0,0.32), 0 1.5px 8px 0 rgba(0,0,0,0.10);
}
[data-theme='dark'] .api-docs::before {
  background: linear-gradient(180deg, rgba(30,32,38,0.44) 60%, rgba(30,32,38,0.82) 100%);
  box-shadow: 0 8px 32px 0 rgba(0,0,0,0.22);
}

.docs-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--el-border-color-light);
  
  .header-content {
    flex: 1;
    
    .docs-title {
      font-size: 32px;
      font-weight: 700;
      margin: 0 0 8px 0;
      display: flex;
      align-items: center;
      gap: 12px;
      color: var(--el-text-color-primary);
      
      .header-icon {
        display: flex;
        align-items: center;
        color: var(--el-color-primary);
      }
    }
    
    .docs-subtitle {
      font-size: 16px;
      color: var(--el-text-color-secondary);
      margin: 0;
      line-height: 1.5;
    }
  }
  
  .header-actions {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    
    .action-icon {
      display: flex;
      align-items: center;
    }
  }
}

.status-cards {
  margin-bottom: 32px;
  
  .status-card {
    height: 100%;
    
    .card-content {
      display: flex;
      align-items: center;
      gap: 16px;
      
      .card-icon {
        width: 56px;
        height: 56px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        
        &.success {
          background-color: rgba(var(--el-color-success-rgb), 0.1);
          color: var(--el-color-success);
        }
        
        &.primary {
          background-color: rgba(var(--el-color-primary-rgb), 0.1);
          color: var(--el-color-primary);
        }
        
        &.warning {
          background-color: rgba(var(--el-color-warning-rgb), 0.1);
          color: var(--el-color-warning);
        }
        
        &.info {
          background-color: rgba(var(--el-color-info-rgb), 0.1);
          color: var(--el-color-info);
        }
      }
      
      .card-info {
        flex: 1;
        
        .card-title {
          font-size: 14px;
          color: var(--el-text-color-secondary);
          margin: 0 0 4px 0;
          font-weight: 500;
        }
        
        .card-value {
          font-size: 24px;
          font-weight: 700;
          margin: 0;
          color: var(--el-text-color-primary);
        }
      }
    }
  }
}

.endpoints-section {
  margin-bottom: 32px;
  
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    
    .section-title {
      font-size: 20px;
      font-weight: 600;
      margin: 0;
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--el-text-color-primary);
      
      .section-icon {
        display: flex;
        align-items: center;
        color: var(--el-color-primary);
      }
    }
    
    .section-actions {
      display: flex;
      gap: 12px;
      
      .search-input {
        width: 200px;
      }
      
      .category-select {
        width: 150px;
      }
    }
  }
  
  .endpoints-list {
    :deep(.auth-required-row) {
      background-color: rgba(var(--el-color-danger-rgb), 0.05);
      
      &:hover {
        background-color: rgba(var(--el-color-danger-rgb), 0.1) !important;
      }
    }
    
    .method-tag {
      font-weight: 600;
      min-width: 60px;
      text-align: center;
    }
    
    .path-code {
      font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
      font-size: 13px;
      color: var(--el-text-color-primary);
      background-color: var(--el-fill-color-light);
      padding: 2px 6px;
      border-radius: 4px;
    }
  }
}

.test-panel {
  background-color: var(--el-bg-color);
  border-radius: 12px;
  border: 1px solid var(--el-border-color-light);
  margin-bottom: 32px;
  overflow: hidden;
  
  .panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 24px;
    background-color: var(--el-fill-color-light);
    border-bottom: 1px solid var(--el-border-color-light);
    
    .panel-title {
      font-size: 18px;
      font-weight: 600;
      margin: 0;
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--el-text-color-primary);
      
      .panel-icon {
        display: flex;
        align-items: center;
        color: var(--el-color-primary);
      }
    }
  }
  
  .panel-content {
    padding: 24px;
    
    .endpoint-info {
      background-color: var(--el-fill-color-lighter);
      border-radius: 8px;
      padding: 20px;
      margin-bottom: 24px;
      
      .info-row {
        display: flex;
        align-items: center;
        margin-bottom: 12px;
        
        &:last-child {
          margin-bottom: 0;
        }
        
        .info-label {
          font-weight: 600;
          color: var(--el-text-color-secondary);
          min-width: 80px;
        }
        
        .info-value {
          color: var(--el-text-color-primary);
          flex: 1;
        }
        
        .full-path {
          font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
          font-size: 14px;
          color: var(--el-color-primary);
          background-color: var(--el-fill-color-light);
          padding: 4px 8px;
          border-radius: 4px;
        }
      }
    }
    
    .test-form {
      .form-title {
        font-size: 16px;
        font-weight: 600;
        margin: 0 0 20px 0;
        color: var(--el-text-color-primary);
      }
      
      .demo-form {
        .param-hint {
          font-size: 12px;
          color: var(--el-text-color-placeholder);
          margin-top: 4px;
          display: block;
        }
      }
    }
    
    .response-section {
      margin-top: 32px;
      
      .response-title {
        font-size: 16px;
        font-weight: 600;
        margin: 0 0 16px 0;
        color: var(--el-text-color-primary);
      }
      
      .response-info {
        display: flex;
        gap: 24px;
        margin-bottom: 16px;
        
        .response-status,
        .response-time {
          display: flex;
          align-items: center;
          gap: 8px;
          
          .status-label,
          .time-label {
            font-weight: 600;
            color: var(--el-text-color-secondary);
          }
          
          .time-value {
            color: var(--el-text-color-primary);
            font-weight: 500;
          }
        }
      }
      
      .response-content {
        .response-tabs {
          :deep(.el-tabs__header) {
            margin: 0;
          }
          
          .response-pre {
            margin: 0;
            padding: 16px;
            background-color: var(--el-fill-color-lighter);
            border-radius: 8px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 13px;
            line-height: 1.5;
            color: var(--el-text-color-primary);
            max-height: 400px;
            overflow: auto;
            
            &::-webkit-scrollbar {
              width: 8px;
              height: 8px;
            }
            
            &::-webkit-scrollbar-track {
              background: var(--el-fill-color-light);
              border-radius: 4px;
            }
            
            &::-webkit-scrollbar-thumb {
              background: var(--el-border-color);
              border-radius: 4px;
              
              &:hover {
                background: var(--el-border-color-dark);
              }
            }
          }
        }
      }
    }
  }
}

.quick-links {
  .links-title {
    font-size: 20px;
    font-weight: 600;
    margin: 0 0 20px 0;
    color: var(--el-text-color-primary);
  }
  
  .links-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
    
    .link-card {
      cursor: pointer;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
      
      &:hover {
        transform: translateY(-4px);
        box-shadow: var(--el-box-shadow-dark);
      }
      
      .link-content {
        display: flex;
        align-items: center;
        gap: 16px;
        
        .link-icon {
          width: 48px;
          height: 48px;
          border-radius: 12px;
          display: flex;
          align-items: center;
          justify-content: center;
          
          &.primary {
            background-color: rgba(var(--el-color-primary-rgb), 0.1);
            color: var(--el-color-primary);
          }
          
          &.success {
            background-color: rgba(var(--el-color-success-rgb), 0.1);
            color: var(--el-color-success);
          }
          
          &.warning {
            background-color: rgba(var(--el-color-warning-rgb), 0.1);
            color: var(--el-color-warning);
          }
          
          &.info {
            background-color: rgba(var(--el-color-info-rgb), 0.1);
            color: var(--el-color-info);
          }
        }
        
        .link-info {
          flex: 1;
          
          .link-title {
            font-size: 16px;
            font-weight: 600;
            margin: 0 0 4px 0;
            color: var(--el-text-color-primary);
          }
          
          .link-desc {
            font-size: 13px;
            color: var(--el-text-color-secondary);
            margin: 0;
            line-height: 1.4;
          }
        }
      }
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .api-docs {
    padding: 16px;
  }
  
  .docs-header {
    flex-direction: column;
    gap: 16px;
    
    .header-actions {
      width: 100%;
      justify-content: flex-start;
    }
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start !important;
    gap: 12px;
    
    .section-actions {
      width: 100%;
      
      .search-input {
        flex: 1;
      }
    }
  }
  
  .links-grid {
    grid-template-columns: 1fr !important;
  }
  
  .status-cards {
    .el-col {
      margin-bottom: 16px;
      
      &:last-child {
        margin-bottom: 0;
      }
    }
  }
}

// 动画效果
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

// 自定义滚动条
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

::-webkit-scrollbar-track {
  background: var(--el-fill-color-light);
  border-radius: 5px;
}

::-webkit-scrollbar-thumb {
  background: var(--el-border-color);
  border-radius: 5px;
  
  &:hover {
    background: var(--el-border-color-dark);
  }
}
</style>
