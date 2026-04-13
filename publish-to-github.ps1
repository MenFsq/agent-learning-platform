# Agent Learning Platform - GitHub发布向导
# 作者: 小老虎 🐯
# 日期: 2026-04-13

Write-Host "🚀 Agent Learning Platform - GitHub发布向导" -ForegroundColor Cyan
Write-Host "=" * 70

# 显示项目信息
Write-Host "`n📊 项目概览:" -ForegroundColor Yellow
Write-Host "项目名称: Agent Learning Platform" -ForegroundColor Gray
Write-Host "描述: 基于LangChain + OpenClaw + Vue 3的AI Agent学习平台" -ForegroundColor Gray
Write-Host "文件数量: 9个核心文件" -ForegroundColor Gray
Write-Host "代码行数: ~95,000行" -ForegroundColor Gray
Write-Host "提交次数: 7次" -ForegroundColor Gray
Write-Host "许可证: MIT License" -ForegroundColor Gray

# 显示发布选项
Write-Host "`n🎯 选择发布方式:" -ForegroundColor Green
Write-Host "1️⃣ 全自动发布 (推荐)" -ForegroundColor Cyan
Write-Host "   - 自动创建GitHub仓库" -ForegroundColor Gray
Write-Host "   - 自动配置远程仓库" -ForegroundColor Gray
Write-Host "   - 自动推送所有代码" -ForegroundColor Gray
Write-Host "   - 需要GitHub个人访问令牌" -ForegroundColor Gray

Write-Host "`n2️⃣ 半自动发布" -ForegroundColor Cyan
Write-Host "   - 手动创建GitHub仓库" -ForegroundColor Gray
Write-Host "   - 使用脚本推送代码" -ForegroundColor Gray
Write-Host "   - 需要GitHub仓库URL" -ForegroundColor Gray

Write-Host "`n3️⃣ 手动发布" -ForegroundColor Cyan
Write-Host "   - 完全手动操作" -ForegroundColor Gray
Write-Host "   - 适合熟悉Git/GitHub的用户" -ForegroundColor Gray

Write-Host "`n4️⃣ 查看帮助文档" -ForegroundColor Cyan
Write-Host "   - 查看详细发布指南" -ForegroundColor Gray
Write-Host "   - 获取故障排除帮助" -ForegroundColor Gray

# 获取用户选择
$choice = Read-Host "`n请选择发布方式 (1-4，默认: 1)"
if (-not $choice) { $choice = "1" }

