<template>
  <div class="langchain-mindmap">
    <!-- 页面标题和描述 -->
    <div class="header">
      <h1 class="title">🐯 LangChain 学习与实践路线图</h1>
      <p class="subtitle">基于 LangChain 中文入门指南的完整学习路径 | 一步步验证，确保掌握</p>
      
      <!-- 统计卡片 -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-value">4</div>
          <div class="stat-label">学习阶段</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">12+</div>
          <div class="stat-label">实战案例</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">21</div>
          <div class="stat-label">学习天数</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">3</div>
          <div class="stat-label">集成项目</div>
        </div>
      </div>
    </div>

    <!-- 技术栈展示 -->
    <div class="tech-stack-section">
      <h2 class="section-title">🛠️ 技术栈</h2>
      <div class="tech-tags">
        <span class="tech-tag primary">LangChain</span>
        <span class="tech-tag primary">OpenAI API</span>
        <span class="tech-tag primary">Chroma DB</span>
        <span class="tech-tag">Vue 3</span>
        <span class="tech-tag">TypeScript</span>
        <span class="tech-tag">Python 3.9+</span>
        <span class="tech-tag">FastAPI</span>
        <span class="tech-tag">Docker</span>
        <span class="tech-tag">OpenClaw</span>
        <span class="tech-tag">Git</span>
      </div>
    </div>

    <!-- 思维导图容器 -->
    <div class="mindmap-container">
      <div class="mindmap-header">
        <h2 class="section-title">📊 LangChain 学习流程思维导图</h2>
        <div class="mindmap-controls">
          <button class="control-btn" @click="zoomIn">
            <span class="icon">➕</span> 放大
          </button>
          <button class="control-btn" @click="zoomOut">
            <span class="icon">➖</span> 缩小
          </button>
          <button class="control-btn" @click="resetZoom">
            <span class="icon">🔄</span> 重置
          </button>
          <button class="control-btn" @click="downloadImage">
            <span class="icon">💾</span> 保存
          </button>
        </div>
      </div>
      
      <!-- Mermaid 思维导图 -->
      <div class="mermaid-diagram" ref="mermaidContainer">
        <!-- Mermaid图表将通过JavaScript动态生成 -->
      </div>
    </div>

    <!-- 学习阶段详情 -->
    <div class="phases-section">
      <h2 class="section-title">📅 学习阶段详情</h2>
      
      <div class="phases-grid">
        <!-- 第一阶段 -->
        <div class="phase-card phase-1">
          <div class="phase-header">
            <div class="phase-title">第一阶段：基础入门 (1-3天)</div>
            <div class="phase-duration">🔰 入门级</div>
          </div>
          <div class="phase-content">
            <div class="phase-step">
              <div class="step-title">第1步：环境搭建</div>
              <div class="step-desc">安装依赖、配置API密钥、验证环境</div>
              <div class="step-tech">
                <span class="tech-badge">Python</span>
                <span class="tech-badge">pip</span>
                <span class="tech-badge">环境变量</span>
              </div>
            </div>
            <div class="phase-step">
              <div class="step-title">第2步：第一个程序</div>
              <div class="step-desc">运行第一个LangChain程序，理解基本流程</div>
              <div class="step-tech">
                <span class="tech-badge">OpenAI LLM</span>
                <span class="tech-badge">基础调用</span>
              </div>
            </div>
            <div class="phase-step">
              <div class="step-title">第3步：核心概念</div>
              <div class="step-desc">学习Loader、Document、Text Splitters等概念</div>
              <div class="step-tech">
                <span class="tech-badge">理论概念</span>
                <span class="tech-badge">架构理解</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 第二阶段 -->
        <div class="phase-card phase-2">
          <div class="phase-header">
            <div class="phase-title">第二阶段：实战案例 (3-7天)</div>
            <div class="phase-duration">⚡ 实践级</div>
          </div>
          <div class="phase-content">
            <div class="phase-step">
              <div class="step-title">案例1：Google搜索Agent</div>
              <div class="step-desc">使用Serpapi实现联网搜索问答</div>
              <div class="step-tech">
                <span class="tech-badge">Agent</span>
                <span class="tech-badge">Serpapi</span>
                <span class="tech-badge">工具调用</span>
              </div>
            </div>
            <div class="phase-step">
              <div class="step-title">案例2：长文本总结</div>
              <div class="step-desc">处理超长文档的智能总结</div>
              <div class="step-tech">
                <span class="tech-badge">Text Splitter</span>
                <span class="tech-badge">Summarization</span>
                <span class="tech-badge">Chain</span>
              </div>
            </div>
            <div class="phase-step">
              <div class="step-title">案例3：知识库问答</div>
              <div class="step-desc">构建本地文档的智能问答系统</div>
              <div class="step-tech">
                <span class="tech-badge">RAG</span>
                <span class="tech-badge">Vector DB</span>
                <span class="tech-badge">Embeddings</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 第三阶段 -->
        <div class="phase-card phase-3">
          <div class="phase-header">
            <div class="phase-title">第三阶段：项目集成 (7-14天)</div>
            <div class="phase-duration">🔧 项目级</div>
          </div>
          <div class="phase-content">
            <div class="phase-step">
              <div class="step-title">项目1：Vue代码审查器</div>
              <div class="step-desc">基于LangChain的智能代码审查工具</div>
              <div class="step-tech">
                <span class="tech-badge">Vue 3</span>
                <span class="tech-badge">代码分析</span>
                <span class="tech-badge">最佳实践</span>
              </div>
            </div>
            <div class="phase-step">
              <div class="step-title">项目2：文档问答助手</div>
              <div class="step-desc">支持多格式文档的智能问答系统</div>
              <div class="step-tech">
                <span class="tech-badge">PDF解析</span>
                <span class="tech-badge">Markdown</span>
                <span class="tech-badge">语义搜索</span>
              </div>
            </div>
            <div class="phase-step">
              <div class="step-title">项目3：技术文档生成器</div>
              <div class="step-desc">自动生成代码的技术文档</div>
              <div class="step-tech">
                <span class="tech-badge">文档生成</span>
                <span class="tech-badge">模板系统</span>
                <span class="tech-badge">格式化输出</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 第四阶段 -->
        <div class="phase-card phase-4">
          <div class="phase-header">
            <div class="phase-title">第四阶段：高级应用 (14-21天)</div>
            <div class="phase-duration">🚀 专家级</div>
          </div>
          <div class="phase-content">
            <div class="phase-step">
              <div class="step-title">高级1：多Agent协作</div>
              <div class="step-desc">实现多个Agent协同工作的复杂系统</div>
              <div class="step-tech">
                <span class="tech-badge">多Agent</span>
                <span class="tech-badge">任务编排</span>
                <span class="tech-badge">协作系统</span>
              </div>
            </div>
            <div class="phase-step">
              <div class="step-title">高级2：自适应学习</div>
              <div class="step-desc">系统能够从用户反馈中学习和优化</div>
              <div class="step-tech">
                <span class="tech-badge">机器学习</span>
                <span class="tech-badge">反馈循环</span>
                <span class="tech-badge">性能优化</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 验证策略 -->
    <div class="validation-section">
      <h2 class="section-title">🧪 验证策略</h2>
      <div class="validation-content">
        <div class="validation-item">
          <div class="validation-icon">✅</div>
          <div class="validation-text">
            <strong>环境验证</strong> - 检查Python、依赖、API密钥
          </div>
        </div>
        <div class="validation-item">
          <div class="validation-icon">✅</div>
          <div class="validation-text">
            <strong>概念验证</strong> - 验证Loader、Splitter、Vectorstore等概念
          </div>
        </div>
        <div class="validation-item">
          <div class="validation-icon">✅</div>
          <div class="validation-text">
            <strong>案例验证</strong> - 验证所有实战案例
          </div>
        </div>
        <div class="validation-item">
          <div class="validation-icon">✅</div>
          <div class="validation-text">
            <strong>项目验证</strong> - 验证集成项目功能
          </div>
        </div>
      </div>
    </div>

    <!-- 资源链接 -->
    <div class="resources-section">
      <h2 class="section-title">🔗 资源链接</h2>
      <div class="resources-grid">
        <a href="https://github.com/liaokongVFX/LangChain-Chinese-Getting-Started-Guide" target="_blank" class="resource-link">
          <div class="resource-icon">📚</div>
          <div class="resource-content">
            <div class="resource-title">LangChain中文入门指南</div>
            <div class="resource-desc">GitHub上的完整中文教程</div>
          </div>
        </a>
        <a href="https://python.langchain.com/" target="_blank" class="resource-link">
          <div class="resource-icon">🐍</div>
          <div class="resource-content">
            <div class="resource-title">LangChain官方文档</div>
            <div class="resource-desc">官方英文文档和API参考</div>
          </div>
        </a>
        <a href="https://docs.openclaw.ai" target="_blank" class="resource-link">
          <div class="resource-icon">🐯</div>
          <div class="resource-content">
            <div class="resource-title">OpenClaw文档</div>
            <div class="resource-desc">OpenClaw技能开发指南</div>
          </div>
        </a>
        <a href="https://clawhub.ai" target="_blank" class="resource-link">
          <div class="resource-icon">🌐</div>
          <div class="resource-content">
            <div class="resource-title">BotLearn社区</div>
            <div class="resource-desc">AI Agent能力平台社区</div>
          </div>
        </a>
      </div>
    </div>

    <!-- 页脚 -->
    <div class="footer">
      <p class="footer-text">📚 基于 <a href="https://github.com/liaokongVFX/LangChain-Chinese-Getting-Started-Guide" target="_blank">LangChain中文入门指南</a> | 🐯 由小老虎整理 | 📅 最后更新: 2026-04-14</p>
      <p class="footer-note">遵循"一步步来，多验证"原则，确保每个阶段都真正掌握</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

