# Agent Learning Platform - 前后端分离架构推送脚本
# 作者: 小老虎 🐯
# 日期: 2026-04-13

Write-Host "🚀 Agent Learning Platform - 前后端分离架构推送脚本" -ForegroundColor Cyan
Write-Host "=" * 70

# 显示项目信息
Write-Host "`n📊 项目信息:" -ForegroundColor Yellow
Write-Host "项目名称: Agent Learning Platform" -ForegroundColor Gray
Write-Host "架构: 前后端分离 (Frontend + Backend)" -ForegroundColor Gray
Write-Host "前端技术栈: Vue 3 + TypeScript + Vite" -ForegroundColor Gray
Write-Host "后端技术栈: FastAPI + LangChain + OpenClaw" -ForegroundColor Gray
Write-Host "许可证: MIT License" -ForegroundColor Gray

# 检查当前目录
$currentDir = Get-Location
Write-Host "`n📁 当前目录: $currentDir" -ForegroundColor Cyan

# 检查项目结构
Write-Host "`n🔍 检查项目结构..." -ForegroundColor Cyan

$folders = @("frontend", "backend", "docs", "scripts", "docker")
foreach ($folder in $folders) {
    if (Test-Path $folder) {
        Write-Host "  ✅ $folder 目录存在" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  $folder 目录不存在" -ForegroundColor Yellow
    }
}

# 检查关键文件
$files = @("README.md", "ARCHITECTURE.md", ".gitignore", "LICENSE")
foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file 文件存在" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  $file 文件不存在" -ForegroundColor Yellow
    }
}

# 检查Git状态
Write-Host "`n🔍 检查Git状态..." -ForegroundColor Cyan
try {
    $gitStatus = git status 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Git仓库已初始化" -ForegroundColor Green
        
        # 显示提交历史
        Write-Host "`n📜 提交历史 (最近5次):" -ForegroundColor Cyan
        git log --oneline -5
        
        # 显示未提交的更改
        $changes = git status --porcelain
        if ($changes) {
            Write-Host "`n📝 未提交的更改:" -ForegroundColor Yellow
            $changes | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
        } else {
            Write-Host "`n✅ 没有未提交的更改" -ForegroundColor Green
        }
    }
} catch {
    Write-Host "  ❌ Git未初始化或出错" -ForegroundColor Red
}

# 提示用户输入GitHub信息
Write-Host "`n🔑 需要以下信息推送到GitHub:" -ForegroundColor Yellow

# 1. GitHub仓库URL
Write-Host "`n1️⃣ GitHub仓库URL:" -ForegroundColor Green
Write-Host "   - 格式: https://github.com/你的用户名/agent-learning-platform.git" -ForegroundColor Gray
Write-Host "   - 如果你还没有创建仓库，请先访问 https://github.com/new" -ForegroundColor Gray
Write-Host "   - 仓库名称建议: agent-learning-platform" -ForegroundColor Gray

# 2. 推送选项
Write-Host "`n2️⃣ 推送选项:" -ForegroundColor Green
Write-Host "   A. 推送所有更改 (包括前后端分离架构)" -ForegroundColor Gray
Write-Host "   B. 只推送架构文档" -ForegroundColor Gray
Write-Host "   C. 手动操作" -ForegroundColor Gray

# 获取用户选择
$choice = Read-Host "`n请选择推送选项 (A/B/C)"

