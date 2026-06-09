# NewZork M3 — "Street Level" Spec

**Status:** DRAFT (pending M2 sign-off)
**Predecessor:** M2 ("Restore the Lights") — player has powered the museum
**Successor:** M4+ (above-ground expansion)

## 1. Concept

M2 ends with the player in the toolshed, having just restored power to the museum. M3 is the moment they step **outside** for the first time. The surface is just as frozen and dead as the underground, but it's *open* — the player sees the ruined skyline for the first time. The emotional beat: relief at escaping the museum, dread at what they find outside.

**Tone shift:** M1-M2 was claustrophobic. M3 opens up. Long sight lines. Cold wind. Silence of an empty city.

## 2. Win-Condition-Free Milestone

M3 is a **chapter transition**, not a finale. No new win condition — that's M6. M3 ends with the player at the edge of a subway grate, looking down into the dark rail tunnels. The next milestone (M4) starts there.

**M3 ends on a hook:** the tunnels below + the city above, both beckoning. Player chooses direction.

## 3. New Rooms (5 surface, 1 tunnel entrance)

```
                    [Rooftop View] (feature, not a room — `look up`)
                            |
[Schermerhorn St]  ←  [Boerum Place]  →  [Atlantic Ave]
        |                                          |
[Parking Lot]  ←————————————[MUSEUM EXIT]  →  [City Hall Steps]
        |                                          |
    (dead end)                              [Barclay St]
```

**Surface rooms (5):**
- `museum_exit` — the door out. Currently a feature of the toolshed (the ladder). Becomes a real exit after the player climbs it.
- `boerum_place` — a wide intersection, abandoned cars, snow drifts. A traffic light still swings in the wind.
- `schermerhorn_st` — a side street, parked cars buried up to their windows. A bodega with a faded "OPEN" sign.
- `atlantic_ave` — a longer avenue, more drift, a stack of newspapers frozen to a bench. **Has a subway grate.**
- `parking_lot` — a small municipal lot, dead end. Contains an old taxi with keys in it (feature, not takeable in M3 — the player has no idea how to drive).

**Tunnel entrance (1):**
- `subway_grate` — a feature in `atlantic_ave`. Iron bars frozen shut, can be examined but not entered in M3. The "hook" for M4.

## 4. New Mechanics

