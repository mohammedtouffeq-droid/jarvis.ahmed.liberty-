"""
=============================================================================
             ⚡ J.A.R.V.I.S. LIBERTY // MASTER TACTICAL SERVER ⚡
                     Engineered for Boss Ahmed
=============================================================================
"""

import os
import sys
import json
import asyncio
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

# Add root directory to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from core.config import load_settings, save_settings
from core.speech import speech_engine
from core.telemetry import get_system_vitals
from core.controller import dispatcher
from core.memory import memory_store

app = FastAPI(title="J.A.R.V.I.S. Liberty Tactical Server")

# Mount Static Assets
STATIC_DIR = BASE_DIR / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

class CommandPayload(BaseModel):
    command: str

class SettingsPayload(BaseModel):
    voice_enabled: bool = True
    speech_rate: int = 0
    speech_volume: int = 100

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception:
                pass

manager = ConnectionManager()

@app.get("/")
async def root():
    return FileResponse(str(STATIC_DIR / "index.html"))

@app.post("/api/power/on")
async def power_on():
    speech_engine.is_armed = True
    salute = speech_engine.get_boot_salute()
    speech_engine.speak(salute, force=True)
    await manager.broadcast({"type": "log", "tag": "JARVIS", "message": salute})
    return {"status": "armed", "salute": salute}

@app.post("/api/power/off")
async def power_off():
    speech_engine.is_armed = False
    farewell = "System safe standby engaged. Auxiliary voice and loops deactivated, Boss Ahmed."
    speech_engine.speak(farewell, force=True)
    await manager.broadcast({"type": "log", "tag": "SYSTEM", "message": farewell})
    return {"status": "standby", "message": farewell}

@app.post("/api/execute")
async def execute_directive(payload: CommandPayload):
    if not speech_engine.is_armed:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": "J.A.R.V.I.S. is currently in SAFE STANDBY. Engage Master Power first."}
        )
    result = dispatcher.dispatch(payload.command)
    await manager.broadcast({
        "type": "log",
        "tag": "EXECUTED" if result.get("status") == "success" else "ALERT",
        "message": result.get("message", "")
    })
    return result

@app.get("/api/vitals")
async def get_vitals():
    return get_system_vitals()

@app.get("/api/memory")
async def get_memory():
    return {
        "goals": memory_store.get_goals(),
        "history": memory_store.get_recent_history(15)
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep-alive ping / wait for client messages
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)

def run_server():
    import uvicorn
    settings = load_settings()
    host = "0.0.0.0"
    port = settings.get("port", 7777)
    print(f"\n⚡ J.A.R.V.I.S. LIBERTY SERVER ENGAGING on http://localhost:{port}")
    uvicorn.run(app, host=host, port=port, log_level="info")

if __name__ == "__main__":
    run_server()