// 引用Mermaid容器
const mermaidContainer = ref<HTMLElement | null>(null)

// 缩放控制
let zoomLevel = 1

const zoomIn = () => {
  if (zoomLevel < 2) {
    zoomLevel += 0.1
    updateZoom()
  }
}

const zoomOut = () => {
  if (zoomLevel > 0.5) {
    zoomLevel -= 0.1
    updateZoom()
  }
}

const resetZoom = () => {
  zoomLevel = 1
  updateZoom()
}

const updateZoom = () => {
  if (mermaidContainer.value) {
    mermaidContainer.value.style.transform = `scale(${zoomLevel})`
    mermaidContainer.value.style.transformOrigin = 'center'
  }
}

// 保存图片功能
const downloadImage = () => {
  // 这里可以添加保存为图片的功能
  alert('保存功能将在后续版本中实现')
}

// 初始化Mermaid图表
const initMermaid = () => {
  if (!mermaidContainer.value) return

  // 清除现有内容
  mermaidContainer.value.innerHTML = ''

  // 创建Mermaid图表
  const mermaidCode = `
flowchart TD
    Start[🎯 开始学习 LangChain] --> Phase1
    
    subgraph Phase1[第一阶段: 基础入门 1-3天]
        P1S1[📦 环境搭建] --> P1S2[🖥️ 第一个程序]
        P1S2 --> P1S3[📚 核心概念]
        
        P1S1 --> P1V1{验证: 环境正常}
        P1S2 --> P1V2{验证: 程序运行}
        P1S3 --> P1V3{验证: 概念理解}
    end
    
    Phase1 --> Phase2
    
    subgraph Phase2[第二阶段: 实战案例 3-7天]
        P2C1[🔍 案例1: Google搜索Agent] --> P2C2[📄 案例2: 长文本总结]
        P2C2 --> P2C3[💬 案例3: 知识库问答]
        P2C3 --> P2C4[🛠️ 案例4: 自定义Agent]
        
        P2C1 --> P2V1{验证: 搜索正常}
        P2C2 --> P2V2{验证: 总结准确}
        P2C3 --> P2V3{验证: 问答正确}
        P2C4 --> P2V4{验证: 工具调用}
    end
    
    Phase2 --> Phase3
    
    subgraph Phase3[第三阶段: 项目集成 7-14天]
        P3P1[🎨 项目1: Vue代码审查器] --> P3P2[📖 项目2: 文档问答助手]
        P3P2 --> P3P3[📝 项目3: 文档生成器]
        
        P3P1 --> P3V1{验证: 代码分析}
        P3P2 --> P3V2{验证: 问答质量}
        P3P3 --> P3V3{验证: 文档生成}
    end
    
    Phase3 --> Phase4
    
    subgraph Phase4[第四阶段: 高级应用 14-21天]
        P4A1[🤝 高级1: 多Agent协作] --> P4A2[🧠 高级2: 自适应学习]
        P4A2 --> P4A3[🚀 高级3: 生产部署]
        
        P4A1 --> P4V1{验证: 协作效率}
        P4A2 --> P4V2{验证: 学习效果}
        P4A3 --> P4V3{验证: 部署稳定}
    end
    
    Phase4 --> Success[✅ 完成学习与实践]
    
    Success --> Integration[🔗 集成到OpenClaw]
    Integration --> Community[🌐 分享到BotLearn]
    Community --> Continuous[🔄 持续优化]
  `

  // 创建pre元素用于显示Mermaid代码
  const preElement = document.createElement('pre')
  preElement.className = 'mermaid'
  preElement.textContent = mermaidCode
  
  mermaidContainer.value.appendChild(preElement)

  // 如果Mermaid库已加载，初始化图表
  if (window.mermaid) {
    window.mermaid.init(undefined, document.querySelectorAll('.mermaid'))
  }
}

