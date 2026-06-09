"""
World data for NewZork M1-M3

This module contains the room and item definitions for the first three milestones
of the NewZork text adventure game.
"""

# Global state
lights_on = False


# Rooms
rooms = {
    "main_concourse": {
        "id": "main_concourse",
        "name": "Main Concourse",
        "description": "You stand on the entry platform of what was once the NYC Transit Museum. Two decommissioned subway cars sit on rusted tracks, and a single emergency light casts flickering shadows across the concourse. The air is thick with dust and the silence is absolute.",
        "short_desc": "You're back in the main concourse, where two old subway cars sit in the dim light.",
        "exits": {
            "east": "exhibits_hall",
            "down": "lower_platform"
        },
        "items": ["flashlight"],
        "features": ["control_room_door", "broken_panel"],
        "dark": False,
        "cold": False
    },
    "exhibits_hall": {
        "id": "exhibits_hall",
        "name": "Exhibits Hall",
        "description": "The exhibits hall is lined with display cases filled with old subway tokens, faded signage, and dusty artifacts. A glass case in the center displays a subway token. To the north, a heavy door marked 'MAINTENANCE' blocks the way.",
        "short_desc": "You're in the exhibits hall, surrounded by dusty displays and a locked door to the north.",
        "exits": {
            "west": "main_concourse",
            "north": "control_room"
        },
        "items": ["subway_token", "maintenance_key"],
        "features": ["control_room_door"],
        "dark": False,
        "cold": False
    },
    "control_room": {
        "id": "control_room",
        "name": "Control Room",
        "description": "The control room is small and cramped, with a desk covered in old equipment and a single chair. An emergency cabinet hangs on the wall, and the only exit is south back to the exhibits hall.",
        "short_desc": "You're in the control room, a cramped space with a desk and emergency cabinet.",
        "exits": {
            "south": "exhibits_hall"
        },
        "items": ["emergency_flares", "fuel_cell"],
        "features": [],
        "dark": False,
        "cold": False
    },
    "lower_platform": {
        "id": "lower_platform",
        "name": "Lower Platform",
        "description": "The stairs down have partially collapsed, and the platform below is shrouded in darkness. A rusted turnstile blocks the path, and an old MTA map hangs crookedly on the wall. You can barely make out the shapes of abandoned subway cars in the shadows.",
        "short_desc": "You're on the dark lower platform, where collapsed stairs lead to shadowy depths.",
        "exits": {
            "up": "main_concourse"
        },
        "items": ["panel_key"],
        "features": ["rusted_turnstile", "mta_map", "generator", "broken_panel"],
        "dark": True,
        "cold": False
    },
    "toolshed": {
        "id": "toolshed",
        "name": "Toolshed",
        "description": "A cramped maintenance toolshed. Rakes, shovels, and snow shovels line the walls. A radio sits on a shelf, its display dead.",
        "short_desc": "You're in the cramped maintenance toolshed. Tools line the walls.",
        "exits": {
            "south": "lower_platform",
            "up": "museum_exit"
        },
        "items": [],
        "features": [],
        "dark": False,
        "cold": False
    },
    "old_office": {
        "id": "old_office",
        "name": "Old Office",
        "description": "The museum curator's old office. Papers are scattered across the floor. A coffee mug sits on the desk, frozen mid-spill.",
        "short_desc": "You're in the curator's old office, papers scattered everywhere.",
        "exits": {
            "west": "lower_platform"
        },
        "items": [],
        "features": [],
        "dark": False,
        "cold": False
    },
    "museum_exit": {
        "id": "museum_exit",
        "name": "Museum Exit",
        "description": "You've emerged from the museum into the open air. The door behind you leads back to safety. Ahead, the streets of Brooklyn stretch out under a gray sky.",
        "short_desc": "You're at the museum exit, the door back inside to your south.",
        "exits": {
            "south": "toolshed",
            "north": "boerum_place",
            "east": "atlantic_ave"
        },
        "items": [],
        "features": [],
        "dark": False,
        "cold": True
    },
    "boerum_place": {
        "id": "boerum_place",
        "name": "Boerum Place",
        "description": "A wide intersection, abandoned cars buried in snow up to their windows. The wind whistles between buildings. A traffic light still swings in the wind.",
        "short_desc": "You're in Boerum Place, snow-covered cars and a swaying traffic light.",
        "exits": {
            "south": "museum_exit",
            "west": "schermerhorn_st",
            "east": "atlantic_ave",
            "north": "city_hall_steps"
        },
        "items": [],
        "features": ["traffic_light"],
        "dark": False,
        "cold": True
    },
    "schermerhorn_st": {
        "id": "schermerhorn_st",
        "name": "Schermerhorn Street",
        "description": "A side street lined with parked cars buried up to their windows. A bodega with a faded 'OPEN' sign sits on the corner. The wind cuts through your clothes.",
        "short_desc": "You're on Schermerhorn Street, parked cars and a bodega with a faded sign.",
        "exits": {
            "east": "boerum_place",
            "south": "parking_lot"
        },
        "items": ["winter_coat"],
        "features": [],
        "dark": False,
        "cold": True
    },
    "parking_lot": {
        "id": "parking_lot",
        "name": "Parking Lot",
        "description": "A small municipal parking lot, dead end. An old taxi with keys in the ignition sits abandoned. Snow drifts pile against the fence.",
        "short_desc": "You're in the parking lot, a dead end with an abandoned taxi.",
        "exits": {
            "north": "schermerhorn_st"
        },
        "items": [],
        "features": ["taxi_cab"],
        "dark": False,
        "cold": True
    },
    "atlantic_ave": {
        "id": "atlantic_ave",
        "name": "Atlantic Avenue",
        "description": "A longer avenue, more drifts. A stack of newspapers frozen to a bench. The wind howls between the buildings. A subway grate is set into the street.",
        "short_desc": "You're on Atlantic Avenue, wind howling and a frozen bench with newspapers.",
        "exits": {
            "west": "boerum_place",
            "north": "city_hall_steps"
        },
        "items": [],
        "features": ["frozen_bench", "subway_grate"],
        "dark": False,
        "cold": True
    },
    "city_hall_steps": {
        "id": "city_hall_steps",
        "name": "City Hall Steps",
        "description": "The steps of the old Brooklyn City Hall, now just rubble and snow. The building is a skeleton. To the east, Barclay Street continues.",
        "short_desc": "You're on the City Hall steps, rubble and snow everywhere.",
        "exits": {
            "south": "boerum_place",
            "west": "atlantic_ave",
            "east": "barclay_st"
        },
        "items": [],
        "features": [],
        "dark": False,
        "cold": True
    },
    "barclay_st": {
        "id": "barclay_st",
        "name": "Barclay Street",
        "description": "The end of Barclay Street, blocked by a fallen tree. Snow piles against the trunk. The silence is absolute.",
        "short_desc": "You're at the end of Barclay Street, blocked by a fallen tree.",
        "exits": {
            "west": "city_hall_steps"
        },
        "items": [],
        "features": [],
        "dark": False,
        "cold": True
    }
}

