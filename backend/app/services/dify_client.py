import httpx
import os
from typing import Dict, Any, Optional
from fastapi import HTTPException

class DifyClient:
    def __init__(self):
        self.base_url = os.getenv("DIFY_BASE_URL", "https://api.dify.ai/v1")
        self.api_key = os.getenv("DIFY_API_KEY")
        self.data_api_key = os.getenv("DIFY_DATASET_API_KEY", self.api_key)
        self.client = httpx.AsyncClient()

    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """通用请求方法，使用工作流API密钥"""
        return await self._make_request_with_key(method, endpoint, self.api_key, **kwargs)

    async def _make_data_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """数据集相关请求，使用数据集API密钥"""
        return await self._make_request_with_key(method, endpoint, self.data_api_key, **kwargs)

    async def _make_request_with_key(self, method: str, endpoint: str, api_key: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # 如果没有API密钥，使用空授权头
        if not api_key:
            headers.pop("Authorization", None)

        try:
            response = await self.client.request(
                method, url, headers=headers, **kwargs
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Dify API error: {e.response.text}"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Dify connection error: {str(e)}"
            )

    # 知识库相关API
    async def get_datasets(self, **params):
        return await self._make_data_request("GET", "/datasets", params=params)

    async def create_dataset(self, data: Dict[str, Any]):
        return await self._make_data_request("POST", "/datasets", json=data)

    async def delete_dataset(self, dataset_id: str):
        return await self._make_data_request("DELETE", f"/datasets/{dataset_id}")

    async def get_dataset_documents(self, dataset_id: str, **params):
        return await self._make_data_request("GET", f"/datasets/{dataset_id}/documents", params=params)

    async def create_document_by_file(self, dataset_id: str, data: Dict[str, Any], files: Dict[str, Any]):
        url = f"{self.base_url}/datasets/{dataset_id}/document/create-by-file"
        headers = {
            "Authorization": f"Bearer {self.data_api_key}",
        }

        try:
            # 创建multipart form数据
            form_data = {}
            for key, value in data.items():
                form_data[key] = (None, str(value))

            # 添加文件
            form_data.update(files)

            response = await self.client.post(
                url, headers=headers, files=form_data
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Dify API error: {e.response.text}"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Dify connection error: {str(e)}"
            )

    async def delete_document(self, dataset_id: str, document_id: str):
        return await self._make_data_request("DELETE", f"/datasets/{dataset_id}/documents/{document_id}")

    # 工作流相关API
    async def run_workflow(self, data: Dict[str, Any]):
        return await self._make_request("POST", "/workflows/run", json=data)

    async def get_workflow_run(self, workflow_run_id: str):
        return await self._make_request("GET", f"/workflows/run/{workflow_run_id}")

    # 文件上传API
    async def upload_file(self, file_data: bytes, filename: str, user: str):
        files = {"file": (filename, file_data)}
        data = {"user": user}
        return await self._make_request("POST", "/files/upload", files=files, data=data)

    async def close(self):
        await self.client.aclose()

# 全局Dify客户端实例（延迟初始化）
def get_dify_client():
    """获取Dify客户端实例，确保环境变量已加载"""
    from dotenv import load_dotenv
    load_dotenv(dotenv_path="/Volumes/Users/dev/qoder/Dify_User/.env")
    return DifyClient()

dify_client = get_dify_client()