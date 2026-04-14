<template>
  <div ref="dashboardRef" class="dashboard-page">
    <Particles id="dashboard-particles" :options="particlesOptions as any" class="particles-layer" />

    <div class="page-container">
      <div class="dashboard-shell">
        <DashboardHero
          user-name="小老虎"
          subtitle="一站式 AI Agent 开发、学习、部署工作台。以更轻的界面承接项目进度、学习路径和社区动向，让你在同一条工作流里持续推进。"
          :metrics="heroMetrics"
          :highlights="heroHighlights"
        />

        <OverviewStats :items="overviewMetrics" />
        <ProjectShowcase :items="projects" />
        <LearningRail :items="learningItems" />
        <QuickEntryGrid :items="quickActions" />
        <CommunityTicker :items="communityFeed" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import {
  Blocks,
  BookMarked,
  Bot,
  Compass,
  FileCode2,
  FolderGit2,
  GraduationCap,
  Layers3,
  MessagesSquare,
  Radar,
  Rocket,
  Sparkles,
  TerminalSquare,
  Workflow
} from 'lucide-vue-next'
import { ParticlesComponent as Particles } from 'particles.vue3'
import { loadSlim } from '@tsparticles/slim'
import { tsParticles } from '@tsparticles/engine'

import CommunityTicker from '@/components/dashboard/CommunityTicker.vue'
import DashboardHero from '@/components/dashboard/DashboardHero.vue'
import LearningRail from '@/components/dashboard/LearningRail.vue'
import OverviewStats from '@/components/dashboard/OverviewStats.vue'
import ProjectShowcase from '@/components/dashboard/ProjectShowcase.vue'
import QuickEntryGrid from '@/components/dashboard/QuickEntryGrid.vue'
import type {
  CommunityTickerItem,
  HeroMetric,
  LearningItem,
  OverviewMetric,
  ProjectItem,
  QuickActionItem
} from '@/components/dashboard/types'

const dashboardRef = ref<HTMLElement | null>(null)
let observer: IntersectionObserver | null = null

const heroMetrics: HeroMetric[] = [
  { label: '今日活跃', value: 18 },
  { label: '进行中项目', value: 6 },
  { label: '学习进度', value: 72, suffix: '%' }
]

const heroHighlights = [
  {
    title: 'Project Pulse',
    value: '3 个冲刺中',
    detail: '智能文档助手、RAG Copilot 与代码审查 Agent 正在持续推进。'
  },
  {
    title: 'Focus Window',
    value: '4.6h 深度工作',
    detail: '今天的高专注区间集中在编排、调试与部署准备。'
  },
  {
    title: 'Community Signal',
    value: '12 条新反馈',
    detail: '教程、精选示例与社区问答均有新的可跟进内容。'
  }
]

const overviewMetrics: OverviewMetric[] = [
  {
    id: 'project-progress',
    label: '项目总进度',
    value: 84,
    suffix: '%',
    hint: '本周的主要目标已经完成大半，节奏稳定。',
    delta: '+12%',
    icon: Workflow,
    sparkline: [18, 28, 26, 42, 48, 63, 84]
  },
  {
    id: 'todo-count',
    label: '待办任务数',
    value: 9,
    hint: '待办保持在可控范围，适合持续推进。',
    delta: '-3',
    icon: Layers3,
    sparkline: [18, 16, 14, 13, 11, 10, 9]
  },
  {
    id: 'learning-rate',
    label: '学习完成率',
    value: 76,
    suffix: '%',
    hint: '当前学习路径集中在 LangChain 与部署能力。',
    delta: '+8%',
    icon: GraduationCap,
    sparkline: [30, 40, 43, 54, 58, 63, 76]
  },
  {
    id: 'run-count',
    label: '代码运行次数',
    value: 128,
    hint: '本周实验密度较高，验证速度保持稳定。',
    delta: '+24',
    icon: TerminalSquare,
    sparkline: [42, 58, 53, 64, 82, 99, 128]
  },
  {
    id: 'community-engagement',
    label: '社区互动数',
    value: 36,
    hint: '社区反馈正持续反哺你的项目与学习路径。',
    delta: '+6',
    icon: MessagesSquare,
    sparkline: [8, 12, 15, 18, 24, 28, 36]
  }
]

