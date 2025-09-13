from fastapi.templating import Jinja2Templates
from pathlib import Path
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Define custom Jinja filters
def todatetime(value):
    if isinstance(value, datetime):
        return value
    return datetime.strptime(value, "%Y-%m-%d")

def datetimeadd(value, days=0):
    return value + timedelta(days=days)

def datetimeformat(value, format_str="%Y-%m-%d"):
    return value.strftime(format_str)

templates.env.filters["todatetime"] = todatetime
templates.env.filters["datetimeadd"] = datetimeadd
templates.env.filters["datetimeformat"] = datetimeformat
