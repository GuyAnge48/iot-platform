# app/routers/auth.py
# Routeur d'authentification — login / logout
# MOCK : pas de vraie vérification des credentials pour la démo

from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/login")
async def login_page(request: Request):
    # Passage du request via keyword argument (Starlette >= 0.21)
    return templates.TemplateResponse(request, "auth/login.html")

@router.post("/login")
async def login_submit(request: Request, username: str = Form(...), password: str = Form(...)):
    # MOCK — tout identifiant non vide est accepté
    if username and password:
        return RedirectResponse(url="/dashboard", status_code=303)
    return templates.TemplateResponse(request, "auth/login.html", {"error": "Identifiants invalides"})

@router.get("/logout")
async def logout():
    return RedirectResponse(url="/login", status_code=303)