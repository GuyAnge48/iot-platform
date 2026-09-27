# app/routers/devices.py
# Routeur appareils — liste, fiche détail, envoi de commande

from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.mock.data import MOCK_DEVICES, get_telemetry_mock
import json

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/devices")
async def devices_list(request: Request, search: str = ""):
    devices = MOCK_DEVICES
    if search:
        devices = [d for d in devices if search.lower() in d["name"].lower()]

    # Retour fragment HTML si requête HTMX (recherche live)
    if request.headers.get("HX-Request"):
        return templates.TemplateResponse(request, "app/devices/_list_fragment.html", {"devices": devices})

    return templates.TemplateResponse(request, "app/devices/list.html", {
        "devices": devices,
        "search": search,
        "active_page": "devices",
    })

@router.get("/devices/{device_id}")
async def device_detail(request: Request, device_id: str):
    device = next((d for d in MOCK_DEVICES if d["id"] == device_id), None)
    if not device:
        return templates.TemplateResponse(request, "app/devices/list.html", {
            "devices": MOCK_DEVICES,
            "error": "Appareil introuvable",
        })

    # Télémétrie simulée sur le premier composant de type sensor
    sensor_components = [c for c in device["components"] if c["type"] == "sensor"]
    telemetry = []
    if sensor_components:
        telemetry = get_telemetry_mock(device_id, sensor_components[0]["id"])

    return templates.TemplateResponse(request, "app/devices/detail.html", {
        "device": device,
        "telemetry": json.dumps(telemetry),
        "active_page": "devices",
    })

@router.post("/devices/{device_id}/command")
async def send_command(request: Request, device_id: str, command: str = Form(...)):
    """MOCK — simule l'envoi d'une commande vers un appareil."""
    device = next((d for d in MOCK_DEVICES if d["id"] == device_id), None)
    success = device and device["status"] != "offline"

    if success:
        html = f"""
        <div id="command-result"
             class="bg-green-900/40 border border-green-700 text-green-300 rounded-lg p-3 text-sm flex items-center gap-2"
             _="on load wait 3s then add .opacity-0 .transition-opacity then wait 0.5s then remove me">
            <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
            Commande <strong class="text-green-200">{command}</strong> envoyée avec succès.
        </div>"""
    else:
        html = """
        <div id="command-result"
             class="bg-red-900/40 border border-red-700 text-red-300 rounded-lg p-3 text-sm flex items-center gap-2">
            <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
            Échec : appareil hors ligne.
        </div>"""
    return HTMLResponse(html)