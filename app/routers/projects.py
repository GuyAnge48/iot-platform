# app/routers/projects.py
# ================================================================
# Routeur Projets — logique User → Project → Component
# ================================================================
# Routes :
#   GET  /projects                          → liste des projets de l'utilisateur
#   GET  /projects/{project_id}             → détail d'un projet + ses composants
#   POST /projects                          → créer un nouveau projet
#   POST /projects/{project_id}/components  → ajouter un composant à un projet
# ================================================================

from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app.mock.data import MOCK_USER_PROJECTS
import uuid
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# MOCK — Utilisateur connecté simulé
# En production, cet ID viendrait de la session/JWT
CURRENT_USER_ID = "user-001"
CURRENT_USER_NAME = "Guy Ange"

def get_user_projects(user_id: str):
    """
    Retourne uniquement les projets appartenant à l'utilisateur.
    IMPORTANT : filtre par user_id pour isoler les données entre utilisateurs.
    En production, cet filtrage sera fait par la base de données.
    """
    return [p for p in MOCK_USER_PROJECTS if p["user_id"] == user_id]

def get_project_by_id(project_id: str, user_id: str):
    """
    Retourne un projet si et seulement s'il appartient à l'utilisateur.
    Si le projet appartient à un autre utilisateur → retourne None (accès refusé).
    """
    return next(
        (p for p in MOCK_USER_PROJECTS
         if p["id"] == project_id and p["user_id"] == user_id),
        None
    )

# ----------------------------------------------------------------
# GET /projects — Liste des projets de l'utilisateur connecté
# ----------------------------------------------------------------
@router.get("/projects")
async def projects_list(request: Request):
    """Affiche la liste des projets de l'utilisateur connecté."""

    # Récupère uniquement les projets de cet utilisateur
    user_projects = get_user_projects(CURRENT_USER_ID)

    # Calcule les stats pour l'affichage
    total_components = sum(len(p["components"]) for p in user_projects)

    return templates.TemplateResponse(request, "app/projects/list.html", {
        "projects": user_projects,
        "user_name": CURRENT_USER_NAME,
        "stats": {
            "total_projects": len(user_projects),
            "total_components": total_components,
            "active_projects": sum(1 for p in user_projects if p["status"] == "active"),
        },
        "active_page": "projects",
    })

# ----------------------------------------------------------------
# GET /projects/{project_id} — Détail d'un projet + ses composants
# ----------------------------------------------------------------
@router.get("/projects/{project_id}")
async def project_detail(request: Request, project_id: str):
    """
    Affiche le détail d'un projet et UNIQUEMENT ses composants.
    Vérifie que le projet appartient bien à l'utilisateur connecté.
    """

    # Vérification d'appartenance — un utilisateur ne peut voir que SES projets
    project = get_project_by_id(project_id, CURRENT_USER_ID)

    if not project:
        # Projet introuvable ou accès refusé
        return templates.TemplateResponse(request, "app/projects/list.html", {
            "projects": get_user_projects(CURRENT_USER_ID),
            "error": "Projet introuvable ou accès refusé.",
            "active_page": "projects",
        })

    return templates.TemplateResponse(request, "app/projects/detail.html", {
        "project": project,
        # Les composants sont déjà filtrés — ils appartiennent à ce projet uniquement
        "components": project["components"],
        "active_page": "projects",
    })

# ----------------------------------------------------------------
# POST /projects — Créer un nouveau projet
# ----------------------------------------------------------------
@router.post("/projects")
async def create_project(
    request: Request,
    name: str = Form(...),
    description: str = Form("")
):
    """
    Crée un nouveau projet pour l'utilisateur connecté.
    Le projet est automatiquement associé à CURRENT_USER_ID.
    """

    # Génère un ID unique pour le projet
    new_id = f"uproject-{uuid.uuid4().hex[:8]}"

    # Crée le projet avec les données du formulaire
    new_project = {
        "id": new_id,
        "user_id": CURRENT_USER_ID,     # Association automatique à l'utilisateur
        "name": name,
        "description": description,
        "created_at": "À l'instant",
        "status": "active",
        "components": [],               # Projet vide au départ
    }

    # Ajoute le projet au mock (en production : INSERT en base de données)
    MOCK_USER_PROJECTS.append(new_project)

    # Redirige vers le détail du projet nouvellement créé
    return RedirectResponse(url=f"/projects/{new_id}", status_code=303)

# ----------------------------------------------------------------
# POST /projects/{project_id}/components — Ajouter un composant
# ----------------------------------------------------------------
@router.post("/projects/{project_id}/components")
async def add_component(
    request: Request,
    project_id: str,
    name: str = Form(...),
    type: str = Form(...),
    description: str = Form(""),
    unit: str = Form("")
):
    """
    Ajoute un composant à un projet.
    Vérifie que le projet appartient à l'utilisateur connecté.
    Le composant est automatiquement associé au projet.
    """

    # Vérification d'appartenance
    project = get_project_by_id(project_id, CURRENT_USER_ID)

    if not project:
        return HTMLResponse("Projet introuvable ou accès refusé.", status_code=403)

    # Génère un ID unique pour le composant
    comp_id = f"comp-{uuid.uuid4().hex[:8]}"

    # Crée le composant avec association automatique au projet
    new_component = {
        "id": comp_id,
        "project_id": project_id,       # Association automatique au projet
        "name": name,
        "type": type,                   # sensor ou actuator
        "description": description,
        "status": "active",
        "unit": unit,
        "created_at": "À l'instant",
    }

    # Ajoute le composant au projet (en production : INSERT en base de données)
    project["components"].append(new_component)

    # Redirige vers le détail du projet pour voir le nouveau composant
    return RedirectResponse(url=f"/projects/{project_id}", status_code=303)
