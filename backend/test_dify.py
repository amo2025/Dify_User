#!/usr/bin/env python3
"""
Dify API集成测试脚本
"""
import asyncio
import os
from app.services.dify_client import DifyClient

async def test_dify_connection():
    """测试Dify连接"""

    # 设置测试用的API密钥（需要用户提供真实的密钥）
    test_api_key = os.getenv("DIFY_TEST_API_KEY", "your-dify-api-key-here")

    client = DifyClient()
    client.base_url = "https://api.dify.ai/v1"
    client.api_key = test_api_key

    print("🧪 开始Dify API集成测试...")
    print(f"📡 目标API: {client.base_url}")
    print(f"🔑 API密钥: {'*' * len(client.api_key) if client.api_key else '未设置'}")

    try:
        # 测试获取知识库列表
        print("\n1. 测试获取知识库列表...")
        datasets = await client.get_datasets(limit=5)
        print(f"✅ 成功获取知识库列表: {len(datasets.get('data', []))} 个知识库")

        # 测试获取工作流运行状态（需要有效的工作流ID）
        print("\n2. 测试工作流API...")
        # 这里需要有效的工作流ID，暂时跳过具体运行测试
        print("⚠️  工作流测试需要有效的工作流ID，跳过具体执行")

        print("\n🎉 Dify API集成测试完成！")

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        print("💡 请检查:")
        print("  1. API密钥是否正确")
        print("  2. 网络连接是否正常")
        print("  3. Dify服务是否可用")
    finally:
        await client.close()

if __name__ == "__main__":
    # 如果提供了API密钥，则进行测试
    if os.getenv("DIFY_TEST_API_KEY"):
        asyncio.run(test_dify_connection())
    else:
        print("⚠️  未设置DIFY_TEST_API_KEY环境变量")
        print("💡 请设置环境变量: export DIFY_TEST_API_KEY=your-actual-api-key")
        print("💡 或者直接修改test_api_key变量为您的Dify API密钥")