# https://chatgpt.com/
# write a python game like zork with 6 rooms, goblins, swords and one dragon

# Text Adventure Game: Dragon’s Lair
# A small Zork-like adventure by ChatGPT

import sys

# --- Game setup ---
rooms = {
    "Entrance": {
        "desc": "You stand at the entrance of a dark cave. Paths lead east and south.",
        "east": "Hallway",
        "south": "Armory",
    },
    "Hallway": {
        "desc": "A narrow hallway with mossy walls. You hear faint growls to the east.",
        "west": "Entrance",
        "east": "Goblin Room",
    },
    "Goblin Room": {
        "desc": "Two goblins guard a door to the north. They look angry!",
        "west": "Hallway",
        "north": "Dragon Lair",
        "enemy": "goblins",
    },
    "Armory": {
        "desc": "An old armory with broken shields. A shiny sword rests on a rack.",
        "north": "Entrance",
        "item": "sword",
    },
    "Dragon Lair": {
        "desc": "The lair of the mighty dragon! Treasure glitters behind it.",
        "south": "Goblin Room",
        "enemy": "dragon",
    },
    "Treasure Room": {
        "desc": "A golden chamber filled with treasure. You’ve won!",
    },
}

inventory = []
current_room = "Entrance"
game_over = False

# --- Helper functions ---
def show_status():
    print(f"\nYou are in the {current_room}.")
    print(rooms[current_room]["desc"])
    print("Inventory:", inventory)

def move(direction):
    global current_room
    if direction in rooms[current_room]:
        next_room = rooms[current_room][direction]
        current_room = next_room
        print(f"\nYou move {direction} to the {current_room}.")
    else:
        print("You can't go that way!")

def take_item():
    if "item" in rooms[current_room]:
        item = rooms[current_room]["item"]
        print(f"You take the {item}.")
        inventory.append(item)
        del rooms[current_room]["item"]
    else:
        print("There’s nothing to take here.")

def fight(enemy):
    global game_over, current_room
    if enemy == "goblins":
        if "sword" in inventory:
            print("You swing your sword and defeat the goblins!")
            del rooms[current_room]["enemy"]
        else:
            print("The goblins overpower you. You are defeated.")
            game_over = True
    elif enemy == "dragon":
        if "sword" in inventory:
            print("With a mighty strike, you slay the dragon!")
            del rooms[current_room]["enemy"]
            current_room = "Treasure Room"
            print("\nYou step into the Treasure Room. Gold and jewels glitter everywhere.")
            print("You are victorious!")
            game_over = True
        else:
            print("The dragon breathes fire! You are burned to ashes.")
            game_over = True

# --- Game loop ---
print("\nWelcome to Dragon’s Lair — a mini text adventure!")
print("Commands: go [direction], take, attack, quit")

while not game_over:
    show_status()
    command = input("\n> ").lower().strip()

    if command.startswith("go "):
        move(command.split()[1])
    elif command == "take":
        take_item()
    elif command == "attack":
        if "enemy" in rooms[current_room]:
            fight(rooms[current_room]["enemy"])
        else:
            print("There’s nothing to attack here.")
    elif command == "quit":
        print("You leave the cave. Goodbye!")
        sys.exit()
    else:
        print("I don’t understand that command.")

if game_over:
    print("\n--- GAME OVER ---")
