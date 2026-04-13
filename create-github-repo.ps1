# Agent Learning Platform - GitHub仓库创建脚本
# 作者: 小老虎 🐯
# 日期: 2026-04-13

Write-Host "🚀 Agent Learning Platform - GitHub仓库创建脚本" -ForegroundColor Cyan
Write-Host "=" * 70

# 显示项目信息
Write-Host "`n📊 项目信息:" -ForegroundColor Yellow
Write-Host "项目名称: Agent Learning Platform" -ForegroundColor Gray
Write-Host "项目描述: A complete learning platform for AI Agent development" -ForegroundColor Gray
Write-Host "技术栈: Vue 3 + TypeScript + FastAPI + LangChain + OpenClaw" -ForegroundColor Gray
Write-Host "许可证: MIT License" -ForegroundColor Gray
Write-Host "创建者: LittleTiger 🐯" -ForegroundColor Gray

# 检查Git状态
Write-Host "`n🔍 检查Git状态..." -ForegroundColor Cyan
git status
Write-Host ""

# 显示提交历史
Write-Host "📜 提交历史 (最近5次):" -ForegroundColor Cyan
git log --oneline -5

# 提示用户输入GitHub信息
Write-Host "`n🔑 需要以下信息创建GitHub仓库:" -ForegroundColor Yellow

# 1. GitHub用户名
Write-Host "`n1️⃣ GitHub用户名:" -ForegroundColor Green
Write-Host "   - 这是你在GitHub上的用户名" -ForegroundColor Gray
Write-Host "   - 示例: panda-developer, tigerkin, your-username" -ForegroundColor Gray
$githubUsername = Read-Host "请输入你的GitHub用户名"

if (-not $githubUsername) {
    Write-Host "❌ 未提供GitHub用户名，退出脚本" -ForegroundColor Red
    exit 1
}

# 2. GitHub个人访问令牌
Write-Host "`n2️⃣ GitHub个人访问令牌 (Personal Access Token):" -ForegroundColor Green
Write-Host "   - 需要创建仓库的权限" -ForegroundColor Gray
Write-Host "   - 如何获取: https://github.com/settings/tokens" -ForegroundColor Gray
Write-Host "   - 权限要求: repo (完全控制私有仓库)" -ForegroundColor Gray
Write-Host "   - 令牌名称建议: 'agent-learning-platform-create-repo'" -ForegroundColor Gray
$githubToken = Read-Host "请输入GitHub个人访问令牌"

if (-not $githubToken) {
    Write-Host "❌ 未提供GitHub令牌，退出脚本" -ForegroundColor Red
    exit 1
}

# 3. 仓库名称
Write-Host "`n3️⃣ 仓库名称:" -ForegroundColor Green
Write-Host "   - 建议: agent-learning-platform" -ForegroundColor Gray
Write-Host "   - 也可以使用其他名称" -ForegroundColor Gray
$repoName = Read-Host "请输入仓库名称 (默认: agent-learning-platform)"
if (-not $repoName) { $repoName = "agent-learning-platform" }

# 4. 仓库描述
Write-Host "`n4️⃣ 仓库描述:" -ForegroundColor Green
Write-Host "   - 建议: A complete learning platform for AI Agent development based on LangChain + OpenClaw + Vue 3" -ForegroundColor Gray
$repoDescription = Read-Host "请输入仓库描述"
if (-not $repoDescription) { 
    $repoDescription = "A complete learning platform for AI Agent development based on LangChain + OpenClaw + Vue 3"
}

# 5. 仓库可见性
Write-Host "`n5️⃣ 仓库可见性:" -ForegroundColor Green
Write-Host "   - public: 公开仓库 (推荐，便于分享和协作)" -ForegroundColor Gray
Write-Host "   - private: 私有仓库 (仅限邀请的用户访问)" -ForegroundColor Gray
$repoVisibility = Read-Host "请输入可见性 (public/private，默认: public)"
if (-not $repoVisibility) { $repoVisibility = "public" }

# 确认信息
Write-Host "`n📋 确认创建信息:" -ForegroundColor Yellow
Write-Host "GitHub用户名: $githubUsername" -ForegroundColor Gray
Write-Host "仓库名称: $repoName" -ForegroundColor Gray
Write-Host "仓库描述: $repoDescription" -ForegroundColor Gray
Write-Host "可见性: $repoVisibility" -ForegroundColor Gray
Write-Host "仓库URL: https://github.com/$githubUsername/$repoName" -ForegroundColor Gray

$confirm = Read-Host "`n确认创建GitHub仓库? (y/n)"
if ($confirm -ne 'y') {
    Write-Host "❌ 用户取消创建" -ForegroundColor Red
    exit 0
}

# 创建GitHub仓库
Write-Host "`n🔄 正在创建GitHub仓库..." -ForegroundColor Cyan

# 构建API请求
$apiUrl = "https://api.github.com/user/repos"
$headers = @{
    "Authorization" = "token $githubToken"
    "Accept" = "application/vnd.github.v3+json"
    "User-Agent" = "Agent-Learning-Platform-Creator"
}

$body = @{
    name = $repoName
    description = $repoDescription
    private = ($repoVisibility -eq "private")
    auto_init = $false  # 不自动初始化README
    license_template = "mit"
    gitignore_template = "Node"
} | ConvertTo-Json

