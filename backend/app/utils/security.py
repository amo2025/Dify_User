"""
安全工具模块 - 处理加密和敏感信息
"""
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from typing import Optional

class SecurityUtils:
    """安全工具类"""

    def __init__(self):
        # 从环境变量获取加密密钥，如果没有则生成一个（仅用于开发）
        self.secret_key = os.getenv('ENCRYPTION_SECRET_KEY')
        if not self.secret_key:
            # 开发环境使用固定密钥（生产环境必须设置环境变量）
            self.secret_key = "dify-studio-default-encryption-key-2024"

        # 生成Fernet密钥
        self.fernet = self._create_fernet_key(self.secret_key)

    def _create_fernet_key(self, password: str) -> Fernet:
        """从密码生成Fernet密钥"""
        salt = b'dify_studio_salt_'  # 应该使用随机盐，这里简化
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return Fernet(key)

    def encrypt_data(self, data: str) -> str:
        """加密数据"""
        if not data:
            return ""
        encrypted_data = self.fernet.encrypt(data.encode())
        return encrypted_data.decode()

    def decrypt_data(self, encrypted_data: str) -> Optional[str]:
        """解密数据"""
        if not encrypted_data:
            return None
        try:
            decrypted_data = self.fernet.decrypt(encrypted_data.encode())
            return decrypted_data.decode()
        except Exception:
            # 解密失败可能是因为数据未加密或密钥不匹配
            return None

    def mask_api_key(self, api_key: str) -> str:
        """掩码显示API密钥"""
        if not api_key:
            return ""
        if len(api_key) <= 8:
            return "*" * len(api_key)
        return api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:]

# 全局安全工具实例
security_utils = SecurityUtils()