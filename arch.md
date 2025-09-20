### **Dify Studio 技术架构文档**  
**版本**: 1.0  
**目标系统**: 基于Dify 2.0的本地AI工作流管理平台  
**技术栈**: React + FastAPI + SQLite + Docker  

---

### **一、架构设计原则**
1. **前后端分离**：前端专注交互，后端处理业务逻辑与Dify API代理。
2. **轻量可移植**：SQLite存储元数据，Docker容器化部署。
3. **安全隔离**：后端代理所有Dify API调用，避免前端暴露敏感信息。
4. **异步扩展性**：核心耗时操作（如LLM生成DSL）支持异步队列扩展。

---

### **二、系统架构图**
```plaintext
+-------------------+       +---------------------+       +-----------------+
|   React Frontend  |<----->| FastAPI Backend     |<----->| Dify Local      |
| (TypeScript)      | HTTP  | (Python 3.10+)      | HTTP  | (v2.0)          |
+-------------------+       +---------------------+       +-----------------+
       ↑                              ↑
       |                              | SQLite
       +------------------------------+ (应用元数据)
```

---

### **三、技术栈详解**
#### **1. 前端 (React)**
- **框架**: React 18 + TypeScript  
- **状态管理**: Redux Toolkit（管理全局状态如Dify配置、模型列表）  
- **UI库**: Ant Design（表格、表单、通知组件）  
- **关键库**:  
  - `react-query`: 智能数据同步（工作流状态轮询）  
  - `react-flow`: 工作流DSL可视化预览（未来扩展）  
  - `react-dropzone`: 知识库文件拖拽上传  

#### **2. 后端 (FastAPI)**
- **核心框架**: FastAPI（异步支持 + 自动API文档）  
- **数据库**: SQLite + SQLAlchemy ORM  
- **异步任务**: Celery + Redis（可选，用于解耦LLM生成DSL任务）  
- **安全**: JWT认证（预留接口）、环境变量加密  
- **关键依赖**:  
  - `httpx`: 异步HTTP客户端（调用Dify API）  
  - `pydantic`: 数据模型验证（DSL JSON校验）  
  - `loguru`: 结构化日志  

#### **3. 基础设施**
- **容器化**: Docker Compose（一键部署）  
- **网络**: 前端(3000) + 后端(8000) 端口暴露  
- **存储卷**: SQLite数据库持久化挂载  

---

### **四、核心模块实现方案**
#### **1. Dify API代理层（关键安全设计）**
```python
# 示例：后端代理Dify创建工作流
@app.post("/api/workflows")
async def create_workflow(dsl: dict):
    dify_url = f"{settings.DIFY_BASE_URL}/workflows"
    async with httpx.AsyncClient() as client:
        response = await client.post(
            dify_url,
            json=dsl,
            headers={"Authorization": f"Bearer {settings.DIFY_API_KEY}"}
        )
        response.raise_for_status()
        return response.json()
```
- **安全机制**：  
  - Dify API Key存储在服务端环境变量  
  - 前端仅传递业务数据（如DSL JSON），不接触密钥  

#### **2. 智能工作流生成（核心难点）**
```python
# 步骤1：构造LLM提示词模板
DSL_PROMPT_TEMPLATE = """
你是一个Dify工作流专家。请严格按以下规则生成DSL：
1. 输出纯净JSON，符合Dify 2.0 DSL规范
2. 使用节点类型: http_request/llm/if_condition...
3. 用户需求：{{user_input}}
```

```python
# 步骤2：调用LLM并解析
@app.post("/api/workflows/generate-dsl")
async def generate_dsl(prompt: str, model_id: str):
    # 从数据库获取模型配置
    model_config = await get_model_config(model_id)
    
    # 调用LLM API（如DeepSeek）
    llm_response = await call_llm_api(
        model_config.endpoint,
        messages=[
            {"role": "system", "content": DSL_PROMPT_TEMPLATE},
            {"role": "user", "content": prompt}
        ]
    )
    
    # 提取并验证JSON
    dsl_json = extract_json(llm_response)  # 使用正则+json.loads
    validate_dsl_schema(dsl_json)  # 使用JSON Schema校验
    return dsl_json
```

#### **3. 数据持久化设计（SQLite模型）**
```python
class Workflow(Base):
    __tablename__ = "workflows"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    tags = Column(String)  # 逗号分隔的标签
    dify_workflow_id = Column(String)  # Dify返回的ID
    dsl_json = Column(JSON)  # 原始DSL存储
    last_status = Column(String)  # 轮询更新状态
```

---

### **五、部署架构**
#### **Docker Compose 配置**
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DIFY_BASE_URL=http://host.docker.internal:5000  # 指向本地Dify
      - DIFY_API_KEY=${DIFY_API_KEY}  # 从.env注入
    volumes:
      - ./backend/data:/app/data  # SQLite持久化

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - VITE_API_BASE_URL=http://localhost:8000/api  # 指向后端
```

#### **关键环境变量**
```env
# backend/.env
DIFY_API_KEY=your_dify_master_key
CELERY_BROKER_URL=redis://redis:6379/0  # 若启用异步
```

---

### **六、容错与扩展设计**
1. **DSL生成降级方案**：  
   - 首次生成失败 → 返回错误提示 + 建议手动上传JSON  
   - 集成JSON Schema校验 → 避免无效DSL发送至Dify  

2. **状态同步鲁棒性**：  
   - 工作流状态轮询：指数退避重试（1s, 2s, 4s...）  
   - 离线检测：标记`last_status`为`unknown`  

3. **水平扩展准备**：  
   - 异步任务队列：Celery + Redis处理LLM请求  
   - 无状态后端：未来可扩展多个FastAPI实例  

---

### **七、监控与日志**
- **前端**：Sentry捕获JS异常  
- **后端**：Loguru结构化日志 → 输出至文件+控制台  
- **关键指标**：  
  - API响应延迟（Prometheus监控）  
  - DSL生成成功率（自定义指标）  

---

### **八、技术风险与应对**
| 风险点                  | 应对方案                               |
|-------------------------|----------------------------------------|
| LLM生成DSL格式不稳定    | 多层校验：正则提取+JSON Schema+try/catch |
| Dify API版本升级不兼容  | 抽象API Client层 + 版本隔离配置        |
| 大文件上传超时          | 前端分块上传 + 后端流式转发            |
| SQLite并发写入冲突      | 使用aiosqlite + 写队列序列化           |

---
