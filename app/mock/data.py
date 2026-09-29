# MOCK DATA — À remplacer par les appels FastAPI/PostgreSQL réels
from datetime import datetime, timedelta
import random

MOCK_PROJECTS = [
    {"id": "proj-1", "name": "Laboratoire A", "device_count": 4},
    {"id": "proj-2", "name": "Serre agricole", "device_count": 5},
    {"id": "proj-3", "name": "Station météo", "device_count": 2},
    {"id": "proj-4", "name": "Bâtiment B2", "device_count": 1},
]

MOCK_DEVICES = [
    {
        "id": "device-001",
        "name": "Station météo salon",
        "type": "sensor_hub",
        "status": "online",
        "project_id": "proj-3",
        "project_name": "Station météo",
        "last_seen": "Il y a 2 secondes",
        "components": [
            {"id": "temp-1", "name": "Température", "type": "sensor",
             "value": 27.4, "unit": "°C", "icon": "thermometer"},
            {"id": "hum-1", "name": "Humidité", "type": "sensor",
             "value": 62.1, "unit": "%", "icon": "droplets"},
            {"id": "press-1", "name": "Pression", "type": "sensor",
             "value": 1013.2, "unit": "hPa", "icon": "gauge"},
        ],
        "commands": ["reboot", "calibrate", "set_interval"],
    },
    {
        "id": "device-002",
        "name": "Contrôleur serre",
        "type": "actuator_hub",
        "status": "online",
        "project_id": "proj-2",
        "project_name": "Serre agricole",
        "last_seen": "Il y a 5 secondes",
        "components": [
            {"id": "pump-1", "name": "Pompe irrigation", "type": "actuator",
             "value": "OFF", "unit": "", "icon": "zap"},
            {"id": "light-1", "name": "Éclairage", "type": "actuator",
             "value": "ON", "unit": "", "icon": "sun"},
            {"id": "soil-1", "name": "Humidité sol", "type": "sensor",
             "value": 45.3, "unit": "%", "icon": "droplets"},
        ],
        "commands": ["pump_on", "pump_off", "light_on", "light_off"],
    },
    {
        "id": "device-003",
        "name": "Capteur labo alpha",
        "type": "sensor_hub",
        "status": "warning",
        "project_id": "proj-1",
        "project_name": "Laboratoire A",
        "last_seen": "Il y a 3 minutes",
        "components": [
            {"id": "co2-1", "name": "CO₂", "type": "sensor",
             "value": 1450, "unit": "ppm", "icon": "wind"},
            {"id": "temp-2", "name": "Température", "type": "sensor",
             "value": 31.8, "unit": "°C", "icon": "thermometer"},
        ],
        "commands": ["reboot", "reset_sensor"],
    },
    {
        "id": "device-004",
        "name": "Portail bâtiment B2",
        "type": "access_control",
        "status": "offline",
        "project_id": "proj-4",
        "project_name": "Bâtiment B2",
        "last_seen": "Il y a 2 heures",
        "components": [
            {"id": "lock-1", "name": "Verrou", "type": "actuator",
             "value": "LOCKED", "unit": "", "icon": "lock"},
        ],
        "commands": ["unlock", "lock", "reboot"],
    },
    {
        "id": "device-005",
        "name": "Robot laboratoire",
        "type": "robot",
        "status": "online",
        "project_id": "proj-1",
        "project_name": "Laboratoire A",
        "last_seen": "Il y a 1 seconde",
        "components": [
            {"id": "motor-1", "name": "Moteur gauche", "type": "actuator",
             "value": "IDLE", "unit": "", "icon": "cpu"},
            {"id": "motor-2", "name": "Moteur droit", "type": "actuator",
             "value": "IDLE", "unit": "", "icon": "cpu"},
            {"id": "dist-1", "name": "Distance", "type": "sensor",
             "value": 34.2, "unit": "cm", "icon": "ruler"},
        ],
        "commands": ["move_forward", "move_backward", "stop", "reboot"],
    },
]

