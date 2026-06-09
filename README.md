# NewZork — Web Build (M3.5)

A browser-based terminal UI for NewZork, served by a small FastAPI
WebSocket backend. State lives in a server-side dict keyed by session,
with a localStorage mirror on the client for refresh-survival and a
downloadable save file for cross-device persistence.

## Quick start

```bash
cd ~/Source/newzork
pip install fastapi 'uvicorn[standard]'
python3 server.py
# Open http://localhost:8000/
```

The terminal UI is a single HTML file (`static/index.html`) with no
external dependencies. The game engine (`engine.py`) is the same logic
the CLI uses, just refactored to be I/O-free.

## How state works

```
┌──────────────┐   WebSocket    ┌──────────────┐
│   Browser    │ ─────────────► │  FastAPI     │
│              │ ◄───────────── │  server.py   │
│ localStorage │                │              │
│  (mirror)    │                │ SESSIONS =   │
│              │                │ {sid: state} │
└──────────────┘                └──────────────┘
```

- **On every command**, the server runs `engine.process_command(state, text)`,
  mutates `state`, and returns `{text, state, prompt}` to the client.
- **On every response**, the client writes `state` to `localStorage`.
- **On page load**, the server sends an `init` message with a fresh game
  state. The client compares its localStorage state's `turns` to the
  server's and prompts to load the saved game if it has more progress.
- **Save button** asks the server for current state and triggers a
  `.json` file download.
- **Load button** opens a file picker, parses the JSON, and sends it to
  the server via `{type: "load", state: {...}}`.
- **Reset button** clears localStorage and tells the server to start a
  fresh game for this session.

## Files

| File | Purpose |
|------|---------|
| `engine.py` | I/O-free game logic. State is a plain dict. |
| `server.py` | FastAPI app: HTTP `/` + `/health`, WebSocket `/ws` |
| `static/index.html` | Terminal UI: ANSI rendering, command history, save/load |
| `regression_web.py` | Engine smoke test (26 assertions) |
| `test_ws.py` | End-to-end WebSocket test (7 protocol checks) |

## Tests

```bash
python3 regression_web.py   # engine correctness
python3 test_ws.py          # WebSocket protocol (server must be running)
python3 regression.py       # original CLI regression suite (still green)
```

## What's next

- **M4: The Tunnels Below** — extend the engine to add rail tunnel
  rooms, unlock the subway grate, and add the first M4+ puzzle.
- **Login / multi-device saves** — add optional auth when (and only
  when) someone asks. Not building until then.
- **Deployment** — the app runs on any VPS with Python 3.10+ and
  ~512MB RAM. A `Dockerfile` + `fly.toml` would get it on the public
  internet in 30 minutes.
