# app/main.py
# Point d'entrée principal de l'application FastAPI

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException

# Import de tous les routeurs
from app.routers import auth, dashboard, devices, alerts, telemetry, automations, teams
from app.ws.manager import router as ws_router

app = FastAPI(title="IoT Platform")

# Fichiers statiques
app.mount("/static", StaticFiles(directory="static"), name="static")

# Moteur de templates Jinja2
templates = Jinja2Templates(directory="templates")

# Inclusion de tous les routeurs
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(devices.router)
app.include_router(alerts.router)
app.include_router(telemetry.router)
app.include_router(automations.router)
app.include_router(teams.router)
app.include_router(ws_router)

# Route placeholder — paramètres (page à développer)
@app.get("/settings")
async def settings(request: Request):
    return templates.TemplateResponse(request, "app/coming_soon.html", {
        "active_page": "settings",
        "page_name": "Paramètres"
    })

@app.get("/")
async def root():
    return RedirectResponse(url="/login")

# Gestionnaire d'erreur 404
@app.exception_handler(404)
async def not_found(request: Request, exc: HTTPException):
    return templates.TemplateResponse(request, "errors/404.html", status_code=404)
