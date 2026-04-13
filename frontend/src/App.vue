<template>
  <div id="app">
    <!-- 导航栏 -->
    <AppHeader />
    
    <!-- 主要内容 -->
    <main class="main-content">
      <router-view />
    </main>
    
    <!-- 页脚 -->
    <footer class="app-footer">
      <div class="footer-content">
        <div class="footer-left">
          <div class="footer-logo">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="#3b82f6" />
              <path d="M2 17L12 22L22 17" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
              <path d="M2 12L12 17L22 12" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
            <span>Agent Learning Platform</span>
          </div>
          <p class="footer-description">
            一个现代化的AI Agent学习平台，帮助开发者掌握前沿技术
          </p>
        </div>
        
        <div class="footer-right">
          <div class="footer-links">
            <div class="link-group">
              <h4>产品</h4>
              <a href="#">功能</a>
              <a href="#">定价</a>
              <a href="#">API</a>
            </div>
            <div class="link-group">
              <h4>资源</h4>
              <a href="#">文档</a>
              <a href="#">教程</a>
              <a href="#">博客</a>
            </div>
            <div class="link-group">
              <h4>社区</h4>
              <a href="#">GitHub</a>
              <a href="#">Discord</a>
              <a href="#">Twitter</a>
            </div>
          </div>
        </div>
      </div>
      
      <div class="footer-bottom">
        <p>© 2026 Agent Learning Platform. 保留所有权利。</p>
        <div class="footer-bottom-links">
          <a href="#">隐私政策</a>
          <a href="#">服务条款</a>
          <a href="#">Cookie政策</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import AppHeader from './components/Layout/AppHeader.vue'
</script>

<style>
#app {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  background: #f8fafc;
}

/* 页脚样式 */
.app-footer {
  background: white;
  border-top: 1px solid #f0f2f5;
  padding: 40px 32px 24px;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 48px;
  margin-bottom: 32px;
}

.footer-left {
  flex: 1;
  max-width: 400px;
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.footer-logo span {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
}

.footer-description {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
}

.footer-right {
  flex: 2;
}

.footer-links {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 48px;
}

.link-group h4 {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 16px;
}

.link-group a {
  display: block;
  font-size: 14px;
  color: #666;
  text-decoration: none;
  margin-bottom: 8px;
  transition: color 0.2s ease;
}

.link-group a:hover {
  color: #3b82f6;
}

.footer-bottom {
  max-width: 1200px;
  margin: 0 auto;
  padding-top: 24px;
  border-top: 1px solid #f0f2f5;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-bottom p {
  font-size: 14px;
  color: #94a3b8;
}

.footer-bottom-links {
  display: flex;
  gap: 24px;
}

.footer-bottom-links a {
  font-size: 14px;
  color: #94a3b8;
  text-decoration: none;
  transition: color 0.2s ease;
}

.footer-bottom-links a:hover {
  color: #3b82f6;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .app-footer {
    padding: 32px 20px 20px;
  }
  
  .footer-content {
    flex-direction: column;
    gap: 32px;
  }
  
  .footer-links {
    grid-template-columns: repeat(2, 1fr);
    gap: 32px;
  }
  
  .footer-bottom {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
}
</style>