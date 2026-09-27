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
                {"device_id": "device-001", "component_id": "temp-1",
                 "value": round(27.0 + random.uniform(-1.5, 1.5), 1), "unit": "°C"},
                {"device_id": "device-001", "component_id": "hum-1",
                 "value": round(62.0 + random.uniform(-3, 3), 1), "unit": "%"},
                {"device_id": "device-005", "component_id": "dist-1",
                 "value": round(30.0 + random.uniform(-10, 10), 1), "unit": "cm"},
            ]
            for upd in updates:
                await manager.broadcast(upd)
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        manager.disconnect(websocket)