MOCK_ALERTS = [
    {
        "id": "alert-1",
        "device_id": "device-003",
        "device_name": "Capteur labo alpha",
        "severity": "warning",
        "message": "CO₂ au-dessus du seuil (1450 ppm > 1000 ppm)",
        "timestamp": "Il y a 3 minutes",
        "acknowledged": False,
    },
    {
        "id": "alert-2",
        "device_id": "device-004",
        "device_name": "Portail bâtiment B2",
        "severity": "error",
        "message": "Appareil hors ligne depuis plus de 30 minutes",
        "timestamp": "Il y a 2 heures",
        "acknowledged": False,
    },
    {
        "id": "alert-3",
        "device_id": "device-001",
        "device_name": "Station météo salon",
        "severity": "info",
        "message": "Calibration effectuée avec succès",
        "timestamp": "Il y a 1 heure",
        "acknowledged": True,
    },
]

def get_telemetry_mock(device_id: str, component_id: str, points: int = 20):
    """Génère des données historiques de télémétrie simulées."""
    base_values = {
        "temp-1": (25.0, 2.0),
        "hum-1": (60.0, 5.0),
        "press-1": (1013.0, 3.0),
        "co2-1": (800.0, 200.0),
        "temp-2": (30.0, 2.0),
        "soil-1": (45.0, 5.0),
        "dist-1": (30.0, 10.0),
    }
    base, spread = base_values.get(component_id, (50.0, 10.0))
    now = datetime.now()
    return [
        {
            "timestamp": (now - timedelta(minutes=(points - i) * 5)).strftime("%H:%M"),
            "value": round(base + random.uniform(-spread, spread), 1),
        }
        for i in range(points)
    ]

def get_stats():
    total = len(MOCK_DEVICES)
    online = sum(1 for d in MOCK_DEVICES if d["status"] == "online")
    alerts = sum(1 for a in MOCK_ALERTS if not a["acknowledged"])
    return {
        "total_devices": total,
        "online_devices": online,
        "offline_devices": total - online,
        "active_alerts": alerts,
        "total_projects": len(MOCK_PROJECTS),
    }
# MOCK — Règles d'automatisation
# Une règle = condition sur un composant → action déclenchée
MOCK_AUTOMATIONS = [
    {
        "id": "auto-001",
        "name": "Alerte température élevée",
        "description": "Déclenche une alerte si la température dépasse 30°C",
        "status": "active",
        "device_id": "device-001",
        "device_name": "Station météo salon",
        "trigger": {
            "component_id": "temp-1",
            "component_name": "Température",
            "operator": ">",       # Opérateur de comparaison
            "value": 30.0,
            "unit": "°C"
        },
        "action": {
            "type": "alert",       # Type d'action : alert, command, notification
            "message": "Température trop élevée — vérifier la ventilation"
        },
        "last_triggered": "Il y a 2 heures",
        "trigger_count": 3,        # Nombre de fois déclenchée
    },
    {
        "id": "auto-002",
        "name": "Pompe irrigation automatique",
        "description": "Active la pompe si l'humidité du sol descend sous 40%",
        "status": "active",
        "device_id": "device-002",
        "device_name": "Contrôleur serre",
        "trigger": {
            "component_id": "soil-1",
            "component_name": "Humidité sol",
            "operator": "<",
            "value": 40.0,
            "unit": "%"
        },
        "action": {
            "type": "command",
            "command": "pump_on",
            "message": "Activation automatique de la pompe d'irrigation"
        },
        "last_triggered": "Il y a 30 minutes",
        "trigger_count": 12,
    },
    {
        "id": "auto-003",
        "name": "Alerte CO₂ laboratoire",
        "description": "Alerte critique si CO₂ dépasse 1200 ppm",
        "status": "active",
        "device_id": "device-003",
        "device_name": "Capteur labo alpha",
        "trigger": {
            "component_id": "co2-1",
            "component_name": "CO₂",
            "operator": ">",
            "value": 1200.0,
            "unit": "ppm"
        },
        "action": {
            "type": "alert",
            "message": "Niveau CO₂ critique — évacuation recommandée"
        },
        "last_triggered": "Il y a 3 minutes",
        "trigger_count": 1,
    },
    {
        "id": "auto-004",
        "name": "Notification appareil hors ligne",
        "description": "Notifie si un appareil ne répond plus depuis 30 minutes",
        "status": "inactive",
        "device_id": "device-004",
        "device_name": "Portail bâtiment B2",
        "trigger": {
            "component_id": None,
            "component_name": "Connexion",
            "operator": "==",
            "value": "offline",
            "unit": ""
        },
        "action": {
            "type": "notification",
            "message": "Appareil hors ligne depuis plus de 30 minutes"
        },
        "last_triggered": "Il y a 2 heures",
        "trigger_count": 5,
    },
]

