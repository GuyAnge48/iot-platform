# app/main.py
# Point d'entrée principal de l'application FastAPI
# Monte les fichiers statiques, les templates Jinja2 et tous les routeurs

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.exceptions import HTTPException

from app.routers import auth, dashboard, devices, alerts
from app.ws.manager import router as ws_router

app = FastAPI(title="IoT Platform")

# Fichiers statiques (JS, CSS custom si besoin)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Moteur de templates Jinja2
templates = Jinja2Templates(directory="templates")

# Inclusion de tous les routeurs
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(devices.router)
app.include_router(alerts.router)
app.include_router(ws_router)

@app.get("/")
async def root():
    return RedirectResponse(url="/login")

# Gestionnaire d'erreur 404 — page propre au lieu d'une réponse JSON brute
@app.exception_handler(404)
async def not_found(request: Request, exc: HTTPException):
    return templates.TemplateResponse(request, "errors/404.html", status_code=404)