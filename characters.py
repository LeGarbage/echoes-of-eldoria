# characters.py
import copy

class CharacterClass:
    def __init__(self, name, strength, agility, magic, health, description):
        self.name = name
        self.strength = strength
        self.agility = agility
        self.magic = magic
        self.health = health  # Health attribute for each class
        self.description = description

    def display_stats(self):
        print(f"\nClass: {self.name}")
        print(f"Strength: {self.strength}")
        print(f"Agility: {self.agility}")
        print(f"Magic: {self.magic}")
        print(f"Health: {self.health}")
        print(f"Description: {self.description}")

# Define each class with specific stats, including health
knight = CharacterClass(
    name="Knight",
    strength=8,
    agility=2,
    magic=2,
    health=100,  # Knight has high health
    description="A heavily armored warrior with high defense and melee prowess."
)

mage = CharacterClass(
    name="Mage",
    strength=2,
    agility=4,
    magic=10,
    health=60,  # Mage has lower health
    description="A master of elemental magic, powerful in spells but physically vulnerable."
)

rogue = CharacterClass(
    name="Rogue",
    strength=5,
    agility=9,
    magic=3,
    health=80,  # Rogue has moderate health
    description="A stealthy and agile fighter, skilled in critical strikes and evasion."
)

druid = CharacterClass(
    name="Druid",
    strength=4,
    agility=5,
    magic=7,
    health=90,  # Druid has moderate health
    description="A nature-based caster with healing spells and the ability to summon creatures."
)

# Store classes in a dictionary for easy selection
classes = {
    "1": knight,
    "2": mage,
    "3": rogue,
    "4": druid
}

def choose_class():
    print("Choose your character class:")
    for key, character_class in classes.items():
        print(f"{key}. {character_class.name}")

    choice = input("Enter the number of your chosen class: ")

    if choice in classes:
        selected_class = classes[choice]
        print("\nYou have chosen the following class:")
        selected_class.display_stats()
        return copy.deepcopy(selected_class)  # Return a copy of the class
    else:
        print("Invalid choice. Please try again.")
        return choose_class()