# MOCK — Équipes et utilisateurs
MOCK_TEAMS = [
    {
        "id": "team-001",
        "name": "Équipe Laboratoire",
        "description": "Gestion des capteurs du laboratoire A",
        "member_count": 3,
        "project_ids": ["proj-1"],
        "created_at": "Il y a 2 mois",
    },
    {
        "id": "team-002",
        "name": "Équipe Agricole",
        "description": "Supervision de la serre et des capteurs de terrain",
        "member_count": 4,
        "project_ids": ["proj-2", "proj-3"],
        "created_at": "Il y a 1 mois",
    },
    {
        "id": "team-003",
        "name": "Équipe Sécurité",
        "description": "Contrôle d'accès et surveillance bâtiments",
        "member_count": 2,
        "project_ids": ["proj-4"],
        "created_at": "Il y a 3 semaines",
    },
]

MOCK_USERS = [
    {
        "id": "user-001",
        "name": "Guy Ange Cédric",
        "email": "guyange@iot-platform.com",
        "role": "admin",
        "team_id": "team-001",
        "team_name": "Équipe Laboratoire",
        "status": "active",
        "last_seen": "En ligne",
        "avatar": "GA",
    },
    {
        "id": "user-002",
        "name": "Kouamé Jean",
        "email": "jean@iot-platform.com",
        "role": "operator",
        "team_id": "team-001",
        "team_name": "Équipe Laboratoire",
        "status": "active",
        "last_seen": "Il y a 5 minutes",
        "avatar": "KJ",
    },
    {
        "id": "user-003",
        "name": "Aya Diallo",
        "email": "aya@iot-platform.com",
        "role": "operator",
        "team_id": "team-002",
        "team_name": "Équipe Agricole",
        "status": "active",
        "last_seen": "Il y a 1 heure",
        "avatar": "AD",
    },
    {
        "id": "user-004",
        "name": "Ibrahim Koné",
        "email": "ibrahim@iot-platform.com",
        "role": "viewer",
        "team_id": "team-002",
        "team_name": "Équipe Agricole",
        "status": "inactive",
        "last_seen": "Il y a 2 jours",
        "avatar": "IK",
    },
    {
        "id": "user-005",
        "name": "Fatou Traoré",
        "email": "fatou@iot-platform.com",
        "role": "operator",
        "team_id": "team-003",
        "team_name": "Équipe Sécurité",
        "status": "active",
        "last_seen": "Il y a 30 minutes",
        "avatar": "FT",
    },
    {
        "id": "user-006",
        "name": "Sékou Bamba",
        "email": "sekou@iot-platform.com",
        "role": "viewer",
        "team_id": "team-003",
        "team_name": "Équipe Sécurité",
        "status": "active",
        "last_seen": "Il y a 3 heures",
        "avatar": "SB",
    },
]

# MOCK — Configuration de la plateforme et clés API
MOCK_SETTINGS = {
    # Profil de l'utilisateur connecté
    "profile": {
        "name": "Guy Ange Cédric",
        "email": "guyange@iot-platform.com",
        "role": "admin",
        "avatar": "GA",
        "joined": "Il y a 2 mois",
    },
    # Configuration générale de la plateforme
    "platform": {
        "name": "IoT Platform",
        "timezone": "Africa/Abidjan",
        "language": "Français",
        "version": "1.0.0",
        "websocket_interval": 2,   # Intervalle envoi données WebSocket (secondes)
        "max_devices": 100,        # Limite d'appareils par projet
    },
    # Notifications
    "notifications": {
        "email_alerts": True,
        "push_alerts": True,
        "alert_threshold": "warning",  # Niveau minimum : info / warning / error
    },
}

