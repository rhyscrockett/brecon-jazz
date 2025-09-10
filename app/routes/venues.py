from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.templates import templates

router = APIRouter()

@router.get("/venues", response_class=HTMLResponse)
async def get_venues(request: Request):
    # Only render template; all data is loaded client-side from static JSON
    return templates.TemplateResponse(
        "venues.html",
        {"request": request, "title": "Venues"}
    )