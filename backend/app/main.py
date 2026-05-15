from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
import json
import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import base64

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


class JsonFormatRequest(BaseModel):
    json_str: str
    indent: Optional[int] = 2


class JsonFormatResponse(BaseModel):
    valid: bool
    formatted: Optional[str] = None
    error: Optional[str] = None
    minified: Optional[str] = None


class Md5EncryptRequest(BaseModel):
    text: str
    uppercase: Optional[bool] = False


class Md5EncryptResponse(BaseModel):
    original_text: str
    md5_hash: str
    uppercase: bool


class Md5CompareRequest(BaseModel):
    text: str
    md5_hash: str


class Md5CompareResponse(BaseModel):
    match: bool
    original_text: str
    provided_hash: str


class NumberToChineseRequest(BaseModel):
    number: float


class NumberToChineseResponse(BaseModel):
    number: float
    chinese: str


class RsaKeyGenerateRequest(BaseModel):
    key_size: Optional[int] = 2048


class RsaKeyGenerateResponse(BaseModel):
    public_key: str
    private_key: str
    key_size: int


class RsaEncryptRequest(BaseModel):
    plaintext: str
    public_key: str


class RsaEncryptResponse(BaseModel):
    ciphertext: str
    plaintext: str


class RsaDecryptRequest(BaseModel):
    ciphertext: str
    private_key: str


class RsaDecryptResponse(BaseModel):
    plaintext: str
    ciphertext: str


def number_to_chinese(num):
    digits = ['零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖']
    units = ['', '拾', '佰', '仟']
    big_units = ['', '万', '亿', '兆']
    
    if num == 0:
        return '零元整'
    
    if num < 0:
        return '负' + number_to_chinese(abs(num))
    
    integer_part = int(num)
    decimal_part = int(round((num - integer_part) * 100))
    
    result = ''
    
    if integer_part > 0:
        integer_str = str(integer_part)
        length = len(integer_str)
        zero_flag = False
        
        for i, digit in enumerate(integer_str):
            d = int(digit)
            pos = length - 1 - i
            unit_pos = pos % 4
            big_unit_pos = pos // 4
            
            if d == 0:
                zero_flag = True
                if unit_pos == 0 and big_unit_pos > 0:
                    result += big_units[big_unit_pos]
            else:
                if zero_flag:
                    result += '零'
                    zero_flag = False
                result += digits[d] + units[unit_pos]
                if unit_pos == 0 and big_unit_pos > 0:
                    result += big_units[big_unit_pos]
        
        result += '元'
    
    if decimal_part > 0:
        jiao = decimal_part // 10
        fen = decimal_part % 10
        
        if jiao > 0:
            result += digits[jiao] + '角'
        elif integer_part > 0 and fen > 0:
            result += '零'
        
        if fen > 0:
            result += digits[fen] + '分'
    else:
        result += '整'
    
    return result


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


@app.post("/api/tools/json/format", response_model=JsonFormatResponse)
def format_json(request: JsonFormatRequest):
    try:
        parsed = json.loads(request.json_str)
        formatted = json.dumps(parsed, indent=request.indent, ensure_ascii=False)
        minified = json.dumps(parsed, separators=(',', ':'), ensure_ascii=False)
        return JsonFormatResponse(
            valid=True,
            formatted=formatted,
            minified=minified,
            error=None
        )
    except json.JSONDecodeError as e:
        return JsonFormatResponse(
            valid=False,
            formatted=None,
            minified=None,
            error=f"JSON解析错误: {str(e)}"
        )


@app.post("/api/tools/json/validate", response_model=JsonFormatResponse)
def validate_json(request: JsonFormatRequest):
    try:
        parsed = json.loads(request.json_str)
        return JsonFormatResponse(
            valid=True,
            formatted=None,
            minified=None,
            error=None
        )
    except json.JSONDecodeError as e:
        return JsonFormatResponse(
            valid=False,
            formatted=None,
            minified=None,
            error=f"JSON解析错误: {str(e)}"
        )


