#!/usr/bin/env python3
"""
NewZork engine — I/O-free game logic.

All commands return (text_output, game_state_dict). The CLI and the web
server both consume the same engine. State is a plain dict that can be
serialized to JSON for saves / localStorage mirrors.

M1-M3: The Concourse → Restore the Lights → Street Level
"""

import copy
import sys
import world_data


# === Public API ===

def new_game():
    """Create a fresh game state as a serializable dict."""
    return {
        "current_room": "main_concourse",
        "inventory": [],
        "visited_rooms": [],
        "door_unlocked": False,
        "lights_on": False,
        "score": 0,
        "panel_opened": False,
        "generator_used": False,
        "warmth": 100,
        "health": 100,
        "worn_items": [],
        "turns": 0,
    }


def process_command(state, command_line):
    """Process a command line. Returns the text output (with ANSI codes).

    Mutates `state` in place. `state` is a dict matching new_game()'s shape.
    World data (rooms, items) is deep-copied on first use so each game
    session gets its own mutable copy.
    """
    _ensure_world_copy(state)

    if not command_line or not command_line.strip():
        return ""

    parts = command_line.strip().lower().split()
    verb = parts[0]
    args = parts[1:] if len(parts) > 1 else []

    out = []

    if verb in ("look", "l", "examine", "x"):
        _look(state, args, out)
    elif verb == "read":
        _read(state, args, out)
    elif verb in ("go", "walk", "move"):
        _go(state, args, out)
    elif verb in ("n", "north", "s", "south", "e", "east", "w", "west", "u", "up", "d", "down"):
        _go(state, [verb], out)
    elif verb in ("take", "get", "grab", "pick"):
        if verb == "pick" and args and args[0] == "up":
            _take(state, args[1:], out)
        else:
            _take(state, args, out)
    elif verb in ("drop", "put", "leave"):
        _drop(state, args, out)
    elif verb in ("inventory", "i", "inv"):
        _inventory(state, out)
    elif verb in ("use", "activate", "apply"):
        _use(state, args, out)
    elif verb == "score":
        _score(state, out)
    elif verb in ("help", "?"):
        _help(out)
    elif verb in ("quit", "exit"):
        out.append(_crawl_farewell())
    else:
        out.append(f"{R}You can't do that here. Try: look, go, take, use, inventory, score, help, quit.{E}")

    state["turns"] += 1
    return "\n".join(out)


def opening_crawl():
    """Return the opening crawl text (ANSI-colored)."""
    return _crawl_opening()


def prompt_for(state):
    """Return the prompt string for the given state (e.g. '> [W:75] ')."""
    _ensure_world_copy(state)
    rooms = _world(state)["rooms"]
    if rooms[state["current_room"]].get("cold", False):
        return f"> [W:{state['warmth']}] "
    return "> "


# === Internals ===

# ANSI color codes
Y = "\033[93m"  # yellow — room names, exits
C = "\033[96m"  # cyan   — item names
W = "\033[97m"  # white  — narrative
R = "\033[91m"  # red    — danger, errors
G = "\033[92m"  # green  — success
M = "\033[95m"  # magenta— hints
B = "\033[1m"   # bold
E = "\033[0m"   # reset

# Per-session world copies
_WORLD_COPIES = {}


def _ensure_world_copy(state):
    sid = id(state)
    if sid not in _WORLD_COPIES:
        _WORLD_COPIES[sid] = {
            "rooms": copy.deepcopy(world_data.rooms),
            "items": copy.deepcopy(world_data.items),
            "features": copy.deepcopy(world_data.features),
        }
        if not isinstance(state.get("visited_rooms"), list):
            state["visited_rooms"] = []


def _world(state):
    _ensure_world_copy(state)
    return _WORLD_COPIES[id(state)]


def _crawl_opening():
    return (
        f"{W}══════════════════════════════════════════\n"
        f"  NEWZORK — October 1999\n"
        f"══════════════════════════════════════════{E}\n"
        f"{W}The city fell three months ago. The dead\n"
        f"walk the frozen streets. You've barricaded\n"
        f"yourself in the old Transit Museum, but\n"
        f"supplies are running low...{E}\n"
    )


def _crawl_farewell():
    return f"{W}The darkness closes in...{E}"


