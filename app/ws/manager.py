from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio, json, random

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active.remove(ws)

    async def broadcast(self, data: dict):
        for ws in self.active:
            try:
                await ws.send_json(data)
            except Exception:
                pass

manager = ConnectionManager()

@router.websocket("/ws/telemetry")
async def telemetry_ws(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Simulation : envoi de mises à jour toutes les 2 secondes
            updates = [
                {"device_id": "device-001", "component_id": "temp-1",  # device-001 — Température simulée entre 25.5 et 28.5 °C
                 "value": round(27.0 + random.uniform(-1.5, 1.5), 1), "unit": "°C"},
                {"device_id": "device-001", "component_id": "hum-1", # device-001 — Humidité simulée entre 59 et 65 %  
                 "value": round(62.0 + random.uniform(-3, 3), 1), "unit": "%"},
                {"device_id": "device-005", "component_id": "dist-1", # device-005 — Distance simulée entre 20 et 40 cm
                 "value": round(30.0 + random.uniform(-10, 10), 1), "unit": "cm"},
           # Ajout de device-002 — humidité du sol
               {"device_id": "device-002", "component_id": "soil-1",
                "value": round(72.0 + random.uniform(-4, 4), 1), "unit": "%"}
            ]
            for upd in updates:
                await manager.broadcast(upd)
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        manager.disconnect(websocket)