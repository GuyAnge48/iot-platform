# app/routers/settings.py
# Page paramètres — profil utilisateur, configuration plateforme, clés API

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.mock.data import MOCK_SETTINGS, MOCK_API_KEYS
import secrets

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/settings")
async def settings_page(request: Request):
    """Page principale des paramètres."""
    return templates.TemplateResponse(request, "app/settings/index.html", {
        "settings": MOCK_SETTINGS,
        "api_keys": MOCK_API_KEYS,
        "active_page": "settings",
    })

@router.post("/settings/api-keys/generate")
async def generate_api_key():
    """
    MOCK — Génère une nouvelle clé API.
    HTMX appelle cet endpoint et insère la nouvelle clé dans la liste.
    """
    # Génère une clé aléatoire sécurisée
    new_key = f"iot_live_{secrets.token_urlsafe(20)}"
    key_id  = f"key-{len(MOCK_API_KEYS) + 1:03d}"

    # Ajoute la clé au mock
    new_key_obj = {
        "id": key_id,
        "name": f"Nouvelle clé {len(MOCK_API_KEYS) + 1}",
        "key": new_key,
        "permissions": ["read"],
        "created_at": "À l'instant",
        "last_used": "Jamais",
        "status": "active",
    }
    MOCK_API_KEYS.append(new_key_obj)

    # Retourne un fragment HTML inséré par HTMX dans la liste
    return HTMLResponse(f"""
    <div id="{key_id}" class="flex items-center gap-4 px-5 py-4 border-t border-gray-800 bg-indigo-900/10">
        <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-white">{new_key_obj['name']}</p>
            <p class="text-xs font-mono text-indigo-300 mt-1 truncate">{new_key}</p>
        </div>
        <span class="text-xs bg-green-900/50 text-green-400 border border-green-800 px-2 py-0.5 rounded-full">
            active
        </span>
        <span class="text-xs text-gray-600">À l'instant</span>
    </div>
    """)

@router.post("/settings/api-keys/{key_id}/revoke")
async def revoke_api_key(key_id: str):
    """
    MOCK — Révoque une clé API.
    HTMX remplace la ligne par un message de confirmation.
    """
    key = next((k for k in MOCK_API_KEYS if k["id"] == key_id), None)
    if key:
        key["status"] = "inactive"

    return HTMLResponse(f"""
    <div id="{key_id}" class="flex items-center gap-4 px-5 py-4 border-t border-gray-800 opacity-40">
        <div class="flex-1 min-w-0">
            <p class="text-sm text-gray-500 line-through">{key['name'] if key else 'Clé'}</p>
            <p class="text-xs text-gray-600 mt-1">Clé révoquée</p>
        </div>
        <span class="text-xs bg-gray-800 text-gray-600 border border-gray-700 px-2 py-0.5 rounded-full">
            révoquée
        </span>
    </div>
    """)
