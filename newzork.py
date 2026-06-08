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
            elif verb in ["quit", "exit"]:
                quit_command(args)
            else:
                print(f"{RED}You can't do that here. Try: look, quit.{RESET}")
                
        except KeyboardInterrupt:
            print(f"\n{WHITE}The darkness closes in...{RESET}")
            sys.exit(0)
        except EOFError:
            print(f"\n{WHITE}The darkness closes in...{RESET}")
            sys.exit(0)

if __name__ == "__main__":
    main()