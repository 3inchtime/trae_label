from fastapi import APIRouter, HTTPException
from urllib.parse import quote, unquote
from ..schemas import UrlEncodeRequest, UrlEncodeResponse, UrlDecodeRequest, UrlDecodeResponse

router = APIRouter(prefix="/url", tags=["url"])


@router.post("/encode", response_model=UrlEncodeResponse)
def url_encode(request: UrlEncodeRequest):
    if not request.url:
        raise HTTPException(status_code=400, detail="请输入要编码的URL或文本")
    
    try:
        encoded = quote(request.url, safe=request.safe)
        return UrlEncodeResponse(
            original=request.url,
            encoded=encoded
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"编码失败: {str(e)}")


@router.post("/decode", response_model=UrlDecodeResponse)
def url_decode(request: UrlDecodeRequest):
    if not request.url:
        raise HTTPException(status_code=400, detail="请输入要解码的URL或文本")
    
    try:
        decoded = unquote(request.url)
        return UrlDecodeResponse(
            original=request.url,
            decoded=decoded
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"解码失败: {str(e)}")
