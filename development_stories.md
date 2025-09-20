# Dify Studio 开发故事

## 项目概述
Dify Studio是一个基于Dify 2.0的二次开发项目，作为本地部署Dify服务的增强型管理门户。所有功能（除模型管理外）都基于Dify原生API进行代理和增强。

## 技术栈
- **前端**: React 18 + TypeScript + Ant Design
- **后端**: FastAPI + SQLite + SQLAlchemy (代理Dify API)
- **部署**: Docker + Docker Compose

## 开发故事

### 故事1: 项目基础架构搭建 (MVP)
**作为** 开发者
**我想要** 搭建完整的前后端基础架构
**以便** 能够快速开始功能开发

**验收标准**:
- [ ] 创建前后端Docker容器配置
- [ ] 配置环境变量管理
- [ ] 实现基础的路由和API结构
- [ ] 设置开发环境的热重载

**技术任务**:
1. 创建 `docker-compose.yml` 文件
2. 配置前端Vite + React开发环境
3. 配置后端FastAPI + SQLAlchemy
4. 设置跨域请求处理
5. 配置环境变量文件

### 故事2: Dify配置管理
**作为** 用户
**我想要** 配置Dify实例的连接信息
**以便** 能够安全地连接到我的Dify服务

**验收标准**:
- [ ] 提供初始化设置界面
- [ ] 安全存储Dify BASE_URL和API_KEY
- [ ] 验证Dify连接有效性
- [ ] 支持配置的修改和更新

**API端点**:
- `GET /api/config` - 获取当前配置
- `POST /api/config` - 更新Dify配置
- `GET /api/config/test` - 测试Dify连接

### 故事3: 模型管理模块 (唯一独立功能)
**作为** 用户
**我想要** 管理我的AI模型
**以便** 能够查看、添加、启用/禁用模型

**验收标准**:
- [ ] 显示模型列表（卡片或表格视图）
- [ ] 支持添加新模型（区分Ollama和在线提供商）
- [ ] 支持启用/禁用切换
- [ ] 支持模型删除

**API端点**:
- `GET /api/models` - 获取模型列表
- `POST /api/models` - 添加新模型
- `PATCH /api/models/{model_id}` - 启用/禁用模型
- `DELETE /api/models/{model_id}` - 删除模型

### 故事4: 智能工作流生成（核心增强功能）
**作为** 用户
**我想要** 通过自然语言描述生成工作流DSL
**以便** 能够快速创建工作流而无需手动编写JSON

**验收标准**:
- [ ] 提供自然语言输入界面
- [ ] 支持选择生成模型
- [ ] 显示生成的DSL预览（代码高亮）
- [ ] 支持手动编辑和验证DSL
- [ ] 支持保存生成的工作流

**API端点**:
- `POST /api/workflows/generate-dsl` - 智能生成DSL (Dify Studio特有)
- `POST /api/workflows` - 代理Dify创建工作流 (POST /workflows)
- `GET /api/workflows/{workflow_id}` - 代理获取工作流详情

### 故事5: 工作流管理 (基于Dify API)
**作为** 用户
**我想要** 管理我的工作流
**以便** 能够查看、执行、监控工作流状态

**验收标准**:
- [ ] 显示工作流列表，支持标签筛选
- [ ] 支持工作流执行和状态监控
- [ ] 支持工作流删除
- [ ] 实时状态轮询和显示

**Dify API代理**:
- `GET /api/workflows` - 代理Dify获取工作流列表
- `POST /api/workflows/{workflow_id}/run` - 代理Dify执行工作流 (POST /workflows/run)
- `GET /api/workflows/runs/{run_id}` - 代理获取执行状态 (GET /workflows/run/{workflow_run_id})

### 故事6: 知识库管理 (基于Dify API)
**作为** 用户
**我想要** 管理我的知识库和文档
**以便** 能够上传、查看、删除文档

**验收标准**:
- [ ] 显示知识库列表
- [ ] 支持拖拽文件上传
- [ ] 显示文档处理状态
- [ ] 支持文档删除

**Dify API代理**:
- `GET /api/datasets` - 代理获取知识库列表 (GET /datasets)
- `POST /api/datasets` - 代理创建知识库 (POST /datasets)
- `POST /api/datasets/{dataset_id}/files` - 代理上传文件 (POST /datasets/{dataset_id}/document/create-by-file)
- `GET /api/datasets/{dataset_id}/files` - 代理获取文档列表 (GET /datasets/{dataset_id}/documents)
- `DELETE /api/datasets/{dataset_id}/files/{document_id}` - 代理删除文档 (DELETE /datasets/{dataset_id}/documents/{document_id})
- `DELETE /api/datasets/{dataset_id}` - 代理删除知识库 (DELETE /datasets/{dataset_id})

### 故事7: 错误处理和用户体验
**作为** 用户
**我想要** 良好的错误提示和用户体验
**以便** 能够轻松使用应用并解决问题

**验收标准**:
- [ ] 全局错误处理（前后端）
- [ ] 友好的错误消息提示
- [ ] 加载状态指示
- [ ] 响应式设计支持

### 故事8: 部署和运维
**作为** 运维人员
**我想要** 一键部署应用
**以便** 能够快速部署和维护应用

**验收标准**:
- [ ] Docker Compose一键部署
- [ ] 环境变量配置管理
- [ ] 数据库持久化
- [ ] 日志记录和监控

## 优先级排序
1. 故事1: 项目基础架构搭建 (MVP)
2. 故事2: Dify配置管理
3. 故事3: 模型管理模块 (唯一独立功能)
4. 故事5: 工作流管理（基于Dify API）
5. 故事6: 知识库管理（基于Dify API）
6. 故事4: 智能工作流生成（增强功能）
7. 故事7: 错误处理和用户体验
8. 故事8: 部署和运维

## 技术风险点
1. **LLM生成DSL格式不稳定** - 需要多层校验机制
2. **Dify API版本兼容性** - 需要抽象API客户端层
3. **大文件上传超时** - 需要分块上传和流式转发
4. **SQLite并发写入冲突** - 需要写队列序列化

## 验证的Dify API端点
基于docs/目录验证的Dify原生API：
- 工作流执行: POST /workflows/run
- 获取执行状态: GET /workflows/run/{workflow_run_id}
- 文件上传: POST /files/upload
- 获取知识库列表: GET /datasets
- 创建知识库: POST /datasets
- 文件创建文档: POST /datasets/{dataset_id}/document/create-by-file
- 获取文档列表: GET /datasets/{dataset_id}/documents
- 删除文档: DELETE /datasets/{dataset_id}/documents/{document_id}
- 删除知识库: DELETE /datasets/{dataset_id}

## 下一步行动
1. 开始实现故事1（基础架构搭建）
2. 配置开发环境
3. 创建初始代码结构