#!/usr/bin/env python3
"""
NewZork - A text adventure game set in a zombie-apocalyptic Manhattan, October 1999.

M1 - The Concourse: A minimal implementation with 4 rooms and basic commands.
"""

import sys
import world_data

# ANSI color codes
YELLOW = '\033[93m'
CYAN = '\033[96m'
WHITE = '\033[97m'
RED = '\033[91m'
RESET = '\033[0m'

# Game state
class GameState:
    def __init__(self):
        self.current_room = "main_concourse"
        self.inventory = []
        self.visited_rooms = set()
        self.door_unlocked = False  # Special state for the control room door

# Initialize game state
game_state = GameState()

def print_crawl():
    """Print the opening crawl."""
    print(f"{WHITE}══════════════════════════════════════════")
    print(f"  NEWZORK — October 1999")
    print(f"══════════════════════════════════════════{RESET}")
    print(f"{WHITE}The city fell three months ago. The dead")
    print(f"walk the frozen streets. You've barricaded")
    print(f"yourself in the old Transit Museum, but")
    print(f"supplies are running low...")
    print()

def describe_room(room_id):
    """Describe the current room."""
    room = world_data.rooms[room_id]
    
    # Print room name in yellow
    print(f"{YELLOW}[{room['name']}]{RESET}")
    
    # Print description (full or short based on visit)
    if room_id not in game_state.visited_rooms:
        print(f"{WHITE}{room['description']}{RESET}")
        game_state.visited_rooms.add(room_id)
    else:
        print(f"{WHITE}{room['short_desc']}{RESET}")
    
    # List visible items
    if room['items']:
        print(f"\nYou can see: ", end="")
        item_names = [world_data.items[item_id]['name'] for item_id in room['items']]
        print(f"{CYAN}" + ", ".join(item_names) + f"{RESET}")
    
    # List exits
    if room['exits']:
        exits = list(room['exits'].keys())
        print(f"\nExits: {YELLOW}" + ", ".join(exits) + f"{RESET}")
    
    print()

def look_command(args):
    """Handle the look command."""
    if not args:
        # Look at current room
        describe_room(game_state.current_room)
        return
    
    # Look at specific item
    item_name = " ".join(args).lower()
    
    # Check if item is in current room
    current_room = world_data.rooms[game_state.current_room]
    for item_id in current_room['items']:
        item = world_data.items[item_id]
        if item_name in [item['name']] + item.get('synonyms', []):
            print(f"{CYAN}{item['name'].capitalize()}{RESET}: {WHITE}{item['description']}{RESET}")
            return
    
    # Check if item is in inventory
    for item_id in game_state.inventory:
        item = world_data.items[item_id]
        if item_name in [item['name']] + item.get('synonyms', []):
            print(f"{CYAN}{item['name'].capitalize()}{RESET}: {WHITE}{item['description']}{RESET}")
            return
    
    # Check if item is a feature
    for feature_id in current_room['features']:
        feature = world_data.features[feature_id]
        if item_name in [feature['name']] + feature.get('synonyms', []):
            print(f"{CYAN}{feature['name'].capitalize()}{RESET}: {WHITE}{feature['description']}{RESET}")
            return
    
    print(f"{RED}You don't see that here.{RESET}")

def take_command(args):
    """Handle the take command."""
    if not args:
        print(f"{RED}Take what?{RESET}")
        return
    
    item_name = " ".join(args).lower()
    
    # Strip articles
    articles = ["a", "an", "the", "it"]
    words = item_name.split()
    if words and words[0] in articles:
        item_name = " ".join(words[1:])
    
    current_room = world_data.rooms[game_state.current_room]
    
    # Find the item in the room
    item_id = None
    for iid in current_room['items']:
        item = world_data.items[iid]
        if item_name in [item['name']] + item.get('synonyms', []):
            item_id = iid
            break
    
    if not item_id:
        print(f"{RED}You don't see that here.{RESET}")
        return
    
    item = world_data.items[item_id]
    
    if not item.get('takeable', False):
        print(f"{RED}You can't take that.{RESET}")
        return
    
    # Remove item from room and add to inventory
    current_room['items'].remove(item_id)
    game_state.inventory.append(item_id)
    
    print(f"{WHITE}Taken.{RESET}")


def inventory_command(args):
    """Handle the inventory command."""
    if not game_state.inventory:
        print(f"{WHITE}You're not carrying anything.{RESET}")
        return
    
    print(f"{WHITE}You're carrying:{RESET}")
    for item_id in game_state.inventory:
        item = world_data.items[item_id]
        print(f"  {CYAN}{item['name']}{RESET}")


