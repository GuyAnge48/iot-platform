# app/main.py
# Point d'entrée principal de l'application FastAPI

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException

# Import de tous les routeurs
from app.routers import auth, dashboard, devices, alerts, telemetry, automations, teams, settings, projects
from app.ws.manager import router as ws_router

app = FastAPI(title="IoT Platform")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(projects.router)   # Nouveaux routeur projets
app.include_router(devices.router)
app.include_router(alerts.router)
app.include_router(telemetry.router)
app.include_router(automations.router)
app.include_router(teams.router)
app.include_router(settings.router)
app.include_router(ws_router)

@app.get("/")
async def root():
    return RedirectResponse(url="/login")

@app.exception_handler(404)
async def not_found(request: Request, exc: HTTPException):
    return templates.TemplateResponse(request, "errors/404.html", status_code=404)
