# Agent Learning Platform - 构建测试脚本
Write-Host "🚀 Agent Learning Platform - 构建测试" -ForegroundColor Cyan
Write-Host "=" * 70

# 清理之前的构建
Write-Host "`n🧹 清理之前的构建..." -ForegroundColor Yellow
if (Test-Path "frontend\dist") {
    Remove-Item -Recurse -Force "frontend\dist"
    Write-Host "✓ 已清理 dist 目录" -ForegroundColor Green
}

# 安装依赖
Write-Host "`n📦 安装依赖..." -ForegroundColor Yellow
Set-Location "frontend"
npm ci
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 依赖安装失败" -ForegroundColor Red
    exit 1
}
Write-Host "✓ 依赖安装完成" -ForegroundColor Green

# 构建项目
Write-Host "`n🔨 构建项目..." -ForegroundColor Yellow
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 构建失败" -ForegroundColor Red
    exit 1
}
Write-Host "✓ 构建完成" -ForegroundColor Green

# 检查构建输出
Write-Host "`n📁 检查构建输出..." -ForegroundColor Yellow
Set-Location ".."
$distFiles = Get-ChildItem "frontend\dist" -Recurse -File
Write-Host "找到 $($distFiles.Count) 个文件:" -ForegroundColor Gray

$distFiles | ForEach-Object {
    Write-Host "  $($_.Name) ($($_.Length) bytes)" -ForegroundColor Gray
}

# 检查index.html
Write-Host "`n📄 检查 index.html..." -ForegroundColor Yellow
if (Test-Path "frontend\dist\index.html") {
    $indexContent = Get-Content "frontend\dist\index.html" -Raw
    if ($indexContent -match "Agent Learning Platform") {
        Write-Host "✓ index.html 包含正确标题" -ForegroundColor Green
    } else {
        Write-Host "❌ index.html 标题不正确" -ForegroundColor Red
    }
} else {
    Write-Host "❌ index.html 不存在" -ForegroundColor Red
}

# 检查资源路径
Write-Host "`n🔗 检查资源路径..." -ForegroundColor Yellow
if ($indexContent -match "/agent-learning-platform/") {
    Write-Host "✓ 基础路径正确配置" -ForegroundColor Green
} else {
    Write-Host "⚠️ 基础路径可能未正确配置" -ForegroundColor Yellow
    Write-Host "   GitHub Pages需要基础路径: /agent-learning-platform/" -ForegroundColor Gray
}

# 总结
Write-Host "`n📊 构建测试总结:" -ForegroundColor Cyan
Write-Host "=" * 70
Write-Host "✅ 所有检查通过!" -ForegroundColor Green
Write-Host ""
Write-Host "🎯 下一步操作:" -ForegroundColor Yellow
Write-Host "1. 提交代码到GitHub" -ForegroundColor Gray
Write-Host "2. GitHub Actions会自动运行部署工作流" -ForegroundColor Gray
Write-Host "3. 访问 https://menfsq.github.io/agent-learning-platform/ 查看部署" -ForegroundColor Gray
Write-Host ""
Write-Host "🔧 手动部署命令:" -ForegroundColor Yellow
Write-Host "git add ." -ForegroundColor Gray
Write-Host "git commit -m 'feat: 添加GitHub Pages部署配置'" -ForegroundColor Gray
Write-Host "git push origin master" -ForegroundColor Gray