from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import tools, timestamp, json_tools, md5_tools, number_chinese, rsa_tools, timer, weight_convert, time_difference

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


@app.get("/api/health")
def health_check():
    return {"status": "healthy"}


app.include_router(tools.router, prefix="/api")
app.include_router(timestamp.router, prefix="/api/tools")
app.include_router(json_tools.router, prefix="/api/tools")
app.include_router(md5_tools.router, prefix="/api/tools")
app.include_router(number_chinese.router, prefix="/api/tools")
app.include_router(rsa_tools.router, prefix="/api/tools")
app.include_router(timer.router, prefix="/api/tools")
app.include_router(weight_convert.router, prefix="/api/tools")
app.include_router(time_difference.router, prefix="/api/tools")
