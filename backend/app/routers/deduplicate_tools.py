from fastapi import APIRouter, HTTPException
from ..schemas import DeduplicateRequest, DeduplicateResponse
from collections import OrderedDict

router = APIRouter(prefix="/deduplicate", tags=["deduplicate"])


@router.post("/process", response_model=DeduplicateResponse)
def deduplicate_text(request: DeduplicateRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="请输入要去重的文本")

    lines = request.text.split('\n')
    original_line_count = len(lines)

    processed_lines = []
    seen = set()

    for line in lines:
        if request.remove_empty_lines and not line.strip():
            continue

        key = line.lower() if request.ignore_case else line

        if key not in seen:
            seen.add(key)
            processed_lines.append(line)

    if not request.keep_order:
        processed_lines = sorted(processed_lines)

    deduplicated_text = '\n'.join(processed_lines)
    deduplicated_line_count = len(processed_lines)
    removed_count = original_line_count - deduplicated_line_count

    return DeduplicateResponse(
        original_text=request.text,
        deduplicated_text=deduplicated_text,
        original_line_count=original_line_count,
        deduplicated_line_count=deduplicated_line_count,
        removed_count=removed_count,
        ignore_case=request.ignore_case,
        remove_empty_lines=request.remove_empty_lines,
        keep_order=request.keep_order
    )
