class Inventory:
    def __init__(self):
        """Initialize the inventory with an empty list."""
        self.items = []
        self.equipped_armor = {}  # To store the armor currently equipped
        self.equipped_weapon = {}  # To store the weapon currently equipped

    def view_inventory(self):
        """Display all items in the inventory."""
        if not self.items:
            print("Your inventory is empty.")
        else:
            print("Your inventory contains:")
            for idx, item in enumerate(self.items, start=1):
                print(f"{idx}. {item['name']} (x{item['quantity']}) - Type: {item['type']}")
                if item['type'] == 'Weapon':
                    print(f"   Attack: {item['damage']}")
                elif item['type'] == 'Armor':
                    print(f"   Defense: {item['defense']}")
                elif item['type'] == 'Potion':
                    print(f"   Level: {item['level']}")

    def add_item(self, item_name, item_type, quantity=1, damage=0, defense=0, level=1):
        """Add an item to the inventory, or increase its quantity if it exists."""
        for item in self.items:
            if item['name'] == item_name and item['damage'] == damage and item['defense'] == defense and item['level'] == level:
                item['quantity'] += quantity
                print(f"{item_name} quantity increased by {quantity}.")
                return

        # If the item doesn't exist, create a new one
        self.items.append({'name': item_name, 'type': item_type, 'quantity': quantity, 'damage': damage, 'defense': defense, 'level': level})
        print(f"{item_name} added to the inventory.")

    def remove_item(self, item_name, quantity=1):
        """Remove a certain quantity of an item from the inventory."""
        for item in self.items:
            if item['name'] == item_name:
                if item['quantity'] >= quantity:
                    item['quantity'] -= quantity
                    print(f"{quantity} of {item_name} removed from your inventory.")
                    if item['quantity'] == 0:
                        self.items.remove(item)  # Remove the item completely if quantity is 0
                    return
                else:
                    print(f"Not enough {item_name} to remove. You only have {item['quantity']} left.")
                    return

        print(f"{item_name} not found in your inventory.")

    def use_item(self, item_name):
        """Use an item from the inventory. Different behavior depending on item type."""
        for item in self.items:
            if item['name'] == item_name:
                if item['quantity'] > 0:
                    if item['type'] == 'Potion':
                        potion_effect = self.use_potion(item)
                        self.remove_item(item_name, 1)  # Remove one potion after use
                        return potion_effect
                    elif item['type'] == 'Weapon':
                        self.equipped_weapon = item  # Equip the weapon
                        print(f"You equip the {item_name}, preparing to attack!")
                        self.remove_item(item_name, 1)  # Remove weapon after use (equip)
                        return
                    elif item['type'] == 'Armor':
                        self.equipped_armor = item  # Equip the armor
                        print(f"You equip the {item_name}, increasing your defense!")
                        self.remove_item(item_name, 1)  # Remove the armor from inventory
                        return
                    else:
                        print(f"You use the {item_name}.")
                        self.remove_item(item_name, 1)
                        return
                else:
                    print(f"You don't have any {item_name} left to use.")
                    return

        print(f"{item_name} not found in your inventory.")


    def use_potion(self, potion):
        """Use a potion from the inventory and return the potion and its effect value."""
        if potion['type'] == 'Potion':
            if potion['name'] == 'Healing Potion':
                healing_amount = potion['level'] * 10  # Healing increases with level
                print(f"You drink a {potion['name']} and restore {healing_amount} health!")
                return [potion['name'], healing_amount]
            elif potion['name'] == 'Mana Potion':
                mana_restore = potion['level'] * 5  # Mana restored increases with level
                print(f"You drink a {potion['name']} and restore {mana_restore} mana!")
                return [potion['name'], mana_restore]
            elif potion['name'] == 'Strength Potion':
                strength_boost = potion['level'] * 2  # Strength boost increases with level
                print(f"You drink a {potion['name']} and gain {strength_boost} strength!")
                return [potion['name'], strength_boost]
            else:
                print(f"You drink a {potion['name']}.")
                return [potion['name'], 0]
        else:
            print(f"{potion['name']} is not a potion.")
            return ['invalid', 0]
    def choose_item(self):
        """
        Display the inventory, prompt the player to select an item by number,
        and use the selected item. Returns the result from use_item.
        """
        self.view_inventory()  # Show inventory first

        # Check if there are items to choose from
        if not self.items:
            print("No items available to use.")
            return None

        try:
            choice = int(input("\nEnter the number of the item you want to use: "))

            # Validate the choice is within range
            if 1 <= choice <= len(self.items):
                selected_item = self.items[choice - 1]  # Get the selected item
                print(f"You selected {selected_item['name']}.")

                # Use the item and return the result
                return self.use_item(selected_item["name"])
            else:
                print("Invalid choice. Please choose a valid item number.")
                return self.choose_item()  # Recursively call if invalid choice
        except ValueError:
            print("Invalid input. Please enter a number.")
            return self.choose_item()  # Recursively call if input is not a number