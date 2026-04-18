<template>
  <div class="test-page">
    <h1>系统连接测试</h1>
    
    <div class="test-section">
      <h3>后端API测试</h3>
      <el-button @click="testBackendHealth">测试后端健康检查</el-button>
      <div v-if="backendHealth" class="test-result">
        <p>状态: {{ backendHealth.status }}</p>
        <p>服务: {{ backendHealth.service }}</p>
        <p>版本: {{ backendHealth.version }}</p>
      </div>
    </div>
    
    <div class="test-section">
      <h3>Agent API测试</h3>
      <el-button @click="testAgentAPI">测试Agent API</el-button>
      <div v-if="agents" class="test-result">
        <p>Agent数量: {{ agents.length }}</p>
        <div v-for="agent in agents" :key="agent.id" class="agent-item">
          <p>{{ agent.name }} - {{ agent.status }}</p>
        </div>
      </div>
    </div>
    
    <div class="test-section">
      <h3>创建测试Agent</h3>
      <el-button @click="createTestAgent">创建测试Agent</el-button>
      <div v-if="createdAgent" class="test-result">
        <p>创建成功: {{ createdAgent.name }}</p>
        <p>ID: {{ createdAgent.id }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { healthAPI, agentAPI } from '@/api/index.ts'

const backendHealth = ref<any>(null)
const agents = ref<any[]>([])
const createdAgent = ref<any>(null)

const testBackendHealth = async () => {
  try {
    const response = await healthAPI.checkHealth()
    backendHealth.value = response.data
  } catch (error) {
    console.error('后端健康检查失败:', error)
    backendHealth.value = { status: 'error', error: String(error) }
  }
}

const testAgentAPI = async () => {
  try {
    const response = await agentAPI.getAgents()
    agents.value = response.data
  } catch (error) {
    console.error('Agent API测试失败:', error)
    agents.value = []
  }
}

const createTestAgent = async () => {
  try {
    const response = await agentAPI.createAgent({
      name: '测试Agent',
      description: '这是一个测试用的Agent',
      type: 'conversational',
      model: 'gpt-3.5-turbo',
      temperature: 0.7,
      memory: true,
      tools: ['calculator', 'web-search']
    })
    createdAgent.value = response.data
  } catch (error) {
    console.error('创建测试Agent失败:', error)
    createdAgent.value = null
  }
}
</script>

<style scoped>
.test-page {
  padding: 20px;
}

.test-section {
  margin: 20px 0;
  padding: 20px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
}

.test-result {
  margin-top: 10px;
  padding: 10px;
  background: #f5f7fa;
  border-radius: 4px;
}

.agent-item {
  padding: 5px;
  border-bottom: 1px solid #e4e7ed;
}
</style>