# Items
items = {
    "flashlight": {
        "id": "flashlight",
        "name": "flashlight",
        "description": "A heavy Maglite, half-dead. It flickers when you shake it.",
        "takeable": True,
        "use_with": {},
        "consumable": False,
        "light_source": True,
        "edible": False,
        "drinkable": False,
        "weapon": False,
        "synonyms": ["light", "torch"]
    },
    "subway_token": {
        "id": "subway_token",
        "name": "subway token",
        "description": "An old brass subway token from a city that no longer runs.",
        "takeable": True,
        "use_with": {},
        "consumable": False,
        "light_source": False,
        "edible": False,
        "drinkable": False,
        "weapon": False,
        "synonyms": ["token", "coin"]
    },
    "maintenance_key": {
        "id": "maintenance_key",
        "name": "maintenance key",
        "description": "A tagged key ring with a faded 'MTA MAINT' label.",
        "takeable": True,
        "use_with": {
            "control_room_door": "unlock"
        },
        "consumable": False,
        "light_source": False,
        "edible": False,
        "drinkable": False,
        "weapon": False,
        "synonyms": ["key", "keys"]
    },
    "emergency_flares": {
        "id": "emergency_flares",
        "name": "emergency flares",
        "description": "Three road flares in a weathered metal box.",
        "takeable": True,
        "use_with": {},
        "consumable": True,
        "light_source": True,
        "edible": False,
        "drinkable": False,
        "weapon": False,
        "synonyms": ["flares", "box"]
    },
    "panel_key": {
        "id": "panel_key",
        "name": "panel key",
        "description": "A tiny brass key with an electrical union stamp. It's warm to the touch.",
        "takeable": True,
        "use_with": {
            "broken_panel": "unlock"
        },
        "consumable": False,
        "light_source": False,
        "edible": False,
        "drinkable": False,
        "weapon": False,
        "synonyms": ["key", "tiny key", "brass key"]
    },
    "fuel_cell": {
        "id": "fuel_cell",
        "name": "fuel cell",
        "description": "A heavy steel cylinder with radiation stickers. The gauge reads 73%.",
        "takeable": True,
        "use_with": {
            "generator": "restore_power"
        },
        "consumable": True,
        "light_source": False,
        "edible": False,
        "drinkable": False,
        "weapon": False,
        "synonyms": ["cell", "nuclear cell", "steel cylinder"]
    }
}

