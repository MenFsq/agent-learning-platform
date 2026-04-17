@echo off
title Agent Learning Platform - 一键启动
color 0A

echo ========================================
echo   Agent Learning Platform 一键启动脚本
echo ========================================
echo.

echo [1] 检查系统依赖...
echo.

where node >nul 2>nul
if %errorlevel% equ 0 (
    echo   Node.js: 已安装
) else (
    echo   Node.js: 未安装
    goto error
)

where npm >nul 2>nul
if %errorlevel% equ 0 (
    echo   npm: 已安装
) else (
    echo   npm: 未安装
    goto error
)

where python >nul 2>nul
if %errorlevel% equ 0 (
    echo   Python: 已安装
) else (
    echo   Python: 未安装
    goto error
)

echo.
echo [2] 启动前端服务...
echo.
start "前端服务" cmd /k "cd /d frontend && echo 启动前端开发服务器... && npm run dev"
timeout /t 3 >nul

echo.
echo [3] 启动后端服务...
echo.
start "后端服务" cmd /k "cd /d backend && echo 启动统一后端API服务器... && ..\.venv\Scripts\python.exe start_unified.py"
timeout /t 3 >nul

echo.
echo [4] 验证服务状态...
echo.

echo   测试前端服务...
curl -s -o nul -w "%%{http_code}" http://localhost:5174
if errorlevel 1 (
    echo   前端服务: 启动中...
) else (
    echo   前端服务: 运行正常
)

echo   测试后端服务...
curl -s -o nul -w "%%{http_code}" http://localhost:8005/health
if errorlevel 1 (
    echo   后端服务: 启动中...
) else (
    echo   后端服务: 运行正常
)

echo.
echo ========================================
echo   启动完成！
echo ========================================
echo.
echo   前端应用: http://localhost:5174
echo   后端API:  http://localhost:8005
echo   API文档: http://localhost:8005/docs
echo.
echo   按任意键打开浏览器访问...
pause >nul

start http://localhost:5174
start http://localhost:8005/docs

echo.
echo   服务已启动，可以开始开发！
echo   按任意键退出本窗口...
pause >nul
exit

:error
echo.
echo   ❌ 系统依赖检查失败，请安装必要的开发工具
echo.
echo   需要安装:
echo     - Node.js (https://nodejs.org/)
echo     - Python (https://python.org/)
echo.
pause
exit