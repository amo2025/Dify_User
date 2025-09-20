from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import uuid

from app.utils.database import get_db
from app.models.model import AIModel

router = APIRouter()

@router.get("/")
def get_models(db: Session = Depends(get_db)):
    models = db.query(AIModel).all()
    return models

@router.post("/")
def create_model(
    model_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    model_id = str(uuid.uuid4())

    model = AIModel(
        id=model_id,
        name=model_data["name"],
        provider=model_data["provider"],
        model_name=model_data["model_name"],
        base_url=model_data.get("base_url"),
        api_key=model_data.get("api_key"),
        enabled=model_data.get("enabled", True),
        config=model_data.get("config", {})
    )

    db.add(model)
    db.commit()
    db.refresh(model)

    return {
        "message": "模型创建成功",
        "model": model
    }

@router.patch("/{model_id}")
def update_model(
    model_id: str,
    update_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    model = db.query(AIModel).filter(AIModel.id == model_id).first()

    if not model:
        raise HTTPException(status_code=404, detail="模型不存在")

    for key, value in update_data.items():
        if hasattr(model, key):
            setattr(model, key, value)

    db.commit()
    db.refresh(model)

    return {
        "message": "模型更新成功",
        "model": model
    }

@router.delete("/{model_id}")
def delete_model(
    model_id: str,
    db: Session = Depends(get_db)
):
    model = db.query(AIModel).filter(AIModel.id == model_id).first()

    if not model:
        raise HTTPException(status_code=404, detail="模型不存在")

    db.delete(model)
    db.commit()

    return {"message": "模型删除成功"}