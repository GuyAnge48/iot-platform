# app/routers/dashboard.py
# Page principale du dashboard — stats globales + appareils récents + alertes actives

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.mock.data import MOCK_DEVICES, MOCK_ALERTS, get_stats

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse(request, "app/dashboard/index.html", {
        "stats": get_stats(),
        "devices": MOCK_DEVICES[:4],
        "alerts": [a for a in MOCK_ALERTS if not a["acknowledged"]],
        "active_page": "dashboard",
    })