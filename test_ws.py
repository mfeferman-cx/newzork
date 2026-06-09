#!/usr/bin/env python3
"""
test_ws.py — End-to-end WebSocket test for the NewZork web server.

Connects, runs a few commands, verifies the server returns expected state.
"""

import asyncio
import json
import websockets


async def main():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as ws:
        # 1. Receive init
        init = json.loads(await ws.recv())
        assert init["type"] == "init", f"expected init, got {init}"
        assert init["state"]["current_room"] == "main_concourse"
        assert init["state"]["warmth"] == 100
        print(f"PASS init: session_id={init['session_id'][:8]}..., room={init['state']['current_room']}")
        print(f"     prompt: {init['prompt'].strip()}")

        # 2. Send a command
        await ws.send(json.dumps({"type": "command", "text": "take flashlight"}))
        out = json.loads(await ws.recv())
        assert out["type"] == "output"
        assert "flashlight" in out["state"]["inventory"]
        print(f"PASS 'take flashlight': {out['text'].strip()[:60]}")

        # 3. Move
        await ws.send(json.dumps({"type": "command", "text": "go east"}))
        out = json.loads(await ws.recv())
        assert out["state"]["current_room"] == "exhibits_hall"
        print(f"PASS 'go east': now in {out['state']['current_room']}")

        # 4. Save request
        await ws.send(json.dumps({"type": "save_request"}))
        save = json.loads(await ws.recv())
        assert save["type"] == "save_data"
        assert "flashlight" in save["state"]["inventory"]
        print(f"PASS save_data: {len(save['state']['inventory'])} items, score={save['state']['score']}")

        # 5. Load
        await ws.send(json.dumps({
            "type": "load",
            "state": {**save["state"], "current_room": "lower_platform", "warmth": 50}
        }))
        out = json.loads(await ws.recv())
        assert out["state"]["current_room"] == "lower_platform"
        assert out["state"]["warmth"] == 50
        print(f"PASS load: room={out['state']['current_room']}, warmth={out['state']['warmth']}")

        # 6. Reset
        await ws.send(json.dumps({"type": "reset"}))
        init = json.loads(await ws.recv())
        assert init["type"] == "init"
        assert init["state"]["current_room"] == "main_concourse"
        assert init["state"]["inventory"] == []
        print(f"PASS reset: back to fresh game")

        # 7. Quit
        await ws.send(json.dumps({"type": "command", "text": "quit"}))
        out = json.loads(await ws.recv())
        assert "darkness" in out["text"].lower()
        print(f"PASS 'quit': {out['text']}")

        print("\n--- ALL WS TESTS PASS ---")


if __name__ == "__main__":
    asyncio.run(main())
