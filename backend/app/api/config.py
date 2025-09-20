import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Dict, Any

from app.utils.database import get_db
from app.models.config import DifyConfig
from app.services.dify_client import dify_client

router = APIRouter()

@router.get("/")
def get_config(db: Session = Depends(get_db)):
    config = db.query(DifyConfig).filter(DifyConfig.id == "default").first()

    if not config:
        return {
            "base_url": os.getenv("DIFY_BASE_URL", "https://api.dify.ai/v1"),
            "api_key": os.getenv("DIFY_API_KEY", ""),
            "configured": bool(os.getenv("DIFY_API_KEY"))
        }

    return {
        "base_url": config.base_url,
        "api_key": config.get_masked_api_key(),
        "configured": True
    }

@router.post("/")
def update_config(
    config_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    config = db.query(DifyConfig).filter(DifyConfig.id == "default").first()

    if config:
        config.base_url = config_data.get("base_url", config.base_url)
        # 只有当提供了新的API密钥时才更新
        if "api_key" in config_data:
            config.api_key = config_data["api_key"]
    else:
        config = DifyConfig(
            id="default",
            base_url=config_data.get("base_url", "https://api.dify.ai/v1"),
            api_key=config_data.get("api_key", "")
        )
        db.add(config)

    db.commit()
    db.refresh(config)

    return {
        "message": "配置更新成功",
        "base_url": config.base_url,
        "api_key": config.get_masked_api_key()
    }

@router.get("/test")
async def test_connection(db: Session = Depends(get_db)):
    config = db.query(DifyConfig).filter(DifyConfig.id == "default").first()

    if not config or not config.api_key:
        raise HTTPException(status_code=400, detail="请先配置Dify API密钥")

    # 临时设置客户端配置进行测试
    original_base_url = dify_client.base_url
    original_api_key = dify_client.api_key
    original_data_api_key = dify_client.data_api_key

    try:
        dify_client.base_url = config.base_url
        dify_client.api_key = config.api_key
        # 对于数据集操作，使用数据集API密钥（优先使用环境变量中的配置）
        dify_client.data_api_key = os.getenv("DIFY_DATASET_API_KEY", config.api_key)

        # 测试获取知识库列表
        response = await dify_client.get_datasets(limit=1)
        return {
            "success": True,
            "message": "连接测试成功",
            "data": response
        }
    except Exception as e:
        import traceback
        error_detail = f"连接测试失败: {str(e)}\n{traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_detail)
    finally:
        # 恢复原始配置
        dify_client.base_url = original_base_url
        dify_client.api_key = original_api_key
        dify_client.data_api_key = original_data_api_key