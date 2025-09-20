from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from sqlalchemy.pool import NullPool
import os

# 使用SQLite数据库
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dify_studio.db")

# 创建同步引擎（SQLAlchemy 1.4兼容）
# 在生产环境中应该使用连接池，开发环境使用NullPool
engine = create_engine(
    DATABASE_URL,
    echo=True,
    poolclass=NullPool,
    # SQLite需要这个参数来支持多线程，但在生产环境中应该使用更安全的数据库
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# 创建会话工厂
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

# 声明基类
Base = declarative_base()

# 依赖注入获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()