# 提交GitHub Actions修复
Write-Host "🚀 提交GitHub Actions部署修复" -ForegroundColor Cyan
Write-Host "=" * 70

# 显示修复内容
Write-Host "`n🔧 修复内容:" -ForegroundColor Yellow
Write-Host "1. 更新部署工作流 (deploy.yml)" -ForegroundColor Gray
Write-Host "   - 使用GitHub Pages官方actions" -ForegroundColor Gray
Write-Host "   - 移除缓存配置避免路径问题" -ForegroundColor Gray
Write-Host "   - 设置NODE_ENV=production环境变量" -ForegroundColor Gray
Write-Host "   - 添加详细构建验证" -ForegroundColor Gray

Write-Host "`n2. 更新CI工作流 (ci.yml)" -ForegroundColor Gray
Write-Host "   - 移除缓存配置" -ForegroundColor Gray

Write-Host "`n3. 更新package.json" -ForegroundColor Gray
Write-Host "   - Node.js版本要求: >=24.0.0" -ForegroundColor Gray

# 检查Git状态
Write-Host "`n🔍 Git状态:" -ForegroundColor Yellow
git status

# 添加文件
Write-Host "`n📦 添加文件..." -ForegroundColor Yellow
git add .
Write-Host "✓ 文件已添加" -ForegroundColor Green

# 提交
Write-Host "`n💾 提交更改..." -ForegroundColor Yellow
git commit -m "fix: 修复GitHub Actions部署错误

- 更新Node.js到24版本
- 使用GitHub Pages官方actions避免缓存问题
- 设置NODE_ENV=production确保正确构建
- 移除有问题的缓存配置
- 添加构建验证步骤"

Write-Host "✓ 提交完成" -ForegroundColor Green

# 推送
Write-Host "`n📤 推送到GitHub..." -ForegroundColor Yellow
git push origin master

Write-Host "`n✅ 修复已提交并推送!" -ForegroundColor Green
Write-Host "=" * 70
Write-Host "🎯 下一步:" -ForegroundColor Cyan
Write-Host "1. 查看GitHub Actions运行状态:" -ForegroundColor Gray
Write-Host "   https://github.com/MenFsq/agent-learning-platform/actions" -ForegroundColor Gray
Write-Host ""
Write-Host "2. 等待部署完成 (约3-5分钟)" -ForegroundColor Gray
Write-Host ""
Write-Host "3. 访问部署的网站:" -ForegroundColor Gray
Write-Host "   https://menfsq.github.io/agent-learning-platform/" -ForegroundColor Gray
Write-Host ""
Write-Host "4. 检查GitHub Pages设置:" -ForegroundColor Gray
Write-Host "   https://github.com/MenFsq/agent-learning-platform/settings/pages" -ForegroundColor Gray