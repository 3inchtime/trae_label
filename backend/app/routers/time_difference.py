from fastapi import APIRouter, HTTPException
from datetime import datetime
from ..schemas import TimeDifferenceRequest, TimeDifferenceResponse

router = APIRouter(prefix="/time-difference", tags=["time-difference"])


@router.post("/calculate", response_model=TimeDifferenceResponse)
def calculate_time_difference(request: TimeDifferenceRequest):
    try:
        start = datetime.strptime(request.start_time, request.format)
        end = datetime.strptime(request.end_time, request.format)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"时间格式不匹配，请使用格式: {request.format}"
        )
    
    if end < start:
        start, end = end, start
    
    delta = end - start
    
    years = end.year - start.year
    months = end.month - start.month
    days = end.day - start.day
    
    if days < 0:
        months -= 1
        prev_month = end.month - 1 if end.month > 1 else 12
        if prev_month in [1, 3, 5, 7, 8, 10, 12]:
            days_in_prev_month = 31
        elif prev_month in [4, 6, 9, 11]:
            days_in_prev_month = 30
        else:
            year = end.year if prev_month != 12 else end.year - 1
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                days_in_prev_month = 29
            else:
                days_in_prev_month = 28
        days += days_in_prev_month
    
    if months < 0:
        years -= 1
        months += 12
    
    total_seconds = int(delta.total_seconds())
    total_minutes = total_seconds // 60
    total_hours = total_minutes // 60
    total_days = delta.days
    
    remaining_seconds = total_seconds % 60
    remaining_minutes = (total_seconds // 60) % 60
    remaining_hours = (total_seconds // 3600) % 24
    
    return TimeDifferenceResponse(
        start_time=request.start_time,
        end_time=request.end_time,
        years=years,
        months=months,
        days=days,
        hours=remaining_hours,
        minutes=remaining_minutes,
        seconds=remaining_seconds,
        total_days=total_days,
        total_hours=total_hours,
        total_minutes=total_minutes,
        total_seconds=total_seconds
    )
