# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

Dify Studio 是一个基于 Dify 2.0 的本地 AI 工作流管理平台，提供前后端分离的架构：
- **前端**: React 18 + TypeScript + Vite + Ant Design
- **后端**: FastAPI + SQLite + SQLAlchemy
- **部署**: Docker Compose

## 开发命令

### 前端开发
```bash
cd frontend
npm install          # 安装依赖
npm run dev          # 启动开发服务器 (端口 3000)
npm run build       # 构建生产版本
npm run lint        # 运行 ESLint 检查
npm run preview     # 预览生产构建
```

### 后端开发
```bash
cd backend
# 创建虚拟环境 (如果尚未创建)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 安装开发依赖（可选）
pip install -r requirements-dev.txt  # 如果有的话

# 启动开发服务器
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 生成新的 requirements.txt（当添加新依赖时）
pip freeze > requirements.txt

# 访问 API 文档
# http://localhost:8000/docs
```

### Docker 开发
```bash
# 使用 Docker Compose 启动所有服务
docker-compose up --build

# 在后台运行
docker-compose up -d --build

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 项目架构

### 前端结构 (`frontend/`)
- `src/` - React 组件和业务逻辑
- `vite.config.ts` - Vite 配置
- `tsconfig.json` - TypeScript 配置

### 后端结构 (`backend/`)
- `app/` - 应用代码
  - `api/` - FastAPI 路由模块
  - `models/` - 数据库模型
  - `services/` - 业务服务层
  - `utils/` - 工具函数
- `main.py` - FastAPI 应用入口
- `requirements.txt` - Python 依赖

### 核心 API 端点
- `GET /api/models` - 获取 AI 模型列表
- `POST /api/workflows` - 创建工作流
- `GET /api/workflows/{id}` - 获取工作流详情
- `POST /api/workflows/run` - 执行工作流
- `GET/POST /api/datasets` - 知识库管理
- `GET /api/datasets/{id}/documents` - 获取知识库文档列表
- `POST /api/datasets/{id}/documents` - 添加文档到知识库
- `GET /api/config` - 获取系统配置
- `POST /api/config` - 更新系统配置
- `GET /api/config/test` - 测试 Dify API 连接

## 环境配置

复制 `.env.example` 为 `.env` 并配置：
```env
DATABASE_URL=sqlite:///./dify_studio.db
DIFY_BASE_URL=https://api.dify.ai/v1
DIFY_API_KEY=your-workflow-api-key          # 工作流API密钥
DIFY_DATA_API_KEY=your-dataset-api-key      # 数据集API密钥（知识库功能需要）
ALLOWED_ORIGINS=http://localhost:3000
```

**重要**:
- `DIFY_API_KEY`: 用于工作流功能
- `DIFY_DATA_API_KEY`: 用于知识库功能（必须设置）

## 开发注意事项

1. **数据库**: 使用 SQLite 开发，生产环境建议 PostgreSQL
2. **CORS**: 前端运行在端口 3000，后端在端口 8000
3. **API 代理**: 后端代理所有 Dify API 调用，保护 API 密钥
4. **错误处理**: 统一的异常处理在 `app/utils/error_handler.py`
5. **环境变量**: 使用 `.env` 文件管理敏感配置，确保不提交到版本控制
6. **API 密钥管理**: 工作流和数据集使用不同的 API 密钥，通过环境变量配置

## 测试

前端使用 ESLint 进行代码质量检查：
```bash
cd frontend
npm run lint
```

后端可通过 FastAPI 自动生成的文档测试 API 端点。

## 部署

生产部署使用 Docker Compose：
```bash
docker-compose -f docker-compose.yml up --build -d
```

确保配置正确的环境变量，特别是数据库连接字符串和 Dify API 密钥。