def use_command(args):
    """Handle the use command."""
    if not args:
        print(f"{RED}Use what?{RESET}")
        return
    
    # Check if this is "use X on Y" format
    if "on" in args:
        on_index = args.index("on")
        if on_index == 0 or on_index == len(args) - 1:
            print(f"{RED}Use what on what?{RESET}")
            return
        item_name = " ".join(args[:on_index]).lower()
        target_name = " ".join(args[on_index + 1:]).lower()
    else:
        item_name = " ".join(args).lower()
        target_name = None
    
    # Strip articles
    articles = ["a", "an", "the", "it"]
    item_words = item_name.split()
    if item_words and item_words[0] in articles:
        item_name = " ".join(item_words[1:])
    
    if target_name:
        target_words = target_name.split()
        if target_words and target_words[0] in articles:
            target_name = " ".join(target_words[1:])
    
    # Find the item in inventory
    item_id = None
    for iid in game_state.inventory:
        item = world_data.items[iid]
        if item_name in [item['name']] + item.get('synonyms', []):
            item_id = iid
            break
    
    if not item_id:
        print(f"{RED}You don't have that.{RESET}")
        return
    
    item = world_data.items[item_id]
    
    # If no target specified, just try to use the item
    if not target_name:
        if item.get('use_with', {}):
            # Item has specific use cases, need a target
            print(f"{RED}Use {item['name']} on what?{RESET}")
        else:
            # Generic use
            print(f"{WHITE}You use the {item['name']}. Nothing happens.{RESET}")
        return
    
    # Find the target (could be item, feature, or exit)
    current_room = world_data.rooms[game_state.current_room]
    target_id = None
    
    # Check room items
    for iid in current_room['items']:
        target_item = world_data.items[iid]
        if target_name in [target_item['name']] + target_item.get('synonyms', []):
            target_id = iid
            break
    
    # Check room features
    if not target_id:
        for fid in current_room['features']:
            feature = world_data.features[fid]
            if target_name in [feature['name']] + feature.get('synonyms', []):
                target_id = fid
                break
    
    # Check if target is the special door
    if not target_id and target_name in ["door", "maintenance door", "north door"]:
        target_id = "control_room_door"
    
    if not target_id:
        print(f"{RED}You don't see that here.{RESET}")
        return
    
    # Check if item can be used with this target
    use_with = item.get('use_with', {})
    if target_id not in use_with:
        print(f"{RED}That doesn't work.{RESET}")
        return
    
    # Apply the effect
    effect = use_with[target_id]
    if target_id == "control_room_door" and effect == "unlock":
        if game_state.door_unlocked:
            print(f"{WHITE}The door is already unlocked.{RESET}")
        else:
            game_state.door_unlocked = True
            print(f"{WHITE}You unlock the maintenance door with the key.{RESET}")
    else:
        print(f"{WHITE}You use the {item['name']} on the {target_name}. Nothing happens.{RESET}")


def go_command(args):
    """Handle the go command."""
    if not args:
        print(f"{RED}Go where?{RESET}")
        return
    
    direction = args[0]
    
    # Handle direction aliases
    direction_aliases = {
        "n": "north",
        "s": "south",
        "e": "east",
        "w": "west",
        "u": "up",
        "d": "down"
    }
    direction = direction_aliases.get(direction, direction)
    
    current_room = world_data.rooms[game_state.current_room]
    
    # Check if exit exists
    if direction not in current_room['exits']:
        print(f"{RED}You can't go that way.{RESET}")
        return
    
    destination_id = current_room['exits'][direction]
    destination = world_data.rooms[destination_id]
    
    # Special rule: lower_platform is dark and requires light
    if destination_id == "lower_platform":
        has_light = False
        # Check if player has a light source
        for item_id in game_state.inventory:
            item = world_data.items[item_id]
            if item.get('light_source', False):
                has_light = True
                break
        
        if not has_light:
            print(f"{RED}It's too dark to go down there. You'd surely fall and break your neck.{RESET}")
            return
    
    # Special rule: control_room is locked and requires key
    if destination_id == "control_room" and not game_state.door_unlocked:
        print(f"{RED}The maintenance door is locked tight. You'll need a key.{RESET}")
        return
    
    # Move to the new room
    game_state.current_room = destination_id
    describe_room(destination_id)


def quit_command(args):
    """Handle the quit command."""
    print(f"{WHITE}The darkness closes in...{RESET}")
    sys.exit(0)

def main():
    """Main game loop."""
    print_crawl()
    describe_room(game_state.current_room)
    
    while True:
        try:
            command = input("> ").strip().lower()
            
            if not command:
                continue
            
            # Parse command
            parts = command.split()
            verb = parts[0]
            args = parts[1:] if len(parts) > 1 else []
            
            # Handle commands
            if verb in ["look", "l", "examine", "x"]:
                look_command(args)
            elif verb in ["go", "walk", "move"]:
                go_command(args)
            elif verb in ["n", "north", "s", "south", "e", "east", "w", "west", "u", "up", "d", "down"]:
                # Handle direction shortcuts
                go_command([verb])
            elif verb in ["take", "get", "grab", "pick"]:
                # Handle "pick up" as well
                if verb == "pick" and args and args[0] == "up":
                    take_command(args[1:])
                else:
                    take_command(args)
            elif verb in ["inventory", "i", "inv"]:
                inventory_command(args)
            elif verb in ["use", "activate", "apply"]:
                use_command(args)
            elif verb in ["quit", "exit"]:
                quit_command(args)
            else:
                print(f"{RED}You can't do that here. Try: look, go, take, use, inventory, quit.{RESET}")
                
        except KeyboardInterrupt:
            print(f"\n{WHITE}The darkness closes in...{RESET}")
            sys.exit(0)
        except EOFError:
            print(f"\n{WHITE}The darkness closes in...{RESET}")
            sys.exit(0)

if __name__ == "__main__":
    main()