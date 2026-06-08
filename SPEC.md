# NewZork — Text Adventure Spec

## 1. Concept & Vision

**NewZork** is a text adventure set in a zombie-apocalyptic Manhattan, October 1999. You play a survivor navigating the frozen wasteland of NYC's Transit Museum — the last defensible stronghold — while solving puzzles, scavenging, and uncovering what happened to the city. The tone is bleak, atmospheric, and slightly dark-humored. Think *The Last of Us* meets classic Infocom.

**Core loop:** Explore → Interact → Solve → Survive

---

## 2. Technical Stack

- **Language:** Python 3 (single file CLI)
- **Parser:** Hand-rolled tokenizer + noun/verb/preposition resolution (no external libs)
- **State:** JSON save files (`~/.newzork/saves/`)
- **No AI required** — all puzzles are hand-crafted
- **Output:** ANSI-colored terminal text, cross-platform

---

## 3. World Structure

### 3.1 Rooms

Each room has:
- `id` (slug)
- `name` (display)
- `description` (full, shown on first visit)
- `short_desc` (shown on revisit)
- `exits` (map of direction → room_id)
- `items` (list of item IDs present)
- `features` (static interactables: benches, displays, lockers)
- `dark` (bool — requires light source)
- `cold` (bool — exposure damage over turns)

### 3.2 The Map (Phase 1 — Manhattan Core, ~30 rooms)

```
[Grand Central]—[Park Ave Bridge]—[Murray Hill]—[Kips Bay]—[Gramercy]
       |                                      |
[Midtown East]                         [Rosehill]
       |
[Times Square]—[Hell's Kitchen]—[Clinton]
       |
[Columbus Circle]—[Upper West Side]—[Upper East Side]
       |              |                |
[Midtown West]    [Central Park]   [Central Park East]
       |              |                |
[Chelsea]      [Harlem]           [East Harlem]
       |              |                |
[West Village]——[SoHo]——[Lower East]——[Chinatown]——[Financial District]
       |                                                |
[Noho]——————[Greenwich]                                 |
       |                                                |
[West 4th]——[Tribeca]——————————————[Battery Park]
       |
[Canal St]——[Two Bridges]
```

### 3.3 Items

Each item has:
- `id`, `name`, `description`
- `takeable` (bool)
- `use_with` (dict: {target_id: result_event_id})
- `consumable` (bool — destroyed on use)
- `light_source` (bool)
- `edible` / `drinkable`
- `weapon` (bool)
- `synonyms` (list of aliases)

### 3.4 Puzzles (Phase 1 target: 5–7)

1. **Grand Central Power** — Restore emergency lighting in Grand Central to access the underground
2. **Kips Bay Pharmacy** — Find the correct keycode to unlock the pharmacy safe
3. **Gramercy Armory** — Trade 3 specific items to unlock the armory cache
4. **Chinatown Lantern** — Light the lantern at the shrine to reveal the next area
5. **Battery Park Boat** — Clear the debris, find fuel, start the boat to escape
6. **Central Park Frozen Lake** — Find the hidden passage beneath the ice (requires correct item)
7. **Rosehill Crypt** — Solve a text riddle to open the crypt

---

## 4. Parser Contract

### 4.1 Command Format

```
<verb> [article] <noun> [preposition [article] <noun>]
```

### 4.2 Core Verbs

| Verb | Aliases | Behavior |
|------|---------|----------|
| `look` | `l`, `examine`, `x` | Describe room or item |
| `go` | `walk`, `move`, `n/s/e/w/u/d` | Navigate |
| `take` | `get`, `grab`, `pick up` | Add item to inventory |
| `drop` | `put`, `leave` | Remove from inventory |
| `use` | `activate`, `apply` | Trigger item effect |
| `use X on Y` | `apply X to Y` | Combine/interact |
| `open` | `unlock` | Open container/door |
| `read` | — | Read text on item |
| `inventory` | `i`, `inv` | List carried items |
| `save` | — | Save game state |
| `load` | — | Load save |
| `help` | `?` | List commands |

### 4.3 Parser Behavior

- Strip articles (`a`, `an`, `the`, `it`)
- Fuzzy match nouns against room items + inventory
- Unknown commands → contextual hint, not generic error
- Multi-word nouns: "frozen lake" → look up "frozen lake" before splitting

---

## 5. Game State

### 5.1 Player State

```json
{
  "current_room": "grand_central",
  "inventory": [],
  "turns": 0,
  "health": 100,
  "warmth": 100,
  "flags": {
    "grand_central_power": false,
    "pharmacy_safe_open": false,
    "armory_unlocked": false,
    "lantern_lit": false,
    "boat_ready": false,
    "lake_passage": false,
    "crypt_open": false
  },
  "visited_rooms": []
}
```

### 5.2 Save Format

- One JSON file per save slot
- Location: `~/.newzork/saves/slot_{1,2,3}.json`
- Auto-save on room change

---

## 6. Output Format

### 6.1 ANSI Colors

| Color | Use |
|-------|-----|
| Yellow | Room names, exits |
| Cyan | Item names |
| Red | Damage, danger |
| Green | Success, healing |
| Magenta | Puzzle hints |
| White/Bold | Narrative text |

### 6.2 Screen Layout

```
══════════════════════════════════════════
  NEWZORK — October 1999
══════════════════════════════════════════
[Grand Central Terminal — Main Concourse]
You stand beneath the vaulted celestial ceiling of Grand Central's
Main Concourse. Dead tourists slump against pillars. Frost creeps
up the walls. The cold is absolute.

Exits: north (Park Ave), east (Midtown), west (West Corridor)

You can see: frozen_fountain, backpack, newspaper
> _
```

---

## 7. Commands & Scoring

- **Turns** — every command = 1 turn
- **Health** — starts at 100, cold/damage reduces it
- **Score** — puzzle completions, key item discoveries (Phase 1: no scoring, just solvability)
- **Win condition (Phase 1):** Reach Battery Park and board the boat
- **Lose condition:** Health reaches 0

---

## 8. Phase 1 Deliverables

- [x] This SPEC.md
- [ ] `newzork.py` — full game engine + parser
- [ ] `world_data.py` — room + item definitions
- [ ] 30+ rooms defined
- [ ] 5+ puzzles working
- [ ] Save/load functional
- [ ] Help system complete