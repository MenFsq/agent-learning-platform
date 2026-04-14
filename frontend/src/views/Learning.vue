<template>
  <div class="learning-page">
    <!-- LangChain学习思维导图组件 -->
    <LangChainMindMap />
    
    <!-- 其他学习内容可以在这里添加 -->
    <div class="additional-content">
      <div class="content-section">
        <h2>🎯 学习原则</h2>
        <div class="principles-grid">
          <div class="principle-card">
            <div class="principle-icon">📝</div>
            <div class="principle-title">一步步来</div>
            <div class="principle-desc">按照4个阶段21天的计划逐步学习，不跳步</div>
          </div>
          <div class="principle-card">
            <div class="principle-icon">✅</div>
            <div class="principle-title">多验证</div>
            <div class="principle-desc">每个概念都要动手实践，确保真正掌握</div>
          </div>
          <div class="principle-card">
            <div class="principle-icon">🔗</div>
            <div class="principle-title">项目集成</div>
            <div class="principle-desc">将学习成果集成到实际项目中，创造价值</div>
          </div>
          <div class="principle-card">
            <div class="principle-icon">🌐</div>
            <div class="principle-title">社区分享</div>
            <div class="principle-desc">在BotLearn社区分享经验，建立技术影响力</div>
          </div>
        </div>
      </div>
      
      <div class="content-section">
        <h2>🚀 立即开始</h2>
        <div class="start-actions">
          <button class="action-btn primary" @click="startLearning">
            <span class="btn-icon">🐯</span>
            <span class="btn-text">开始第一阶段学习</span>
          </button>
          <button class="action-btn secondary" @click="viewResources">
            <span class="btn-icon">📚</span>
            <span class="btn-text">查看学习资源</span>
          </button>
          <button class="action-btn outline" @click="downloadPlan">
            <span class="btn-icon">💾</span>
            <span class="btn-text">下载学习计划</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import LangChainMindMap from '@/components/LangChainMindMap.vue'

const startLearning = () => {
  // 这里可以添加开始学习的逻辑
  alert('开始第一阶段：环境搭建与基础概念学习')
}

const viewResources = () => {
  // 这里可以添加查看资源的逻辑
  window.open('https://github.com/liaokongVFX/LangChain-Chinese-Getting-Started-Guide', '_blank')
}

const downloadPlan = () => {
  // 这里可以添加下载学习计划的逻辑
  alert('学习计划下载功能将在后续版本中实现')
}
</script>

<style scoped>
.learning-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.additional-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.content-section {
  background: white;
  border-radius: 15px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.05);
}

.content-section h2 {
  font-size: 1.8rem;
  color: #667eea;
  margin-bottom: 25px;
  padding-bottom: 10px;
  border-bottom: 3px solid #667eea;
}

/* 原则网格 */
.principles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.principle-card {
  text-align: center;
  padding: 25px;
  background: #f8f9fa;
  border-radius: 10px;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.principle-card:hover {
  background: white;
  border-color: #667eea;
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.1);
}

.principle-icon {
  font-size: 3rem;
  margin-bottom: 15px;
}

.principle-title {
  font-size: 1.3rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.principle-desc {
  color: #666;
  font-size: 0.95rem;
  line-height: 1.5;
}

/* 开始行动按钮 */
.start-actions {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
  justify-content: center;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px 25px;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  min-width: 200px;
  justify-content: center;
}

.action-btn.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.action-btn.primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

.action-btn.secondary {
  background: #4CAF50;
  color: white;
}

.action-btn.secondary:hover {
  background: #45a049;
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(76, 175, 80, 0.3);
}

.action-btn.outline {
  background: transparent;
  color: #667eea;
  border: 2px solid #667eea;
}

.action-btn.outline:hover {
  background: #667eea;
  color: white;
  transform: translateY(-3px);
}

.btn-icon {
  font-size: 1.2rem;
}

.btn-text {
  white-space: nowrap;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .principles-grid {
    grid-template-columns: 1fr;
  }
  
  .start-actions {
    flex-direction: column;
  }
  
  .action-btn {
    width: 100%;
    min-width: unset;
  }
  
  .content-section {
    padding: 20px;
  }
}
</style>