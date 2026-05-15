from fastapi import APIRouter, HTTPException
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import base64
from ..schemas import RsaKeyGenerateRequest, RsaKeyGenerateResponse, RsaEncryptRequest, RsaEncryptResponse, RsaDecryptRequest, RsaDecryptResponse

router = APIRouter(prefix="/rsa", tags=["rsa"])


@router.post("/generate-keys", response_model=RsaKeyGenerateResponse)
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


@router.post("/encrypt", response_model=RsaEncryptResponse)
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


@router.post("/decrypt", response_model=RsaDecryptResponse)
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
