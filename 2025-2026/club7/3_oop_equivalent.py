# object oriented program
class Creature:
    def __init__(self, name, st, hp):
        self.name = name
        self.strength = st
        self.hit_points = hp
    def print(self):
        print(self.name, self.strength, self.hit_points)

elf = Creature("Elf", 20, 10)
goblin = Creature("Goblin", 18, 12)
elf.print()
goblin.print()
