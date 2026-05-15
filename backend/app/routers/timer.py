from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List
import uuid
from ..schemas import TimerCreateRequest, TimerCreateResponse, TimerStatusResponse, TimerHistoryItem

router = APIRouter(prefix="/timer", tags=["timer"])

active_timers = {}
timer_history = []


@router.post("/create", response_model=TimerCreateResponse)
def create_timer(request: TimerCreateRequest):
    timer_id = str(uuid.uuid4())
    created_at = datetime.now().isoformat()
    
    active_timers[timer_id] = {
        "id": timer_id,
        "name": request.name,
        "duration": request.duration,
        "remaining": request.duration,
        "status": "pending",
        "created_at": created_at,
        "start_time": None
    }
    
    return TimerCreateResponse(
        id=timer_id,
        name=request.name,
        duration=request.duration,
        created_at=created_at
    )


@router.post("/{timer_id}/start")
def start_timer(timer_id: str):
    if timer_id not in active_timers:
        raise HTTPException(status_code=404, detail="计时器不存在")
    
    timer = active_timers[timer_id]
    timer["status"] = "running"
    timer["start_time"] = datetime.now().isoformat()
    
    return {"success": True, "message": "计时器已启动"}


@router.post("/{timer_id}/pause")
def pause_timer(timer_id: str):
    if timer_id not in active_timers:
        raise HTTPException(status_code=404, detail="计时器不存在")
    
    timer = active_timers[timer_id]
    if timer["status"] == "running":
        if timer["start_time"]:
            elapsed = (datetime.now() - datetime.fromisoformat(timer["start_time"])).total_seconds()
            timer["remaining"] = max(0, timer["remaining"] - int(elapsed))
        timer["status"] = "paused"
    
    return {"success": True, "message": "计时器已暂停"}


@router.post("/{timer_id}/reset")
def reset_timer(timer_id: str):
    if timer_id not in active_timers:
        raise HTTPException(status_code=404, detail="计时器不存在")
    
    timer = active_timers[timer_id]
    timer["status"] = "pending"
    timer["remaining"] = timer["duration"]
    timer["start_time"] = None
    
    return {"success": True, "message": "计时器已重置"}


@router.get("/{timer_id}/status", response_model=TimerStatusResponse)
def get_timer_status(timer_id: str):
    if timer_id not in active_timers:
        raise HTTPException(status_code=404, detail="计时器不存在")
    
    timer = active_timers[timer_id]
    
    if timer["status"] == "running" and timer["start_time"]:
        elapsed = (datetime.now() - datetime.fromisoformat(timer["start_time"])).total_seconds()
        remaining = max(0, timer["remaining"] - int(elapsed))
        
        if remaining <= 0:
            timer["status"] = "completed"
            timer["remaining"] = 0
            timer_history.append({
                "id": timer["id"],
                "name": timer["name"],
                "duration": timer["duration"],
                "completed_at": datetime.now().isoformat()
            })
        else:
            timer["remaining"] = remaining
    
    return TimerStatusResponse(
        id=timer["id"],
        name=timer["name"],
        duration=timer["duration"],
        remaining=timer["remaining"],
        status=timer["status"],
        created_at=timer["created_at"]
    )


@router.delete("/{timer_id}")
def delete_timer(timer_id: str):
    if timer_id not in active_timers:
        raise HTTPException(status_code=404, detail="计时器不存在")
    
    del active_timers[timer_id]
    return {"success": True, "message": "计时器已删除"}


@router.get("/active", response_model=List[TimerStatusResponse])
def get_active_timers():
    result = []
    for timer_id, timer in active_timers.items():
        if timer["status"] == "running" and timer["start_time"]:
            elapsed = (datetime.now() - datetime.fromisoformat(timer["start_time"])).total_seconds()
            remaining = max(0, timer["remaining"] - int(elapsed))
            
            if remaining <= 0:
                timer["status"] = "completed"
                timer["remaining"] = 0
                timer_history.append({
                    "id": timer["id"],
                    "name": timer["name"],
                    "duration": timer["duration"],
                    "completed_at": datetime.now().isoformat()
                })
            else:
                timer["remaining"] = remaining
        
        result.append(TimerStatusResponse(
            id=timer["id"],
            name=timer["name"],
            duration=timer["duration"],
            remaining=timer["remaining"],
            status=timer["status"],
            created_at=timer["created_at"]
        ))
    
    return result


@router.get("/history", response_model=List[TimerHistoryItem])
def get_timer_history():
    return timer_history
