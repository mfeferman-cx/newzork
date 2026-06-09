# Watchdog Report: newzork-m2-restore-the-lights

**Status:** failed
**Wait time:** 10 minutes (2026-06-08T23:05:40 → 2026-06-08T23:15:45 CDT)
**Attempts:** 1 (this watchdog run). The previous M2 watchdog also marked this run FAILED; the latest commit `e256e56` is the prior watchdog's own failure report being committed as a doc.

## Validation results

- `world_data.py`: **exists** (modified, new items/features/rooms added) — 95 net additions vs M1
- `newzork.py`: **exists** (modified, new verbs added) — 106 net additions vs M1
- Branch commits: **5 commits** beyond `feat/m1-the-concourse`
  - `cb5c791` feat(m2): create feat/m2-restore-the-lights branch from feat/m1-the-concourse
  - `d3545d8` feat(m2): add panel_key and fuel_cell items
  - `d94f5f6` feat(m2): add read verb and feature examination
  - `1ec5af7` fix(m2): add broken_panel to lower_platform features
  - `e256e56` docs(infra): watchdog M2 report - FAILED, puzzle logic broken  ← prior watchdog's failure report, committed as a doc
  - Minimum required by spec: 4 incremental commits ✅
- Entry point: **starts cleanly** — opening crawl renders, room description + items + exits all print, `>` prompt works
- Test path: **0/9 spec steps passed** when using the spec's exact `panel_key` form; **partial** when using the human-friendly `panel key` form

## Critical failures (reproduced by this watchdog, not just inherited from the prior report)

I re-ran the spec's test path end-to-end by piping commands into `python3 newzork.py`. The following defects are confirmed against the current `HEAD` (`e256e56`):

### Bug 1 — Item id lookup is missing from the parser
**Reproduction:**
```
take flashlight    → Taken.
go down            → [Lower Platform]
take panel_key     → "You don't see that here."   ❌
```
**Root cause:** `take_command` (and `look_command`, `read_command`, `use_command`) match `item_name` against `item['name']` and `item.get('synonyms', [])`, but **not against `item['id']`**. `panel_key` is the id, the name is `panel key`. The spec uses the id form (`take panel_key`, `use panel_key on panel`); the engine rejects it. The human-friendly form (`take panel key`) does work, but the spec and the prior watchdog report both use the id form, and a robust parser should accept both.

**Workaround that does work:** `take panel key` → Taken. Then `use panel key on panel` → "The fusebox panel swings open, revealing ancient wiring." ✅

**Fix:** in each lookup loop, also test `item_name == item['id']` (and for features, `feature['id']`).

### Bug 2 — Conditional exits are additive-only; lights-on gating is broken
**Reproduction:**
```
take flashlight
go down            → [Lower Platform]
                    Exits: up, north, east      ← north and east should be hidden
go north           → [Toolshed]                 ❌ lights are OFF
```
**Root cause:** in `world_data.py`, `lower_platform.exits` is statically defined as `{"up": "main_concourse", "north": "toolshed", "east": "old_office"}`. The `describe_room` function in `newzork.py` *adds* the `north`/`east` exits when `lights_on` is true, but never *removes* them when lights are off. The result: toolshed and old_office are reachable on turn 1, before any puzzle work is done. This is exactly what the spec says must be blocked.

**Fix options:**
- Remove `north`/`east` from the static `lower_platform.exits` dict, and have the engine add them when `lights_on`. Then `describe_room` and `go_command` both need to read from the conditional view, not the raw dict.
- Or: keep them in the data but have `go_command` check `lights_on` and refuse the move with a message like "It's too dark to go that way." — the same gating pattern that already exists for `lower_platform` itself (the dark-stairs check).

### Bug 3 — Score denominator is hard-coded to `/3` but only 1 puzzle exists
**Reproduction:**
```
score              → "Puzzles solved: 0/3 | Score: 0"   ❌
```
**Root cause:** `score_command` has `puzzles_solved = 1 if game_state.lights_on else 0` and prints `/3`. There is no second or third puzzle. The spec only requires one puzzle (`+10` on lights restore). Either the count is wrong, or the denominator is. For M2 the right answer is `1/1` and `Score: 10` after the generator is used.

