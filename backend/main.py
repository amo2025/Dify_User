import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager

from app.api import config, models, workflows, datasets
from app.utils.database import engine, Base
from app.utils.error_handler import global_exception_handler, create_error_response

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时创建数据库表
    Base.metadata.create_all(bind=engine)
    yield
    # 关闭时清理资源
    engine.dispose()

app = FastAPI(
    title="Dify Studio API",
    description="Dify Studio - 本地Dify管理门户",
    version="0.1.0",
    lifespan=lifespan
)

# 配置CORS
# 从环境变量获取允许的源，默认为开发环境
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept"],
    expose_headers=["Content-Type", "Content-Length"],
    max_age=600,  # 预检请求缓存时间（秒）
)

# 添加异常处理器
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, global_exception_handler)

# 注册路由
app.include_router(config.router, prefix="/api/config", tags=["config"])
app.include_router(models.router, prefix="/api/models", tags=["models"])
app.include_router(workflows.router, prefix="/api/workflows", tags=["workflows"])
app.include_router(datasets.router, prefix="/api/datasets", tags=["datasets"])

@app.get("/")
async def root():
    return {
        "message": "Dify Studio API",
        "version": "0.1.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}