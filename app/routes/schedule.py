from datetime import datetime, timedelta
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.templates import templates
from app.database import AsyncSessionLocal
from app.models import Gig

router = APIRouter()

# Dependency to get async DB session
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

# Fetch gigs with band and venue info for a given day
async def fetch_gigs_for_day(db: AsyncSession, day_str: str):
    day_start = datetime.strptime(day_str, "%Y-%m-%d")
    day_end = day_start + timedelta(days=1)

    stmt = select(Gig).options(joinedload(Gig.band), joinedload(Gig.venue)).where(
        Gig.start_time >= day_start, Gig.start_time < day_end
    )
    result = await db.execute(stmt)
    gigs = result.scalars().all()
    return gigs

@router.get("/schedule", response_class=HTMLResponse)
async def schedule_index(request: Request, db: AsyncSession = Depends(get_session)):
    day_str = datetime.now().strftime("%Y-%m-%d")
    gigs = await fetch_gigs_for_day(db, day_str)

    venues = sorted({gig.venue for gig in gigs}, key=lambda v: v.name)
    
    base_date = datetime.strptime(day_str, "%Y-%m-%d")
    start_hour, end_hour = 10, 23
    slots = []
    current = base_date.replace(hour=start_hour, minute=0, second=0)
    end = base_date.replace(hour=end_hour, minute=0, second=0)

    while current <= end:
        slots.append((current.strftime("%H:%M"), []))
        current += timedelta(minutes=30)

    for slot_label, gig_list in slots:
        slot_time = datetime.strptime(f"{day_str} {slot_label}", "%Y-%m-%d %H:%M")
        for gig in gigs:
            if gig.start_time == slot_time:
                duration = max(1, int((gig.end_time - gig.start_time).total_seconds() // 1800))
                gig_display = {
                    "id": gig.id,
                    "act_name": gig.band.name,
                    "venue": {"name": gig.venue.name, "color": gig.venue.color},
                    "duration_slots": duration,
                    "description": gig.description or "",
                }
                gig_list.append(gig_display)

    return templates.TemplateResponse(
        "schedule.html",
        {
            "request": request,
            "time_slots": slots,
            "day": day_str,
            "venues": [{"name": v.name, "color": v.color} for v in venues],
        },
    )


@router.get("/schedule/{day}", response_class=HTMLResponse)
async def get_schedule_day(request: Request, day: str, db: AsyncSession = Depends(get_session)):
    gigs = await fetch_gigs_for_day(db, day)

    venues = sorted({gig.venue for gig in gigs}, key=lambda v: v.name)
    
    base_date = datetime.strptime(day, "%Y-%m-%d")
    start_hour, end_hour = 10, 23
    slots = []
    current = base_date.replace(hour=start_hour, minute=0, second=0)
    end = base_date.replace(hour=end_hour, minute=0, second=0)

    while current <= end:
        slots.append((current.strftime("%H:%M"), []))
        current += timedelta(minutes=30)

    for slot_label, gig_list in slots:
        slot_time = datetime.strptime(f"{day} {slot_label}", "%Y-%m-%d %H:%M")
        for gig in gigs:
            if gig.start_time == slot_time:
                duration = max(1, int((gig.end_time - gig.start_time).total_seconds() // 1800))
                gig_display = {
                    "id": gig.id,
                    "act_name": gig.band.name,
                    "venue": {"name": gig.venue.name, "color": gig.venue.color},
                    "duration_slots": duration,
                    "description": gig.description or "",
                }
                gig_list.append(gig_display)

    template_vars = {
        "request": request,
        "time_slots": slots,
        "day": day,
        "venues": [{"name": v.name, "color": v.color} for v in venues],
    }

    if request.headers.get("Hx-Request"):
        return templates.TemplateResponse("schedule_partial.html", template_vars)
    else:
        return templates.TemplateResponse("schedule.html", template_vars)