try {
    Write-Host "发送请求到GitHub API..." -ForegroundColor Gray
    $response = Invoke-RestMethod -Uri $apiUrl -Method Post -Headers $headers -Body $body -ContentType "application/json"
    
    Write-Host "✅ GitHub仓库创建成功!" -ForegroundColor Green
    Write-Host "仓库URL: $($response.html_url)" -ForegroundColor Cyan
    Write-Host "SSH URL: $($response.ssh_url)" -ForegroundColor Cyan
    Write-Host "HTTPS URL: $($response.clone_url)" -ForegroundColor Cyan
    
    # 设置远程仓库并推送
    $cloneUrl = $response.clone_url
    
    Write-Host "`n🔗 设置远程仓库..." -ForegroundColor Cyan
    git remote add origin $cloneUrl
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️  远程仓库可能已存在，尝试更新..." -ForegroundColor Yellow
        git remote set-url origin $cloneUrl
    }
    
    Write-Host "✅ 远程仓库设置完成" -ForegroundColor Green
    
    # 推送代码
    Write-Host "`n⬆️  推送代码到GitHub..." -ForegroundColor Cyan
    git push -u origin master
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n🎉 恭喜! 代码推送成功!" -ForegroundColor Green
        Write-Host "项目已成功发布到GitHub!" -ForegroundColor Cyan
        
        # 显示成功信息
        Write-Host "`n🌟 项目发布完成!" -ForegroundColor Yellow
        Write-Host "访问地址: $($response.html_url)" -ForegroundColor Cyan
        Write-Host "克隆命令: git clone $cloneUrl" -ForegroundColor Gray
        Write-Host "Web界面: $($response.html_url)/web-ui/dashboard/index.html" -ForegroundColor Gray
        
        Write-Host "`n📊 下一步操作建议:" -ForegroundColor Green
        Write-Host "1. 访问仓库页面查看代码" -ForegroundColor Gray
        Write-Host "2. 设置GitHub Pages展示仪表板" -ForegroundColor Gray
        Write-Host "3. 在BotLearn社区分享项目" -ForegroundColor Gray
        Write-Host "4. 邀请其他开发者贡献" -ForegroundColor Gray
        Write-Host "5. 启用GitHub Actions CI/CD" -ForegroundColor Gray
        
        Write-Host "`n🔧 快速访问链接:" -ForegroundColor Yellow
        Write-Host "• 仓库主页: $($response.html_url)" -ForegroundColor Gray
        Write-Host "• 代码浏览: $($response.html_url)/tree/master" -ForegroundColor Gray
        Write-Host "• Issues: $($response.html_url)/issues" -ForegroundColor Gray
        Write-Host "• Pull Requests: $($response.html_url)/pulls" -ForegroundColor Gray
        Write-Host "• Actions: $($response.html_url)/actions" -ForegroundColor Gray
        Write-Host "• Settings: $($response.html_url)/settings" -ForegroundColor Gray
        
    } else {
        Write-Host "`n❌ 代码推送失败" -ForegroundColor Red
        Write-Host "但仓库已创建成功，你可以手动推送:" -ForegroundColor Yellow
        Write-Host "git remote add origin $cloneUrl" -ForegroundColor Gray
        Write-Host "git push -u origin master" -ForegroundColor Gray
    }
    
} catch {
    Write-Host "`n❌ 创建GitHub仓库失败:" -ForegroundColor Red
    Write-Host "错误信息: $($_.Exception.Message)" -ForegroundColor Gray
    
    Write-Host "`n💡 可能的原因和解决方案:" -ForegroundColor Yellow
    Write-Host "1. GitHub令牌无效或过期" -ForegroundColor Gray
    Write-Host "   - 重新生成令牌: https://github.com/settings/tokens" -ForegroundColor Gray
    Write-Host "   - 确保有 'repo' 权限" -ForegroundColor Gray
    Write-Host "2. 仓库名称已存在" -ForegroundColor Gray
    Write-Host "   - 尝试不同的仓库名称" -ForegroundColor Gray
    Write-Host "3. 网络连接问题" -ForegroundColor Gray
    Write-Host "   - 检查网络连接" -ForegroundColor Gray
    Write-Host "   - 稍后重试" -ForegroundColor Gray
    Write-Host "4. GitHub API限制" -ForegroundColor Gray
    Write-Host "   - 等待一段时间后重试" -ForegroundColor Gray
    
    Write-Host "`n🔧 手动创建方法:" -ForegroundColor Cyan
    Write-Host "1. 访问 https://github.com/new" -ForegroundColor Gray
    Write-Host "2. 填写仓库信息:" -ForegroundColor Gray
    Write-Host "   - Repository name: $repoName" -ForegroundColor Gray
    Write-Host "   - Description: $repoDescription" -ForegroundColor Gray
    Write-Host "   - Visibility: $repoVisibility" -ForegroundColor Gray
    Write-Host "   - 不要勾选 'Initialize with README'" -ForegroundColor Gray
    Write-Host "   - Add .gitignore: Node" -ForegroundColor Gray
    Write-Host "   - Add a license: MIT License" -ForegroundColor Gray
    Write-Host "3. 点击 'Create repository'" -ForegroundColor Gray
    Write-Host "4. 使用之前的推送脚本推送代码" -ForegroundColor Gray
}

Write-Host "`n" + "=" * 70
Write-Host "脚本执行完成" -ForegroundColor Cyan