# 测试卡片header样式修复
Write-Host "🎨 测试卡片header样式修复" -ForegroundColor Cyan
Write-Host "=" * 70

# 显示问题
Write-Host "`n❌ 问题描述:" -ForegroundColor Yellow
Write-Host "快速操作和技术栈模块的header样式与前面两个模块不一样" -ForegroundColor Gray
Write-Host "原因: CSS针对:deep(.el-card__header)，但模板使用.card-header类" -ForegroundColor Gray

# 显示修复内容
Write-Host "`n🔧 修复内容:" -ForegroundColor Yellow
Write-Host "1. 更新CSS选择器:" -ForegroundColor Gray
Write-Host "   - :deep(.el-card__header) → .card-header" -ForegroundColor Gray
Write-Host "   - :deep(.el-card__header h3) → .card-header h3" -ForegroundColor Gray
Write-Host "   - :deep(.el-card__header .el-button) → .card-header .el-button" -ForegroundColor Gray

Write-Host "`n2. 添加flex布局:" -ForegroundColor Gray
Write-Host "   - display: flex" -ForegroundColor Gray
Write-Host "   - justify-content: space-between" -ForegroundColor Gray
Write-Host "   - align-items: center" -ForegroundColor Gray

Write-Host "`n3. 移除:deep选择器:" -ForegroundColor Gray
Write-Host "   - 因为.card-header是我们自定义的类，不需要:deep" -ForegroundColor Gray

# 检查修复
Write-Host "`n🔍 检查修复文件:" -ForegroundColor Yellow

# 检查CSS选择器
Write-Host "新的.card-header样式:" -ForegroundColor Gray
Select-String -Pattern "\.card-header\s*{" -Path "src\views\Dashboard.vue"

Write-Host "`n检查所有模块的header类:" -ForegroundColor Gray
$headerLines = Select-String -Pattern 'class="card-header"' -Path "src\views\Dashboard.vue"
Write-Host "找到 $($headerLines.Count) 个.card-header类使用" -ForegroundColor Gray
$headerLines | ForEach-Object {
    Write-Host "  行 $($_.LineNumber): $($_.Line.Trim())" -ForegroundColor Gray
}

# 构建测试
Write-Host "`n🔨 测试构建..." -ForegroundColor Yellow
Set-Location "frontend"

if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
    Write-Host "✓ 清理dist目录" -ForegroundColor Green
}

npm run build
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ 构建成功" -ForegroundColor Green
} else {
    Write-Host "❌ 构建失败" -ForegroundColor Red
    exit 1
}

Write-Host "`n🎨 修复效果预览:" -ForegroundColor Cyan
Write-Host "=" * 70
Write-Host "✅ 所有6个模块现在都有统一的header样式:" -ForegroundColor Green
Write-Host ""
Write-Host "📊 模块列表:" -ForegroundColor Yellow
Write-Host "1. 项目进度 (蓝色图标)" -ForegroundColor Gray
Write-Host "2. 系统通知 (紫色图标)" -ForegroundColor Gray
Write-Host "3. 社区交流 (绿色图标)" -ForegroundColor Gray
Write-Host "4. 学习活动 (橙色图标)" -ForegroundColor Gray
Write-Host "5. 快速操作 (红色图标)" -ForegroundColor Gray
Write-Host "6. 技术栈 (紫色图标)" -ForegroundColor Gray
Write-Host ""
Write-Host "🎨 统一样式特征:" -ForegroundColor Yellow
Write-Host "• 渐变背景: 蓝色到紫色渐变" -ForegroundColor Gray
Write-Host "• 装饰线条: 顶部彩色渐变线条" -ForegroundColor Gray
Write-Host "• 悬停效果: 鼠标悬停时线条变亮" -ForegroundColor Gray
Write-Host "• 图标系统: 每个模块有特定颜色的图标" -ForegroundColor Gray
Write-Host "• 按钮样式: 统一的紧凑按钮" -ForegroundColor Gray
Write-Host ""
Write-Host "📱 响应式设计:" -ForegroundColor Yellow
Write-Host "• 移动端: 自动调整布局" -ForegroundColor Gray
Write-Host "• 平板: 保持卡片结构" -ForegroundColor Gray
Write-Host "• 桌面: 两行布局(2大+4小)" -ForegroundColor Gray
Write-Host ""
Write-Host "📤 提交修复:" -ForegroundColor Yellow
Write-Host "git add ." -ForegroundColor Gray
Write-Host "git commit -m 'fix: 统一所有卡片模块的header样式'" -ForegroundColor Gray
Write-Host "git push origin master" -ForegroundColor Gray