from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/tools", tags=["tools"])


@router.get("", response_model=List[schemas.Tool])
def get_tools(db: Session = Depends(get_db)):
    tools = db.query(models.Tool).all()
    return tools


@router.post("", response_model=schemas.Tool)
def create_tool(tool: schemas.ToolCreate, db: Session = Depends(get_db)):
    db_tool = models.Tool(**tool.model_dump())
    db.add(db_tool)
    db.commit()
    db.refresh(db_tool)
    return db_tool


@router.get("/{tool_id}", response_model=schemas.Tool)
def get_tool(tool_id: int, db: Session = Depends(get_db)):
    tool = db.query(models.Tool).filter(models.Tool.id == tool_id).first()
    if tool is None:
        raise HTTPException(status_code=404, detail="工具不存在")
    return tool
