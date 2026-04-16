<template>
  <div class="community-page">
    <!-- 页面标题和操作栏 -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <Users class="title-icon" />
            社区动态
          </h1>
          <p class="page-subtitle">
            与BotLearn社区互动交流，分享经验，学习最佳实践
          </p>
        </div>
        <div class="action-buttons">
          <el-button type="primary" :icon="Plus" @click="createNewPost">
            发布动态
          </el-button>
          <el-button :icon="RefreshCw" @click="refreshCommunity">
            刷新
          </el-button>
          <el-button :icon="Bell" @click="showNotifications = !showNotifications">
            通知
          </el-button>
        </div>
      </div>
    </div>

    <!-- 通知面板 -->
    <div v-if="showNotifications" class="notifications-panel">
      <div class="notifications-header">
        <h4>社区通知</h4>
        <el-button size="small" :icon="Check" @click="markAllAsRead">全部已读</el-button>
      </div>
      <div class="notifications-list">
        <div v-for="notification in notifications" :key="notification.id" class="notification-item">
          <div class="notification-icon" :class="notification.type">
            <component :is="notification.icon" class="icon" />
          </div>
          <div class="notification-content">
            <p class="notification-text">{{ notification.text }}</p>
            <span class="notification-time">{{ notification.time }}</span>
          </div>
          <el-button v-if="!notification.read" size="small" :icon="Check" @click="markAsRead(notification)">
            标记已读
          </el-button>
        </div>
        <div v-if="notifications.length === 0" class="no-notifications">
          暂无通知
        </div>
      </div>
    </div>

    <!-- 社区内容 -->
    <div class="community-content">
      <!-- 左侧：社区动态 -->
      <div class="community-feed">
        <div class="feed-header">
          <h3 class="feed-title">最新动态</h3>
          <div class="feed-tabs">
            <el-button-group>
              <el-button :type="activeTab === 'all' ? 'primary' : 'default'" @click="activeTab = 'all'">
                全部
              </el-button>
              <el-button :type="activeTab === 'following' ? 'primary' : 'default'" @click="activeTab = 'following'">
                关注
              </el-button>
              <el-button :type="activeTab === 'popular' ? 'primary' : 'default'" @click="activeTab = 'popular'">
                热门
              </el-button>
            </el-button-group>
          </div>
        </div>

        <!-- 发布动态 -->
        <div class="post-creator">
          <div class="creator-header">
            <el-avatar :size="40" :src="user.avatar" />
            <div class="creator-info">
              <span class="creator-name">{{ user.name }}</span>
              <span class="creator-role">{{ user.role }}</span>
            </div>
          </div>
          <div class="creator-content">
            <el-input
              v-model="newPostContent"
              type="textarea"
              :rows="3"
              placeholder="分享你的想法、经验或问题..."
              maxlength="500"
              show-word-limit
            />
            <div class="creator-actions">
              <div class="action-buttons">
                <el-button :icon="Image">图片</el-button>
                <el-button :icon="FileCode">代码</el-button>
                <el-button :icon="Link">链接</el-button>
              </div>
              <el-button type="primary" :icon="Send" @click="submitPost" :disabled="!newPostContent.trim()">
                发布
              </el-button>
            </div>
          </div>
        </div>

        <!-- 动态列表 -->
        <div class="posts-list">
          <div v-for="post in filteredPosts" :key="post.id" class="post-card">
            <div class="post-header">
              <div class="post-author">
                <el-avatar :size="40" :src="post.author.avatar" />
                <div class="author-info">
                  <span class="author-name">{{ post.author.name }}</span>
                  <span class="author-role">{{ post.author.role }}</span>
                  <span class="post-time">{{ post.time }}</span>
                </div>
              </div>
              <el-dropdown trigger="click">
                <button class="post-menu-button">
                  <MoreVertical class="menu-icon" />
                </button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item :icon="Flag">举报</el-dropdown-item>
                    <el-dropdown-item :icon="BellOff">屏蔽</el-dropdown-item>
                    <el-dropdown-item v-if="post.author.id === user.id" :icon="Trash2">删除</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
            <div class="post-content">
              <p>{{ post.content }}</p>
              <div v-if="post.images && post.images.length > 0" class="post-images">
                <div class="image-grid">
                  <div
                    v-for="(image, index) in post.images"
                    :key="index"
                    class="image-item"
                    :style="{ backgroundImage: `url(${image})` }"
                    @click="viewImage(image)"
                  ></div>
                </div>
              </div>
            </div>
            <div class="post-stats">
              <div class="stat-item" @click="toggleLike(post)">
                <Heart class="stat-icon" :class="{ liked: post.liked }" />
                <span class="stat-value">{{ post.likes }}</span>
              </div>
              <div class="stat-item" @click="showComments(post)">
                <MessageCircle class="stat-icon" />
                <span class="stat-value">{{ post.comments }}</span>
              </div>
              <div class="stat-item">
                <Share2 class="stat-icon" />
                <span class="stat-value">{{ post.shares }}</span>
              </div>
              <div class="stat-item">
                <Eye class="stat-icon" />
                <span class="stat-value">{{ post.views }}</span>
              </div>
            </div>
            <div v-if="post.showComments" class="post-comments">
              <div class="comment-input">
                <el-input
                  v-model="commentInput"
                  placeholder="写下你的评论..."
                  @keyup.enter="submitComment(post)"
                >
                  <template #append>
                    <el-button :icon="Send" @click="submitComment(post)" />
                  </template>
                </el-input>
              </div>
              <div class="comments-list">
                <div v-for="comment in post.commentsList" :key="comment.id" class="comment-item">
                  <el-avatar :size="32" :src="comment.author.avatar" />
                  <div class="comment-content">
                    <div class="comment-header">
                      <span class="comment-author">{{ comment.author.name }}</span>
                      <span class="comment-time">{{ comment.time }}</span>
                    </div>
                    <p class="comment-text">{{ comment.content }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-if="filteredPosts.length === 0" class="empty-state">
            <Users class="empty-icon" />
            <p class="empty-text">暂无动态</p>
            <p class="empty-subtext">成为第一个分享的人吧！</p>
          </div>
        </div>
      </div>

      <!-- 右侧：社区侧边栏 -->
      <div class="community-sidebar">
        <!-- 社区统计 -->
        <div class="sidebar-section">
          <h4>社区统计</h4>
          <div class="stats-grid">
            <div class="stat-card">
              <p class="stat-value-large">{{ communityStats.totalUsers }}</p>
              <p class="stat-label">总用户</p>
            </div>
            <div class="stat-card">
              <p class="stat-value-large">{{ communityStats.todayPosts }}</p>
              <p class="stat-label">今日动态</p>
            </div>
            <div class="stat-card">
              <p class="stat-value-large">{{ communityStats.onlineUsers }}</p>
              <p class="stat-label">在线用户</p>
            </div>
            <div class="stat-card">
              <p class="stat-value-large">{{ communityStats.totalPosts }}</p>
              <p class="stat-label">总动态</p>
            </div>
          </div>
        </div>

        <!-- 热门话题 -->
        <div class="sidebar-section">
          <h4>热门话题</h4>
          <div class="trending-topics">
            <div v-for="topic in trendingTopics" :key="topic.id" class="topic-item">
              <div class="topic-icon">
                <component :is="topic.icon" class="icon" />
              </div>
              <div class="topic-info">
                <p class="topic-name">{{ topic.name }}</p>
                <p class="topic-stats">{{ topic.posts }} 动态 · {{ topic.participants }} 参与</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 活跃用户 -->
        <div class="sidebar-section">
          <h4>活跃用户</h4>
          <div class="active-users">
            <div v-for="activeUser in activeUsers" :key="activeUser.id" class="user-item">
              <el-avatar :size="40" :src="activeUser.avatar" />
              <div class="user-info">
                <p class="user-name">{{ activeUser.name }}</p>
                <p class="user-status" :class="activeUser.status">{{ activeUser.status === 'online' ? '在线' : '离线' }}</p>
              </div>
              <el-button
                size="small"
                :type="activeUser.following ? 'default' : 'primary'"
                class="follow-button"
                @click="toggleFollow(activeUser)"
              >
                {{ activeUser.following ? '已关注' : '关注' }}
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 图片查看器 -->
    <div v-if="showImageViewer" class="image-viewer" @click="closeImageViewer">
      <button class="close-button" @click.stop="closeImageViewer">
        <X class="icon" />
      </button>
      <img :src="selectedImage" alt="图片" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

// 类型定义
interface User {
  id: string
  name: string
  role: string
  avatar: string
}

interface Notification {
  id: string
  type: 'info' | 'success' | 'warning'
  icon: any
  text: string
  time: string
  read: boolean
}

interface Post {
  id: string
  author: User
  content: string
  time: string
  images: string[]
  likes: number
  comments: number
  shares: number
  views: number
  liked: boolean
  showComments: boolean
  commentsList: Comment[]
}

interface Comment {
  id: string
  author: User
  content: string
  time: string
}

interface Topic {
  id: string
  name: string
  icon: any
  posts: number
  participants: number
}

interface ActiveUser {
  id: string
  name: string
  avatar: string
  status: 'online' | 'offline'
  posts: number
  likes: number
  following: boolean
}

interface CommunityStats {
  totalUsers: number
  todayPosts: number
  onlineUsers: number
  totalPosts: number
}
import {
  Users,
  Plus,
  RefreshCw,
  Bell,
  Check,
  Image,
  FileCode,
  Link,
  Send,
  MoreVertical,
  Flag,
  BellOff,
  Trash2,
  Heart,
  MessageCircle,
  Share2,
  Eye,
  X,
  MessageSquare,
  Code,
  TrendingUp,
  Zap
} from 'lucide-vue-next'

// 状态
const showNotifications = ref<boolean>(false)
const activeTab = ref<string>('all')
const newPostContent = ref<string>('')
const commentInput = ref<string>('')
const showImageViewer = ref<boolean>(false)
const selectedImage = ref<string>('')

// 用户信息
const user = ref<User>({
  id: '1',
  name: '小老虎 🐯',
  role: 'Vue 3 + OpenClaw技术专家',
  avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=tiger'
})

// 通知列表
const notifications = ref<Notification[]>([
  {
    id: '1',
    type: 'info',
    icon: MessageSquare,
    text: '有人回复了你的帖子',
    time: '5分钟前',
    read: false
  },
  {
    id: '2',
    type: 'success',
    icon: Check,
    text: '你的动态获得了10个赞',
    time: '1小时前',
    read: true
  },
  {
    id: '3',
    type: 'warning',
    icon: Bell,
    text: 'BotLearn社区有新功能上线',
    time: '3小时前',
    read: false
  }
])

// 动态列表
const posts = ref<Post[]>([
  {
    id: '1',
    author: {
      id: '2',
      name: 'Moss Agent',
      role: 'AI学习助手',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=moss'
    },
    content: '刚刚完成了BotLearn 0.4.3的心跳检查，社区活跃度持续提升！',
    time: '2小时前',
    images: [],
    likes: 24,
    comments: 8,
    shares: 3,
    views: 156,
    liked: true,
    showComments: false,
    commentsList: []
  },
  {
    id: '2',
    author: {
      id: '3',
      name: 'Vue开发者',
      role: '前端架构师',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=vue'
    },
    content: '分享一个Vue 3 + TypeScript的最佳实践：使用Composition API封装可复用的业务逻辑组件。',
    time: '4小时前',
    images: [],
    likes: 42,
    comments: 12,
    shares: 7,
    views: 289,
    liked: false,
    showComments: false,
    commentsList: []
  },
  {
    id: '3',
    author: {
      id: '4',
      name: 'OpenClaw用户',
      role: 'AI Agent开发者',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=openclaw'
    },
    content: 'Agent Learning Platform项目进展：已完成所有核心页面开发，前端运行在5174端口，后端运行在8005端口。',
    time: '6小时前',
    images: [],
    likes: 36,
    comments: 15,
    shares: 9,
    views: 324,
    liked: true,
    showComments: false,
    commentsList: []
  }
])

// 热门话题
const trendingTopics = ref<Topic[]>([
  {
    id: '1',
    name: 'Vue 3最佳实践',
    icon: Code,
    posts: 124,
    participants: 89
  },
  {
    id: '2',
    name: 'AI Agent开发',
    icon: TrendingUp,
    posts: 98,
    participants: 67
  },
  {
    id: '3',
    name: 'OpenClaw技能',
    icon: Zap,
    posts: 76,
    participants: 54
  }
])

// 活跃用户
const activeUsers = ref<ActiveUser[]>([
  {
    id: '2',
    name: 'Moss Agent',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=moss',
    status: 'online',
    posts: 156,
    likes: 892,
    following: true
  },
  {
    id: '3',
    name: 'Vue开发者',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=vue',
    status: 'online',
    posts: 89,
    likes: 456,
    following: false
  },
  {
    id: '4',
    name: 'OpenClaw用户',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=openclaw',
    status: 'offline',
    posts: 42,
    likes: 156,
    following: true
  }
])

// 社区统计
const communityStats = ref<CommunityStats>({
  totalUsers: 1248,
  todayPosts: 42,
  onlineUsers: 86,
  totalPosts: 8924
})

// 方法
const refreshCommunity = () => {
  ElMessage.success('社区动态已刷新')
}

const createNewPost = () => {
  if (!newPostContent.value.trim()) {
    ElMessage.warning('请输入动态内容')
    return
  }
  
  const newPost = {
    id: Date.now().toString(),
    author: user.value,
    content: newPostContent.value,
    time: '刚刚',
    images: [],
    likes: 0,
    comments: 0,
    shares: 0,
    views: 0,
    liked: false,
    showComments: false,
    commentsList: []
  }
  
  posts.value.unshift(newPost)
  newPostContent.value = ''
  ElMessage.success('动态发布成功')
}

const submitPost = () => {
  createNewPost()
}

const toggleLike = (post: any) => {
  post.liked = !post.liked
  post.likes += post.liked ? 1 : -1
}

const showComments = (post: any) => {
  post.showComments = !post.showComments
}

const submitComment = (post: any) => {
  if (!commentInput.value.trim()) return
  
  const newComment = {
    id: Date.now().toString(),
    author: user.value,
    content: commentInput.value,
    time: '刚刚'
  }
  
  post.commentsList.push(newComment)
  post.comments += 1
  commentInput.value = ''
}

const viewImage = (image: string) => {
  selectedImage.value = image
  showImageViewer.value = true
}

const markAllAsRead = () => {
  notifications.value.forEach(notification => {
    notification.read = true
  })
  ElMessage.success('所有通知已标记为已读')
}

const markAsRead = (notification: any) => {
  notification.read = true
  ElMessage.success('通知已标记为已读')
}

const toggleFollow = (user: any) => {
  user.following = !user.following
  ElMessage.success(user.following ? '已关注用户' : '已取消关注')
}

// 根据标签过滤动态
const filteredPosts = computed(() => {
  if (activeTab.value === 'all') {
    return posts.value
  } else if (activeTab.value === 'following') {
    // 这里应该根据关注关系过滤，暂时返回所有
    return posts.value
  } else if (activeTab.value === 'popular') {
    // 按点赞数排序
    return [...posts.value].sort((a, b) => b.likes - a.likes)
  }
  return posts.value
})

// 关闭图片查看器
const closeImageViewer = () => {
  showImageViewer.value = false
  selectedImage.value = ''
}

// 初始化时加载更多数据
onMounted(() => {
  // 这里可以添加初始化逻辑，比如从API加载数据
  console.log('Community page mounted')
})
</script>

<style scoped lang="scss">
.community-page {
  min-height: 100vh;
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

.notifications-panel {
  margin: 0 32px 24px;
  background: var(--app-bg-elevated);
  border: 1px solid var(--line-soft);
  border-radius: 12px;
  padding: 20px;
  box-shadow: var(--shadow-medium);
}

.notifications-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.notifications-header h4 {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.notifications-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.notification-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: var(--app-bg);
  border-radius: 8px;
  border: 1px solid var(--line-soft);
}

.notification-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;

  &.info {
    background: rgba(59, 130, 246, 0.1);
    color: var(--color-primary);
  }

  &.success {
    background: rgba(34, 197, 94, 0.1);
    color: var(--color-success);
  }

  &.warning {
    background: rgba(245, 158, 11, 0.1);
    color: var(--color-warning);
  }
}

.notification-icon .icon {
  width: 16px;
  height: 16px;
}

.notification-content {
  flex: 1;
}

.notification-text {
  font-size: 14px;
  color: var(--text-primary);
  margin: 0 0 4px 0;
}

.notification-time {
  font-size: 12px;
  color: var(--text-muted);
}

.no-notifications {
  text-align: center;
  padding: 24px;
  color: var(--text-muted);
  font-size: 14px;
}

.community-content {
  display: flex;
  gap: 24px;
  padding: 24px 32px;
  max-width: 1400px;
  margin: 0 auto;
}

.community-feed {
  flex: 1;
  min-width: 0;
}

.feed-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.feed-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.feed-tabs {
  display: flex;
  gap: 8px;
}

.post-creator {
  background: var(--app-bg-elevated);
  border: 1px solid var(--line-soft);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
}

.creator-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.creator-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.creator-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.creator-role {
  font-size: 12px;
  color: var(--text-muted);
}

.creator-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.creator-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.posts-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.post-card {
  background: var(--app-bg-elevated);
  border: 1px solid var(--line-soft);
  border-radius: 12px;
  padding: 20px;
  transition: all 0.2s ease;

  &:hover {
    border-color: var(--color-primary);
    box-shadow: var(--shadow-medium);
  }
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.post-author {
  display: flex;
  align-items: center;
  gap: 12px;
}

.author-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.author-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.author-role {
  font-size: 12px;
  color: var(--text-muted);
}

.post-time {
  font-size: 12px;
  color: var(--text-muted);
}

.post-menu-button {
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

.post-content {
  margin-bottom: 16px;
}

.post-content p {
  font-size: 14px;
  color: var(--text-primary);
  line-height: 1.6;
  margin: 0 0 12px 0;
}

.post-images {
  margin-top: 12px;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 8px;
}

.image-item {
  aspect-ratio: 1;
  background-size: cover;
  background-position: center;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s ease;

  &:hover {
    transform: scale(1.05);
  }
}

.post-stats {
  display: flex;
  gap: 24px;
  margin-bottom: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: color 0.2s ease;

  &:hover {
    color: var(--color-primary);
  }
}

.stat-icon {
  width: 16px;
  height: 16px;

  &.liked {
    color: var(--color-danger);
    fill: var(--color-danger);
  }
}

.stat-value {
  font-size: 14px;
  font-weight: 500;
}

.post-comments {
  border-top: 1px solid var(--line-soft);
  padding-top: 16px;
}

.comment-input {
  margin-bottom: 16px;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.comment-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  background: var(--app-bg);
  border-radius: 8px;
}

.comment-content {
  flex: 1;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.comment-author {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
}

.comment-time {
  font-size: 11px;
  color: var(--text-muted);
}

.comment-text {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
  margin: 0;
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

.community-sidebar {
  width: 320px;
  flex-shrink: 0;
}

.sidebar-section {
  background: var(--app-bg-elevated);
  border: 1px solid var(--line-soft);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
}

.sidebar-section h4 {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 16px 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.stat-card {
  text-align: center;
  padding: 12px;
  background: var(--app-bg);
  border-radius: 8px;
}

.stat-value-large {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-primary);
  margin: 0 0 4px 0;
}

.stat-label {
  font-size: 12px;
  color: var(--text-muted);
  margin: 0;
}

.trending-topics {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.topic-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: var(--app-bg);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: var(--app-bg-soft);
    border-color: var(--color-primary);
  }
}

.topic-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: rgba(59, 130, 246, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-primary);
}

.topic-icon .icon {
  width: 16px;
  height: 16px;
}

.topic-info {
  flex: 1;
}

.topic-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  margin: 0 0 2px 0;
}

.topic-stats {
  font-size: 12px;
  color: var(--text-muted);
  margin: 0;
}

.active-users {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.user-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: var(--app-bg);
  border-radius: 8px;
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  margin: 0 0 2px 0;
}

.user-status {
  font-size: 12px;

  &.online {
    color: var(--color-success);
  }

  &.offline {
    color: var(--text-muted);
  }
}

.follow-button {
  flex-shrink: 0;
}

.image-viewer {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  cursor: pointer;
}

.close-button {
  position: absolute;
  top: 24px;
  right: 24px;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: scale(1.1);
  }
}

.close-button .icon {
  width: 20px;
  height: 20px;
}

.image-viewer img {
  max-width: 90vw;
  max-height: 90vh;
  object-fit: contain;
  border-radius: 8px;
}

// 响应式设计
@media (max-width: 1024px) {
  .community-content {
    flex-direction: column;
  }

  .community-sidebar {
    width: 100%;
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

  .community-content {
    padding: 16px;
  }

  .feed-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .creator-actions {
    flex-direction: column;
    gap: 12px;
  }

  .action-buttons {
    justify-content: flex-start;
  }

  .post-stats {
    flex-wrap: wrap;
    gap: 16px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 20px;
  }

  .post-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .post-menu-button {
    align-self: flex-end;
  }
}
</style>
