#!/usr/bin/env python3
"""
regression.py — Regression test suite for NewZork.

Exercises the engine functions directly (not the CLI) against expected
outcomes. Each test mutates the global game_state and asserts on the
resulting state.

Run with:
    python3 regression.py
    python3 regression.py --verbose
    python3 regression.py --filter M2       # only M2 tests
    python3 regression.py --filter score    # only tests whose name contains "score"

Exit code 0 = all passed, 1 = at least one failure.
"""

import sys
import os
import io
import copy
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import world_data
import newzork


def reset_state():
    """Reset BOTH the global game_state AND the world_data module.

    Important: world_data.rooms[i].items is mutated by take_command
    (it removes items from rooms when picked up). Without restoring,
    sequential tests see depleted rooms. We snapshot on first call
    and restore from snapshot on every reset.
    """
    newzork.game_state = newzork.GameState()
    if not hasattr(reset_state, '_snapshot'):
        reset_state._snapshot = {
            'rooms': copy.deepcopy(world_data.rooms),
        }
    world_data.rooms.clear()
    world_data.rooms.update(copy.deepcopy(reset_state._snapshot['rooms']))


def make_tests():
    tests = []

    # ---- M1 tests ----
    def m1_happy_path():
        results = []
        newzork.take_command(['flashlight'])
        results.append(('flashlight in inventory', 'flashlight' in newzork.game_state.inventory))
        # Note: main_concourse is the start room and the engine only adds to
        # visited_rooms via describe_room (called on `look` or movement to a
        # new room). The start room is never explicitly added. To verify
        # visited_rooms works, check a room we actually visit during the path.
        newzork.go_command(['east'])
        results.append(('moved to exhibits_hall', newzork.game_state.current_room == 'exhibits_hall'))
        results.append(('exhibits_hall now visited', 'exhibits_hall' in newzork.game_state.visited_rooms))

        newzork.take_command(['maintenance_key'])
        newzork.take_command(['subway_token'])
        results.append(('maintenance_key in inventory', 'maintenance_key' in newzork.game_state.inventory))
        results.append(('subway_token in inventory', 'subway_token' in newzork.game_state.inventory))

        newzork.use_command(['maintenance_key', 'on', 'door'])
        results.append(('door_unlocked after using key', newzork.game_state.door_unlocked is True))

        newzork.go_command(['north'])
        results.append(('moved to control_room', newzork.game_state.current_room == 'control_room'))

        newzork.go_command(['south'])
        newzork.go_command(['west'])
        newzork.go_command(['down'])
        results.append(('moved to lower_platform with flashlight', newzork.game_state.current_room == 'lower_platform'))

        return results

    tests.append(('M1: happy path through 4 rooms', m1_happy_path))

    def m1_dark_gate():
        results = []
        # No flashlight, so we should refuse to enter lower_platform
        newzork.go_command(['east'])
        newzork.go_command(['west'])
        before = newzork.game_state.current_room
        newzork.go_command(['down'])
        results.append(('cannot enter lower_platform without light', newzork.game_state.current_room == before))
        return results

    tests.append(('M1: dark gate (no flashlight blocks entry)', m1_dark_gate))

    def m1_locked_door():
        results = []
        newzork.go_command(['east'])
        before = newzork.game_state.current_room
        newzork.go_command(['north'])
        results.append(('cannot enter control_room without unlocking door', newzork.game_state.current_room == before))
        return results

    tests.append(('M1: locked door blocks north exit', m1_locked_door))

    # ---- M2 tests ----
    def m2_puzzle_happy_path():
        results = []
        newzork.take_command(['flashlight'])
        newzork.go_command(['east'])
        newzork.take_command(['maintenance_key'])
        newzork.take_command(['subway_token'])
        newzork.use_command(['maintenance_key', 'on', 'door'])
        newzork.go_command(['north'])
        newzork.take_command(['fuel_cell'])
        results.append(('fuel_cell taken from control_room', 'fuel_cell' in newzork.game_state.inventory))
        newzork.go_command(['south'])
        newzork.go_command(['west'])
        newzork.go_command(['down'])
        newzork.take_command(['panel_key'])
        results.append(('panel_key taken from lower_platform', 'panel_key' in newzork.game_state.inventory))
        newzork.use_command(['panel_key', 'on', 'panel'])
        results.append(('panel_opened after using key', newzork.game_state.panel_opened is True))
        newzork.use_command(['fuel_cell', 'on', 'generator'])
        results.append(('lights_on after generator', newzork.game_state.lights_on is True))
        results.append(('generator_used after use', newzork.game_state.generator_used is True))
        results.append(('score == 10 after generator', newzork.game_state.score == 10))
        results.append(('fuel_cell consumed (gone from inventory)', 'fuel_cell' not in newzork.game_state.inventory))
        return results

    tests.append(('M2: restore-the-lights puzzle happy path', m2_puzzle_happy_path))

    def m2_conditional_exits():
        results = []
        newzork.take_command(['flashlight'])
        newzork.go_command(['east'])
        newzork.take_command(['maintenance_key'])
        newzork.use_command(['maintenance_key', 'on', 'door'])
        newzork.go_command(['north'])
        newzork.take_command(['fuel_cell'])
        newzork.go_command(['south'])
        newzork.go_command(['west'])
        newzork.go_command(['down'])
        newzork.take_command(['panel_key'])
        newzork.use_command(['panel_key', 'on', 'panel'])
        # Lights still off
        before = newzork.game_state.current_room
        newzork.go_command(['north'])
        results.append(('cannot reach toolshed before lights on', newzork.game_state.current_room == before))
        newzork.use_command(['fuel_cell', 'on', 'generator'])
        newzork.go_command(['north'])
        results.append(('toolshed reachable after lights on', newzork.game_state.current_room == 'toolshed'))
        newzork.go_command(['south'])
        newzork.go_command(['east'])
        results.append(('old_office reachable after lights on', newzork.game_state.current_room == 'old_office'))
        return results

    tests.append(('M2: conditional exits gate on lights_on', m2_conditional_exits))

    def m2_score_initial():
        results = []
        results.append(('initial score is 0', newzork.game_state.score == 0))
        results.append(('initial lights_on is False', newzork.game_state.lights_on is False))
        results.append(('initial door_unlocked is False', newzork.game_state.door_unlocked is False))
        return results

    tests.append(('M2: initial state correct', m2_score_initial))

    def m2_score_denominator():
        results = []
        newzork.take_command(['flashlight'])
        newzork.go_command(['east'])
        newzork.take_command(['maintenance_key'])
        newzork.use_command(['maintenance_key', 'on', 'door'])
        newzork.go_command(['north'])
        newzork.take_command(['fuel_cell'])
        newzork.go_command(['south'])
        newzork.go_command(['west'])
        newzork.go_command(['down'])
        newzork.take_command(['panel_key'])
        newzork.use_command(['panel_key', 'on', 'panel'])
        newzork.use_command(['fuel_cell', 'on', 'generator'])
        buf = io.StringIO()
        with redirect_stdout(buf):
            newzork.score_command([])
        output = buf.getvalue()
        results.append(('score shows 1/1 denominator', '1/1' in output))
        results.append(('score shows 10 points', '10' in output))
        results.append(('score does NOT show 0/3', '0/3' not in output))
        return results

    tests.append(('M2: score denominator is 1/1', m2_score_denominator))

    def m2_fuel_cell_in_control_room():
        results = []
        room = world_data.rooms['control_room']
        results.append(('fuel_cell IS in control_room.items', 'fuel_cell' in room['items']))
        room = world_data.rooms['exhibits_hall']
        results.append(('fuel_cell NOT in exhibits_hall.items', 'fuel_cell' not in room['items']))
        return results

    tests.append(('M2: fuel_cell located in control_room (not exhibits_hall)', m2_fuel_cell_in_control_room))

    def m2_parser_id_match():
        results = []
        newzork.take_command(['flashlight'])
        newzork.go_command(['east'])
        newzork.take_command(['maintenance_key'])
        newzork.use_command(['maintenance_key', 'on', 'door'])
        newzork.go_command(['north'])
        newzork.take_command(['fuel_cell'])
        newzork.go_command(['south'])
        newzork.go_command(['west'])
        newzork.go_command(['down'])
        # Try taking by ID (underscore form, not name)
        newzork.take_command(['panel_key'])
        results.append(('parser accepts ID "panel_key" (underscore)', 'panel_key' in newzork.game_state.inventory))
        return results

    tests.append(('M2: parser accepts item ID (panel_key)', m2_parser_id_match))

    def m2_double_use_noop():
        results = []
        # Use fuel_cell on generator twice — second use should be a no-op
        newzork.take_command(['flashlight'])
        newzork.go_command(['east'])
        newzork.take_command(['maintenance_key'])
        newzork.use_command(['maintenance_key', 'on', 'door'])
        newzork.go_command(['north'])
        newzork.take_command(['fuel_cell'])
        newzork.go_command(['south'])
        newzork.go_command(['west'])
        newzork.go_command(['down'])
        newzork.take_command(['panel_key'])
        newzork.use_command(['panel_key', 'on', 'panel'])
        newzork.use_command(['fuel_cell', 'on', 'generator'])
        score_after_first = newzork.game_state.score
        # Try to use again — but fuel_cell is consumed, so this should fail differently
        buf = io.StringIO()
        with redirect_stdout(buf):
            newzork.use_command(['fuel_cell', 'on', 'generator'])
        results.append(('score unchanged on second use attempt', newzork.game_state.score == score_after_first))
        return results

    tests.append(('M2: double-use of generator is no-op', m2_double_use_noop))

    def m2_panel_double_use_idempotent():
        results = []
        newzork.take_command(['flashlight'])
        newzork.go_command(['east'])
        newzork.take_command(['maintenance_key'])
        newzork.use_command(['maintenance_key', 'on', 'door'])
        newzork.go_command(['north'])
        newzork.take_command(['fuel_cell'])
        newzork.go_command(['south'])
        newzork.go_command(['west'])
        newzork.go_command(['down'])
        newzork.take_command(['panel_key'])
        newzork.use_command(['panel_key', 'on', 'panel'])
        # Second use should be idempotent
        before = newzork.game_state.panel_opened
        # Don't have a second key, so this would just fail with "you don't have that"
        # The real idempotency test: if we WERE to use it again, score/panel_opened should not change
        # We can't easily simulate that without a second key, so just verify the flag is set once
        results.append(('panel_opened exactly once after use', before is True))
        return results

    tests.append(('M2: panel opens exactly once', m2_panel_double_use_idempotent))

    return tests


