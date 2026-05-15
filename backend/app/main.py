from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from . import models, schemas
from .database import engine, get_db


class TimestampConvertRequest(BaseModel):
    timestamp: Optional[int] = None
    datetime_str: Optional[str] = None
    format: Optional[str] = "%Y-%m-%d %H:%M:%S"


class TimestampConvertResponse(BaseModel):
    timestamp: int
    datetime_str: str
    format: str

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="便携工具平台 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "欢迎使用便携工具平台 API", "version": "1.0.0"}


@app.get("/api/tools", response_model=List[schemas.Tool])
def get_tools(db: Session = Depends(get_db)):
    tools = db.query(models.Tool).all()
    return tools


@app.post("/api/tools", response_model=schemas.Tool)
def create_tool(tool: schemas.ToolCreate, db: Session = Depends(get_db)):
    db_tool = models.Tool(**tool.model_dump())
    db.add(db_tool)
    db.commit()
    db.refresh(db_tool)
    return db_tool


@app.get("/api/tools/{tool_id}", response_model=schemas.Tool)
def get_tool(tool_id: int, db: Session = Depends(get_db)):
    tool = db.query(models.Tool).filter(models.Tool.id == tool_id).first()
    if tool is None:
        raise HTTPException(status_code=404, detail="工具不存在")
    return tool


@app.get("/api/health")
def health_check():
    return {"status": "healthy"}


@app.post("/api/tools/timestamp/convert", response_model=TimestampConvertResponse)
def convert_timestamp(request: TimestampConvertRequest):
    if request.timestamp is not None:
        dt = datetime.fromtimestamp(request.timestamp)
        datetime_str = dt.strftime(request.format)
        return TimestampConvertResponse(
            timestamp=request.timestamp,
            datetime_str=datetime_str,
            format=request.format
        )
    elif request.datetime_str is not None:
        try:
            dt = datetime.strptime(request.datetime_str, request.format)
            timestamp = int(dt.timestamp())
            return TimestampConvertResponse(
                timestamp=timestamp,
                datetime_str=request.datetime_str,
                format=request.format
            )
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"时间格式不匹配，请使用格式: {request.format}"
            )
    else:
        dt = datetime.now()
        timestamp = int(dt.timestamp())
        datetime_str = dt.strftime(request.format)
        return TimestampConvertResponse(
            timestamp=timestamp,
            datetime_str=datetime_str,
            format=request.format
        )


@app.get("/api/tools/timestamp/now")
def get_current_timestamp():
    dt = datetime.now()
    return {
        "timestamp": int(dt.timestamp()),
        "datetime_str": dt.strftime("%Y-%m-%d %H:%M:%S"),
        "milliseconds": int(dt.timestamp() * 1000)
    }
