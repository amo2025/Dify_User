"""
全局错误处理工具
"""
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exceptions import RequestValidationError
from typing import Union
import logging

logger = logging.getLogger(__name__)

async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""

    # 记录错误日志
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail,
                "code": exc.status_code,
                "success": False
            }
        )

    elif isinstance(exc, RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "error": "请求参数验证失败",
                "details": exc.errors(),
                "code": 422,
                "success": False
            }
        )

    # 其他未处理异常
    return JSONResponse(
        status_code=500,
        content={
            "error": "服务器内部错误",
            "code": 500,
            "success": False
        }
    )

def create_error_response(
    status_code: int,
    message: str,
    details: Union[dict, list, None] = None
):
    """创建标准错误响应"""
    return JSONResponse(
        status_code=status_code,
        content={
            "error": message,
            "details": details,
            "code": status_code,
            "success": False
        }
    )

def handle_dify_api_error(exc: Exception) -> HTTPException:
    """处理Dify API错误"""
    if hasattr(exc, 'response') and hasattr(exc.response, 'status_code'):
        status_code = exc.response.status_code
        detail = f"Dify API错误: {getattr(exc.response, 'text', str(exc))}"
    else:
        status_code = 500
        detail = f"Dify连接错误: {str(exc)}"

    return HTTPException(status_code=status_code, detail=detail)