### Cold (per-turn damage)
- Player has a `warmth` stat, starts at 100
- Every turn spent in a surface room: warmth -5
- `flashlight` does NOT help with cold (it never did — that was M1's design mistake)
- If warmth reaches 0, player takes 1 health damage per turn
- **Restoration:** going back underground (museum) restores +10 warmth per turn
- **Display:** `>` prompt shows `[W:75]` after the cursor when on the surface

### Ladder (single-use transition)
- The toolshed ladder is a feature with `use_with: {}` (cannot be interacted with, just an exit)
- Going `up` from toolshed → museum_exit
- M3 player discovers this by accident (`go up` works)

### No new verbs
- Reuse `look`, `go`, `take`, `use`, `read`, `score` from M1-M2
- No `climb` verb — `up`/`down` is enough
- Cold mechanic is automatic, no new commands

## 5. State Changes from M2

### Player state
- Add `warmth: 100` to game state
- Add `health: 100` to game state (declared in M1 spec but never used; M3 finally uses it)
- Existing M2 fields: `score`, `lights_on`, `inventory`, `current_room`, `visited_rooms` — unchanged

### World state
- No new global flags
- The `lights_on` flag from M2 stays True (player has power; doesn't go away when they leave)

### Room connections
- `toolshed.exits` adds `up: museum_exit`
- `museum_exit.exits`: `down: toolshed`, `north: boerum_place`, `east: atlantic_ave`
- `boerum_place.exits`: `south: museum_exit`, `west: schermerhorn_st`, `east: atlantic_ave`, `north: city_hall_steps`
- `schermerhorn_st.exits`: `east: boerum_place`, `south: parking_lot`
- `parking_lot.exits`: `north: schermerhorn_st` (dead end)
- `atlantic_ave.exits`: `west: boerum_place`, `north: city_hall_steps`
- `city_hall_steps.exits`: `south: boerum_place`, `west: atlantic_ave`, `east: barclay_st`
- `barclay_st.exits`: `west: city_hall_steps` (dead end, in M3)

## 6. New Items (1 takeable, 4 features)

**Takeable:**
- `winter_coat` — found on a hook in `schermerhorn_st` bodega. `takeable: True`, `wearable: True`. Description: "A faded parka with a fur-lined hood. The zipper is stuck but the buttons work." **Effect:** wearing it halves cold damage (warmth -2 instead of -5 per turn). HINT: `read label` reveals it's a women's large.

**Features (not takeable in M3):**
- `traffic_light` — in `boerum_place`. Swings in the wind, creaks. Atmosphere.
- `frozen_bench` — in `atlantic_ave`. Has the newspaper stack.
- `taxi_cab` — in `parking_lot`. Keys in the ignition. (Player can't drive yet — M4+ puzzle hook.)
- `subway_grate` — in `atlantic_ave`. Iron bars. Has a `text` field: "FROZEN SHUT. The grate is locked from below. The rail tunnels go somewhere, but you can't get in from here."

## 7. New Verbs (0)

**Decision (locked 2026-06-08): automatic wear.** No `wear` verb. When the player picks up the `winter_coat`, the engine prints "You put on the parka. It's stiff but warm." and toggles the coat-worn flag. The coat is auto-removed from inventory and added to a `worn_items` list. To take it off (e.g. to give to someone, future M4+ scenario), the player drops it normally and the engine notes "You shrug off the parka."

Rationale: the parka is a survival item, not a fashion choice. Adding a new verb to wear a coat is friction the player doesn't need. M3 is the milestone that teaches the player about cold; we don't want them to have to learn a new verb just to survive.

## 8. Test Path (must work end-to-end)

```
# At end of M2, player is in toolshed
go up                  → [Museum Exit]  — sees daylight for the first time
go north               → [Boerum Place]  — open air, cold
                       Warmth: 100 → 95
score                  → "Puzzles solved: 1/1 | Score: 10"
go west                → [Schermerhorn St]
take winter_coat       → "You put on the parka..." (no new verb, automatic)
go south               → [Parking Lot]
look taxi              → description of the cab, keys visible
go north               → [Schermerhorn St]
go east                → [Boerum Place]
go east                → [Atlantic Ave]
look grate             → "FROZEN SHUT..." text
go north               → [City Hall Steps]
look up                → "You can see the Manhattan skyline, all dark."
go west                → [Atlantic Ave]
go west                → [Boerum Place]
go south               → [Museum Exit]  — back underground, warmth restores
go down                → [Toolshed]
score                  → "1/1 | Score: 10"
# Warmth should be back to 100 after 3 turns underground
quit
```

**Validation:** warmth counter must:
- Drop from 100 → 95 → 90 → 85 on surface
- Stay at 85 with the coat (i.e. -2/turn after wearing it; this requires the test path to walk the surface without the coat, then back underground, then with the coat to demonstrate)
- Restore to 100 after 3 turns back underground

## 9. Out of Scope (deferred to M4+)

- Rail tunnel navigation (M4 introduces the actual tunnel-grate opening and the first tunnel segment)
- Surface Manhattan expansion beyond Boerum Place block (M4-M6)
- More puzzles (M3 has zero puzzles, only mechanics)
- Win condition (M6)
- Save/load (M5+ if at all)

## 10. Open Questions for You

1. ~~**Automatic vs. explicit `wear`?** (Section 7)~~ — **RESOLVED 2026-06-08: automatic wear.** No `wear` verb.
2. **Warmth display in prompt?** Always show `[W:75]` or only when on the surface?
3. **Health damage at 0 warmth: instant death or recoverable?** My vote: damage at 0 warmth, but going back underground heals both warmth AND health.
4. **Tone of opening crawl for M3?** Should there be a new crawl when the player first goes up, or is the moment of stepping into daylight enough?

## 11. Estimated Effort

- `world_data.py`: +6 rooms, +1 item, +4 features. ~150 lines.
- `newzork.py`: warmth/health state, per-turn damage loop, conditional surface room behavior, prompt update, automatic wear logic for `winter_coat`. ~80 lines.
- Engine implication for automatic wear: `take_command` checks if the taken item has `auto_wear: True` in its data; if so, skip the usual "added to inventory" path and instead add to `worn_items` with a flavor message. Cold damage reads `worn_items` to apply the parka's -50% reduction.
- Test path: 1-2 commits per step, ~6-8 commits total.
- New verbs: 0 (or 1 if we add `wear`).
- 1-2 hours of build time for CodeMaster. Watchdog validates in 10 min.

## 12. What M3 Establishes for M4+

- **The cold mechanic** is the surface's defining challenge
- **Tunnel grates** are the bridge between surface and subway; M4+ will unlock them with the right item
- **Dead-end rooms with evocative features** (taxi cab, frozen bench) are the place to plant future puzzle hooks
- **The "look up" command** (reusing `look` on a feature) becomes a way to add atmosphere without new verbs
