# 测试Node.js版本兼容性
Write-Host "🔧 测试Node.js版本兼容性" -ForegroundColor Cyan
Write-Host "=" * 70

# 检查当前Node.js版本
Write-Host "`n📊 当前系统Node.js版本:" -ForegroundColor Yellow
node --version
npm --version

# 检查前端项目要求
Write-Host "`n📦 前端项目要求:" -ForegroundColor Yellow
$packageJson = Get-Content "frontend\package.json" | ConvertFrom-Json
Write-Host "Node.js要求: $($packageJson.engines.node)" -ForegroundColor Gray
Write-Host "npm要求: $($packageJson.engines.npm)" -ForegroundColor Gray

# 测试构建
Write-Host "`n🔨 测试构建..." -ForegroundColor Yellow
Set-Location "frontend"

# 清理之前的构建
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
    Write-Host "✓ 清理dist目录" -ForegroundColor Green
}

# 安装依赖
Write-Host "安装依赖..." -ForegroundColor Gray
npm ci
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 依赖安装失败" -ForegroundColor Red
    exit 1
}
Write-Host "✓ 依赖安装成功" -ForegroundColor Green

# 构建项目
Write-Host "构建项目..." -ForegroundColor Gray
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 构建失败" -ForegroundColor Red
    exit 1
}
Write-Host "✓ 构建成功" -ForegroundColor Green

# 检查构建输出
Write-Host "`n📁 检查构建输出:" -ForegroundColor Yellow
Set-Location ".."
$distFiles = Get-ChildItem "frontend\dist" -Recurse -File
Write-Host "生成 $($distFiles.Count) 个文件" -ForegroundColor Gray

# 总结
Write-Host "`n✅ Node.js版本兼容性测试通过!" -ForegroundColor Green
Write-Host "=" * 70
Write-Host "GitHub Actions配置已更新:" -ForegroundColor Cyan
Write-Host "1. Node.js版本: 24" -ForegroundColor Gray
Write-Host "2. 修复了缓存路径问题" -ForegroundColor Gray
Write-Host "3. 添加了详细错误处理" -ForegroundColor Gray
Write-Host ""
Write-Host "🎯 下一步操作:" -ForegroundColor Yellow
Write-Host "1. 提交修复后的工作流文件" -ForegroundColor Gray
Write-Host "2. 推送到GitHub触发新的部署" -ForegroundColor Gray
Write-Host "3. 查看GitHub Actions运行状态" -ForegroundColor Gray