def _describe_room(state, room_id, out):
    rooms = _world(state)["rooms"]
    room = copy.deepcopy(rooms[room_id])

    if room_id == "lower_platform" and state["lights_on"]:
        room["exits"] = dict(room["exits"])
        room["exits"]["north"] = "toolshed"
        room["exits"]["east"] = "old_office"
        room["dark"] = False

    out.append(f"{Y}[{room['name']}]{E}")
    if room_id not in state["visited_rooms"]:
        out.append(f"{W}{room['description']}{E}")
        state["visited_rooms"].append(room_id)
    else:
        out.append(f"{W}{room['short_desc']}{E}")

    items = _world(state)["items"]
    if room["items"]:
        names = [items[iid]["name"] for iid in room["items"]]
        out.append(f"\nYou can see: {C}" + ", ".join(names) + f"{E}")

    if room["exits"]:
        exits = list(room["exits"].keys())
        out.append(f"\nExits: {Y}" + ", ".join(exits) + f"{E}")

    out.append("")


def _strip_articles(s):
    articles = {"a", "an", "the", "it"}
    words = s.split()
    if words and words[0] in articles:
        return " ".join(words[1:])
    return s


def _look(state, args, out):
    if not args:
        _describe_room(state, state["current_room"], out)
        return

    name = _strip_articles(" ".join(args).lower())
    rooms = _world(state)["rooms"]
    items = _world(state)["items"]
    features = _world(state)["features"]
    current = rooms[state["current_room"]]

    for iid in current["items"]:
        item = items[iid]
        if name == iid or name == item["name"] or name in item.get("synonyms", []):
            out.append(f"{C}{item['name'].capitalize()}{E}: {W}{item['description']}{E}")
            return
    for iid in state["inventory"]:
        item = items[iid]
        if name == iid or name == item["name"] or name in item.get("synonyms", []):
            out.append(f"{C}{item['name'].capitalize()}{E}: {W}{item['description']}{E}")
            return
    for iid in state["worn_items"]:
        item = items[iid]
        if name == iid or name == item["name"] or name in item.get("synonyms", []):
            out.append(f"{C}{item['name'].capitalize()}{E}: {W}{item['description']}{E}")
            return
    for fid in current["features"]:
        feat = features[fid]
        if name == fid or name == feat["name"] or name in feat.get("synonyms", []):
            out.append(f"{C}{feat['name'].capitalize()}{E}: {W}{feat['description']}{E}")
            return

    out.append(f"{R}You don't see that here.{E}")


def _read(state, args, out):
    if not args:
        out.append(f"{R}Read what?{E}")
        return

    name = _strip_articles(" ".join(args).lower())
    rooms = _world(state)["rooms"]
    items = _world(state)["items"]
    features = _world(state)["features"]
    current = rooms[state["current_room"]]

    candidates = []
    for iid in current["items"]:
        candidates.append((iid, items[iid]))
    for iid in state["inventory"]:
        candidates.append((iid, items[iid]))
    for iid in state["worn_items"]:
        candidates.append((iid, items[iid]))
    for fid in current["features"]:
        candidates.append((fid, features[fid]))

    for cid, c in candidates:
        if name == cid or name == c["name"] or name in c.get("synonyms", []):
            out.append(f"{C}{c['name'].capitalize()}{E}: {W}{c['description']}{E}")
            if "text" in c:
                if cid == "broken_panel" and state["panel_opened"]:
                    out.append(f"{W}The wiring inside is scorched. You'll need a fuel cell to restore power.{E}")
                elif cid == "generator" and state["generator_used"]:
                    out.append(f"{W}The generator hums steadily. The fuel gauge reads 73%.{E}")
                else:
                    out.append(f"{W}{c['text']}{E}")
            return
    out.append(f"{R}You don't see that here.{E}")


def _take(state, args, out):
    if not args:
        out.append(f"{R}Take what?{E}")
        return
    name = _strip_articles(" ".join(args).lower())
    rooms = _world(state)["rooms"]
    items = _world(state)["items"]
    current = rooms[state["current_room"]]

    item_id = None
    for iid in current["items"]:
        it = items[iid]
        if name == iid or name == it["name"] or name in it.get("synonyms", []):
            item_id = iid
            break
    if not item_id:
        out.append(f"{R}You don't see that here.{E}")
        return

    it = items[item_id]
    if not it.get("takeable", False):
        out.append(f"{R}You can't take that.{E}")
        return

    if it.get("auto_wear", False):
        current["items"].remove(item_id)
        state["worn_items"].append(item_id)
        out.append(f"{W}You put on the {it['name']}. It's stiff but warm.{E}")
        return

    current["items"].remove(item_id)
    state["inventory"].append(item_id)
    out.append(f"{W}Taken.{E}")