// 组件挂载时初始化
onMounted(() => {
  // 加载Mermaid库
  const script = document.createElement('script')
  script.src = 'https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js'
  script.onload = () => {
    // 配置Mermaid
    window.mermaid.initialize({
      startOnLoad: true,
      theme: 'default',
      flowchart: {
        useMaxWidth: true,
        htmlLabels: true,
        curve: 'basis'
      },
      securityLevel: 'loose'
    })
    
    // 初始化图表
    setTimeout(initMermaid, 100)
  }
  document.head.appendChild(script)
})

// 组件卸载时清理
onUnmounted(() => {
  // 可以在这里清理资源
})
</script>

<style scoped>
.langchain-mindmap {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
  line-height: 1.6;
  color: #333;
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
}

/* 头部样式 */
.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 40px;
  border-radius: 20px;
  margin-bottom: 30px;
  text-align: center;
  box-shadow: 0 20px 60px rgba(0,0,0,0.1);
}

.title {
  font-size: 2.5rem;
  margin-bottom: 10px;
  font-weight: 800;
}

.subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
  margin-bottom: 30px;
}

/* 统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 20px;
  margin-top: 30px;
}

.stat-card {
  background: rgba(255,255,255,0.1);
  padding: 20px;
  border-radius: 15px;
  backdrop-filter: blur(10px);
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-value {
  font-size: 2.5rem;
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.8;
}

/* 技术栈 */
.tech-stack-section {
  background: white;
  border-radius: 15px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.05);
}

