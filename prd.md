好的，完全理解。基于您选择的技术栈（React + FastAPI）和部署方式（Docker），我将为您提供一份全新的、完整的PRD文档。

---

### **PRD: Dify Studio - 个人AI工作流管理平台**

**版本**: 2.0
**状态**: 终稿
**技术栈**: React + FastAPI + SQLite + Docker
**目标Dify版本**: 2.0

#### 1. 项目概述

**1.1. 项目名称**
Dify Studio

**1.2. 项目简介**
Dify Studio是一个前后端分离的Web应用程序，旨在作为本地部署Dify服务的增强型管理门户。后端使用FastAPI构建高效的RESTful代理层，前端使用React构建交互界面。应用通过Docker容器化，提供一键式本地部署体验，帮助用户更高效地管理Dify的模型、工作流和知识库。

**1.3. 目标用户**
技术背景较强的个人用户，如开发者、MLOps工程师。

**1.4. 核心价值**
*   **开箱即用**：通过Docker Compose快速部署，无需复杂的环境配置。
*   **安全代理**：后端作为代理网关，安全地处理Dify API调用，避免前端直接暴露敏感信息（如API Keys）。
*   **功能增强**：在Dify原生API基础上，提供智能工作流生成、统一元数据管理等增强功能。

#### 2. 系统架构与技术栈

**2.1. 前端 (Frontend)**
*   **框架**: React 18
*   **语言**: TypeScript
*   **状态管理**: Redux Toolkit / Zustand
*   **UI组件库**: Ant Design / MUI
*   **构建工具**: Vite

**2.2. 后端 (Backend)**
*   **框架**: FastAPI
*   **语言**: Python 3.10+
*   **数据库**: SQLite (用于存储应用元数据)
*   **ORM/SQL工具**: SQLAlchemy + Alembic
*   **异步处理**: 原生`async/await`

**2.3. 部署与基础设施**
*   **容器化**: Docker + Docker Compose
*   **反向代理**: 可集成Nginx (可选，用于更复杂的生产部署)

#### 3. 功能需求详述

**3.1. 全局功能**
*   **Dify配置管理**：提供初始化设置界面，配置Dify实例的`BASE_URL`和`API_KEY`。这些凭证由后端安全地存储。
*   **统一错误处理**：前后端均需实现全局异常捕获，并向用户返回友好的错误信息。
*   **响应式设计**：前端界面应适配桌面及平板设备。

**3.2. 模型管理**
*   **后端接口**:
    *   `GET /api/models`: 获取本地存储的模型列表。
    *   `POST /api/models`: 验证并添加新模型（调用Dify `POST /models`接口）。
    *   `PATCH /api/models/{model_id}`: 启用/禁用模型（调用Dify `PATCH /models/{model_id}`接口）。
    *   `DELETE /api/models/{model_id}`: 删除模型（调用Dify `DELETE /models/{model_id}`接口，并删除本地记录）。
*   **前端界面**:
    *   模型列表视图（卡片或表格）。
    *   添加模型表单（区分Ollama和在线模型提供商）。
    *   操作按钮：启用/禁用切换、删除。

**3.3. 工作流管理 (核心功能)**
*   **后端接口**:
    *   `GET /api/workflows`: 获取工作流列表（合并Dify状态和本地元数据）。
    *   `POST /api/workflows/generate-dsl`: **智能生成DSL**。接收用户自然语言描述，构造Prompt，调用指定的LLM API（如Kimi、DeepSeek），并返回生成的DSL JSON。
    *   `POST /api/workflows`: 创建的工作流（将DSL发送至Dify `POST /workflows`，成功后存入本地DB）。
    *   `GET /api/workflows/{workflow_id}`: 获取特定工作流详情及状态（代理调用Dify）。
    *   `DELETE /api/workflows/{workflow_id}`: 删除工作流（调用Dify接口，并清理本地DB）。
*   **前端界面**:
    *   工作流列表页，支持按标签筛选。
    *   **“智能创建”向导式页面**：
        1.  选择生成模型。
        2.  输入自然语言描述。
        3.  显示生成后的DSL预览（代码高亮编辑器）。
    *   手动上传JSON文件入口。
    *   工作流状态定时轮询与显示。

**3.4. 知识库管理**
*   **后端接口**:
    *   `GET /api/datasets`: 获取知识库列表。
    *   `POST /api/datasets`: 创建知识库（调用Dify `POST /datasets`）。
    *   `POST /api/datasets/{dataset_id}/files`: **文件上传代理**。接收前端上传的文件，然后转发至Dify `POST /datasets/{dataset_id}/upload`接口。
    *   `GET /api/datasets/{dataset_id}/files`: 获取知识库内文档列表。
    *   `DELETE /api/datasets/{dataset_id}/files/{document_id}`: 删除文档。
    *   `DELETE /api/datasets/{dataset_id}`: 删除知识库。
*   **前端界面**:
    *   知识库列表页。
    *   知识库详情页，内含拖拽上传区域和文档列表。
    *   显示文档处理状态。

#### 4. 数据模型（后端SQLite）

*   `DifyConfig`表: `id`, `base_url`, `api_key`, `created_at`
*   `Model`表: `id`, `name`, `provider`, `config` (JSON), `is_enabled`, `dify_model_id` (与Dify关联的ID)
*   `Workflow`表: `id`, `name`, `tags`, `dify_workflow_id`, `dify_workflow_dsl` (存储原始DSL), `last_status`
*   `Dataset`表: `id`, `name`, `dify_dataset_id`

#### 5. 部署方案

项目根目录提供 `docker-compose.yml` 文件，定义两个服务：

```yaml
version: '3.8'
services:
  dify-studio-backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - DATABASE_URL=sqlite+aiosqlite:///./app.db
    volumes:
      - backend-data:/app/data # 持久化SQLite数据库

  dify-studio-frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - dify-studio-backend
    environment:
      - VITE_API_BASE_URL=http://localhost:8000/api # 指向后端地址

volumes:
  backend-data:
```

#### 6. 非功能性需求

*   **性能**: 后端API响应时间应小于500ms（不包括外部LLM生成DSL的时间）。
*   **安全性**: 所有发往Dify的API Key均在后端处理，不暴露给前端。对用户上传的文件进行基本的安全检查（如文件类型、大小限制）。
*   **可维护性**: 代码结构清晰，有详细的注释。提供API文档（FastAPI自动生成`/docs`）。
*   **可部署性**: 一行命令`docker-compose up -d`即可完成整个应用的部署。

--- 