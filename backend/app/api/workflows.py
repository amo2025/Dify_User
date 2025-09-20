from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.utils.database import get_db
from app.services.dify_client import dify_client
from app.models.config import DifyConfig

router = APIRouter()

@router.post("/{workflow_id}/run")
async def run_workflow(
    workflow_id: str,
    run_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    # 获取数据库中的配置
    config = db.query(DifyConfig).filter(DifyConfig.id == "default").first()

    if not config or not config.api_key:
        raise HTTPException(status_code=400, detail="请先配置Dify API密钥")

    # 临时设置客户端配置
    original_base_url = dify_client.base_url
    original_api_key = dify_client.api_key

    try:
        dify_client.base_url = config.base_url
        dify_client.api_key = config.api_key

        response = await dify_client.run_workflow({
            "workflow_id": workflow_id,
            **run_data
        })
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"工作流执行失败: {str(e)}")
    finally:
        # 恢复原始配置
        dify_client.base_url = original_base_url
        dify_client.api_key = original_api_key

@router.get("/runs/{run_id}")
async def get_workflow_run(
    run_id: str,
    db: Session = Depends(get_db)
):
    # 获取数据库中的配置
    config = db.query(DifyConfig).filter(DifyConfig.id == "default").first()

    if not config or not config.api_key:
        raise HTTPException(status_code=400, detail="请先配置Dify API密钥")

    # 临时设置客户端配置
    original_base_url = dify_client.base_url
    original_api_key = dify_client.api_key

    try:
        dify_client.base_url = config.base_url
        dify_client.api_key = config.api_key

        response = await dify_client.get_workflow_run(run_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取工作流执行状态失败: {str(e)}")
    finally:
        # 恢复原始配置
        dify_client.base_url = original_base_url
        dify_client.api_key = original_api_key

@router.post("/generate-dsl")
async def generate_workflow_dsl(
    description: str,
    model_id: str = None,
    db: Session = Depends(get_db)
):
    # 这里是智能生成DSL的核心功能
    # 需要集成LLM来根据自然语言描述生成工作流DSL
    # 暂时返回示例响应

    return {
        "dsl": {
            "name": "生成的工作流",
            "description": description,
            "nodes": [
                {
                    "id": "node_1",
                    "type": "llm",
                    "config": {
                        "model": "gpt-3.5-turbo",
                        "prompt": f"处理以下请求: {description}"
                    }
                }
            ],
            "edges": []
        },
        "message": "DSL生成成功（示例）"
    }