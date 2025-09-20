#!/usr/bin/env python3
"""
Dify配置检查脚本
"""

import os
from pathlib import Path

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

print("=== Dify配置检查 ===")
print()

# 检查环境变量
print("1. 环境变量配置:")
base_url = os.getenv('DIFY_BASE_URL')
api_key = os.getenv('DIFY_API_KEY')
data_api_key = os.getenv('DIFY_DATA_API_KEY')

print(f"   DIFY_BASE_URL: {base_url}")
print(f"   DIFY_API_KEY: {'已设置' if api_key else '未设置'}")
print(f"   DIFY_DATA_API_KEY: {'已设置' if data_api_key else '未设置'}")

if not api_key:
    print("   ⚠️  警告: DIFY_API_KEY 未设置（工作流功能需要）")

if not data_api_key:
    print("   ❌ 错误: DIFY_DATA_API_KEY 未设置（知识库功能需要）")
    exit(1)

if base_url == "https://api.dify.ai/v1":
    print("   ⚠️  警告: 使用的是云端Dify API，请确保您有有效的API密钥")
elif base_url == "http://localhost:8091/v1":
    print("   ✅ 使用的是本地Dify实例")
else:
    print(f"   ℹ️  使用自定义Dify实例: {base_url}")

print()
print("2. 配置说明:")
print("   - DIFY_BASE_URL: Dify API的基础URL")
print("   - DIFY_API_KEY: Dify API密钥（从Dify平台获取）")
print()

print("3. 获取API密钥的方法:")
print("   a) 本地Dify实例:")
print("      1. 访问 http://localhost:8091")
print("      2. 登录Dify管理界面")
print("      3. 进入「设置」->「API密钥」")
print("      4. 复制「数据集API密钥」")
print()
print("   b) 云端Dify:")
print("      1. 访问 https://cloud.dify.ai")
print("      2. 登录您的账户")
print("      3. 进入「设置」->「API密钥」")
print("      4. 复制您的API密钥")
print()

print("4. 重启服务:")
print("   配置完成后，需要重启服务:")
print("   docker-compose down && docker-compose up -d")
print()

print("✅ 配置检查完成")