@app.post("/api/tools/md5/encrypt", response_model=Md5EncryptResponse)
def md5_encrypt(request: Md5EncryptRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="请输入要加密的文本")
    
    md5 = hashlib.md5()
    md5.update(request.text.encode('utf-8'))
    md5_hash = md5.hexdigest()
    
    if request.uppercase:
        md5_hash = md5_hash.upper()
    
    return Md5EncryptResponse(
        original_text=request.text,
        md5_hash=md5_hash,
        uppercase=request.uppercase
    )


@app.post("/api/tools/md5/compare", response_model=Md5CompareResponse)
def md5_compare(request: Md5CompareRequest):
    if not request.text or not request.md5_hash:
        raise HTTPException(status_code=400, detail="请输入文本和MD5哈希值")
    
    md5 = hashlib.md5()
    md5.update(request.text.encode('utf-8'))
    calculated_hash = md5.hexdigest()
    
    match = calculated_hash.lower() == request.md5_hash.lower()
    
    return Md5CompareResponse(
        match=match,
        original_text=request.text,
        provided_hash=request.md5_hash
    )


@app.post("/api/tools/number-to-chinese", response_model=NumberToChineseResponse)
def convert_number_to_chinese(request: NumberToChineseRequest):
    chinese = number_to_chinese(request.number)
    return NumberToChineseResponse(
        number=request.number,
        chinese=chinese
    )


@app.post("/api/tools/rsa/generate-keys", response_model=RsaKeyGenerateResponse)
def generate_rsa_keys(request: RsaKeyGenerateRequest):
    valid_key_sizes = [1024, 2048, 3072, 4096]
    if request.key_size not in valid_key_sizes:
        raise HTTPException(
            status_code=400,
            detail=f"密钥长度必须是: {', '.join(map(str, valid_key_sizes))}"
        )
    
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=request.key_size,
        backend=default_backend()
    )
    
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    return RsaKeyGenerateResponse(
        public_key=public_pem.decode('utf-8'),
        private_key=private_pem.decode('utf-8'),
        key_size=request.key_size
    )


@app.post("/api/tools/rsa/encrypt", response_model=RsaEncryptResponse)
def rsa_encrypt(request: RsaEncryptRequest):
    if not request.plaintext:
        raise HTTPException(status_code=400, detail="请输入要加密的明文")
    if not request.public_key:
        raise HTTPException(status_code=400, detail="请输入公钥")
    
    try:
        public_key = serialization.load_pem_public_key(
            request.public_key.encode('utf-8'),
            backend=default_backend()
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"公钥格式错误: {str(e)}")
    
    try:
        ciphertext = public_key.encrypt(
            request.plaintext.encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        ciphertext_base64 = base64.b64encode(ciphertext).decode('utf-8')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"加密失败: {str(e)}")
    
    return RsaEncryptResponse(
        ciphertext=ciphertext_base64,
        plaintext=request.plaintext
    )


@app.post("/api/tools/rsa/decrypt", response_model=RsaDecryptResponse)
def rsa_decrypt(request: RsaDecryptRequest):
    if not request.ciphertext:
        raise HTTPException(status_code=400, detail="请输入要解密的密文")
    if not request.private_key:
        raise HTTPException(status_code=400, detail="请输入私钥")
    
    try:
        private_key = serialization.load_pem_private_key(
            request.private_key.encode('utf-8'),
            password=None,
            backend=default_backend()
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"私钥格式错误: {str(e)}")
    
    try:
        ciphertext_bytes = base64.b64decode(request.ciphertext)
        plaintext_bytes = private_key.decrypt(
            ciphertext_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        plaintext = plaintext_bytes.decode('utf-8')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"解密失败: {str(e)}")
    
    return RsaDecryptResponse(
        plaintext=plaintext,
        ciphertext=request.ciphertext
    )
