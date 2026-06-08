"""
World data for NewZork M1 - The Concourse

This module contains the room and item definitions for the first milestone
of the NewZork text adventure game.
"""

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
        "features": ["control_room_door"],
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
        "items": ["emergency_flares"],
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
        "items": [],
        "features": ["rusted_turnstile", "mta_map"],
        "dark": True,
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
        "takeable": False,
        "use_with": {},
        "synonyms": ["map", "subway map"]
    }
}