def _drop(state, args, out):
    if not args:
        out.append(f"{R}Drop what?{E}")
        return
    name = _strip_articles(" ".join(args).lower())
    rooms = _world(state)["rooms"]
    items = _world(state)["items"]
    current = rooms[state["current_room"]]

    item_id = None
    for iid in state["inventory"]:
        it = items[iid]
        if name == iid or name == it["name"] or name in it.get("synonyms", []):
            item_id = iid
            break
    if not item_id:
        for iid in state["worn_items"]:
            it = items[iid]
            if name == iid or name == it["name"] or name in it.get("synonyms", []):
                item_id = iid
                break
    if not item_id:
        out.append(f"{R}You don't have that.{E}")
        return

    it = items[item_id]
    if item_id in state["inventory"]:
        state["inventory"].remove(item_id)
    elif item_id in state["worn_items"]:
        state["worn_items"].remove(item_id)
        out.append(f"{W}You shrug off the {it['name']}.{E}")

    current["items"].append(item_id)
    out.append(f"{W}Dropped.{E}")


def _use(state, args, out):
    if not args:
        out.append(f"{R}Use what?{E}")
        return

    if "on" in args:
        on_idx = args.index("on")
        if on_idx == 0 or on_idx == len(args) - 1:
            out.append(f"{R}Use what on what?{E}")
            return
        item_name = _strip_articles(" ".join(args[:on_idx]).lower())
        target_name = _strip_articles(" ".join(args[on_idx + 1:]).lower())
    else:
        item_name = _strip_articles(" ".join(args).lower())
        target_name = None

    items = _world(state)["items"]
    features = _world(state)["features"]
    rooms = _world(state)["rooms"]
    current = rooms[state["current_room"]]

    item_id = None
    for iid in state["inventory"]:
        it = items[iid]
        if item_name == iid or item_name == it["name"] or item_name in it.get("synonyms", []):
            item_id = iid
            break
    if not item_id:
        out.append(f"{R}You don't have that.{E}")
        return
    it = items[item_id]

    if not target_name:
        if it.get("use_with", {}):
            out.append(f"{R}Use {it['name']} on what?{E}")
        else:
            out.append(f"{W}You use the {it['name']}. Nothing happens.{E}")
        return

    target_id = None
    for iid in current["items"]:
        ti = items[iid]
        if target_name == iid or target_name == ti["name"] or target_name in ti.get("synonyms", []):
            target_id = iid
            break
    if not target_id:
        for fid in current["features"]:
            f = features[fid]
            if target_name == fid or target_name == f["name"] or target_name in f.get("synonyms", []):
                target_id = fid
                break
    if not target_id and target_name in ("door", "maintenance door", "north door"):
        target_id = "control_room_door"
    if not target_id:
        out.append(f"{R}You don't see that here.{E}")
        return

    use_with = it.get("use_with", {})
    if target_id not in use_with:
        out.append(f"{R}That doesn't work.{E}")
        return

    effect = use_with[target_id]
    if target_id == "control_room_door" and effect == "unlock":
        if state["door_unlocked"]:
            out.append(f"{W}The door is already unlocked.{E}")
        else:
            state["door_unlocked"] = True
            out.append(f"{W}You unlock the maintenance door with the key.{E}")
    elif target_id == "broken_panel" and effect == "unlock":
        if state["panel_opened"]:
            out.append(f"{W}The fusebox panel is already open.{E}")
        else:
            state["panel_opened"] = True
            out.append(f"{W}The fusebox panel swings open, revealing ancient wiring.{E}")
    elif target_id == "generator" and effect == "restore_power":
        if state["generator_used"]:
            out.append(f"{W}The generator is already running.{E}")
        else:
            state["generator_used"] = True
            state["lights_on"] = True
            state["score"] += 10
            out.append(f"{W}The generator groans to life. Fluorescent lights flicker on throughout the museum. You feel less alone.{E}")
            if it.get("consumable", False):
                state["inventory"].remove(item_id)
            _describe_room(state, state["current_room"], out)
    else:
        out.append(f"{W}You use the {it['name']} on the {target_name}. Nothing happens.{E}")