const projects: ProjectItem[] = [
  {
    id: 1,
    name: '智能文档助手',
    summary: '面向企业知识库的 RAG 应用，正在优化检索链路和引用展示。',
    status: 'In Review',
    statusTone: 'primary',
    progress: 82,
    updatedAt: '今天 14:20',
    members: [
      { name: 'Tiger', avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=tiger' },
      { name: 'Mia', avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=mia' },
      { name: 'Chen', avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=chen' }
    ]
  },
  {
    id: 2,
    name: '代码审查 Agent',
    summary: '自动定位潜在回归点并给出修复建议，当前聚焦规则置信度调优。',
    status: 'Active Sprint',
    statusTone: 'warning',
    progress: 61,
    updatedAt: '今天 11:05',
    members: [
      { name: 'Neo', avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=neo' },
      { name: 'Lynn', avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=lynn' }
    ]
  },
  {
    id: 3,
    name: 'PromptOps 控制台',
    summary: '统一查看提示词版本、实验结果与部署状态，用于提升协作效率。',
    status: 'Stable',
    statusTone: 'success',
    progress: 93,
    updatedAt: '昨天 18:40',
    members: [
      { name: 'Kai', avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=kai' },
      { name: 'Rin', avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=rin' },
      { name: 'Lio', avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=lio' }
    ]
  },
  {
    id: 4,
    name: '多 Agent 协作实验',
    summary: '验证 Planner / Executor / Reviewer 多角色协同时的效率提升模型。',
    status: 'Exploring',
    statusTone: 'primary',
    progress: 47,
    updatedAt: '昨天 09:15',
    members: [{ name: 'Ava', avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=ava' }]
  }
]

const learningItems: LearningItem[] = [
  {
    id: 1,
    title: 'LangChain Agentic Patterns',
    category: 'Reasoning',
    progress: 78,
    duration: '2 / 3 单元',
    icon: BookMarked
  },
  {
    id: 2,
    title: 'RAG Pipeline In Practice',
    category: 'Retrieval',
    progress: 64,
    duration: '4 / 6 单元',
    icon: Compass
  },
  {
    id: 3,
    title: 'PromptOps Deployment Basics',
    category: 'Delivery',
    progress: 100,
    duration: '已完成',
    icon: Rocket,
    completed: true
  },
  {
    id: 4,
    title: 'Evaluation And Guardrails',
    category: 'Quality',
    progress: 41,
    duration: '1 / 4 单元',
    icon: Radar
  }
]

const quickActions: QuickActionItem[] = [
  { id: 1, title: '项目管理', description: '查看进行中冲刺与版本进度。', icon: FolderGit2, href: '/projects' },
  { id: 2, title: '学习指南', description: '继续当前学习路径与课程卡片。', icon: GraduationCap, href: '/learning' },
  { id: 3, title: 'API 文档', description: '查看后端API文档和测试接口。', icon: FileCode2, href: 'http://localhost:8001/docs', external: true },
  { id: 4, title: '社区问答', description: '跟进精选讨论与高质量回答。', icon: MessagesSquare, href: '/community' },
  { id: 5, title: '部署工具', description: '查看当前构建、发布与运行状态。', icon: Rocket, href: '/projects' },
  { id: 6, title: 'API 控制台', description: '整理接口调用、日志和实验数据。', icon: Blocks, href: '/settings' },
  { id: 7, title: 'Agent 编排', description: '聚焦工作流结构、节点与协作关系。', icon: Bot, href: '/projects' },
  { id: 8, title: '环境设置', description: '调整主题、偏好和系统连接配置。', icon: Sparkles, href: '/settings' }
]

const communityFeed: CommunityTickerItem[] = [
  { id: 1, title: 'API 文档', detail: '后端API文档已就绪，支持在线测试', href: 'http://localhost:8001/docs', external: true },
  { id: 2, title: '最新教程', detail: 'LangGraph 流程拆解与状态管理更新', href: '/community' },
  { id: 3, title: '热门示例', detail: 'Vue + Agent 工具调用模板本周增长最快', href: '/community' },
  { id: 4, title: '社区精选', detail: 'RAG 与 PromptOps 的实战问答持续升温', href: '/community' }
]

const particlesOptions = {
  background: {
    color: { value: 'transparent' }
  },
  fpsLimit: 60,
  particles: {
    number: {
      value: 34,
      density: {
        enable: true,
        area: 900
      }
    },
    color: {
      value: ['#3b82f6', '#06b6d4', '#8b5cf6']
    },
    links: {
      enable: true,
      distance: 160,
      color: '#3b82f6',
      opacity: 0.08,
      width: 1
    },
    opacity: {
      value: { min: 0.08, max: 0.22 }
    },
    move: {
      enable: true,
      speed: 0.35,
      random: true,
      outModes: {
        default: 'out'
      }
    },
    size: {
      value: { min: 1, max: 2.4 }
    }
  },
  interactivity: {
    events: {
      onHover: {
        enable: true,
        mode: 'grab'
      },
      resize: true
    },
    modes: {
      grab: {
        distance: 120,
        links: {
          opacity: 0.16
        }
      }
    }
  },
  detectRetina: true
}

loadSlim(tsParticles)

const setupReveal = async () => {
  await nextTick()

  observer?.disconnect()

  observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible')
          observer?.unobserve(entry.target)
        }
      })
    },
    {
      threshold: 0.14
    }
  )

  dashboardRef.value?.querySelectorAll<HTMLElement>('[data-reveal]').forEach((element: HTMLElement) => {
    observer?.observe(element)
  })
}

onMounted(() => {
  setupReveal()
})

onBeforeUnmount(() => {
  observer?.disconnect()
})
</script>

<style scoped lang="scss">
.dashboard-page {
  position: relative;
  min-height: calc(100vh - var(--header-height));
}

.particles-layer {
  position: fixed;
  inset: var(--header-height) 0 0;
  z-index: 0;
  pointer-events: none;
  opacity: 0.72;
}

.dashboard-shell {
  position: relative;
  z-index: 1;
  width: 100%;
  display: grid;
  gap: var(--section-gap);
  padding-block: clamp(28px, 3vw, 40px) 54px;
}

@media (max-width: 640px) {
  .dashboard-shell {
    padding-block: 22px 42px;
  }
}
</style>
