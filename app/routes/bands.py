from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.templates import templates

router = APIRouter()

@router.get("/bands", response_class=HTMLResponse)
async def get_bands(request: Request):
    # Placeholder band data
    bands_data = [
        {"name": "Jazz Trio", "social": "#", "sample": "#"},
        {"name": "Sax Quartet", "social": "#", "sample": "#"},
        {"name": "Blues Duo", "social": "#", "sample": "#"},
    ]
    return templates.TemplateResponse("bands.html", {"request": request, "bands": bands_data})