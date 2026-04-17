<template>
  <div class="projects-page">
    <!-- 页面标题和操作栏 -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <FolderKanban class="title-icon" />
            项目管理
          </h1>
          <p class="page-subtitle">
            管理你的AI Agent项目，跟踪进度，协作开发
          </p>
        </div>
        <div class="action-buttons">
          <el-button type="primary" :icon="Plus" @click="createNewProject">
            新建项目
          </el-button>
          <el-button :icon="RefreshCw" @click="refreshProjects">
            刷新列表
          </el-button>
          <el-button :icon="Filter" @click="showFilter = !showFilter">
            筛选
          </el-button>
        </div>
      </div>
    </div>

    <!-- 筛选面板 -->
    <div v-if="showFilter" class="filter-panel">
      <div class="filter-content">
        <div class="filter-row">
          <div class="filter-item">
            <span class="filter-label">项目状态</span>
            <el-select v-model="filterStatus" placeholder="选择状态" clearable>
              <el-option label="进行中" value="active" />
              <el-option label="已完成" value="completed" />
              <el-option label="已归档" value="archived" />
            </el-select>
          </div>
          <div class="filter-item">
            <span class="filter-label">可见性</span>
            <el-select v-model="filterVisibility" placeholder="选择可见性" clearable>
              <el-option label="公开" value="public" />
              <el-option label="私有" value="private" />
            </el-select>
          </div>
          <div class="filter-item">
            <span class="filter-label">排序方式</span>
            <el-select v-model="sortBy" placeholder="选择排序">
              <el-option label="创建时间" value="created_at" />
              <el-option label="更新时间" value="updated_at" />
              <el-option label="项目名称" value="name" />
            </el-select>
          </div>
        </div>
        <div class="filter-actions">
          <el-button @click="clearFilters">清空筛选</el-button>
          <el-button type="primary" @click="applyFilters">应用筛选</el-button>
        </div>
      </div>
    </div>

    <!-- 项目统计 -->
    <div class="projects-stats">
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #3b82f6, #06b6d4);">
          <FolderKanban class="icon" />
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.total }}</div>
          <div class="stat-label">总项目数</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #10b981, #14b8a6);">
          <Play class="icon" />
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.active }}</div>
          <div class="stat-label">进行中</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #f59e0b, #f97316);">
          <Users class="icon" />
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.collaborators }}</div>
          <div class="stat-label">协作者</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #8b5cf6, #a855f7);">
          <Calendar class="icon" />
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.dueSoon }}</div>
          <div class="stat-label">即将到期</div>
        </div>
      </div>
    </div>

    <!-- 项目列表 -->
    <div class="projects-list">
      <div class="list-header">
        <h3 class="list-title">我的项目</h3>
        <div class="view-controls">
          <el-button-group>
            <el-button :icon="Grid" :type="viewMode === 'grid' ? 'primary' : 'default'" @click="viewMode = 'grid'">
              网格视图
            </el-button>
            <el-button :icon="List" :type="viewMode === 'list' ? 'primary' : 'default'" @click="viewMode = 'list'">
              列表视图
            </el-button>
          </el-button-group>
        </div>
      </div>

      <!-- 网格视图 -->
      <div v-if="viewMode === 'grid'" class="projects-grid">
        <div
          v-for="project in filteredProjects"
          :key="project.id"
          class="project-card"
          @click="viewProject(project)"
        >
          <div class="project-card-header">
            <div class="project-icon">
              <FolderKanban class="icon" />
            </div>
            <div class="project-info">
              <h4 class="project-name">{{ project.name }}</h4>
              <div class="project-meta">
                <span class="project-status" :class="project.status">
                  {{ getStatusText(project.status) }}
                </span>
                <span class="project-visibility" :class="project.is_public ? 'public' : 'private'">
                  {{ project.is_public ? '公开' : '私有' }}
                </span>
              </div>
            </div>
            <el-dropdown trigger="click" @command="handleProjectCommand">
              <button class="project-menu-button">
                <MoreVertical class="menu-icon" />
              </button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item :command="{ action: 'view', project }">
                    <Eye class="dropdown-icon" />查看详情
                  </el-dropdown-item>
                  <el-dropdown-item :command="{ action: 'edit', project }">
                    <Pencil class="dropdown-icon" />编辑项目
                  </el-dropdown-item>
                  <el-dropdown-item :command="{ action: 'archive', project }">
                    <Archive class="dropdown-icon" />归档项目
                  </el-dropdown-item>
                  <el-dropdown-item :command="{ action: 'delete', project }" divided>
                    <Trash2 class="dropdown-icon" />删除项目
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
          <div class="project-description">
            {{ project.description || '暂无描述' }}
          </div>
          <div class="project-stats">
            <div class="stat-item">
              <Users class="stat-icon" />
              <span class="stat-value">{{ project.collaborator_count || 1 }}</span>
            </div>
            <div class="stat-item">
              <CheckCircle class="stat-icon" />
              <span class="stat-value">{{ project.task_completed || 0 }}/{{ project.task_total || 0 }}</span>
            </div>
            <div class="stat-item">
              <Calendar class="stat-icon" />
              <span class="stat-value">{{ formatDate(project.due_date) }}</span>
            </div>
          </div>
          <div class="project-progress">
            <div class="progress-bar">
              <div
                class="progress-fill"
                :style="{ width: `${project.progress || 0}%` }"
                :class="getProgressClass(project.progress || 0)"
              ></div>
            </div>
            <span class="progress-text">{{ project.progress || 0 }}%</span>
          </div>
        </div>

        <div v-if="filteredProjects.length === 0" class="empty-state">
          <FolderKanban class="empty-icon" />
          <p class="empty-text">暂无项目</p>
          <p class="empty-subtext">点击"新建项目"开始创建</p>
        </div>
      </div>

      <!-- 列表视图 -->
      <div v-else class="projects-table">
        <el-table :data="filteredProjects" style="width: 100%">
          <el-table-column prop="name" label="项目名称" width="200">
            <template #default="{ row }">
              <div class="project-name-cell">
                <FolderKanban class="project-icon" />
                <span>{{ row.name }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="description" label="描述" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="getStatusTagType(row.status)" size="small">
                {{ getStatusText(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="progress" label="进度" width="120">
            <template #default="{ row }">
              <div class="progress-cell">
                <div class="progress-bar">
                  <div
                    class="progress-fill"
                    :style="{ width: `${row.progress || 0}%` }"
                    :class="getProgressClass(row.progress || 0)"
                  ></div>
                </div>
                <span class="progress-text">{{ row.progress || 0 }}%</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="due_date" label="截止日期" width="120">
            <template #default="{ row }">
              {{ formatDate(row.due_date) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150">
            <template #default="{ row }">
              <div class="table-actions">
                <el-button size="small" :icon="Eye" @click="viewProject(row)">查看</el-button>
                <el-button size="small" :icon="Pencil" @click="editProject(row)">编辑</el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>

    <!-- 新建/编辑项目对话框 -->
    <el-dialog
      v-model="showProjectDialog"
      :title="isEditing ? '编辑项目' : '新建项目'"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="projectFormRef"
        :model="projectForm"
        :rules="projectRules"
        label-width="100px"
        label-position="top"
      >
        <el-form-item label="项目名称" prop="name">
          <el-input v-model="projectForm.name" placeholder="输入项目名称" />
        </el-form-item>
        <el-form-item label="项目描述" prop="description">
          <el-input
            v-model="projectForm.description"
            type="textarea"
            :rows="3"
            placeholder="描述项目目标和范围"
          />
        </el-form-item>
        <el-form-item label="项目类型" prop="type">
          <el-select v-model="projectForm.type" placeholder="选择项目类型">
            <el-option label="AI Agent开发" value="agent-dev" />
            <el-option label="模型训练" value="model-training" />
            <el-option label="数据标注" value="data-labeling" />
            <el-option label="研究项目" value="research" />
            <el-option label="产品开发" value="product-dev" />
          </el-select>
        </el-form-item>
        <el-form-item label="项目状态" prop="status">
          <el-select v-model="projectForm.status" placeholder="选择项目状态">
            <el-option label="规划中" value="planning" />
            <el-option label="进行中" value="active" />
            <el-option label="测试中" value="testing" />
            <el-option label="已完成" value="completed" />
            <el-option label="已归档" value="archived" />
          </el-select>
        </el-form-item>
        <el-form-item label="截止日期" prop="due_date">
          <el-date-picker
            v-model="projectForm.due_date"
            type="date"
            placeholder="选择截止日期"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item label="项目可见性">
          <el-switch
            v-model="projectForm.is_public"
            active-text="公开"
            inactive-text="私有"
          />
        </el-form-item>
        <el-form-item label="初始进度" prop="progress">
          <el-slider
            v-model="projectForm.progress"
            :min="0"
            :max="100"
            :step="1"
            show-input
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showProjectDialog = false">取消</el-button>
          <el-button type="primary" @click="saveProject">
            {{ isEditing ? '保存' : '创建' }}
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 项目详情对话框 -->
    <el-dialog
      v-model="showProjectDetail"
      :title="selectedProject?.name"
      width="800px"
      :close-on-click-modal="false"
    >
      <div v-if="selectedProject" class="project-detail">
        <div class="detail-header">
          <div class="detail-title-section">
            <h3>{{ selectedProject.name }}</h3>
            <div class="detail-meta">
              <el-tag :type="getStatusTagType(selectedProject.status)" size="small">
                {{ getStatusText(selectedProject.status) }}
              </el-tag>
              <el-tag :type="selectedProject.is_public ? 'success' : 'info'" size="small">
                {{ selectedProject.is_public ? '公开' : '私有' }}
              </el-tag>
              <span class="detail-date">创建于 {{ formatDate(selectedProject.created_at) }}</span>
            </div>
          </div>
          <div class="detail-actions">
            <el-button :icon="Pencil" @click="editProject(selectedProject)">编辑</el-button>
            <el-button :icon="Share2" @click="shareProject(selectedProject)">分享</el-button>
          </div>
        </div>

        <div class="detail-content">
          <div class="detail-section">
            <h4>项目描述</h4>
            <p>{{ selectedProject.description || '暂无描述' }}</p>
          </div>

          <div class="detail-section">
            <h4>项目进度</h4>
            <div class="progress-section">
              <div class="progress-bar-large">
                <div
                  class="progress-fill"
                  :style="{ width: `${selectedProject.progress || 0}%` }"
                  :class="getProgressClass(selectedProject.progress || 0)"
                ></div>
              </div>
              <div class="progress-stats">
                <span class="progress-value">{{ selectedProject.progress || 0 }}%</span>
                <span class="progress-due">截止日期: {{ formatDate(selectedProject.due_date) }}</span>
              </div>
            </div>
          </div>

          <div class="detail-section">
            <h4>项目统计</h4>
            <div class="stats-grid">
              <div class="stat-item">
                <span class="stat-label">任务总数</span>
                <span class="stat-value">{{ selectedProject.task_total || 0 }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">已完成</span>
                <span class="stat-value">{{ selectedProject.task_completed || 0 }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">进行中</span>
                <span class="stat-value">{{ selectedProject.task_in_progress || 0 }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">协作者</span>
                <span class="stat-value">{{ selectedProject.collaborator_count || 1 }}</span>
              </div>
            </div>
          </div>

          <div class="detail-section">
            <h4>最近活动</h4>
            <div class="activity-list">
              <div v-for="activity in selectedProject.recent_activities || []" :key="activity.id" class="activity-item">
                <div class="activity-icon">
                  <component :is="activity.icon" class="icon" />
                </div>
                <div class="activity-content">
                  <p class="activity-text">{{ activity.text }}</p>
                  <span class="activity-time">{{ activity.time }}</span>
                </div>
              </div>
              <div v-if="!selectedProject.recent_activities?.length" class="no-activity">
                暂无活动记录
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import {
  FolderKanban,
  Plus,
  RefreshCw,
  Filter,
  Grid,
  List,
  MoreVertical,
  Eye,
  Pencil,
  Archive,
  Trash2,
  Users,
  Play,
  Calendar,
  CheckCircle,
  Share2
} from 'lucide-vue-next'
import { projectAPI } from '@/utils/api'

// 类型定义
interface Project {
  id: number
  name: string
  description?: string
  type?: string
  status: string
  is_public: boolean
  progress?: number
  due_date?: string
  created_at: string
  updated_at: string
  owner_id: number
  task_total?: number
  task_completed?: number
  task_in_progress?: number
  collaborator_count?: number
  recent_activities?: any[]
}

interface ProjectStats {
  total: number
  active: number
  completed: number
  archived: number
  collaborators: number
  dueSoon: number
}

// 响应式数据
const searchQuery = ref('')
const showFilter = ref(false)
const filterStatus = ref('')
const filterVisibility = ref('')
const sortBy = ref('created_at')
const viewMode = ref('grid')
const projects = ref<Project[]>([])
const selectedProject = ref<Project | null>(null)
const showProjectDialog = ref(false)
const showProjectDetail = ref(false)
const isEditing = ref(false)
const loading = ref(false)

// 统计数据
const stats = ref<ProjectStats>({
  total: 0,
  active: 0,
  completed: 0,
  archived: 0,
  collaborators: 0,
  dueSoon: 0
})

// 表单数据
const projectForm = ref({
  id: 0,
  name: '',
  description: '',
  type: 'agent-dev',
  status: 'planning',
  is_public: false,
  due_date: '',
  progress: 0
})

const projectFormRef = ref<FormInstance>()
const projectRules: FormRules = {
  name: [
    { required: true, message: '请输入项目名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入项目描述', trigger: 'blur' },
    { min: 10, max: 500, message: '长度在 10 到 500 个字符', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择项目类型', trigger: 'change' }
  ],
  status: [
    { required: true, message: '请选择项目状态', trigger: 'change' }
  ]
}

// 计算属性
const filteredProjects = computed(() => {
  let filtered = projects.value
  
  // 状态筛选
  if (filterStatus.value) {
    filtered = filtered.filter(p => p.status === filterStatus.value)
  }
  
  // 可见性筛选
  if (filterVisibility.value) {
    filtered = filtered.filter(p => 
      filterVisibility.value === 'public' ? p.is_public : !p.is_public
    )
  }
  
  // 搜索筛选
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(p => 
      p.name.toLowerCase().includes(query) ||
      p.description?.toLowerCase().includes(query)
    )
  }
  
  // 排序
  filtered = [...filtered].sort((a, b) => {
    if (sortBy.value === 'name') {
      return a.name.localeCompare(b.name)
    } else if (sortBy.value === 'updated_at') {
      return new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime()
    } else {
      return new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    }
  })
  
  return filtered
})

// 方法
const getStatusText = (status: string) => {
  switch (status) {
    case 'planning': return '规划中'
    case 'active': return '进行中'
    case 'testing': return '测试中'
    case 'completed': return '已完成'
    case 'archived': return '已归档'
    default: return '未知'
  }
}

const getStatusTagType = (status: string) => {
  switch (status) {
    case 'planning': return 'info'
    case 'active': return 'success'
    case 'testing': return 'warning'
    case 'completed': return ''
    case 'archived': return 'info'
    default: return 'info'
  }
}

const getProgressClass = (progress: number) => {
  if (progress >= 80) return 'high'
  if (progress >= 50) return 'medium'
  return 'low'
}

const formatDate = (dateString?: string) => {
  if (!dateString) return '未设置'
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

const refreshProjects = async () => {
  try {
    loading.value = true
    const response = await projectAPI.getMyProjects()
    projects.value = response.data
    
    // 更新统计数据
    updateStats()
    
    ElMessage.success('项目列表刷新成功')
  } catch (error) {
    console.error('获取项目列表失败:', error)
    ElMessage.error('获取项目列表失败')
  } finally {
    loading.value = false
  }
}

const updateStats = () => {
  const total = projects.value.length
  const active = projects.value.filter(p => p.status === 'active').length
  const completed = projects.value.filter(p => p.status === 'completed').length
  const archived = projects.value.filter(p => p.status === 'archived').length
  const collaborators = projects.value.reduce((sum, p) => sum + (p.collaborator_count || 1), 0)
  
  // 计算即将到期的项目（7天内）
  const now = new Date()
  const sevenDaysLater = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000)
  const dueSoon = projects.value.filter(p => {
    if (!p.due_date) return false
    const dueDate = new Date(p.due_date)
    return dueDate > now && dueDate <= sevenDaysLater
  }).length
  
  stats.value = { total, active, completed, archived, collaborators, dueSoon }
}

const createNewProject = () => {
  isEditing.value = false
  projectForm.value = {
    id: 0,
    name: '',
    description: '',
    type: 'agent-dev',
    status: 'planning',
    is_public: false,
    due_date: '',
    progress: 0
  }
  showProjectDialog.value = true
}

const editProject = (project: Project) => {
  isEditing.value = true
  projectForm.value = {
    id: project.id,
    name: project.name,
    description: project.description || '',
    type: project.type || 'agent-dev',
    status: project.status,
    is_public: project.is_public,
    due_date: project.due_date || '',
    progress: project.progress || 0
  }
  showProjectDialog.value = true
}

const saveProject = async () => {
  if (!projectFormRef.value) return
  
  try {
    await projectFormRef.value.validate()
    
    const projectData = {
      name: projectForm.value.name,
      description: projectForm.value.description,
      is_public: projectForm.value.is_public
    }
    
    if (isEditing.value) {
      await projectAPI.updateProject(projectForm.value.id, projectData)
      ElMessage.success('项目更新成功')
    } else {
      await projectAPI.createProject(projectData)
      ElMessage.success('项目创建成功')
    }
    
    showProjectDialog.value = false
    await refreshProjects()
  } catch (error) {
    console.error('保存项目失败:', error)
    ElMessage.error('保存项目失败')
  }
}

const viewProject = (project: Project) => {
  selectedProject.value = project
  showProjectDetail.value = true
}

const shareProject = (project: Project) => {
  // 模拟分享功能
  const shareUrl = `${window.location.origin}/project/${project.id}`
  navigator.clipboard.writeText(shareUrl)
  ElMessage.success('项目链接已复制到剪贴板')
}

const handleProjectCommand = (command: { action: string; project: Project }) => {
  switch (command.action) {
    case 'view':
      viewProject(command.project)
      break
    case 'edit':
      editProject(command.project)
      break
    case 'archive':
      archiveProject(command.project)
      break
    case 'delete':
      deleteProject(command.project)
      break
  }
}

const archiveProject = async (project: Project) => {
  try {
    await ElMessageBox.confirm(
      `确定要归档项目 "${project.name}" 吗？归档后项目将只读。`,
      '确认归档',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await projectAPI.updateProject(project.id, { status: 'archived' })
    ElMessage.success('项目已归档')
    await refreshProjects()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('归档项目失败:', error)
      ElMessage.error('归档项目失败')
    }
  }
}

const deleteProject = async (project: Project) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除项目 "${project.name}" 吗？此操作不可恢复。`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await projectAPI.deleteProject(project.id)
    
    if (selectedProject.value?.id === project.id) {
      selectedProject.value = null
      showProjectDetail.value = false
    }
    
    ElMessage.success('项目删除成功')
    await refreshProjects()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除项目失败:', error)
      ElMessage.error('删除项目失败')
    }
  }
}

const applyFilters = () => {
  showFilter.value = false
  ElMessage.info('筛选条件已应用')
}

const clearFilters = () => {
  filterStatus.value = ''
  filterVisibility.value = ''
  sortBy.value = 'created_at'
  ElMessage.info('筛选条件已清空')
}

onMounted(async () => {
  await refreshProjects()
})
</script>

<style scoped lang="scss">
.projects-page {
  min-height: calc(100dvh - var(--header-height));
  background: var(--app-bg);
}

.page-header {
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

.filter-panel {
  padding: 20px 32px;
  border-bottom: 1px solid var(--line-soft);
  background: var(--app-bg-elevated);
}

.filter-content {
  max-width: 800px;
}

.filter-row {
  display: flex;
  gap: 20px;
  margin-bottom: 16px;
}

.filter-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-label {
  font-size: 13px;
  color: var(--text-secondary);
  font-weight: 500;
}

.filter-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.projects-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  padding: 24px 32px;
}

.stat-card {
  background: var(--app-bg-elevated);
  border: 1px solid var(--line-soft);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all 0.2s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stat-icon .icon {
  width: 24px;
  height: 24px;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1;
}

.stat-label {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.projects-list {
  padding: 0 32px 32px;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.list-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.view-controls {
  display: flex;
  gap: 8px;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.project-card {
  background: var(--app-bg-elevated);
  border: 1px solid var(--line-soft);
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    border-color: var(--color-primary);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }
}

.project-card-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 16px;
}

.project-icon {
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

.project-icon .icon {
  width: 20px;
  height: 20px;
}

.project-info {
  flex: 1;
  min-width: 0;
}

.project-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 8px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.project-meta {
  display: flex;
  gap: 8px;
  align-items: center;
}

.project-status {
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 500;

  &.planning {
    background: rgba(59, 130, 246, 0.1);
    color: var(--color-primary);
  }

  &.active {
    background: rgba(34, 197, 94, 0.1);
    color: var(--color-success);
  }

  &.testing {
    background: rgba(245, 158, 11, 0.1);
    color: var(--color-warning);
  }

  &.completed {
    background: rgba(148, 163, 184, 0.1);
    color: var(--text-muted);
  }

  &.archived {
    background: rgba(139, 92, 246, 0.1);
    color: var(--color-accent);
  }
}

.project-visibility {
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 500;

  &.public {
    background: rgba(34, 197, 94, 0.1);
    color: var(--color-success);
  }

  &.private {
    background: rgba(148, 163, 184, 0.1);
    color: var(--text-muted);
  }
}

.project-menu-button {
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 4px;
  border-radius: 6px;
  transition: all 0.2s ease;

  &:hover {
    background: var(--app-bg);
    color: var(--text-primary);
  }
}

.menu-icon {
  width: 16px;
  height: 16px;
}

.project-description {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.project-stats {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--text-secondary);
}

.stat-item .stat-icon {
  width: 14px;
  height: 14px;
  color: var(--text-secondary);
}

.stat-value {
  font-weight: 500;
  color: var(--text-primary);
}

.project-progress {
  display: flex;
  align-items: center;
  gap: 12px;
}

.progress-bar {
  flex: 1;
  height: 6px;
  background: var(--app-bg);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.3s ease;

  &.high {
    background: var(--color-success);
  }

  &.medium {
    background: var(--color-warning);
  }

  &.low {
    background: var(--color-error);
  }
}

.progress-text {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-primary);
  min-width: 40px;
}

.empty-state {
  grid-column: 1 / -1;
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

.projects-table {
  background: var(--app-bg-elevated);
  border: 1px solid var(--line-soft);
  border-radius: 12px;
  overflow: hidden;
}

.project-name-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.project-name-cell .project-icon {
  width: 24px;
  height: 24px;
  border-radius: 6px;
}

.progress-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.table-actions {
  display: flex;
  gap: 8px;
}

.project-detail {
  .detail-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 24px;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--line-soft);
  }

  .detail-title-section h3 {
    font-size: 20px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0 0 12px 0;
  }

  .detail-meta {
    display: flex;
    gap: 8px;
    align-items: center;
  }

  .detail-date {
    font-size: 13px;
    color: var(--text-secondary);
  }

  .detail-actions {
    display: flex;
    gap: 8px;
  }

  .detail-content {
    .detail-section {
      margin-bottom: 24px;

      h4 {
        font-size: 16px;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0 0 12px 0;
      }

      p {
        font-size: 14px;
        color: var(--text-secondary);
        line-height: 1.6;
        margin: 0;
      }
    }
  }

  .progress-section {
    .progress-bar-large {
      height: 8px;
      background: var(--app-bg);
      border-radius: 4px;
      overflow: hidden;
      margin-bottom: 8px;
    }

    .progress-stats {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .progress-value {
      font-size: 16px;
      font-weight: 600;
      color: var(--text-primary);
    }

    .progress-due {
      font-size: 13px;
      color: var(--text-secondary);
    }
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }

  .stat-item {
    background: var(--app-bg);
    border: 1px solid var(--line-soft);
    border-radius: 8px;
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .stat-label {
    font-size: 13px;
    color: var(--text-secondary);
  }

  .stat-value {
    font-size: 18px;
    font-weight: 600;
    color: var(--text-primary);
  }

  .activity-list {
    .activity-item {
      display: flex;
      gap: 12px;
      padding: 12px 0;
      border-bottom: 1px solid var(--line-soft);

      &:last-child {
        border-bottom: none;
      }
    }

    .activity-icon {
      width: 32px;
      height: 32px;
      border-radius: 8px;
      background: var(--app-bg);
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--color-primary);
      flex-shrink: 0;
    }

    .activity-icon .icon {
      width: 16px;
      height: 16px;
    }

    .activity-content {
      flex: 1;
    }

    .activity-text {
      font-size: 14px;
      color: var(--text-primary);
      margin: 0 0 4px 0;
    }

    .activity-time {
      font-size: 12px;
      color: var(--text-secondary);
    }

    .no-activity {
      text-align: center;
      padding: 24px;
      color: var(--text-muted);
      font-size: 14px;
    }
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
  }

  .projects-stats {
    padding: 16px;
    grid-template-columns: repeat(2, 1fr);
  }

  .projects-list {
    padding: 0 16px 16px;
  }

  .list-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .projects-grid {
    grid-template-columns: 1fr;
  }

  .filter-row {
    flex-direction: column;
    gap: 12px;
  }

  .project-detail .detail-header {
    flex-direction: column;
    gap: 16px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
