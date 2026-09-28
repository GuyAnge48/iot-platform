# app/routers/teams.py
# Page équipes — gestion des utilisateurs et leurs rôles
# Affiche les équipes, les membres et leurs permissions

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.mock.data import MOCK_TEAMS, MOCK_USERS

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/teams")
async def teams_page(request: Request):
    """Page principale des équipes — liste équipes + membres."""

    # Statistiques globales
    stats = {
        "total_teams": len(MOCK_TEAMS),
        "total_users": len(MOCK_USERS),
        "active_users": sum(1 for u in MOCK_USERS if u["status"] == "active"),
        "admins": sum(1 for u in MOCK_USERS if u["role"] == "admin"),
    }

    return templates.TemplateResponse(request, "app/teams/index.html", {
        "teams": MOCK_TEAMS,
        "users": MOCK_USERS,
        "stats": stats,
        "active_page": "teams",
    })