.section-title {
  font-size: 1.8rem;
  color: #667eea;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 3px solid #667eea;
}

.tech-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tech-tag {
  background: #e9ecef;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.9rem;
  color: #495057;
  transition: all 0.3s ease;
}

.tech-tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 3px 10px rgba(0,0,0,0.1);
}

.tech-tag.primary {
  background: #667eea;
  color: white;
  font-weight: 600;
}

/* 思维导图容器 */
.mindmap-container {
  background: white;
  border-radius: 15px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.05);
  overflow: hidden;
}

.mindmap-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 15px;
}

.mindmap-controls {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.control-btn {
  background: #667eea;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: all 0.3s ease;
}

.control-btn:hover {
  background: #5a67d8;
  transform: translateY(-2px);
}

.control-btn .icon {
  font-size: 1.1rem;
}

.mermaid-diagram {
  background: #f8f9fa;
  border-radius: 10px;
  padding: 20px;
  overflow: auto;
  min-height: 500px;
  border: 2px solid #e9ecef;
  transition: transform 0.3s ease;
}

/* 学习阶段 */
.phases-section {
  margin-bottom: 30px;
}

.phases-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.phase-card {
  background: white;
  border-radius: 15px;
  padding: 25px;
  border-left: 5px solid;
  box-shadow: 0 3px 10px rgba(0,0,0,0.08);
  transition: transform 0.3s ease;
}

.phase-card:hover {
  transform: translateY(-5px);
}

.phase-1 { border-left-color: #4CAF50; }
.phase-2 { border-left-color: #2196F3; }
.phase-3 { border-left-color: #FF9800; }
.phase-4 { border-left-color: #9C27B0; }

.phase-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.phase-title {
  font-size: 1.3rem;
  font-weight: bold;
  color: #333;
}

.phase-duration {
  background: #f0f0f0;
  padding: 5px 12px;
  border-radius: 15px;
  font-size: 0.9rem;
  color: #666;
}

.phase-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.phase-step {
  padding: 15px;
  background: #f8f9fa;
  border-radius: 10px;
  border-left: 3px solid #667eea;
}

.step-title {
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
  font-size: 1.1rem;
}

.step-desc {
  color: #666;
  font-size: 0.95rem;
  margin-bottom: 10px;
}

.step-tech {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.tech-badge {
  background: #e9ecef;
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  color: #495057;
}

/* 验证策略 */
.validation-section {
  background: white;
  border-radius: 15px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.05);
}

.validation-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
}

.validation-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 10px;
  transition: transform 0.3s ease;
}

.validation-item:hover {
  transform: translateX(5px);
}

.validation-icon {
  font-size: 1.5rem;
}

.validation-text {
  font-size: 1rem;
}

/* 资源链接 */
.resources-section {
  background: white;
  border-radius: 15px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.05);
}

.resources-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.resource-link {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 10px;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.resource-link:hover {
  background: white;
  border-color: #667eea;
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.1);
}

.resource-icon {
  font-size: 2rem;
}

.resource-content {
  flex: 1;
}

.resource-title {
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.resource-desc {
  color: #666;
  font-size: 0.9rem;
}

/* 页脚 */
.footer {
  text-align: center;
  padding: 30px;
  background: white;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.05);
}

.footer-text {
  color: #666;
  margin-bottom: 10px;
}

.footer-text a {
  color: #667eea;
  text-decoration: none;
}

.footer-text a:hover {
  text-decoration: underline;
}

.footer-note {
  color: #888;
  font-size: 0.9rem;
  font-style: italic;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .title {
    font-size: 2rem;
  }
  
  .subtitle {
    font-size: 1rem;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .mindmap-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .phases-grid {
    grid-template-columns: 1fr;
  }
  
  .validation-content {
    grid-template-columns: 1fr;
  }
  
  .resources-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .header {
    padding: 20px;
  }
  
  .title {
    font-size: 1.5rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .tech-tags {
    justify-content: center;
  }
  
  .mindmap-controls {
    width: 100%;
    justify-content: center;
  }
}
</style>

<!-- 全局Mermaid样式 -->
<style>
.mermaid {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
}

.mermaid .node rect,
.mermaid .node circle,
.mermaid .node ellipse,
.mermaid .node polygon {
  fill: #667eea;
  stroke: #5a67d8;
  stroke-width: 2px;
}

.mermaid .node.clickable {
  cursor: pointer;
}

.mermaid .cluster rect {
  fill: rgba(102, 126, 234, 0.1);
  stroke: rgba(102, 126, 234, 0.3);
  stroke-width: 1px;
  rx: 10;
  ry: 10;
}

.mermaid .edgePath .path {
  stroke: #667eea;
  stroke-width: 2px;
}

.mermaid .edgeLabel {
  background-color: white;
  padding: 2px 5px;
  border-radius: 3px;
  font-size: 12px;
}

.mermaid .label {
  color: white;
  font-weight: 600;
}

.mermaid .label text {
  fill: white;
}

/* 验证节点样式 */
.mermaid .node.diamond {
  fill: #4CAF50;
  stroke: #45a049;
}

.mermaid .node.diamond .label {
  color: white;
}
</style>