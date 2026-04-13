# Agent Learning Platform - GitHub推送脚本
# 作者: 小老虎 🐯
# 日期: 2026-04-13

Write-Host "🚀 Agent Learning Platform - GitHub推送脚本" -ForegroundColor Cyan
Write-Host "=" * 60

# 检查当前目录
$currentDir = Get-Location
Write-Host "当前目录: $currentDir" -ForegroundColor Yellow

# 检查Git仓库状态
Write-Host "`n📊 检查Git仓库状态..." -ForegroundColor Cyan
git status

# 显示提交历史
Write-Host "`n📜 提交历史:" -ForegroundColor Cyan
git log --oneline -5

# 提示用户输入GitHub仓库URL
Write-Host "`n🔗 请提供GitHub仓库URL:" -ForegroundColor Yellow
Write-Host "格式: https://github.com/用户名/仓库名.git" -ForegroundColor Gray
Write-Host "示例: https://github.com/your-username/agent-learning-platform.git" -ForegroundColor Gray
$repoUrl = Read-Host "请输入GitHub仓库URL"

if (-not $repoUrl) {
    Write-Host "❌ 未提供仓库URL，退出脚本" -ForegroundColor Red
    exit 1
}

# 添加远程仓库
Write-Host "`n➕ 添加远程仓库..." -ForegroundColor Cyan
git remote add origin $repoUrl

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  远程仓库可能已存在，尝试更新..." -ForegroundColor Yellow
    git remote set-url origin $repoUrl
}

# 推送代码到GitHub
Write-Host "`n⬆️  推送代码到GitHub..." -ForegroundColor Cyan
Write-Host "这将推送 master 分支到 origin 远程仓库" -ForegroundColor Gray

$confirm = Read-Host "确认推送? (y/n)"
if ($confirm -ne 'y') {
    Write-Host "❌ 用户取消推送" -ForegroundColor Red
    exit 0
}

Write-Host "正在推送..." -ForegroundColor Green
git push -u origin master

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ 代码推送成功!" -ForegroundColor Green
    Write-Host "仓库地址: $repoUrl" -ForegroundColor Cyan
    
    # 显示推送后的状态
    Write-Host "`n📊 推送后状态:" -ForegroundColor Cyan
    git remote -v
    git branch -vv
    
    Write-Host "`n🎉 恭喜! Agent Learning Platform 项目已成功推送到GitHub!" -ForegroundColor Green
    Write-Host "现在你可以:" -ForegroundColor Yellow
    Write-Host "1. 访问仓库页面查看代码" -ForegroundColor Gray
    Write-Host "2. 分享给其他开发者" -ForegroundColor Gray
    Write-Host "3. 开始接受贡献" -ForegroundColor Gray
    Write-Host "4. 设置GitHub Actions CI/CD" -ForegroundColor Gray
} else {
    Write-Host "`n❌ 推送失败，可能的原因:" -ForegroundColor Red
    Write-Host "1. 仓库URL错误" -ForegroundColor Gray
    Write-Host "2. 没有权限推送" -ForegroundColor Gray
    Write-Host "3. 网络连接问题" -ForegroundColor Gray
    Write-Host "4. 需要先创建GitHub仓库" -ForegroundColor Gray
    
    Write-Host "`n💡 解决方案:" -ForegroundColor Yellow
    Write-Host "1. 确保GitHub仓库已创建" -ForegroundColor Gray
    Write-Host "2. 检查仓库URL是否正确" -ForegroundColor Gray
    Write-Host "3. 确认有推送权限" -ForegroundColor Gray
    Write-Host "4. 手动创建仓库后重试" -ForegroundColor Gray
}

Write-Host "`n" + "=" * 60
Write-Host "脚本执行完成" -ForegroundColor Cyan