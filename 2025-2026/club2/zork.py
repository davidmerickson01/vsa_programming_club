#!/usr/bin/env python3
"""
lotr_adventure.py — A tiny Lord of the Rings–themed text adventure.
No classes, simple procedural style.
Goal: Recover the One Ring and bring it back to the Shire.
"""

import sys

# -----------------------------
# World setup
# -----------------------------

rooms = {
    "shire": {
        "name": "The Shire",
        "desc": "You stand in the peaceful fields of the Shire. Smoke rises from Hobbiton to the west. "
                "A path leads east toward the wild lands.",
        "exits": {"east": "old_road"},
        "items": [],
        "enemy": None
    },
    "old_road": {
        "name": "The Old Road",
        "desc": "A winding dirt path bordered by ancient trees. The air feels uneasy. Paths lead west and east.",
        "exits": {"west": "shire", "east": "orc_camp"},
        "items": ["elven dagger"],
        "enemy": None
    },
    "orc_camp": {
        "name": "Orc Camp",
        "desc": "A foul stench fills the air. A snarling orc stands guard before a dark cave to the east.",
        "exits": {"west": "old_road", "east": "mordor_gate"},
        "items": [],
        "enemy": {"name": "orc", "hp": 10, "attack": 3, "alive": True}
    },
    "mordor_gate": {
        "name": "Gate of Mordor",
        "desc": "The black gates loom high. Amid ashes and bones lies a small golden ring, gleaming faintly.",
        "exits": {"west": "orc_camp"},
        "items": ["the one ring"],
        "enemy": None
    }
}

# -----------------------------
# Player state
# -----------------------------

location = "shire"
inventory = []
hp = 15
base_attack = 2

# -----------------------------
# Helper functions
# -----------------------------

def describe():
    r = rooms[location]
    print(f"\n== {r['name']} ==\n{r['desc']}")
    if r["items"]:
        print("You see:", ", ".join(r["items"]))
    if r["enemy"] and r["enemy"]["alive"]:
        e = r["enemy"]
        print(f"An {e['name']} is here! (HP: {e['hp']})")
    print("Exits:", ", ".join(r["exits"].keys()))

def move(direction):
    global location
    r = rooms[location]
    if direction in r["exits"]:
        location = r["exits"][direction]
        describe()
    else:
        print("You can't go that way.")

def take(item):
    r = rooms[location]
    if item in r["items"]:
        inventory.append(item)
        r["items"].remove(item)
        print(f"You take {item}.")
    else:
        print("You don't see that here.")

def drop(item):
    if item in inventory:
        rooms[location]["items"].append(item)
        inventory.remove(item)
        print(f"You drop {item}.")
    else:
        print("You don't have that.")

def show_inventory():
    if not inventory:
        print("You carry nothing.")
    else:
        print("You carry:", ", ".join(inventory))

def attack(target):
    global hp
    r = rooms[location]
    enemy = r["enemy"]
    if not enemy or not enemy["alive"]:
        print("There's nothing to attack here.")
        return
    if enemy["name"] != target:
        print("You don't see that here.")
        return
    # compute damage
    weapon_bonus = 3 if "elven dagger" in inventory else 0
    dmg = base_attack + weapon_bonus
    enemy["hp"] -= dmg
    print(f"You strike the {enemy['name']} for {dmg} damage!")
    if enemy["hp"] <= 0:
        enemy["alive"] = False
        print(f"You have defeated the {enemy['name']}! The path east is now safe.")
        return
    # enemy attacks back
    hp -= enemy["attack"]
    print(f"The {enemy['name']} strikes you for {enemy['attack']} damage! (HP: {hp})")
    if hp <= 0:
        print("You fall in battle. Middle-earth is doomed...")
        sys.exit(0)

def help_text():
    print("""
Commands:
  north, south, east, west - move
  look                     - look around
  take <item>              - pick up item
  drop <item>              - drop item
  inventory (or i)         - show what you carry
  attack <enemy>           - attack creature
  help                     - show this text
  quit                     - end game
""")

# -----------------------------
# Game loop
# -----------------------------

print("Welcome to The Lord of the Rings: A Tiny Adventure!")
print("Your quest: Recover the One Ring and return it safely to the Shire.\n")
describe()

while True:
    cmd = input("\n> ").strip().lower()
    if not cmd:
        continue
    words = cmd.split()
    verb = words[0]
    obj = " ".join(words[1:]) if len(words) > 1 else ""

    if verb in ("north", "south", "east", "west"):
        move(verb)
    elif verb == "look":
        describe()
    elif verb == "take":
        take(obj)
    elif verb == "drop":
        drop(obj)
    elif verb in ("inventory", "i"):
        show_inventory()
    elif verb == "attack":
        attack(obj)
    elif verb == "help":
        help_text()
    elif verb in ("quit", "exit"):
        print("Farewell, traveler of Middle-earth.")
        break
    else:
        print("That command has no meaning in this age.")

    # Win condition: return ring to the Shire
    if location == "shire" and "the one ring" in inventory:
        print("\nYou hold up the One Ring as the sun rises over the hills of the Shire.")
        print("Your quest is complete. Middle-earth is safe — for now.")
        break
