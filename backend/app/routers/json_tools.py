from fastapi import APIRouter
import json
from ..schemas import JsonFormatRequest, JsonFormatResponse

router = APIRouter(prefix="/json", tags=["json"])


@router.post("/format", response_model=JsonFormatResponse)
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


@router.post("/validate", response_model=JsonFormatResponse)
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
