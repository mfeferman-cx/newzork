# newzork-build — Primary Task (Retry #1 from watchdog)

## Context
Watchdog checked after 10 min and found no output files. Re-spawning the primary task.

## Task
Build NewZork text adventure per `~/Source/newzork/SPEC.md`.

Create two files in `~/Source/newzork/`:

1. **`newzork.py`** — Main game file. Must be >100 lines. Implements:
   - CLI with argparse (--help, --save, --load)
   - Game loop: prompt → parse → execute → display
   - ANSI color output
   - Save/load to `~/.newzork/saves/`
   - Hand-rolled tokenizer + noun/verb/preposition resolution
   - No external libraries (stdlib only)

2. **`world_data.py`** — World/map data. Must be >100 lines. Contains:
   - Room definitions (id, name, description, short_desc, exits, items, features, dark, cold)
   - Item definitions (id, name, description, takeable, edible, etc.)
   - At least 20 rooms from the spec's Manhattan Core map
   - Key items: flashlight, batteries, keys, food, weapons

## Verify
After creating both files, verify the game runs:
```bash
cd ~/Source/newzork && python3 newzork.py --help
```

Report line counts and verify success.

## Retry Note
**Retry #1 from watchdog** — previous attempt timed out with no output.

---
Started: 2026-06-07 09:24 CDT