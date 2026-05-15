from fastapi import APIRouter, HTTPException
import hashlib
from ..schemas import Md5EncryptRequest, Md5EncryptResponse, Md5CompareRequest, Md5CompareResponse

router = APIRouter(prefix="/md5", tags=["md5"])


@router.post("/encrypt", response_model=Md5EncryptResponse)
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


@router.post("/compare", response_model=Md5CompareResponse)
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