def _apply_environment_effects(state, dest_id, out):
    rooms = _world(state)["rooms"]
    dest = rooms[dest_id]

    if dest.get("cold", False):
        if "winter_coat" in state["worn_items"]:
            state["warmth"] = max(0, state["warmth"] - 2)
        else:
            state["warmth"] = max(0, state["warmth"] - 5)
        if state["warmth"] == 0:
            state["health"] = max(0, state["health"] - 1)
            if state["health"] == 0:
                out.append(f"{R}You succumb to the cold. The world fades to white.{E}")
                out.append(f"{M}[GAME OVER]{E}")
    else:
        state["warmth"] = min(100, state["warmth"] + 10)
        state["health"] = min(100, state["health"] + 5)


def _go(state, args, out):
    if not args:
        out.append(f"{R}Go where?{E}")
        return

    aliases = {"n": "north", "s": "south", "e": "east", "w": "west", "u": "up", "d": "down"}
    direction = aliases.get(args[0], args[0])

    rooms = _world(state)["rooms"]
    current = copy.deepcopy(rooms[state["current_room"]])

    if state["current_room"] == "lower_platform" and state["lights_on"]:
        current["exits"] = dict(current["exits"])
        current["exits"]["north"] = "toolshed"
        current["exits"]["east"] = "old_office"

    if direction not in current["exits"]:
        out.append(f"{R}You can't go that way.{E}")
        return

    dest_id = current["exits"][direction]
    dest = rooms[dest_id]

    if dest_id == "lower_platform":
        has_light = any(_world(state)["items"][iid].get("light_source", False) for iid in state["inventory"])
        if not has_light:
            out.append(f"{R}It's too dark to go down there. You'd surely fall and break your neck.{E}")
            return

    if dest_id == "control_room" and not state["door_unlocked"]:
        out.append(f"{R}The maintenance door is locked tight. You'll need a key.{E}")
        return

    state["current_room"] = dest_id
    _apply_environment_effects(state, dest_id, out)
    _describe_room(state, dest_id, out)


def _inventory(state, out):
    all_items = state["inventory"] + state["worn_items"]
    if not all_items:
        out.append(f"{W}You're not carrying anything.{E}")
        return
    out.append(f"{W}You're carrying:{E}")
    items = _world(state)["items"]
    for iid in state["inventory"]:
        out.append(f"  {C}{items[iid]['name']}{E}")
    for iid in state["worn_items"]:
        out.append(f"  {C}{items[iid]['name']} (worn){E}")


def _score(state, out):
    puzzles = 1 if state["lights_on"] else 0
    out.append(f"{W}Puzzles solved: {puzzles}/1 | Score: {state['score']}{E}")


def _help(out):
    out.append(
        f"{W}Commands:{E}\n"
        f"  {C}look (l, x) [thing]{E}      — describe room or examine something\n"
        f"  {C}go (n/s/e/w/u/d){E}         — move (or just type a direction)\n"
        f"  {C}take (get) <item>{E}        — pick something up\n"
        f"  {C}drop <item>{E}              — put something down\n"
        f"  {C}use <item> [on <target>]{E} — use an item, optionally on something\n"
        f"  {C}read <item>{E}              — read text on something\n"
        f"  {C}inventory (i){E}            — list what you're carrying\n"
        f"  {C}score{E}                    — show puzzles solved\n"
        f"  {C}help (?) {E}                — this list\n"
        f"  {C}quit{E}                     — end the game"
    )


# === CLI entry point ===

def main():
    state = new_game()
    print(opening_crawl())
    out = []
    _describe_room(state, state["current_room"], out)
    print("\n".join(out))

    while True:
        try:
            cmd = input(prompt_for(state)).strip().lower()
            if not cmd:
                continue
            output = process_command(state, cmd)
            if output:
                print(output)
            if cmd in ("quit", "exit"):
                break
        except (KeyboardInterrupt, EOFError):
            print(f"\n{W}The darkness closes in...{E}")
            break


if __name__ == "__main__":
    main()