switch ($choice.ToUpper()) {
    "A" {
        Write-Host "`n🚀 选择: 推送所有更改" -ForegroundColor Cyan
        
        # 添加所有文件
        Write-Host "`n📦 添加文件到Git..." -ForegroundColor Cyan
        git add .
        
        # 提交更改
        $commitMessage = "feat: add frontend-backend separated architecture"
        Write-Host "`n💾 提交更改: $commitMessage" -ForegroundColor Cyan
        git commit -m $commitMessage
        
        # 获取仓库URL
        $repoUrl = Read-Host "`n请输入GitHub仓库URL"
        
        if ($repoUrl) {
            # 添加远程仓库
            Write-Host "`n🌐 添加远程仓库..." -ForegroundColor Cyan
            git remote add origin $repoUrl 2>$null
            if ($LASTEXITCODE -ne 0) {
                git remote set-url origin $repoUrl
            }
            
            # 推送代码
            Write-Host "`n🚀 推送到GitHub..." -ForegroundColor Cyan
            git push -u origin master
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "`n🎉 推送成功!" -ForegroundColor Green
                Write-Host "GitHub仓库: $repoUrl" -ForegroundColor Cyan
                
                # 显示后续步骤
                Show-NextSteps $repoUrl
            } else {
                Write-Host "`n❌ 推送失败，请检查网络连接和权限" -ForegroundColor Red
            }
        } else {
            Write-Host "`n⚠️  未提供仓库URL，跳过推送" -ForegroundColor Yellow
        }
    }
    
    "B" {
        Write-Host "`n📄 选择: 只推送架构文档" -ForegroundColor Cyan
        
        # 只添加架构相关文件
        $architectureFiles = @(
            "ARCHITECTURE.md",
            "frontend/README.md",
            "backend/README.md",
            "frontend/",
            "backend/"
        )
        
        foreach ($file in $architectureFiles) {
            if (Test-Path $file) {
                git add $file
                Write-Host "  ✅ 添加: $file" -ForegroundColor Green
            }
        }
        
        # 提交更改
        $commitMessage = "docs: add frontend-backend separated architecture documentation"
        Write-Host "`n💾 提交更改: $commitMessage" -ForegroundColor Cyan
        git commit -m $commitMessage
        
        Write-Host "`n📝 架构文档已提交，可以使用 'git push' 手动推送" -ForegroundColor Cyan
    }
    
    "C" {
        Write-Host "`n🔧 选择: 手动操作" -ForegroundColor Cyan
        Write-Host "`n手动操作命令:" -ForegroundColor Yellow
        Write-Host "1. 添加所有文件: git add ." -ForegroundColor Gray
        Write-Host "2. 提交更改: git commit -m 'feat: add frontend-backend separated architecture'" -ForegroundColor Gray
        Write-Host "3. 添加远程仓库: git remote add origin https://github.com/你的用户名/agent-learning-platform.git" -ForegroundColor Gray
        Write-Host "4. 推送代码: git push -u origin master" -ForegroundColor Gray
    }
    
    default {
        Write-Host "`n❌ 无效选择" -ForegroundColor Red
    }
}

# 显示后续步骤函数
function Show-NextSteps {
    param(
        [string]$repoUrl
    )
    
    Write-Host "`n📋 后续步骤:" -ForegroundColor Yellow
    
    Write-Host "`n1. 🎨 设置GitHub Pages (展示前端)" -ForegroundColor Green
    Write-Host "   - 访问: https://github.com/你的用户名/agent-learning-platform/settings/pages" -ForegroundColor Gray
    Write-Host "   - Source: 选择 'master branch' 或 'docs folder'" -ForegroundColor Gray
    Write-Host "   - 访问地址: https://你的用户名.github.io/agent-learning-platform/" -ForegroundColor Gray
    
    Write-Host "`n2. 🤖 启用GitHub Actions" -ForegroundColor Green
    Write-Host "   - CI/CD流程已配置在 .github/workflows/" -ForegroundColor Gray
    Write-Host "   - 自动运行测试、构建、部署" -ForegroundColor Gray
    
    Write-Host "`n3. 👥 邀请贡献者" -ForegroundColor Green
    Write-Host "   - Settings → Collaborators" -ForegroundColor Gray
    Write-Host "   - 添加其他开发者参与项目" -ForegroundColor Gray
    
    Write-Host "`n4. 📢 分享项目" -ForegroundColor Green
    Write-Host "   - 在BotLearn社区分享项目" -ForegroundColor Gray
    Write-Host "   - 在技术论坛/社交媒体宣传" -ForegroundColor Gray
    Write-Host "   - 邀请其他开发者参与" -ForegroundColor Gray
    
    Write-Host "`n5. 🚀 开始开发" -ForegroundColor Green
    Write-Host "   - 前端开发: cd frontend && npm install && npm run dev" -ForegroundColor Gray
    Write-Host "   - 后端开发: cd backend && 创建虚拟环境并安装依赖" -ForegroundColor Gray
    Write-Host "   - API集成: 前端通过 localhost:5173 访问后端 localhost:8000" -ForegroundColor Gray
    
    Write-Host "`n🔗 项目链接:" -ForegroundColor Cyan
    Write-Host "GitHub仓库: $repoUrl" -ForegroundColor Gray
    
    $repoName = $repoUrl -replace '^https://github\.com/' -replace '\.git$'
    Write-Host "GitHub Pages: https://$repoName" -ForegroundColor Gray
}

Write-Host "`n" + ("=" * 70) -ForegroundColor Cyan
Write-Host "脚本执行完成" -ForegroundColor Cyan
Write-Host "如需帮助，请查看 ARCHITECTURE.md 文件" -ForegroundColor Gray