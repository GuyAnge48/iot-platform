# app/routers/telemetry.py
# Page télémétrie globale — vue de tous les appareils et leurs composants
# Permet de sélectionner un appareil et visualiser ses graphiques en temps réel

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.mock.data import MOCK_DEVICES, get_telemetry_mock
import json

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/telemetry")
async def telemetry_page(request: Request, device_id: str = None):
    """
    Page télémétrie globale.
    - Sans paramètre : affiche les stats globales + le premier appareil online
    - Avec device_id : affiche les graphiques de cet appareil
    """

    # Récupère tous les appareils online pour les stats
    online_devices = [d for d in MOCK_DEVICES if d["status"] == "online"]

    # Appareil sélectionné — par défaut le premier online
    selected_device = None
    telemetry_by_component = {}

    if device_id:
        # Cherche l'appareil demandé
        selected_device = next((d for d in MOCK_DEVICES if d["id"] == device_id), None)
    elif online_devices:
        # Par défaut : premier appareil online
        selected_device = online_devices[0]

    # Génère les données de télémétrie pour chaque composant sensor
    if selected_device:
        for component in selected_device["components"]:
            if component["type"] == "sensor":
                telemetry_by_component[component["id"]] = get_telemetry_mock(
                    selected_device["id"],
                    component["id"]
                )

    return templates.TemplateResponse(request, "app/telemetry/index.html", {
        "devices": MOCK_DEVICES,
        "online_devices": online_devices,
        "selected_device": selected_device,
        # Sérialise en JSON pour injection dans le template JavaScript
        "telemetry_by_component": json.dumps(telemetry_by_component),
        "active_page": "telemetry",
    })