**Fix:** hard-code denominator to 1 for M2, or compute it from a `puzzles` dict in `world_data`.

### Bug 4 — `go south` shortcut is not handled from toolshed/old_office back
Not directly fatal, but the test path is brittle: from `toolshed` the only exit is `south → lower_platform`, so `go back` (used in interactive testing) returns "You can't go that way." Minor.

### Spec internal inconsistencies (informational, not the agent's fault)
The spec's test path says "go north (control_room) → take fuel_cell", but `fuel_cell` is placed in `exhibits_hall.items`, not `control_room.items`. Either the test path is wrong, or `world_data.py` should move `fuel_cell` to `control_room`. The spec also omits the `use maintenance_key on door` step that M1 required; for M2 the spec seems to assume the door is already unlocked, which it is not on a fresh start.

**Suggestion:** move `fuel_cell` from `exhibits_hall` to `control_room` so the spec path lines up, and add the door-unlock step explicitly to the spec.

## Final state

- Branch: `feat/m2-restore-the-lights`
- Last commit: `e256e56` — docs(infra): watchdog M2 report - FAILED, puzzle logic broken
- Files modified vs M1: `world_data.py`, `newzork.py`
- New items: `panel_key`, `fuel_cell` ✅
- New features: `broken_panel`, `generator` ✅
- New rooms: `toolshed`, `old_office` ✅
- New verbs: `read` ✅, `look <feature>` ✅, `score` ✅
- Score logic: +10 on lights restore (would work if puzzle path worked) ✅
- Known issues: **2 critical parser/gating defects, 1 cosmetic score denominator, 1 spec inconsistency**

## Recommendation

**needs-retry.** The world data, new verbs, score scaffolding, and conditional-exit *intent* are all in place. The build is on the right branch with enough commits. Two real defects block the puzzle from being playable end-to-end:

1. Parser does not match item/feature ids.
2. `lower_platform` exits are not gated by `lights_on`.

A targeted fix on the existing branch (no schema redesign) should resolve both. The spec itself should also be updated to either (a) move `fuel_cell` to `control_room`, or (b) revise the test path to take it in `exhibits_hall`. Either fix is one-line.

## Next action

This watchdog cannot re-spawn the primary agent (no `sessions_spawn` tool is exposed in this subagent context). The parent agent (Cato / main session) should re-spawn the primary with the following instruction, then run this watchdog again:

> **Retry from watchdog** — your previous M2 build is on `feat/m2-restore-the-lights` with 4+ commits but the puzzle is not playable. Two specific defects to fix:
>
> 1. In `newzork.py`, every parser loop that currently does `if item_name in [item['name']] + item.get('synonyms', [])` must ALSO accept the item's `id`. The spec uses `panel_key` (the id), not `panel key` (the name). Add a check like `or item_name == item['id']` to the same condition in `take_command`, `look_command`, `read_command`, and `use_command`. Mirror the same fix for `features` (the spec may also need to address features by id).
>
> 2. `lower_platform.exits` in `world_data.py` currently lists `north → toolshed` and `east → old_office` unconditionally. These exits must NOT be available when `lights_on` is false. Fix by either (a) removing them from the static data and adding them in `describe_room`/`go_command` only when `lights_on`, or (b) adding a `lights_on` guard in `go_command` that refuses the move with a "too dark" message — the same pattern that already gates entry into `lower_platform` itself.
>
> 3. Also fix the `score` command: it currently hard-codes `/3` but only 1 puzzle exists. Either change to `1/1` or compute the denominator from a `world_data.puzzles` list.
>
> 4. Bonus: move `fuel_cell` from `exhibits_hall.items` to `control_room.items` so the spec's test path ("go north (control_room) → take fuel_cell") actually works.
>
> Do NOT add unrelated changes. Do NOT rewrite the engine. Make the smallest set of edits that makes the spec's 9-step test path pass. Then capture the actual output of `printf '<all 9 commands>\n' | python3 newzork.py` and paste it into your final report. Then re-run the watchdog.

**Do NOT merge the current `feat/m2-restore-the-lights` branch.** A re-spawn with the four-point fix above should resolve it in one cycle.
