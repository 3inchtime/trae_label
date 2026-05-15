from fastapi import APIRouter, HTTPException
from datetime import datetime
from ..schemas import TimestampConvertResponse, TimestampConvertRequest

router = APIRouter(prefix="/timestamp", tags=["timestamp"])


@router.post("/convert", response_model=TimestampConvertResponse)
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


@router.get("/now")
def get_current_timestamp():
    dt = datetime.now()
    return {
        "timestamp": int(dt.timestamp()),
        "datetime_str": dt.strftime("%Y-%m-%d %H:%M:%S"),
        "milliseconds": int(dt.timestamp() * 1000)
    }