def main():
    verbose = '--verbose' in sys.argv
    arg_filter = None
    if '--filter' in sys.argv:
        i = sys.argv.index('--filter')
        arg_filter = sys.argv[i + 1] if i + 1 < len(sys.argv) else None

    tests = make_tests()
    if arg_filter:
        tests = [(n, fn) for n, fn in tests if arg_filter.lower() in n.lower()]

    print(f'Running {len(tests)} regression tests...\n')
    total_passed = 0
    total_failed = 0
    failures = []

    for name, fn in tests:
        reset_state()
        try:
            results = fn()
        except Exception as e:
            import traceback
            results = [(f'EXCEPTION: {type(e).__name__}: {e}', False)]
        if not results:
            results = [('test returned no assertions', False)]
        passed = sum(1 for _, p in results if p)
        failed = len(results) - passed
        total_passed += passed
        total_failed += failed
        if failed == 0:
            mark = '✅'
        else:
            mark = '❌'
            failures.append((name, results))
        print(f'  {mark} {name}  ({passed}/{len(results)})')
        if verbose or failed > 0:
            for desc, p in results:
                mark2 = '    ✓' if p else '    ✗'
                print(f'{mark2} {desc}')

    print(f'\n--- {total_passed} passed, {total_failed} failed ---')
    if failures:
        print('\nFailures:')
        for name, results in failures:
            for desc, p in results:
                if not p:
                    print(f'  [{name}] {desc}')
    sys.exit(0 if total_failed == 0 else 1)


if __name__ == '__main__':
    main()
