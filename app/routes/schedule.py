from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.templates import templates

router = APIRouter()

@router.get("/schedule", response_class=HTMLResponse)
async def get_schedule(request: Request):
    # For now, static placeholder data
    schedule_data  = [
        {"time": "12:00", "venue": "Main Stage", "act": "Jazz Trio"},
        {"time": "13:00", "venue": "Main Stage", "act": "Sax Quartet"},
        {"time": "12:30", "venue": "Side Stage", "act": "Blues Duo"},
    ]
    return templates.TemplateResponse("schedule.html", {"request": request, "schedule": schedule_data})