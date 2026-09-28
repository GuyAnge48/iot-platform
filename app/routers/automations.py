# app/routers/automations.py
# Page automatisations — règles IF/THEN pour les appareils IoT
# Permet de créer des règles : si condition → action

from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.mock.data import MOCK_AUTOMATIONS, MOCK_DEVICES

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/automations")
async def automations_page(request: Request):
    """Page principale des automatisations."""

    # Statistiques des règles
    active   = sum(1 for a in MOCK_AUTOMATIONS if a["status"] == "active")
    inactive = sum(1 for a in MOCK_AUTOMATIONS if a["status"] == "inactive")
    total_triggers = sum(a["trigger_count"] for a in MOCK_AUTOMATIONS)

    return templates.TemplateResponse(request, "app/automations/index.html", {
        "automations": MOCK_AUTOMATIONS,
        "devices": MOCK_DEVICES,
        "stats": {
            "total": len(MOCK_AUTOMATIONS),
            "active": active,
            "inactive": inactive,
            "total_triggers": total_triggers,
        },
        "active_page": "automations",
    })

@router.post("/automations/{auto_id}/toggle")
async def toggle_automation(auto_id: str):
    """
    MOCK — Active ou désactive une règle.
    HTMX appelle cet endpoint et remplace le badge de statut.
    """
    automation = next((a for a in MOCK_AUTOMATIONS if a["id"] == auto_id), None)
    if not automation:
        return HTMLResponse("Règle introuvable", status_code=404)

    # Bascule le statut
    automation["status"] = "inactive" if automation["status"] == "active" else "active"
    is_active = automation["status"] == "active"

    # Retourne un fragment HTML — HTMX remplace le badge
    return HTMLResponse(f"""
    <div id="status-{auto_id}" class="flex items-center gap-2">
        <span class="text-xs px-2 py-0.5 rounded-full
            {'bg-green-900/50 text-green-400 border border-green-800' if is_active
             else 'bg-gray-800 text-gray-500 border border-gray-700'}">
            {'Active' if is_active else 'Inactive'}
        </span>
        <button hx-post="/automations/{auto_id}/toggle"
                hx-target="#status-{auto_id}"
                hx-swap="outerHTML"
                class="text-xs px-2 py-0.5 rounded border
                    {'border-red-800 text-red-400 hover:bg-red-900/20' if is_active
                     else 'border-green-800 text-green-400 hover:bg-green-900/20'}
                    transition-colors">
            {'Désactiver' if is_active else 'Activer'}
        </button>
    </div>
    """)
