#!/usr/bin/env python3
"""
regression_web.py — Smoke test for the I/O-free engine.

Confirms the refactored engine still produces the same outcomes as the
original CLI engine. Runs a few canonical commands and checks state.

Run with: python3 regression_web.py
Exit code 0 = pass, 1 = fail.
"""

import sys
import os
import json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import engine


def assert_eq(label, actual, expected):
    ok = actual == expected
    mark = "PASS" if ok else "FAIL"
    print(f"  [{mark}] {label}: {'pass' if ok else f'got {actual!r}, expected {expected!r}'}")
    return ok


def main():
    failures = 0
    print("Engine smoke test (M1-M3 canonical paths)\n")

    print("M1: flashlight + door + control room")
    s = engine.new_game()
    engine.process_command(s, "take flashlight")
    failures += not assert_eq("flashlight in inventory", "flashlight" in s["inventory"], True)
    engine.process_command(s, "look")
    failures += not assert_eq("main_concourse visited", "main_concourse" in s["visited_rooms"], True)

    engine.process_command(s, "go east")
    failures += not assert_eq("moved to exhibits_hall", s["current_room"], "exhibits_hall")

    engine.process_command(s, "take maintenance_key")
    failures += not assert_eq("maintenance_key in inventory", "maintenance_key" in s["inventory"], True)

    engine.process_command(s, "use maintenance_key on door")
    failures += not assert_eq("door_unlocked", s["door_unlocked"], True)

    engine.process_command(s, "go north")
    failures += not assert_eq("moved to control_room", s["current_room"], "control_room")

    engine.process_command(s, "take fuel_cell")
    failures += not assert_eq("fuel_cell in inventory", "fuel_cell" in s["inventory"], True)

    print("\nM2: power restoration")
    engine.process_command(s, "go south")
    engine.process_command(s, "go west")
    engine.process_command(s, "go down")

    engine.process_command(s, "take panel_key")
    failures += not assert_eq("panel_key in inventory", "panel_key" in s["inventory"], True)

    engine.process_command(s, "use panel_key on broken_panel")
    failures += not assert_eq("panel_opened", s["panel_opened"], True)

    engine.process_command(s, "use fuel_cell on generator")
    failures += not assert_eq("lights_on", s["lights_on"], True)
    failures += not assert_eq("score after power", s["score"], 10)
    failures += not assert_eq("fuel_cell consumed", "fuel_cell" in s["inventory"], False)

    engine.process_command(s, "go north")
    failures += not assert_eq("in toolshed", s["current_room"], "toolshed")

    print("\nM3: street level")
    engine.process_command(s, "go up")
    failures += not assert_eq("in museum_exit", s["current_room"], "museum_exit")

    engine.process_command(s, "go north")
    failures += not assert_eq("in boerum_place", s["current_room"], "boerum_place")
    failures += not assert_eq("cold room drains warmth", s["warmth"] < 100, True)

    engine.process_command(s, "go west")
    failures += not assert_eq("in schermerhorn_st", s["current_room"], "schermerhorn_st")

    coat_warmth_before = s["warmth"]
    engine.process_command(s, "take winter_coat")
    failures += not assert_eq("coat auto-worn", "winter_coat" in s["worn_items"], True)
    failures += not assert_eq("coat not in inventory", "winter_coat" in s["inventory"], False)

    engine.process_command(s, "go south")
    engine.process_command(s, "go north")
    warmth_after = s["warmth"]
    failures += not assert_eq("coat halves cold damage", coat_warmth_before - warmth_after, 4)

    # Warmth restoration underground
    engine.process_command(s, "go east")
    engine.process_command(s, "go south")
    warmth_just_outside = s["warmth"]
    engine.process_command(s, "go south")  # toolshed
    failures += not assert_eq("warmth restored underground (net gain)", s["warmth"] > warmth_just_outside, True)

    print("\nEngine output contract")
    out = engine.process_command(engine.new_game(), "look")
    failures += not assert_eq("process_command returns str", isinstance(out, str), True)
    failures += not assert_eq("opening_crawl returns str", isinstance(engine.opening_crawl(), str), True)
    failures += not assert_eq("prompt_for returns str", isinstance(engine.prompt_for(engine.new_game()), str), True)

    print("\nState is JSON-serializable")
    s2 = engine.new_game()
    engine.process_command(s2, "take flashlight")
    try:
        json.dumps(s2)
        failures += not assert_eq("state round-trips through JSON", True, True)
    except Exception as e:
        print(f"  [FAIL] state not JSON-serializable: {e}")
        failures += 1

    s3 = json.loads(json.dumps(s2))
    failures += not assert_eq("restored state has flashlight", "flashlight" in s3["inventory"], True)

    print()
    if failures:
        print(f"--- {failures} FAILED ---")
        sys.exit(1)
    print("--- ALL PASS ---")
    sys.exit(0)


if __name__ == "__main__":
    main()
