from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.templates import templates
from app.routes import schedule, bands, venues

app = FastAPI()
app.include_router(schedule.router)
app.include_router(bands.router)
app.include_router(venues.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "title": "Welcome to Brecon Jazz"})