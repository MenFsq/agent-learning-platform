# Agent Learning Platform - 设计标准规范

## 🎨 **设计系统概述**

本规范定义了Agent Learning Platform前端项目的设计标准，确保所有组件和页面保持一致的视觉风格和用户体验。

## 🎯 **核心设计原则**

### **1. 简洁科技风**
- 白色背景 + 浅灰辅助色
- 蓝紫色渐变主色调
- 清晰的视觉层次
- 适度的科技感装饰

### **2. 一致性**
- 所有组件遵循相同设计语言
- 统一的间距、圆角、阴影
- 一致的交互反馈

### **3. 可用性**
- 清晰的视觉反馈
- 直观的导航结构
- 响应式设计支持

## 🎨 **颜色系统**

### **主色调**
```
主色: #3b82f6 (蓝色)
辅色: #8b5cf6 (紫色)
```

### **渐变方案**
```css
/* 主要渐变 */
background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);

/* 次要渐变 */
background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(139, 92, 246, 0.1));
```

### **中性色**
```
背景色: #f8fafc
卡片背景: #ffffff
边框色: #e2e8f0
文字主色: #1a1a1a
文字次色: #64748b
文字辅助色: #94a3b8
```

### **功能色**
```
成功: #10b981
警告: #f59e0b
错误: #ef4444
信息: #3b82f6
```

## 📐 **间距系统**

### **基础单位**
```
基础单位: 4px
```

### **间距规范**
```css
/* 小间距 */
padding: 8px;    /* 2u */
margin: 8px;     /* 2u */

/* 中间距 */
padding: 16px;   /* 4u */
margin: 16px;    /* 4u */

/* 大间距 */
padding: 24px;   /* 6u */
margin: 24px;    /* 6u */

/* 超大间距 */
padding: 32px;   /* 8u */
margin: 32px;    /* 8u */
```

### **网格间距**
```css
/* 卡片内部 */
gap: 16px;       /* 4u */

/* 卡片之间 */
gap: 24px;       /* 6u */

/* 主要内容区域 */
gap: 32px;       /* 8u */
```

## 🔲 **圆角规范**

### **圆角尺寸**
```css
/* 小圆角 - 按钮、标签 */
border-radius: 8px;     /* 2u */

/* 中圆角 - 卡片、输入框 */
border-radius: 12px;    /* 3u */

/* 大圆角 - 模态框、大卡片 */
border-radius: 16px;    /* 4u */

/* 超大圆角 - 特殊元素 */
border-radius: 20px;    /* 5u */
```

## 🌈 **阴影系统**

### **阴影层级**
```css
/* Level 1 - 轻微阴影 */
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);

/* Level 2 - 中等阴影 */
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);

/* Level 3 - 强调阴影 */
box-shadow: 0 8px 24px rgba(59, 130, 246, 0.15);

/* Level 4 - 悬浮阴影 */
box-shadow: 0 12px 32px rgba(59, 130, 246, 0.2);
```

### **悬停效果**
```css
/* 卡片悬停 */
.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.15);
  border-color: #3b82f6;
}

/* 按钮悬停 */
.button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
}
```

## 🎭 **动画规范**

### **过渡时间**
```css
/* 快速过渡 */
transition: all 0.2s ease;

/* 标准过渡 */
transition: all 0.3s ease;

/* 慢速过渡 */
transition: all 0.5s ease;
```

### **动画类型**
```css
/* 淡入 */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* 上滑 */
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 脉冲 */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
```

## 📱 **响应式设计**

### **断点定义**
```css
/* 移动端优先 */
@media (min-width: 640px) { /* sm */ }
@media (min-width: 768px) { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }
```

### **布局调整**
```css
/* 移动端 */
.stats-grid {
  grid-template-columns: 1fr;
}

/* 平板端 */
@media (min-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* 桌面端 */
@media (min-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

## 🧩 **组件规范**

### **1. 卡片组件**
```css
.card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.15);
  border-color: #3b82f6;
}
```

### **2. 按钮组件**
```css
.button {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 12px 24px;
  color: #3b82f6;
  font-weight: 600;
  transition: all 0.3s ease;
}

.button:hover {
  background: #f8fafc;
  border-color: #3b82f6;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}

.button.primary {
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  color: white;
  border: none;
}
```

### **3. 输入框组件**
```css
.input {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 12px 16px;
  background: white;
  transition: all 0.3s ease;
}

.input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  outline: none;
}
```

## 📝 **排版规范**

### **字体系统**
```
主字体: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif
代码字体: 'JetBrains Mono', 'Courier New', monospace
```

### **字体大小**
```css
/* 标题 */
h1 { font-size: 32px; font-weight: 800; }
h2 { font-size: 24px; font-weight: 700; }
h3 { font-size: 20px; font-weight: 600; }
h4 { font-size: 18px; font-weight: 600; }

/* 正文 */
.body-large { font-size: 16px; }
.body { font-size: 14px; }
.body-small { font-size: 12px; }

/* 特殊 */
.caption { font-size: 11px; }
```

### **行高**
```css
/* 标题 */
h1, h2, h3 { line-height: 1.2; }

/* 正文 */
p, span { line-height: 1.5; }

/* 列表 */
li { line-height: 1.6; }
```

## 🎯 **使用指南**

### **开发流程**
1. **设计评审** - 确保符合设计规范
2. **组件开发** - 使用标准组件库
3. **样式实现** - 遵循颜色、间距、圆角规范
4. **交互实现** - 添加标准动画和反馈
5. **响应式测试** - 测试不同屏幕尺寸
6. **代码审查** - 确保规范一致性

### **质量检查清单**
- [ ] 颜色使用符合规范
- [ ] 间距使用4px倍数
- [ ] 圆角尺寸正确
- [ ] 阴影层级合适
- [ ] 动画过渡自然
- [ ] 响应式适配良好
- [ ] 交互反馈清晰
- [ ] 代码结构清晰

## 🔄 **更新记录**

### **v1.0.0 - 2026-04-14**
- 初始设计规范建立
- 定义颜色、间距、圆角系统
- 建立组件设计标准
- 制定响应式设计规范

---

**维护者**: 小老虎 🐯  
**最后更新**: 2026-04-14  
**版本**: 1.0.0