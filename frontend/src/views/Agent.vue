<template>
  <div class="agent-page">
    <!-- 页面标题和操作栏 -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <Bot class="title-icon" />
            Agent 工作台
          </h1>
          <p class="page-subtitle">
            使用 LangChain 构建和运行智能 Agent，实现自动化任务处理
          </p>
        </div>
        <div class="action-buttons">
          <el-button type="primary" :icon="Plus" @click="createNewAgent">
            新建 Agent
          </el-button>
          <el-button :icon="RefreshCw" @click="refreshAgents">
            刷新列表
          </el-button>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="agent-content">
      <!-- 左侧：Agent 列表 -->
      <div class="agent-list-section">
        <div class="section-header">
          <h3 class="section-title">
            <List class="section-icon" />
            我的 Agent
          </h3>
          <el-input
            v-model="searchQuery"
            placeholder="搜索 Agent..."
            :prefix-icon="Search"
            class="search-input"
            clearable
          />
        </div>

        <div class="agent-list">
          <div
            v-for="agent in filteredAgents"
            :key="agent.id"
            class="agent-card"
            :class="{ active: activeAgent?.id === agent.id }"
            @click="selectAgent(agent)"
          >
            <div class="agent-card-header">
              <div class="agent-icon">
                <Bot class="icon" />
              </div>
              <div class="agent-info">
                <h4 class="agent-name">{{ agent.name }}</h4>
                <div class="agent-meta">
                  <span class="agent-type">{{ agent.type }}</span>
                  <span class="agent-status" :class="agent.status">
                    {{ getStatusText(agent.status) }}
                  </span>
                </div>
              </div>
              <el-dropdown trigger="click" @command="handleAgentCommand">
                <button class="agent-menu-button">
                  <MoreVertical class="menu-icon" />
                </button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item :command="{ action: 'start', agent }">
                      <Play class="dropdown-icon" />启动
                    </el-dropdown-item>
                    <el-dropdown-item :command="{ action: 'stop', agent }">
                      <Square class="dropdown-icon" />停止
                    </el-dropdown-item>
                    <el-dropdown-item :command="{ action: 'edit', agent }">
                      <Pencil class="dropdown-icon" />编辑
                    </el-dropdown-item>
                    <el-dropdown-item :command="{ action: 'delete', agent }" divided>
                      <Trash2 class="dropdown-icon" />删除
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
            <div class="agent-description">
              {{ agent.description }}
            </div>
            <div class="agent-stats">
              <div class="stat-item">
                <span class="stat-label">创建时间</span>
                <span class="stat-value">{{ formatDate(agent.createdAt) }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">运行次数</span>
                <span class="stat-value">{{ agent.runCount }}</span>
              </div>
            </div>
          </div>

          <div v-if="filteredAgents.length === 0" class="empty-state">
            <Bot class="empty-icon" />
            <p class="empty-text">暂无 Agent</p>
            <p class="empty-subtext">点击"新建 Agent"开始创建</p>
          </div>
        </div>
      </div>

      <!-- 右侧：Agent 详情和运行面板 -->
      <div class="agent-detail-section">
        <div v-if="activeAgent" class="detail-panel">
          <!-- Agent 详情 -->
          <div class="detail-header">
            <h3 class="detail-title">{{ activeAgent.name }}</h3>
            <div class="detail-actions">
              <el-button
                v-if="activeAgent.status === 'stopped'"
                type="success"
                :icon="Play"
                @click="startAgent(activeAgent)"
              >
                启动 Agent
              </el-button>
              <el-button
                v-else-if="activeAgent.status === 'running'"
                type="warning"
                :icon="Square"
                @click="stopAgent(activeAgent)"
              >
                停止 Agent
              </el-button>
              <el-button :icon="Pencil" @click="editAgent(activeAgent)">
                编辑
              </el-button>
            </div>
          </div>

          <!-- Agent 状态信息 -->
          <div class="agent-status-info">
            <div class="status-card">
              <div class="status-header">
                <Activity class="status-icon" />
                <span class="status-title">运行状态</span>
              </div>
              <div class="status-content">
                <div class="status-indicator" :class="activeAgent.status">
                  <span class="status-dot"></span>
                  <span class="status-text">
                    {{ getStatusText(activeAgent.status) }}
                  </span>
                </div>
                <div class="status-meta">
                  <div class="meta-item">
                    <span class="meta-label">运行时长</span>
                    <span class="meta-value">{{ activeAgent.uptime || '未运行' }}</span>
                  </div>
                  <div class="meta-item">
                    <span class="meta-label">内存使用</span>
                    <span class="meta-value">{{ activeAgent.memoryUsage || 'N/A' }}</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="status-card">
              <div class="status-header">
                <Cpu class="status-icon" />
                <span class="status-title">模型配置</span>
              </div>
              <div class="status-content">
                <div class="model-info">
                  <span class="model-name">{{ activeAgent.model || '未配置' }}</span>
                  <span class="model-provider">{{ activeAgent.provider || 'OpenAI' }}</span>
                </div>
                <div class="model-meta">
                  <div class="meta-item">
                    <span class="meta-label">温度</span>
                    <span class="meta-value">{{ activeAgent.temperature || 0.7 }}</span>
                  </div>
                  <div class="meta-item">
                    <span class="meta-label">最大令牌</span>
                    <span class="meta-value">{{ activeAgent.maxTokens || 2000 }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Agent 配置 -->
          <div class="agent-config">
            <h4 class="config-title">
              <Settings class="config-icon" />
              Agent 配置
            </h4>
            <div class="config-content">
              <div class="config-item">
                <span class="config-label">Agent 类型</span>
                <span class="config-value">{{ activeAgent.type }}</span>
              </div>
              <div class="config-item">
                <span class="config-label">工具数量</span>
                <span class="config-value">{{ activeAgent.tools?.length || 0 }} 个</span>
              </div>
              <div class="config-item">
                <span class="config-label">记忆系统</span>
                <span class="config-value">{{ activeAgent.memory ? '已启用' : '未启用' }}</span>
              </div>
              <div class="config-item">
                <span class="config-label">描述</span>
                <p class="config-description">{{ activeAgent.description }}</p>
              </div>
            </div>
          </div>

          <!-- 运行控制台 -->
          <div class="agent-console">
            <h4 class="console-title">
              <Terminal class="console-icon" />
              运行控制台
            </h4>
            <div class="console-content">
              <div class="console-input">
                <el-input
                  v-model="consoleInput"
                  placeholder="输入指令或问题..."
                  :prefix-icon="MessageSquare"
                  @keyup.enter="sendToAgent"
                >
                  <template #append>
                    <el-button :icon="Send" @click="sendToAgent" />
                  </template>
                </el-input>
              </div>
              <div class="console-output" ref="consoleOutput">
                <div
                  v-for="(message, index) in consoleMessages"
                  :key="index"
                  class="console-message"
                  :class="message.type"
                >
                  <div class="message-header">
                    <span class="message-sender">{{ message.sender }}</span>
                    <span class="message-time">{{ formatTime(message.timestamp) }}</span>
                  </div>
                  <div class="message-content">{{ message.content }}</div>
                </div>
                <div v-if="consoleMessages.length === 0" class="console-empty">
                  <MessageSquare class="empty-icon" />
                  <p>暂无消息，输入指令开始与 Agent 交互</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="no-agent-selected">
          <Bot class="no-agent-icon" />
          <h3>选择或创建一个 Agent</h3>
          <p>从左侧列表中选择一个 Agent，或点击"新建 Agent"开始创建</p>
        </div>
      </div>
    </div>

    <!-- 新建/编辑 Agent 对话框 -->
    <el-dialog
      v-model="showAgentDialog"
      :title="isEditing ? '编辑 Agent' : '新建 Agent'"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="agentFormRef"
        :model="agentForm"
        :rules="agentRules"
        label-width="100px"
        label-position="top"
      >
        <el-form-item label="Agent 名称" prop="name">
          <el-input v-model="agentForm.name" placeholder="输入 Agent 名称" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="agentForm.description"
            type="textarea"
            :rows="3"
            placeholder="描述 Agent 的功能和用途"
          />
        </el-form-item>
        <el-form-item label="Agent 类型" prop="type">
          <el-select v-model="agentForm.type" placeholder="选择 Agent 类型">
            <el-option label="对话 Agent" value="conversational" />
            <el-option label="工具调用 Agent" value="tool-calling" />
            <el-option label="计划执行 Agent" value="planning" />
            <el-option label="自定义 Agent" value="custom" />
          </el-select>
        </el-form-item>
        <el-form-item label="模型配置" prop="model">
          <el-select v-model="agentForm.model" placeholder="选择模型">
            <el-option label="GPT-4" value="gpt-4" />
            <el-option label="GPT-3.5 Turbo" value="gpt-3.5-turbo" />
            <el-option label="Claude 3" value="claude-3" />
            <el-option label="本地模型" value="local" />
          </el-select>
        </el-form-item>
        <el-form-item label="温度" prop="temperature">
          <el-slider
            v-model="agentForm.temperature"
            :min="0"
            :max="1"
            :step="0.1"
            show-input
          />
        </el-form-item>
        <el-form-item label="启用记忆系统">
          <el-switch v-model="agentForm.memory" />
        </el-form-item>
        <el-form-item label="选择工具">
          <el-checkbox-group v-model="agentForm.tools">
            <el-checkbox label="web-search" value="web-search">网页搜索</el-checkbox>
            <el-checkbox label="calculator" value="calculator">计算器</el-checkbox>
            <el-checkbox label="code-executor" value="code-executor">代码执行</el-checkbox>
            <el-checkbox label="file-reader" value="file-reader">文件读取</el-checkbox>
            <el-checkbox label="database-query" value="database-query">数据库查询</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAgentDialog = false">取消</el-button>
          <el-button type="primary" @click="saveAgent">
            {{ isEditing ? '保存' : '创建' }}
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import {
  Bot,
  Plus,
  RefreshCw,
  List,
  Search,
  MoreVertical,
  Play,
  Square,
  Pencil,
  Trash2,
  Activity,
  Cpu,
  Settings,
  Terminal,
  MessageSquare,
  Send
} from 'lucide-vue-next'
import { agentAPI } from '@/api/index.ts'

// 类型定义
interface Agent {
  id: string
  name: string
  description: string
  type: string
  status: 'running' | 'stopped' | 'error'
  model?: string
  provider?: string
  temperature?: number
  maxTokens?: number
  memory?: boolean
  tools?: string[]
  createdAt: string
  runCount: number
  uptime?: string
  memoryUsage?: string
}

interface ConsoleMessage {
  sender: string
  content: string
  type: 'user' | 'agent' | 'system'
  timestamp: Date
}

// 响应式数据
const searchQuery = ref('')
const activeAgent = ref<Agent | null>(null)
const showAgentDialog = ref(false)
const isEditing = ref(false)
const consoleInput = ref('')
const consoleMessages = ref<ConsoleMessage[]>([])
const consoleOutput = ref<HTMLElement>()

// Agent数据
const agents = ref<Agent[]>([])
const loading = ref(false)

// 表单数据
const agentForm = ref({
  id: '',
  name: '',
  description: '',
  type: 'conversational',
  model: 'gpt-3.5-turbo',
  temperature: 0.7,
  memory: false,
  tools: [] as string[]
})

const agentFormRef = ref<FormInstance>()
const agentRules: FormRules = {
  name: [
    { required: true, message: '请输入 Agent 名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入 Agent 描述', trigger: 'blur' },
    { min: 10, max: 500, message: '长度在 10 到 500 个字符', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择 Agent 类型', trigger: 'change' }
  ],
  model: [
    { required: true, message: '请选择模型', trigger: 'change' }
  ]
}

// 计算属性
const filteredAgents = computed(() => {
  if (!searchQuery.value) return agents.value
  const query = searchQuery.value.toLowerCase()
  return agents.value.filter(agent =>
    agent.name.toLowerCase().includes(query) ||
    agent.description.toLowerCase().includes(query) ||
    agent.type.toLowerCase().includes(query)
  )
})

// 方法
const getStatusText = (status: string) => {
  switch (status) {
    case 'running': return '运行中'
    case 'stopped': return '已停止'
    case 'error': return '错误'
    default: return '未知'
  }
}

const selectAgent = (agent: Agent) => {
  activeAgent.value = agent
  consoleMessages.value = []
  addConsoleMessage('system', '已连接到 Agent: ' + agent.name)
}

const createNewAgent = () => {
  isEditing.value = false
  agentForm.value = {
    id: '',
    name: '',
    description: '',
    type: 'conversational',
    model: 'gpt-3.5-turbo',
    temperature: 0.7,
    memory: false,
    tools: []
  }
  showAgentDialog.value = true
}

const editAgent = (agent: Agent) => {
  isEditing.value = true
  agentForm.value = {
    id: agent.id,
    name: agent.name,
    description: agent.description,
    type: agent.type,
    model: agent.model || 'gpt-3.5-turbo',
    temperature: agent.temperature || 0.7,
    memory: agent.memory || false,
    tools: agent.tools || []
  }
  showAgentDialog.value = true
}

const saveAgent = async () => {
  if (!agentFormRef.value) return
  
  try {
    await agentFormRef.value.validate()
    
    const agentData = {
      name: agentForm.value.name,
      description: agentForm.value.description,
      type: agentForm.value.type,
      model: agentForm.value.model,
      temperature: agentForm.value.temperature,
      max_tokens: 2000,
      memory: agentForm.value.memory,
      tools: agentForm.value.tools,
      system_prompt: `你是一个${agentForm.value.name}，${agentForm.value.description}`
    }
    
    if (isEditing.value) {
      // 更新现有 Agent
      await agentAPI.updateAgent(agentForm.value.id, agentData)
      ElMessage.success('Agent 更新成功')
    } else {
      // 创建新 Agent
      await agentAPI.createAgent(agentData)
      ElMessage.success('Agent 创建成功')
    }
    
    showAgentDialog.value = false
    await refreshAgents()
  } catch (error) {
    console.error('保存 Agent 失败:', error)
    ElMessage.error('保存 Agent 失败')
  }
}

const startAgent = async (agent: Agent) => {
  try {
    await agentAPI.startAgent(agent.id)
    addConsoleMessage('system', 'Agent 已启动')
    ElMessage.success('Agent 启动成功')
    await refreshAgents()
  } catch (error) {
    console.error('启动 Agent 失败:', error)
    ElMessage.error('启动 Agent 失败')
  }
}

const stopAgent = async (agent: Agent) => {
  try {
    await agentAPI.stopAgent(agent.id)
    addConsoleMessage('system', 'Agent 已停止')
    ElMessage.success('Agent 停止成功')
    await refreshAgents()
  } catch (error) {
    console.error('停止 Agent 失败:', error)
    ElMessage.error('停止 Agent 失败')
  }
}

const handleAgentCommand = (command: { action: string; agent: Agent }) => {
  switch (command.action) {
    case 'start':
      startAgent(command.agent)
      break
    case 'stop':
      stopAgent(command.agent)
      break
    case 'edit':
      editAgent(command.agent)
      break
    case 'delete':
      deleteAgent(command.agent)
      break
  }
}

const deleteAgent = async (agent: Agent) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除 Agent "${agent.name}" 吗？此操作不可恢复。`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await agentAPI.deleteAgent(agent.id)
    
    if (activeAgent.value?.id === agent.id) {
      activeAgent.value = null
    }
    
    ElMessage.success('Agent 删除成功')
    await refreshAgents()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除 Agent 失败:', error)
      ElMessage.error('删除 Agent 失败')
    }
  }
}

const refreshAgents = async () => {
  try {
    loading.value = true
    const response = await agentAPI.getAgents()
    agents.value = response.data.map((agent: any) => ({
      id: agent.id,
      name: agent.name,
      description: agent.description,
      type: agent.type,
      status: agent.status,
      model: agent.config?.model || '未配置',
      provider: 'OpenAI',
      temperature: agent.config?.temperature || 0.7,
      maxTokens: agent.config?.max_tokens || 2000,
      memory: agent.config?.memory || false,
      tools: agent.config?.tools || [],
      createdAt: agent.created_at,
      runCount: agent.run_count || 0,
      uptime: agent.uptime,
      memoryUsage: agent.memory_usage
    }))
    
    // 更新当前选中的Agent状态
    if (activeAgent.value) {
      const updatedAgent = agents.value.find(a => a.id === activeAgent.value?.id)
      if (updatedAgent) {
        // 直接更新activeAgent的属性，确保响应式更新
        // Vue 3的ref是响应式的，直接赋值会触发更新
        activeAgent.value = { ...updatedAgent }
      } else {
        // 如果当前选中的Agent不在列表中，清空选择
        activeAgent.value = null
      }
    } else if (agents.value.length > 0) {
      // 如果没有选中的Agent，选择第一个
      selectAgent(agents.value[0])
    }
    
    ElMessage.success('Agent 列表刷新成功')
  } catch (error) {
    console.error('获取 Agent 列表失败:', error)
    ElMessage.error('获取 Agent 列表失败')
  } finally {
    loading.value = false
  }
}

const sendToAgent = async () => {
  if (!consoleInput.value.trim() || !activeAgent.value) return
  
  const userMessage = consoleInput.value.trim()
  addConsoleMessage('user', userMessage)
  consoleInput.value = ''
  
  try {
    const response = await agentAPI.interactWithAgent(activeAgent.value.id, userMessage)
    addConsoleMessage('agent', response.data.response)
  } catch (error) {
    console.error('与 Agent 交互失败:', error)
    addConsoleMessage('system', '与 Agent 交互失败，请检查 Agent 状态')
  }
}

const addConsoleMessage = (type: 'user' | 'agent' | 'system', content: string) => {
  const message: ConsoleMessage = {
    sender: type === 'user' ? '用户' : type === 'agent' ? 'Agent' : '系统',
    content,
    type,
    timestamp: new Date()
  }
  consoleMessages.value.push(message)
  
  // 滚动到底部
  nextTick(() => {
    if (consoleOutput.value) {
      consoleOutput.value.scrollTop = consoleOutput.value.scrollHeight
    }
  })
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

const formatTime = (date: Date) => {
  return date.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

onMounted(async () => {
  await refreshAgents()
})
</script>

<style scoped lang="scss">
.agent-page {
  flex: 1;
  min-height: calc(100dvh - var(--header-height));
  min-width: 0;
  display: flex;
  flex-direction: column;
  background: var(--app-bg);
  overflow: hidden;
}

.page-header {
  flex-shrink: 0;
  padding: 24px 32px;
  border-bottom: 1px solid var(--line-soft);
  background: var(--app-bg-elevated);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 24px;
}

.title-section {
  flex: 1;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 8px 0;
}

.title-icon {
  width: 28px;
  height: 28px;
  color: var(--color-primary);
}

.page-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.5;
}

.action-buttons {
  display: flex;
  gap: 12px;
  flex-shrink: 0;
}

.agent-content {
  display: flex;
  flex: 1;
  min-height: 0;
  min-width: 0;
  overflow: hidden;
}

.agent-list-section {
  width: 320px;
  min-height: 0;
  flex-shrink: 0;
  border-right: 1px solid var(--line-soft);
  display: flex;
  flex-direction: column;
  background: var(--app-bg-elevated);
}

.section-header {
  padding: 20px;
  border-bottom: 1px solid var(--line-soft);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 16px 0;
}

.section-icon {
  width: 18px;
  height: 18px;
  color: var(--color-primary);
}

.search-input {
  width: 100%;
}

.agent-list {
  flex: 1;
  overflow-y: auto;
  overscroll-behavior: contain;
  padding: 16px;
}

.agent-card {
  background: var(--app-bg);
  border: 1px solid var(--line-soft);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    border-color: var(--color-primary);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }

  &.active {
    border-color: var(--color-primary);
    background: rgba(59, 130, 246, 0.05);
  }
}

.agent-card-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
}

.agent-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--color-primary), var(--color-accent));
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.agent-icon .icon {
  width: 20px;
  height: 20px;
}

.agent-info {
  flex: 1;
  min-width: 0;
}

.agent-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 4px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.agent-meta {
  display: flex;
  gap: 8px;
  align-items: center;
}

.agent-type {
  font-size: 11px;
  color: var(--text-muted);
  background: var(--app-bg-elevated);
  padding: 2px 6px;
  border-radius: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.agent-status {
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 500;

  &.running {
    background: rgba(34, 197, 94, 0.1);
    color: var(--color-success);
  }

  &.stopped {
    background: rgba(148, 163, 184, 0.1);
    color: var(--text-muted);
  }

  &.error {
    background: rgba(239, 68, 68, 0.1);
    color: var(--color-error);
  }
}

.agent-menu-button {
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 4px;
  border-radius: 6px;
  transition: all 0.2s ease;

  &:hover {
    background: var(--app-bg-elevated);
    color: var(--text-primary);
  }
}

.menu-icon {
  width: 16px;
  height: 16px;
}

.agent-description {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.agent-stats {
  display: flex;
  gap: 16px;
  font-size: 12px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.stat-label {
  color: var(--text-muted);
}

.stat-value {
  color: var(--text-primary);
  font-weight: 500;
}

.empty-state {
  text-align: center;
  padding: 48px 24px;
  color: var(--text-muted);
}

.empty-icon {
  width: 48px;
  height: 48px;
  margin: 0 auto 16px;
  color: var(--text-muted);
  opacity: 0.5;
}

.empty-text {
  font-size: 16px;
  font-weight: 500;
  margin: 0 0 8px 0;
}

.empty-subtext {
  font-size: 13px;
  margin: 0;
}

.agent-detail-section {
  flex: 1;
  min-width: 0;
  overflow-y: auto;
  overscroll-behavior: contain;
  padding: 24px;
}

.detail-panel {
  max-width: 1200px;
  margin: 0 auto;
}

@media (max-width: 1024px) {
  .agent-content {
    flex-direction: column;
  }

  .agent-list-section {
    width: 100%;
    max-height: 320px;
    border-right: none;
    border-bottom: 1px solid var(--line-soft);
  }
}

@media (max-width: 768px) {
  .page-header {
    padding: 16px;
  }

  .header-content {
    flex-direction: column;
    gap: 16px;
  }

  .action-buttons {
    width: 100%;
    justify-content: flex-start;
    flex-wrap: wrap;
  }

  .agent-detail-section {
    padding: 16px;
  }

  .detail-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .detail-actions {
    width: 100%;
    flex-wrap: wrap;
  }

  .status-meta,
  .model-meta,
  .config-content {
    grid-template-columns: 1fr;
  }
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.detail-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.detail-actions {
  display: flex;
  gap: 12px;
}

.agent-status-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.status-card {
  background: var(--app-bg-elevated);
  border: 1px solid var(--line-soft);
  border-radius: 12px;
  padding: 20px;
}

.status-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.status-icon {
  width: 18px;
  height: 18px;
  color: var(--color-primary);
}

.status-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.status-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;

  &.running .status-dot {
    background: var(--color-success);
    box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.2);
  }

  &.stopped .status-dot {
    background: var(--text-muted);
  }

  &.error .status-dot {
    background: var(--color-error);
    box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.2);
  }
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.status-text {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.status-meta {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.meta-label {
  font-size: 12px;
  color: var(--text-muted);
}

.meta-value {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.model-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.model-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.model-provider {
  font-size: 12px;
  color: var(--text-muted);
  background: var(--app-bg);
  padding: 2px 8px;
  border-radius: 4px;
}

.model-meta {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.agent-config {
  background: var(--app-bg-elevated);
  border: 1px solid var(--line-soft);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
}

.config-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 16px 0;
}

.config-icon {
  width: 18px;
  height: 18px;
  color: var(--color-primary);
}

.config-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.config-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.config-label {
  font-size: 13px;
  color: var(--text-muted);
}

.config-value {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.config-description {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
  margin: 0;
  grid-column: 1 / -1;
}

.agent-console {
  background: var(--app-bg-elevated);
  border: 1px solid var(--line-soft);
  border-radius: 12px;
  padding: 20px;
}

.console-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 16px 0;
}

.console-icon {
  width: 18px;
  height: 18px;
  color: var(--color-primary);
}

.console-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.console-input {
  width: 100%;
}

.console-output {
  height: 300px;
  background: var(--app-bg);
  border: 1px solid var(--line-soft);
  border-radius: 8px;
  padding: 16px;
  overflow-y: auto;
  font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
  font-size: 13px;
}

.console-message {
  margin-bottom: 12px;
  padding: 8px 12px;
  border-radius: 6px;

  &.user {
    background: rgba(59, 130, 246, 0.1);
    border-left: 3px solid var(--color-primary);
  }

  &.agent {
    background: rgba(34, 197, 94, 0.1);
    border-left: 3px solid var(--color-success);
  }

  &.system {
    background: rgba(148, 163, 184, 0.1);
    border-left: 3px solid var(--text-muted);
  }
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.message-sender {
  font-weight: 600;
  color: var(--text-primary);
}

.message-time {
  font-size: 11px;
  color: var(--text-muted);
}

.message-content {
  color: var(--text-secondary);
  line-height: 1.5;
  white-space: pre-wrap;
  word-break: break-word;
}

.console-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--text-muted);
  text-align: center;
}

.console-empty .empty-icon {
  width: 48px;
  height: 48px;
  margin-bottom: 16px;
  opacity: 0.3;
}

.no-agent-selected {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  color: var(--text-muted);
}

.no-agent-icon {
  width: 64px;
  height: 64px;
  margin-bottom: 16px;
  opacity: 0.3;
}

.no-agent-selected h3 {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: var(--text-primary);
}
</style>