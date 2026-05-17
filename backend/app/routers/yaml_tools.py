from fastapi import APIRouter
import yaml
from yaml.parser import ParserError
from yaml.scanner import ScannerError
from ..schemas import YamlValidateRequest, YamlValidateResponse

router = APIRouter(prefix="/yaml", tags=["yaml"])


@router.post("/validate", response_model=YamlValidateResponse)
def validate_yaml(request: YamlValidateRequest):
    try:
        parsed = yaml.safe_load(request.yaml_str)
        formatted = yaml.dump(parsed, allow_unicode=True, default_flow_style=False, indent=2)
        return YamlValidateResponse(
            valid=True,
            formatted=formatted,
            error=None,
            line=None,
            column=None
        )
    except (ParserError, ScannerError) as e:
        line = e.problem_mark.line + 1 if e.problem_mark else None
        column = e.problem_mark.column + 1 if e.problem_mark else None
        return YamlValidateResponse(
            valid=False,
            formatted=None,
            error=f"YAML解析错误: {str(e.problem)}",
            line=line,
            column=column
        )
    except Exception as e:
        return YamlValidateResponse(
            valid=False,
            formatted=None,
            error=f"错误: {str(e)}",
            line=None,
            column=None
        )


@router.post("/format", response_model=YamlValidateResponse)
def format_yaml(request: YamlValidateRequest):
    try:
        parsed = yaml.safe_load(request.yaml_str)
        formatted = yaml.dump(parsed, allow_unicode=True, default_flow_style=False, indent=2)
        return YamlValidateResponse(
            valid=True,
            formatted=formatted,
            error=None,
            line=None,
            column=None
        )
    except (ParserError, ScannerError) as e:
        line = e.problem_mark.line + 1 if e.problem_mark else None
        column = e.problem_mark.column + 1 if e.problem_mark else None
        return YamlValidateResponse(
            valid=False,
            formatted=None,
            error=f"YAML解析错误: {str(e.problem)}",
            line=line,
            column=column
        )
    except Exception as e:
        return YamlValidateResponse(
            valid=False,
            formatted=None,
            error=f"错误: {str(e)}",
            line=None,
            column=None
        )
