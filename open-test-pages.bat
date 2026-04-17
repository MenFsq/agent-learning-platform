@echo off
title 打开测试页面
color 0A

echo ========================================
echo   打开 Agent Learning Platform 测试页面
echo ========================================
echo.

echo [1] 打开 Community 页面测试入口...
start "" "http://localhost:5174/test-community.html"

echo [2] 打开 Community 页面...
start "" "http://localhost:5174/community"

echo [3] 打开前端应用主页...
start "" "http://localhost:5174"

echo [4] 打开后端 API 文档...
start "" "http://localhost:8004/docs"

echo.
echo   所有页面已在新窗口中打开！
echo.
echo   按任意键退出...
pause >nul
exit