from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.utils.database import Base
from app.utils.security import security_utils

class DifyConfig(Base):
    __tablename__ = "dify_config"

    id = Column(String, primary_key=True, default="default")
    base_url = Column(String, nullable=False, default="https://api.dify.ai/v1")
    _api_key_encrypted = Column("api_key", String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    @property
    def api_key(self) -> str:
        """获取解密的API密钥"""
        return security_utils.decrypt_data(self._api_key_encrypted) or ""

    @api_key.setter
    def api_key(self, value: str):
        """设置并加密API密钥"""
        self._api_key_encrypted = security_utils.encrypt_data(value)

    def get_masked_api_key(self) -> str:
        """获取掩码显示的API密钥"""
        decrypted_key = security_utils.decrypt_data(self._api_key_encrypted)
        return security_utils.mask_api_key(decrypted_key) if decrypted_key else ""

    def __repr__(self):
        return f"<DifyConfig(base_url='{self.base_url}')>"