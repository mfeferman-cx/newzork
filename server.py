#!/usr/bin/env python3
"""
NewZork web server — FastAPI + WebSocket.

Each browser tab is a session. State lives in a server-side dict keyed by
a session_id cookie. The client mirrors state to localStorage on every
command for refresh-survival. The server doesn't persist; the client is
the source of truth for "I want to come back later" via a save-file
download/upload.

Run with:  python3 server.py
Then open: http://localhost:8000/
"""

import os
import json
import uuid
from typing import Dict

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Cookie
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import engine


HERE = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(HERE, "static")

app = FastAPI(title="NewZork")
app.mount("/static", StaticFiles(directory=STATIC), name="static")


# In-memory session store. Maps session_id -> engine state dict.
SESSIONS: Dict[str, dict] = {}


def _new_session_id() -> str:
    return uuid.uuid4().hex[:16]


def _get_or_create_session(sid):
    if sid and sid in SESSIONS:
        return sid, SESSIONS[sid]
    new_sid = _new_session_id()
    SESSIONS[new_sid] = engine.new_game()
    return new_sid, SESSIONS[new_sid]


@app.get("/")
async def index():
    return FileResponse(os.path.join(STATIC, "index.html"))


@app.get("/health")
async def health():
    return {"status": "ok", "sessions": len(SESSIONS)}


# WebSocket protocol
# Server -> Client:
#   {"type": "init",      "session_id": "...", "state": {...}, "crawl": "...", "prompt": "..."}
#   {"type": "output",    "text": "...", "state": {...}", "prompt": "..."}
#   {"type": "save_data", "state": {...}}
#   {"type": "error",     "message": "..."}
# Client -> Server:
#   {"type": "command",      "text": "go north"}
#   {"type": "reset"}
#   {"type": "load",         "state": {...}}
#   {"type": "save_request"}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket, session_id: str | None = Cookie(default=None)):
    await ws.accept()
    sid, state = _get_or_create_session(session_id)

    out = []
    engine._describe_room(state, state["current_room"], out)
    initial = engine.opening_crawl() + "\n" + "\n".join(out)
    await ws.send_json({
        "type": "init",
        "session_id": sid,
        "state": state,
        "crawl": initial,
        "prompt": engine.prompt_for(state),
    })

    try:
        while True:
            msg = await ws.receive_json()
            kind = msg.get("type")

            if kind == "command":
                text = msg.get("text", "").strip()
                if not text:
                    continue
                output = engine.process_command(state, text)
                await ws.send_json({
                    "type": "output",
                    "text": output,
                    "state": state,
                    "prompt": engine.prompt_for(state),
                })
            elif kind == "reset":
                SESSIONS[sid] = engine.new_game()
                state = SESSIONS[sid]
                out = []
                engine._describe_room(state, state["current_room"], out)
                initial = engine.opening_crawl() + "\n" + "\n".join(out)
                await ws.send_json({
                    "type": "init",
                    "session_id": sid,
                    "state": state,
                    "crawl": initial,
                    "prompt": engine.prompt_for(state),
                })
            elif kind == "load":
                try:
                    new_state = msg.get("state", {})
                    assert "current_room" in new_state
                    assert "inventory" in new_state
                    SESSIONS[sid] = new_state
                    state = SESSIONS[sid]
                    await ws.send_json({
                        "type": "output",
                        "text": "[Save loaded.]",
                        "state": state,
                        "prompt": engine.prompt_for(state),
                    })
                except Exception as e:
                    await ws.send_json({"type": "error", "message": f"Invalid save: {e}"})
            elif kind == "save_request":
                await ws.send_json({"type": "save_data", "state": state})
            elif kind == "ping":
                await ws.send_json({"type": "pong"})
            else:
                await ws.send_json({"type": "error", "message": f"Unknown message type: {kind}"})
    except WebSocketDisconnect:
        pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
