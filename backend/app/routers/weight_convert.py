from fastapi import APIRouter, HTTPException
from ..schemas import WeightConvertRequest, WeightConvertResponse

router = APIRouter(prefix="/weight", tags=["weight"])

WEIGHT_UNITS = {
    'mg': 0.001,
    'g': 1,
    'kg': 1000,
    't': 1000000,
    'oz': 28.3495,
    'lb': 453.592,
    'jin': 500,
    'liang': 50
}


@router.post("/convert", response_model=WeightConvertResponse)
def convert_weight(request: WeightConvertRequest):
    if request.from_unit not in WEIGHT_UNITS:
        raise HTTPException(status_code=400, detail=f"不支持的单位: {request.from_unit}")
    if request.to_unit not in WEIGHT_UNITS:
        raise HTTPException(status_code=400, detail=f"不支持的单位: {request.to_unit}")
    
    grams = request.value * WEIGHT_UNITS[request.from_unit]
    result = grams / WEIGHT_UNITS[request.to_unit]
    
    return WeightConvertResponse(
        value=request.value,
        from_unit=request.from_unit,
        to_unit=request.to_unit,
        result=round(result, 6)
    )
