from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
import httpx

from app.utils.database import get_db
from app.services.dify_client import dify_client

router = APIRouter()

@router.get("/")
async def get_datasets(
    keyword: str = None,
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    try:
        # 获取数据库中的配置
        from app.models.config import DifyConfig
        config = db.query(DifyConfig).filter(DifyConfig.id == "default").first()

        if not config or not config.api_key:
            raise HTTPException(status_code=400, detail="请先配置Dify API密钥")

        # 临时设置客户端配置
        original_base_url = dify_client.base_url
        original_api_key = dify_client.api_key
        original_data_api_key = dify_client.data_api_key

        dify_client.base_url = config.base_url
        dify_client.api_key = config.api_key
        # 对于数据集操作，使用数据集API密钥
        dify_client.data_api_key = config.api_key

        params = {"page": page, "limit": limit}
        if keyword:
            params["keyword"] = keyword

        response = await dify_client.get_datasets(**params)

        # 恢复原始配置
        dify_client.base_url = original_base_url
        dify_client.api_key = original_api_key
        dify_client.data_api_key = original_data_api_key

        return response
    except Exception as e:
        # 确保异常时也恢复配置
        if 'original_base_url' in locals() and 'original_api_key' in locals() and 'original_data_api_key' in locals():
            dify_client.base_url = original_base_url
            dify_client.api_key = original_api_key
            dify_client.data_api_key = original_data_api_key
        raise HTTPException(status_code=500, detail=f"获取知识库列表失败: {str(e)}")

@router.post("/")
async def create_dataset(
    dataset_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    try:
        response = await dify_client.create_dataset(dataset_data)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建知识库失败: {str(e)}")

@router.get("/{dataset_id}/files")
async def get_dataset_files(
    dataset_id: str,
    keyword: str = None,
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    try:
        params = {"page": page, "limit": limit}
        if keyword:
            params["keyword"] = keyword

        response = await dify_client.get_dataset_documents(dataset_id, **params)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取文档列表失败: {str(e)}")

@router.post("/{dataset_id}/files")
async def upload_file_to_dataset(
    dataset_id: str,
    file: UploadFile = File(...),
    process_rule: str = Form("automatic"),
    indexing_technique: str = Form("high_quality"),
    db: Session = Depends(get_db)
):
    try:
        # 读取文件内容
        file_content = await file.read()

        # 调用Dify API上传文件
        response = await dify_client.create_document_by_file(
            dataset_id=dataset_id,
            data={
                "process_rule": process_rule,
                "indexing_technique": indexing_technique,
                "original_url": ""
            },
            files={"file": (file.filename, file_content, file.content_type)}
        )

        return {
            "message": "文件上传成功",
            "dataset_id": dataset_id,
            "file_name": file.filename,
            "document_id": response.get("document_id"),
            "result": response
        }

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Dify文件上传失败: {e.response.text}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")

@router.delete("/{dataset_id}/files/{document_id}")
async def delete_document(
    dataset_id: str,
    document_id: str,
    db: Session = Depends(get_db)
):
    try:
        response = await dify_client.delete_document(dataset_id, document_id)
        return {"message": "文档删除成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除文档失败: {str(e)}")

@router.delete("/{dataset_id}")
async def delete_dataset(
    dataset_id: str,
    db: Session = Depends(get_db)
):
    try:
        response = await dify_client.delete_dataset(dataset_id)
        return {"message": "知识库删除成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除知识库失败: {str(e)}")