switch ($choice) {
    "1" {
        Write-Host "`n🚀 选择: 全自动发布" -ForegroundColor Green
        Write-Host "正在启动全自动发布脚本..." -ForegroundColor Gray
        .\create-github-repo.ps1
    }
    "2" {
        Write-Host "`n⚡ 选择: 半自动发布" -ForegroundColor Green
        Write-Host "正在启动代码推送脚本..." -ForegroundColor Gray
        .\push-to-github.ps1
    }
    "3" {
        Write-Host "`n🔧 选择: 手动发布" -ForegroundColor Green
        Write-Host "`n📋 手动发布步骤:" -ForegroundColor Yellow
        
        Write-Host "`n步骤1: 创建GitHub仓库" -ForegroundColor Cyan
        Write-Host "1. 访问 https://github.com/new" -ForegroundColor Gray
        Write-Host "2. 填写仓库信息:" -ForegroundColor Gray
        Write-Host "   - Repository name: agent-learning-platform" -ForegroundColor Gray
        Write-Host "   - Description: A complete learning platform for AI Agent development" -ForegroundColor Gray
        Write-Host "   - Visibility: public (推荐)" -ForegroundColor Gray
        Write-Host "   - 不要勾选 'Initialize with README'" -ForegroundColor Gray
        Write-Host "   - Add .gitignore: Node" -ForegroundColor Gray
        Write-Host "   - Add a license: MIT License" -ForegroundColor Gray
        Write-Host "3. 点击 'Create repository'" -ForegroundColor Gray
        
        Write-Host "`n步骤2: 获取仓库URL" -ForegroundColor Cyan
        Write-Host "创建后你会看到类似这样的URL:" -ForegroundColor Gray
        Write-Host "https://github.com/你的用户名/agent-learning-platform.git" -ForegroundColor Gray
        
        Write-Host "`n步骤3: 添加远程仓库" -ForegroundColor Cyan
        Write-Host "在项目目录中运行:" -ForegroundColor Gray
        Write-Host "git remote add origin https://github.com/你的用户名/agent-learning-platform.git" -ForegroundColor Gray
        
        Write-Host "`n步骤4: 推送代码" -ForegroundColor Cyan
        Write-Host "git push -u origin master" -ForegroundColor Gray
        
        Write-Host "`n步骤5: 验证推送" -ForegroundColor Cyan
        Write-Host "git remote -v" -ForegroundColor Gray
        Write-Host "git branch -vv" -ForegroundColor Gray
        
        Write-Host "`n🎉 完成! 访问你的GitHub仓库查看代码。" -ForegroundColor Green
    }
    "4" {
        Write-Host "`n📚 选择: 查看帮助文档" -ForegroundColor Green
        
        Write-Host "`n📖 可用文档:" -ForegroundColor Yellow
        Write-Host "1. GITHUB-SETUP.md - GitHub设置完整指南" -ForegroundColor Gray
        Write-Host "2. README.md - 项目说明文档" -ForegroundColor Gray
        Write-Host "3. CONTRIBUTING.md - 贡献指南" -ForegroundColor Gray
        Write-Host "4. PROJECT-STRUCTURE.md - 项目结构文档" -ForegroundColor Gray
        
        Write-Host "`n🔧 可用脚本:" -ForegroundColor Yellow
        Write-Host "1. create-github-repo.ps1 - 全自动创建和推送" -ForegroundColor Gray
        Write-Host "2. push-to-github.ps1 - 半自动推送" -ForegroundColor Gray
        Write-Host "3. setup-project.sh - 项目设置脚本" -ForegroundColor Gray
        
        Write-Host "`n❓ 常见问题:" -ForegroundColor Yellow
        Write-Host "Q: 如何获取GitHub个人访问令牌?" -ForegroundColor Gray
        Write-Host "A: 访问 https://github.com/settings/tokens" -ForegroundColor Gray
        Write-Host "   创建新令牌，选择 'repo' 权限" -ForegroundColor Gray
        
        Write-Host "`nQ: 推送时出现权限错误?" -ForegroundColor Gray
        Write-Host "A: 1. 检查仓库URL是否正确" -ForegroundColor Gray
        Write-Host "   2. 确保你有推送权限" -ForegroundColor Gray
        Write-Host "   3. 检查GitHub令牌是否有效" -ForegroundColor Gray
        
        Write-Host "`nQ: 如何设置GitHub Pages?" -ForegroundColor Gray
        Write-Host "A: 仓库 Settings → Pages → Source: master branch" -ForegroundColor Gray
        Write-Host "   访问: https://你的用户名.github.io/agent-learning-platform/web-ui/dashboard/" -ForegroundColor Gray
        
        Write-Host "`n💡 建议:" -ForegroundColor Cyan
        Write-Host "• 首次发布建议使用 '全自动发布' (选项1)" -ForegroundColor Gray
        Write-Host "• 确保GitHub令牌有 'repo' 权限" -ForegroundColor Gray
        Write-Host "• 公开仓库更易于分享和协作" -ForegroundColor Gray
        Write-Host "• 推送后记得在BotLearn社区分享" -ForegroundColor Gray
    }
    default {
        Write-Host "❌ 无效选择，请重新运行脚本选择1-4" -ForegroundColor Red
    }
}

Write-Host "`n" + "=" * 70
Write-Host "发布向导执行完成" -ForegroundColor Cyan
Write-Host "如有问题，请查看 GITHUB-SETUP.md 文档" -ForegroundColor Gray