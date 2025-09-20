#!/usr/bin/env python3
"""
Dify配置修复脚本
这个脚本帮助诊断和修复Dify配置问题
"""

import os
import sys
from pathlib import Path

# 添加backend目录到Python路径
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

def check_configuration():
    """检查当前配置状态"""
    print("=== Dify配置诊断 ===")

    # 检查环境变量
    print("\n1. 检查环境变量:")
    base_url = os.getenv('DIFY_BASE_URL')
    api_key = os.getenv('DIFY_API_KEY')

    print(f"   DIFY_BASE_URL: {base_url or '未设置'}")
    print(f"   DIFY_API_KEY: {'已设置' if api_key else '未设置'}")

    if not api_key:
        print("   ❌ 错误: DIFY_API_KEY 环境变量未设置")
        return False

    # 检查数据库配置
    print("\n2. 检查数据库配置:")
    try:
        from app.utils.database import SessionLocal, Base, engine
        from app.models.config import DifyConfig

        # 确保数据库表存在
        Base.metadata.create_all(bind=engine)

        db = SessionLocal()
        config = db.query(DifyConfig).filter(DifyConfig.id == "default").first()

        if config:
            print(f"   ✅ 数据库配置存在")
            print(f"      Base URL: {config.base_url}")
            print(f"      API Key: {config.get_masked_api_key()}")
        else:
            print("   ❌ 数据库中没有配置记录")

            # 从环境变量创建配置
            new_config = DifyConfig(
                id="default",
                base_url=base_url or "https://api.dify.ai/v1",
                api_key=api_key
            )
            db.add(new_config)
            db.commit()
            print("   ✅ 已从环境变量创建配置")

        db.close()

    except Exception as e:
        print(f"   ❌ 数据库检查失败: {e}")
        return False

    # 测试Dify连接
    print("\n3. 测试Dify连接:")
    try:
        import asyncio
        from app.services.dify_client import dify_client

        async def test_connection():
            db = SessionLocal()
            config = db.query(DifyConfig).filter(DifyConfig.id == "default").first()

            if not config or not config.api_key:
                print("   ❌ 没有有效的API密钥")
                return False

            # 临时设置配置
            original_base_url = dify_client.base_url
            original_api_key = dify_client.api_key

            try:
                dify_client.base_url = config.base_url
                dify_client.api_key = config.api_key

                response = await dify_client.get_datasets(limit=1)
                print(f"   ✅ 连接成功! 找到 {response.get('total', 0)} 个知识库")
                return True

            except Exception as e:
                print(f"   ❌ 连接失败: {e}")
                return False

            finally:
                # 恢复配置
                dify_client.base_url = original_base_url
                dify_client.api_key = original_api_key
                db.close()

        success = asyncio.run(test_connection())
        return success

    except Exception as e:
        print(f"   ❌ 连接测试异常: {e}")
        return False

def main():
    """主函数"""
    print("Dify配置修复工具")
    print("=" * 50)

    success = check_configuration()

    print("\n" + "=" * 50)
    if success:
        print("✅ 配置检查完成，系统正常")
    else:
        print("❌ 配置存在问题，请参考以下解决方案:")
        print("""
解决方案:
1. 确保Dify平台已正确安装并运行
2. 检查环境变量配置:
   - 编辑 .env 文件
   - 设置正确的 DIFY_BASE_URL (通常是 http://localhost:8091/v1)
   - 设置有效的 DIFY_API_KEY (从Dify平台获取)

3. 重启服务:
   docker-compose down && docker-compose up -d

4. 或者通过API配置界面设置:
   - 访问 http://localhost:3000 (前端)
   - 进入配置页面设置Dify连接参数
""")

if __name__ == "__main__":
    main()