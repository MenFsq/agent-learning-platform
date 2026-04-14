import type { Component } from 'vue'

export interface HeroMetric {
  label: string
  value: number
  suffix?: string
}

export interface OverviewMetric {
  id: string
  label: string
  value: number
  suffix?: string
  hint: string
  delta: string
  icon: Component
  sparkline: number[]
}

export interface ProjectMember {
  name: string
  avatar: string
}

export interface ProjectItem {
  id: number
  name: string
  summary: string
  status: string
  statusTone: 'primary' | 'success' | 'warning'
  progress: number
  updatedAt: string
  members: ProjectMember[]
}

export interface LearningItem {
  id: number
  title: string
  category: string
  progress: number
  duration: string
  icon: Component
  completed?: boolean
}

export interface QuickActionItem {
  id: number
  title: string
  description: string
  icon: Component
  href: string
}

export interface CommunityTickerItem {
  id: number
  title: string
  detail: string
  href: string
}
