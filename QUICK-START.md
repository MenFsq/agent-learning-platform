# Quick Start

本指南用于在本地快速启动项目，不包含架构和进展说明（避免与其他文档重复）。

## 1) 环境要求

- Node.js 18+
- npm 9+
- Python 3.10+

## 2) 启动前端

```bash
cd frontend
npm install
npm run dev
```

默认访问地址（以终端输出为准）：`http://localhost:5173`

## 3) 启动后端

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

默认访问地址（以终端输出为准）：`http://localhost:8000`

## 4) 常用地址

- 前端：`http://localhost:5173`
- 后端：`http://localhost:8000`
- Swagger：`http://localhost:8000/docs`
- ReDoc：`http://localhost:8000/redoc`

如果你的本地端口不同，请以当前运行日志中的地址为准。

## 5) 常见问题

- 端口占用：修改前端或后端启动端口
- 依赖安装失败：先确认 Node/Python 版本，再重新安装
- API 无法访问：先确认后端是否已启动

## 相关文档

- 目录结构：`PROJECT-STRUCTURE.md`
- 架构说明：`ARCHITECTURE.md`
- API 文档访问：`API-DOCS-ACCESS.md`
