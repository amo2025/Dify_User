from sqlalchemy import Column, String, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from app.utils.database import Base

class AIModel(Base):
    __tablename__ = "ai_models"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    provider = Column(String, nullable=False)  # ollama, openai, anthropic, etc.
    model_name = Column(String, nullable=False)
    base_url = Column(String)  # 对于ollama等本地模型
    api_key = Column(String)   # 对于在线提供商
    enabled = Column(Boolean, default=True)
    config = Column(JSON)      # 额外配置
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<AIModel(name='{self.name}', provider='{self.provider}')>"