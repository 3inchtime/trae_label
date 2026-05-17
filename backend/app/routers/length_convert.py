from fastapi import APIRouter, HTTPException
from ..schemas import LengthConvertRequest, LengthConvertResponse

router = APIRouter(prefix="/length", tags=["length"])

LENGTH_UNITS = {
    'mm': 0.001,
    'cm': 0.01,
    'dm': 0.1,
    'm': 1,
    'km': 1000,
    'in': 0.0254,
    'ft': 0.3048,
    'yd': 0.9144,
    'mi': 1609.344,
    'li': 500,
    'zhang': 3.333,
    'chi': 0.333,
    'cun': 0.0333
}


@router.post("/convert", response_model=LengthConvertResponse)
def convert_length(request: LengthConvertRequest):
    if request.from_unit not in LENGTH_UNITS:
        raise HTTPException(status_code=400, detail=f"不支持的单位: {request.from_unit}")
    if request.to_unit not in LENGTH_UNITS:
        raise HTTPException(status_code=400, detail=f"不支持的单位: {request.to_unit}")
    
    meters = request.value * LENGTH_UNITS[request.from_unit]
    result = meters / LENGTH_UNITS[request.to_unit]
    
    return LengthConvertResponse(
        value=request.value,
        from_unit=request.from_unit,
        to_unit=request.to_unit,
        result=round(result, 6)
    )