# Items
items = {
    "flashlight": {
        "id": "flashlight",
        "name": "flashlight",
        "description": "A heavy Maglite, half-dead. It flickers when you shake it.",
        "takeable": True,
        "use_with": {},
        "consumable": False,
        "light_source": True,
        "edible": False,
        "drinkable": False,
        "weapon": False,
        "synonyms": ["light", "torch"]
    },
    "subway_token": {
        "id": "subway_token",
        "name": "subway token",
        "description": "An old brass subway token from a city that no longer runs.",
        "takeable": True,
        "use_with": {},
        "consumable": False,
        "light_source": False,
        "edible": False,
        "drinkable": False,
        "weapon": False,
        "synonyms": ["token", "coin"]
    },
    "maintenance_key": {
        "id": "maintenance_key",
        "name": "maintenance key",
        "description": "A tagged key ring with a faded 'MTA MAINT' label.",
        "takeable": True,
        "use_with": {
            "control_room_door": "unlock"
        },
        "consumable": False,
        "light_source": False,
        "edible": False,
        "drinkable": False,
        "weapon": False,
        "synonyms": ["key", "keys"]
    },
    "emergency_flares": {
        "id": "emergency_flares",
        "name": "emergency flares",
        "description": "Three road flares in a weathered metal box.",
        "takeable": True,
        "use_with": {},
        "consumable": True,
        "light_source": True,
        "edible": False,
        "drinkable": False,
        "weapon": False,
        "synonyms": ["flares", "box"]
    },
    "panel_key": {
        "id": "panel_key",
        "name": "panel key",
        "description": "A tiny brass key with an electrical union stamp. It's warm to the touch.",
        "takeable": True,
        "use_with": {
            "broken_panel": "unlock"
        },
        "consumable": False,
        "light_source": False,
        "edible": False,
        "drinkable": False,
        "weapon": False,
        "synonyms": ["key", "tiny key", "brass key"]
    },
    "fuel_cell": {
        "id": "fuel_cell",
        "name": "fuel cell",
        "description": "A heavy steel cylinder with radiation stickers. The gauge reads 73%.",
        "takeable": True,
        "use_with": {
            "generator": "restore_power"
        },
        "consumable": True,
        "light_source": False,
        "edible": False,
        "drinkable": False,
        "weapon": False,
        "synonyms": ["cell", "nuclear cell", "steel cylinder"]
    },
    "winter_coat": {
        "id": "winter_coat",
        "name": "winter coat",
        "description": "A faded parka with a fur-lined hood. The zipper is stuck but the buttons work.",
        "takeable": True,
        "use_with": {},
        "consumable": False,
        "light_source": False,
        "edible": False,
        "drinkable": False,
        "weapon": False,
        "auto_wear": True,
        "synonyms": ["parka", "coat"]
    }
}

# Features
features = {
    "control_room_door": {
        "id": "control_room_door",
        "name": "maintenance door",
        "description": "A heavy door marked 'MAINTENANCE' blocks the path north. It's locked tight.",
        "takeable": False,
        "use_with": {
            "maintenance_key": "unlock"
        },
        "synonyms": ["door", "maintenance door", "north door"]
    },
    "rusted_turnstile": {
        "id": "rusted_turnstile",
        "name": "rusted turnstile",
        "description": "A rusted turnstile blocks the path, frozen in place by years of neglect.",
        "takeable": False,
        "use_with": {},
        "synonyms": ["turnstile", "gate"]
    },
    "mta_map": {
        "id": "mta_map",
        "name": "MTA map",
        "description": "An old MTA subway map, its colors faded by time and moisture.",
        "text": "A, C, E lines run north-south. The 1, 2, 3 run cross-town. None of it matters now. The maintenance key fits the fusebox on the main concourse.",
        "takeable": False,
        "use_with": {},
        "synonyms": ["map", "subway map"]
    },
    "broken_panel": {
        "id": "broken_panel",
        "name": "broken panel",
        "description": "An old fusebox panel, its face rusted shut. There's a tiny keyhole at the bottom.",
        "text": "The wiring inside is scorched. You'll need a fuel cell to restore power.",
        "takeable": False,
        "use_with": {
            "panel_key": "unlock"
        },
        "synonyms": ["panel", "fusebox", "fusebox panel"]
    },
    "generator": {
        "id": "generator",
        "name": "generator",
        "description": "A massive diesel generator, cold and silent. The fuel cell slot gapes open.",
        "text": "The generator hums steadily. The fuel gauge reads 73%.",
        "takeable": False,
        "use_with": {
            "fuel_cell": "restore_power"
        },
        "synonyms": ["backup generator", "diesel generator"]
    },
    "traffic_light": {
        "id": "traffic_light",
        "name": "traffic light",
        "description": "A traffic light still swings in the wind, creaking on its rusted pole. It's frozen in place, pointing north.",
        "takeable": False,
        "use_with": {},
        "synonyms": ["light", "traffic signal"]
    },
    "frozen_bench": {
        "id": "frozen_bench",
        "name": "frozen bench",
        "description": "A bench with newspapers frozen to it. The stack is thick with time.",
        "takeable": False,
        "use_with": {},
        "synonyms": ["bench"]
    },
    "taxi_cab": {
        "id": "taxi_cab",
        "name": "taxi cab",
        "description": "An old yellow taxi with keys in the ignition. The engine is dead, frozen solid.",
        "takeable": False,
        "use_with": {},
        "synonyms": ["taxi", "cab", "car"]
    },
    "subway_grate": {
        "id": "subway_grate",
        "name": "subway grate",
        "description": "FROZEN SHUT. The grate is locked from below. The rail tunnels go somewhere, but you can't get in from here.",
        "text": "FROZEN SHUT. The grate is locked from below. The rail tunnels go somewhere, but you can't get in from here.",
        "takeable": False,
        "use_with": {},
        "synonyms": ["grate", "subway entrance"]
    }
}