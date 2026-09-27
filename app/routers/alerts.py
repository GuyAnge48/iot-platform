# app/routers/alerts.py
# Routeur alertes — liste et acquittement

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.mock.data import MOCK_ALERTS

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/alerts")
async def alerts_list(request: Request):
    return templates.TemplateResponse(request, "app/alerts/list.html", {
        "alerts": MOCK_ALERTS,
        "active_page": "alerts",
    })

@router.post("/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: str):
    """MOCK — acquitte une alerte (mise à jour en mémoire uniquement)."""
    alert = next((a for a in MOCK_ALERTS if a["id"] == alert_id), None)
    if alert:
        alert["acknowledged"] = True
    return HTMLResponse('<span class="text-xs text-gray-500 italic">Acquittée</span>')