# MOCK — Clés API générées
MOCK_API_KEYS = [
    {
        "id": "key-001",
        "name": "Robot laboratoire",
        "key": "iot_live_xK9mP2qR7nL4vT8wA1jC6hD",
        "permissions": ["read", "write"],
        "created_at": "Il y a 1 mois",
        "last_used": "Il y a 2 minutes",
        "status": "active",
    },
    {
        "id": "key-002",
        "name": "Serre agricole",
        "key": "iot_live_bN3sY6uE9fX2mQ5pW8kI1oJ",
        "permissions": ["read"],
        "created_at": "Il y a 3 semaines",
        "last_used": "Il y a 1 heure",
        "status": "active",
    },
    {
        "id": "key-003",
        "name": "Test intégration",
        "key": "iot_test_cV7tZ4aG0hB5nR2sL9dF3eM",
        "permissions": ["read", "write", "admin"],
        "created_at": "Il y a 1 semaine",
        "last_used": "Jamais",
        "status": "inactive",
    },
]

# ================================================================
# MOCK — Projets utilisateur avec composants associés
# ================================================================
# Nouvelle logique demandée par le mentor :
# Utilisateur → Ses projets → Composants du projet
#
# Structure :
#   user_id    : identifiant de l'utilisateur propriétaire
#   components : liste des composants associés directement au projet
#
# IMPORTANT : ces données sont indépendantes de MOCK_DEVICES
# Un projet peut exister sans device physique connecté
# Les composants ici sont logiques (ce que l'utilisateur a configuré)
# ================================================================

MOCK_USER_PROJECTS = [
    {
        "id": "uproject-001",
        "user_id": "user-001",          # Propriétaire : Guy Ange
        "name": "Robot Agricole",
        "description": "Système automatisé de surveillance agricole",
        "created_at": "Il y a 1 mois",
        "status": "active",
        # Composants associés à CE projet
        "components": [
            {
                "id": "comp-001",
                "project_id": "uproject-001",
                "name": "Capteur température",
                "type": "sensor",
                "description": "Mesure la température ambiante du robot",
                "status": "active",
                "unit": "°C",
                "created_at": "Il y a 1 mois",
            },
            {
                "id": "comp-002",
                "project_id": "uproject-001",
                "name": "Capteur humidité",
                "type": "sensor",
                "description": "Mesure l'humidité du sol",
                "status": "active",
                "unit": "%",
                "created_at": "Il y a 1 mois",
            },
            {
                "id": "comp-003",
                "project_id": "uproject-001",
                "name": "GPS",
                "type": "sensor",
                "description": "Localisation du robot dans le champ",
                "status": "active",
                "unit": "coords",
                "created_at": "Il y a 3 semaines",
            },
            {
                "id": "comp-004",
                "project_id": "uproject-001",
                "name": "Moteur principal",
                "type": "actuator",
                "description": "Contrôle le déplacement du robot",
                "status": "active",
                "unit": "",
                "created_at": "Il y a 3 semaines",
            },
            {
                "id": "comp-005",
                "project_id": "uproject-001",
                "name": "Batterie",
                "type": "sensor",
                "description": "Niveau de charge de la batterie",
                "status": "active",
                "unit": "%",
                "created_at": "Il y a 2 semaines",
            },
        ],
    },
    {
        "id": "uproject-002",
        "user_id": "user-001",          # Propriétaire : Guy Ange
        "name": "Maison Intelligente",
        "description": "Système domotique de supervision du domicile",
        "created_at": "Il y a 3 semaines",
        "status": "active",
        "components": [
            {
                "id": "comp-006",
                "project_id": "uproject-002",
                "name": "Température salon",
                "type": "sensor",
                "description": "Capteur de température du salon",
                "status": "active",
                "unit": "°C",
                "created_at": "Il y a 3 semaines",
            },
            {
                "id": "comp-007",
                "project_id": "uproject-002",
                "name": "Lumière entrée",
                "type": "actuator",
                "description": "Contrôle l'éclairage de l'entrée",
                "status": "active",
                "unit": "",
                "created_at": "Il y a 2 semaines",
            },
            {
                "id": "comp-008",
                "project_id": "uproject-002",
                "name": "Détecteur mouvement",
                "type": "sensor",
                "description": "Détecte les mouvements dans le couloir",
                "status": "active",
                "unit": "",
                "created_at": "Il y a 1 semaine",
            },
        ],
    },
    {
        "id": "uproject-003",
        "user_id": "user-001",          # Propriétaire : Guy Ange
        "name": "Station Météo",
        "description": "Réseau de capteurs météorologiques",
        "created_at": "Il y a 1 semaine",
        "status": "active",
        "components": [],               # Projet vide — aucun composant encore
    },
]
