import characters
from inventory import Inventory
import random
import enemies
import sys
from enemies import radiant_guard, betrayed_scholar, lira  # Import the enemy instances
from enemies import shadow_guard, veiled_priest, corrupted_veiled_one  # Importing the new enemies
from enemies import thornbeast, elderwood_guardian  # Importing the new enemies
from enemies import rune_warden, ice_wraith, cataclysmic_sentinel, fractured_hound, warden_of_pinnacle  # Importing the new enemies


def combat(enemy):
    # Display enemy name and description before combat begins
    print(f"\nYou are about to face {enemy.name}!")
    print(f"{enemy.description}\n")

    # Assume the player starts with a certain amount of mana
    player.mana = 30  # Starting mana pool for the player
    strength_boost = 0  # Holds additional strength from a strength potion
    strength_potion_turns = 0  # Tracks remaining turns for strength potion effect

    # Loop continues while both player and enemy are alive
    while player.health > 0 and enemy.health > 0:
        # Recalculate weapon and armor stats in case of equipment change
        weapon_damage = player_inventory.equipped_weapon.get("damage", 0)
        armor_defense = player_inventory.equipped_armor.get("defense", 0)
        
        print("\n--- Combat Menu ---")
        print("1. Attack")
        print("2. Magic")
        print("3. Use Item")
        print("4. Flee")
        print(f"Your Health: {player.health} | Your Mana: {player.mana}")
        print(f"Enemy Health: {enemy.health}")
        
        # Get player's choice
        choice = input("Choose an action: ")

        if choice == "1":  # Attack
            # Calculate player's attack damage based on strength, weapon damage, and any temporary boost
            player_damage = random.randint(5, 10) + ((player.strength + weapon_damage + strength_boost) * 2)
            print(f"You attack the enemy for {player_damage} damage!")
            enemy.health -= player_damage

        elif choice == "2":  # Magic
            # Define mana cost for casting a spell
            mana_cost = 10
            
            # Check if the player has enough mana to cast the spell
            if player.mana >= mana_cost:
                magic_damage = random.randint(10, 20) + (player.magic * 3)
                print(f"You cast a spell on the enemy for {magic_damage} damage!")
                enemy.health -= magic_damage
                player.mana -= mana_cost  # Deduct mana cost
                print(f"You used {mana_cost} mana. Remaining Mana: {player.mana}")
            else:
                print("Not enough mana to cast a spell.")
                continue

        elif choice == "3":  # Use Item
            # Get the result of using an item, even if none is available
            potion = player_inventory.choose_item()
            
            if potion is not None:
                potion_type, potion_strength = potion[0], potion[1]
                
                if potion_type == "Healing Potion":
                    # Apply health potion
                    player.health = min(player.health + potion_strength, 100)
                    print(f"You used a health potion and restored {potion_strength} health. Current Health: {player.health}")
                
                elif potion_type == "Mana Potion":
                    # Apply mana potion
                    player.mana = min(player.mana + potion_strength, 30)
                    print(f"You used a mana potion and restored {potion_strength} mana. Current Mana: {player.mana}")
                
                elif potion_type == "Strength Potion":
                    # Check if a strength potion effect is already active
                    if strength_potion_turns > 0:
                        print("A strength potion is already active! Wait for it to wear off before using another.")
                    else:
                        # Apply strength potion
                        strength_boost = potion_strength
                        strength_potion_turns = 2  # Strength boost lasts for 2 turns
                        print(f"You used a strength potion! Strength increased by {potion_strength} for 2 turns.")
            
            # Continue the loop after using an item or if no item is available
            continue  # This ensures the loop continues after using an item

        elif choice == "4":  # Flee
            print("You attempt to flee...")
            # Random chance to successfully flee based on agility
            if random.random() < (player.agility * 0.1):
                print("You successfully flee the battle!")
                return "fled"  # Return "fled" if the player successfully flees
            else:
                print("Failed to flee. The enemy attacks!")

        else:
            print("Invalid choice, please select a valid action.")
            continue  # Re-loop if invalid choice

        # Check if the enemy is defeated
        if enemy.health <= 0:
            print("You have defeated the enemy!")
            return "success"  # Return "success" if the player defeats the enemy

        # Enemy's turn to attack
        print("\nThe enemy attacks!")
        
        # Calculate dodge chance based on agility
        if random.random() < (player.agility * 0.05):
            print("You dodged the attack!")
        else:
            # Enemy damage calculation with armor defense applied
            enemy_damage = max(0, random.randint(5, 15) - armor_defense)
            print(f"The enemy deals {enemy_damage} damage to you.")
            player.health -= enemy_damage

        # Check if the player is defeated
        if player.health <= 0:
            print("You have been defeated...")
            game_over()  # Call game_over function if the player dies
            return "failed"  # You can also return "failed" if you want a specific outcome for death

        # Optional: Regenerate a small amount of mana each turn (e.g., 3 mana per turn)
        player.mana = min(player.mana + 3, 30)  # Cap mana at maximum pool (e.g., 30)
        print(f"\nMana regenerated by 3. Current Mana: {player.mana}")

        # Manage strength potion duration
        if strength_potion_turns > 0:
            strength_potion_turns -= 1
            if strength_potion_turns == 0:
                strength_boost = 0  # Reset strength boost when potion effect ends
                print("The effects of the strength potion have worn off.")

def choose_action(options):
    """
    Displays a list of options and asks the player to choose one.
    The last option is always to view the inventory.
    
    :param options: A list of strings with actions to display to the player.
    :param player_inventory: The player’s inventory object that has a view_inventory method.
    :return: The chosen option index.
    """
    # Ensure the inventory option is only added once
    if "View Inventory" not in options:
        options.append("View Inventory")
    
    # Display all options
    print("\nPlease choose an option:")
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")
    
    # Get player input
    try:
        choice = int(input("\nEnter the number of your choice: "))
        
        # Check if the choice is valid
        if 1 <= choice <= len(options):
            if choice == len(options):  # If the player chose 'View Inventory'
                player_inventory.view_inventory()  # Call the view_inventory method
                return choose_action(options[:-1])  # Restart action selection without adding "View Inventory"
            return choice  # Return the player's valid choice
        else:
            print("Invalid choice, please try again.")
            return choose_action(options)  # Recursively call if invalid choice
    except ValueError:
        print("Invalid input. Please enter a number.")
        return choose_action(options)  # Recursively call if input is not a number

def game_over():
    """
    Displays a game over message and exits the game.
    """
    print("\nGAME OVER")
    print("You have been defeated in your journey. Eldoria will remain in darkness without the Shard of Dawn.")
    print("Thank you for playing Echoes of Eldoria!")
    
    # Exit the game
    sys.exit()

def random_drop():
    """Randomly determines and returns a loot item with a name and level for potions."""
    drops = [
        {"type": "Weapon", "name": random.choice(["Shadowfang", "Frostbane", "Emberclaw", "Starfall Blade", "Dragon's Maw", "Thunderstrike", "Venom Edge", "Doomspike", "Inferno Fang", "Vortex Saber"]), "attack": random.randint(5, 10)},
        {"type": "Armor", "name": random.choice(["Ironhide Plate", "Shadow Cloak", "Dragon Scale Vest", "Aegis Shield", "Warden’s Armor", "Celestial Helm", "Ember Guard", "Phantom Mail", "Stoneforge Chestplate", "Mystic Robe"]), "defense": random.randint(3, 8)},
        {"type": "Potion", "name": random.choice(["Healing Potion", "Mana Potion", "Strength Potion"]), "level": random.randint(1, 5)}
    ]
    return random.choice(drops)

def welcome_message():
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("      WELCOME TO THE WORLD OF ELDORIA")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("\nA world shattered by ancient magic... Floating islands connected by enchanted bridges...")
    print("Once united, Eldoria now drifts in the void, each island holding secrets, dangers, and memories of a time long past.")
    print("\nYou are The Seeker, a mysterious figure with no memory, driven by an unexplainable pull toward the lost artifact known as the Shard of Dawn.")
    print("Legends say that this ancient relic holds the power to restore balance to Eldoria or plunge it into eternal darkness.")
    print("\nWill you be the one to reunite the fragments and heal this fractured world?")
    print("Or will your choices bring new chaos upon these lands?")
    print("\nYour journey begins now. Choose wisely, Seeker... for the fate of Eldoria lies in your hands.")
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("                Press Enter to Begin")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    # Wait for the player to press Enter before starting
    input("")

def intro_island_of_whispers():
    """Introduces the player to the first island and sets up their initial objective."""
    
    # Prompt to begin the adventure
    input("Press Enter to begin your adventure...\n")

    # Display the island's overview
    print("You find yourself standing at the edge of a mist-covered island, where shadows drift like phantoms, "
          "and the air is thick with whispers that seem to come from nowhere and everywhere at once.")
    
    print("\nThis is the Island of Whispers—a land veiled in mystery, haunted by voices of those who may no longer "
          "exist, or perhaps, never did.")
    
    # Introduce The Oracle
    print("\nOut of the mist, a figure appears: an ethereal being cloaked in faint, blue light. Her presence is "
          "unsettling yet calming, as if she exists beyond fear. She calls herself The Oracle.")
    
    print("\nThe Oracle: \"Seeker, you are drawn here by fate, though it may feel like choice. The first shard "
          "you seek lies hidden on this island. But beware—its power is tainted, and it can twist the minds of those "
          "unprepared to bear its burden.\"")
    
    print("\nThe Oracle: \"The voices you hear are echoes of those who came before. Listen carefully, for they may "
          "guide you—or deceive you. Not all here wish you well.\"")
    
    # Objective overview
    print("\nYour objective is clear: seek out the first fragment of the Shard of Dawn hidden on the Island of Whispers. "
          "But tread carefully, for the island's secrets may test your resolve and reveal truths you are not yet "
          "prepared to face.")
    
    # Warning message about fragment corruption
    print("\nThe Oracle: \"Once you find the fragment, resist the urge to embrace its power completely. Not all shards "
          "remain pure, and some may try to corrupt your very soul.\"")
    
    print("\nThe Oracle slowly fades back into the mist, leaving you with an uneasy sense of purpose, and an unspoken "
          "warning lingering in the air.")
    
    # Prompt to continue
    input("\nPress Enter to continue...")

def island_of_whispers():
    print("You enter the misty Island of Whispers. Strange apparitions flicker in the distance, and faint whispers seem to call your name.")
    
    while True:
        print("\nYou come to a fork in the path. The whispers grow louder.")
        choice1 = choose_action([
            "Follow the whispers down the left path.",
            "Take the quieter right path.",
            "Turn back to explore a different part of the island."
        ])
        
        if choice1 == 1:
            # Left path encounter
            print("\nYou follow the whispers, feeling an eerie chill. A ghostly figure materializes before you—a specter of a long-lost warrior.")
            encounter = choose_action([
                "Confront the specter.",
                "Attempt to communicate with it.",
                "Retreat quietly."
            ])
            
            if encounter == 1:
                # Combat with Spectral Warrior
                print("The specter raises an ethereal sword, challenging you to combat.")
                outcome = combat(enemies.spectral_warrior)  # Pass the Enemy instance
                
                if outcome == "success":
                    drop = random_drop()
                    print(f"You have defeated the specter. It dissipates into the mist, leaving something behind: {drop['name']}")
                    # Add drop to the player's inventory with keyword arguments
                    player_inventory.add_item(item_name=drop['name'], item_type=drop['type'], 
                                               damage=drop.get('attack', None), defense=drop.get('defense', None), 
                                               level=drop.get('level', None))
                
                elif outcome == "fled":
                    print("You manage to flee, retreating to the path.")
                
            elif encounter == 2:
                # Communication attempt
                if random.choice([True, False]):
                    print("The specter whispers secrets about the Shard of Dawn. You feel a strange connection to it.")
                else:
                    print("The specter vanishes abruptly, leaving a chill in its wake.")
            
            else:
                print("You retreat to the path, the whispers fading behind you.")

        elif choice1 == 2:
            # Right path encounter
            print("\nThe right path is strangely silent. After some time, you encounter a peculiar figure—The Oracle.")
            oracle_encounter = choose_action([
                "Speak with The Oracle.",
                "Ignore her and continue down the path.",
                "Attempt to steal something from her."
            ])
            
            if oracle_encounter == 1:
                print("The Oracle gazes at you with piercing eyes. She speaks cryptically of a darkness encroaching and your fated role in Eldoria.")
                
                if random.choice([True, False]):
                    print("She reveals a clue: 'Beware the Shard's call; it may corrupt as easily as it heals.'")
                else:
                    print("She only mutters riddles, which leave you feeling uneasy.")
                    
            elif oracle_encounter == 2:
                print("You pass The Oracle, but feel as if her eyes follow you, even after she is out of sight.")
                
            else:
                # Attempt to steal
                print("As you try to take something from The Oracle, she vanishes into thin air, and a shadowy creature appears to defend her.")
                outcome = combat(enemies.shadow_guardian)  # Access Enemy instance
                
                if outcome == "success":
                    drop = random_drop()
                    print(f"You defeated the Shadow Guardian. It dissolves, leaving behind: {drop['name']}")
                    # Add drop to the player's inventory with keyword arguments
                    player_inventory.add_item(item_name=drop['name'], item_type=drop['type'], 
                                           damage=drop.get('attack', None), defense=drop.get('defense', None), 
                                           level=drop.get('level', None))
                
                elif outcome == "fled":
                    print("You manage to escape, though you feel a haunting presence watching you.")
        
        else:
            # Explore other parts of the island
            print("\nYou decide to explore a different part of the island, wandering through the thick mist.")
            random_event = random.choice(["item", "enemy", "nothing"])
            
            if random_event == "item":
                drop = random_drop()
                print(f"You stumble upon a hidden stash left by a previous traveler. You find: {drop['name']}")
                # Add drop to the player's inventory with keyword arguments
                player_inventory.add_item(item_name=drop['name'], item_type=drop['type'], 
                                           damage=drop.get('attack', None), defense=drop.get('defense', None), 
                                           level=drop.get('level', None))
                
            elif random_event == "enemy":
                print("Out of the mist, a shadowy creature appears, barring your way.")
                outcome = combat(enemies.mist_stalker)  # Access Enemy instance
                
                if outcome == "success":
                    drop = random_drop()
                    print(f"The Mist Stalker is defeated, leaving behind: {drop['name']}")
                    # Add drop to the player's inventory with keyword arguments
                    player_inventory.add_item(item_name=drop['name'], item_type=drop['type'], 
                                           damage=drop.get('attack', None), defense=drop.get('defense', None), 
                                           level=drop.get('level', None))
                
                elif outcome == "fled":
                    print("You flee back to the main path.")
                    
            else:
                print("You find nothing but swirling mist and faint echoes. It feels as if the island itself is watching you.")

        # Option to leave or continue exploring
        print("\nThe mist thickens around you. Do you wish to continue exploring the Island of Whispers?")
        continue_exploration = choose_action([
            "Continue exploring.",
            "Leave the island and continue your journey."
        ])
        
        if continue_exploration == 2:
            print("You decide to leave the Island of Whispers, the Oracle's words lingering in your mind as you return to your quest.")
            break

def city_of_everlight():
    # Introduce the city and Lira
    print("You arrive at the magnificent City of Everlight, floating high above the world, its structures glowing with radiant energy from the crystals that power it.")
    print("\nYou meet Lira, the exiled Keeper of Knowledge. Her eyes narrow as she assesses you.")
    print("Lira: 'I possess part of the Shard of Dawn, but I will not give it to just anyone. Help me recover a stolen relic, and I may assist you.'")
    print("Lira: 'A faction called the Radiant Order has taken it. They believe the relic will enhance their power.'")

    while True:
        print("\nYou are now faced with your first decision: How will you approach this mission?")
        choice1 = choose_action([
            "Agree to help Lira recover the relic.",
            "Refuse to help and leave the city.",
            "Attempt to steal the relic from Lira directly."
        ])
        
        if choice1 == 1:
            # Agree to help Lira
            print("\nLira nods, but there's a trace of doubt in her eyes. 'I will lead you to the Radiant Order's stronghold. Be prepared for their defenses.'")
            print("You begin your journey towards the stronghold of the Radiant Order.")
            
            stronghold_encounter = choose_action([
                "Infiltrate the stronghold under cover of night.",
                "Challenge the guards head-on at the entrance.",
                "Seek an ally inside the stronghold who may aid you."
            ])
            
            if stronghold_encounter == 1:
                # Stealth infiltration
                print("\nYou move quietly through the shadows, avoiding patrols as you make your way deeper into the stronghold.")
                outcome = combat(radiant_guard)
                
                if outcome == "success":
                    print("You locate the relic, guarded by powerful wards. With a quick move, you disable them and recover the item.")
                    drop = random_drop()
                    print(f"You successfully recover the relic, but it comes with a cost: {drop['name']}.")
                    player_inventory.add_item(item_name=drop['name'], item_type=drop['type'], 
                                               damage=drop.get('attack', None), defense=drop.get('defense', None), 
                                               level=drop.get('level', None))
                    lira_reaction = choose_action([
                        "Return the relic to Lira immediately.",
                        "Examine the relic's power before handing it over."
                    ])
                    
                    if lira_reaction == 1:
                        print("\nYou return the relic to Lira. She is pleased but cautious. 'You have done well. I will now aid you.'")
                    else:
                        print("\nThe relic's power surges as you hold it. Lira's distrust deepens. 'You should have given it to me right away.'")
                
                else:
                    print("The guards catch sight of you, and a brutal battle ensues.")
                    outcome = combat(radiant_guard)
                    if outcome == "success":
                        print("You defeat the guards, but the damage is done. The Radiant Order is now on high alert.")
                    else:
                        print("You barely escape the stronghold with your life, but the relic remains in their possession.")

            elif stronghold_encounter == 2:
                # Direct confrontation with the guards
                print("\nYou march boldly up to the gates and demand entry.")
                outcome = combat(radiant_guard)
                
                if outcome == "success":
                    print("After a fierce battle, you break through the gates, though you have drawn unwanted attention.")
                else:
                    print("The guards overpower you, and you are thrown into a prison cell.")
                    
            elif stronghold_encounter == 3:
                # Seek an ally inside
                print("\nYou approach a former acquaintance, an old scholar who now serves the Radiant Order.")
                ally_choice = choose_action([
                    "Ask for their help in retrieving the relic.",
                    "Attempt to bribe them for information."
                ])
                
                if ally_choice == 1:
                    print("\nThe scholar agrees to help, though reluctantly. They guide you through secret passages inside the stronghold.")
                    outcome = combat(betrayed_scholar)
                    
                    if outcome == "success":
                        drop = random_drop()
                        print(f"You successfully recover the relic with their help, and they even provide you with a valuable item: {drop['name']}.")
                        player_inventory.add_item(item_name=drop['name'], item_type=drop['type'], 
                                                   damage=drop.get('attack', None), defense=drop.get('defense', None), 
                                                   level=drop.get('level', None))
                    else:
                        print("The ally betrays you, and you are forced to flee without the relic.")
                
                else:
                    print("\nThe bribe is accepted, but the information you receive is misleading. You find yourself facing a trap.")

        elif choice1 == 2:
            # Refuse to help Lira
            print("\nLira scowls, and the atmosphere between you becomes tense. 'Very well. You have made your choice.'")
            print("You leave the city, but Lira's distrust weighs heavily on you. You will have to seek another way to achieve your goals.")
            break

        elif choice1 == 3:
            # Steal the relic from Lira
            print("\nYou attempt to steal the relic from Lira, but she catches you.")
            outcome = combat(lira)

            if outcome == "success":
                print("You defeat Lira, but the Shard of Dawn is lost. The city is filled with whispers of your betrayal.")
            else:
                print("Lira's wrath overwhelms you. You fall, defeated by her knowledge and power.")

        print("\nThe city is full of secrets, and your choices matter. Do you wish to continue exploring Everlight or leave?")
        continue_exploration = choose_action([
            "Continue exploring.",
            "Leave the city and continue your journey."
        ])
        
        if continue_exploration == 2:
            print("You leave the City of Everlight, unsure of what lies ahead, but feeling the weight of your actions.")
            break

def shadowed_vale():
    # Introduce the Vale and the player's quest
    print("You enter the Shadowed Vale, a desolate land where the sun rarely shines. The air is thick with dark energy, and the earth is tainted with shadows.")
    print("\nIn the distance, you see the Veiled Ones, a faction that believes the Cataclysm was a necessary purge. They harness the corrupted power of a Shard fragment.")
    print("The Veiled Ones use their power to spread shadows across Eldoria, and it is said that the Shard's corruption fuels their dark magic.")
    print("You must decide whether to steal the fragment, weakening the Veiled Ones but risking their wrath, or attempt to purify it—an act that could backfire terribly.")

    while True:
        # First choice: How to approach the situation
        choice1 = choose_action([
            "Attempt to steal the corrupted Shard fragment.",
            "Try to purify the Shard fragment.",
            "Seek out the Veiled Priest for guidance."
        ])
        
        if choice1 == 1:
            # Steal the corrupted Shard fragment
            print("\nYou decide to steal the corrupted Shard fragment. The Veiled Ones' eyes turn toward you with suspicion.")
            print("You rush toward the altar where the Shard is placed, but a dark figure steps forward to block your path.")
            outcome = combat(shadow_guard)
            
            if outcome == "success":
                print("You successfully steal the Shard fragment, but the shadows seem to stir angrily, as if aware of your theft.")
                drop = random_drop()
                print(f"The Shadow Guard drops something in the fight: {drop['name']}.")
                player_inventory.add_item(item_name=drop['name'], item_type=drop['type'], 
                                           damage=drop.get('attack', None), defense=drop.get('defense', None), 
                                           level=drop.get('level', None))
                
                # Now the Veiled Ones are enraged, so a choice arises:
                choice2 = choose_action([
                    "Flee the Vale with the Shard.",
                    "Fight the Corrupted Veiled One who emerges from the shadows."
                ])
                
                if choice2 == 1:
                    print("\nYou decide to flee, the Veiled Ones' wrath closing in as you escape with the Shard fragment.")
                    print("The darkness behind you churns, but you manage to make it to safety, though you know the Veiled Ones will not forget your actions.")
                else:
                    print("\nYou stand your ground and face the Corrupted Veiled One in battle.")
                    outcome = combat(corrupted_veiled_one)
                    if outcome == "success":
                        print("The Corrupted Veiled One falls, and the Shard fragment slips from their grasp. You have won, but at what cost?")
                    else:
                        print("The Corrupted Veiled One overwhelms you. The last thing you see is the dark power consuming you.")
            
        elif choice1 == 2:
            # Attempt to purify the Shard fragment
            print("\nYou choose to try to purify the Shard fragment. You call upon all your strength and knowledge.")
            print("As you touch the Shard, dark energy pulses through you, threatening to overwhelm your mind and body.")
            outcome = random.choice(["success", "failure"])
            
            if outcome == "success":
                print("\nThe Shard begins to glow with a soft, pure light, as if responding to your attempts to purify it.")
                print("The Veiled Ones look on in disbelief, but their anger begins to subside. The Shard fragment is now cleansed.")
                drop = random_drop()
                print(f"As the Shard purifies, it releases a powerful artifact: {drop['name']}.")
                player_inventory.add_item(item_name=drop['name'], item_type=drop['type'], 
                                           damage=drop.get('attack', None), defense=drop.get('defense', None), 
                                           level=drop.get('level', None))
            else:
                print("\nThe Shard resists your purification, and a wave of dark energy bursts forth, knocking you to the ground.")
                print("The Veiled Ones, enraged by your actions, begin to surround you.")
                outcome = combat(veiled_priest)
                if outcome == "success":
                    print("You manage to defeat the Veiled Priest and escape the Vale, but the Shard remains tainted, its dark energy lingering in the air.")
                else:
                    print("The Veiled Priest overpowers you, and darkness claims your soul.")

        elif choice1 == 3:
            # Seek out the Veiled Priest for guidance
            print("\nYou seek out the Veiled Priest, hoping for a peaceful resolution.")
            print("The Veiled Priest regards you with suspicion, but eventually agrees to speak.")
            priest_choice = choose_action([
                "Ask the Veiled Priest about purifying the Shard.",
                "Request the Veiled Priest's help in stealing the Shard.",
                "Challenge the Veiled Priest to a duel."
            ])
            
            if priest_choice == 1:
                print("\nThe Veiled Priest speaks cryptically: 'Purification is not a simple task. The Shard is not just dark—it is a test.'")
                outcome = random.choice(["success", "failure"])
                
                if outcome == "success":
                    print("The Veiled Priest provides you with some guidance, giving you a clue on how to purify the Shard.")
                else:
                    print("The Veiled Priest laughs darkly. 'You are not yet ready to handle the Shard's power.'")
            
            elif priest_choice == 2:
                print("\nThe Veiled Priest shakes their head. 'Stealing the Shard? You would invoke the wrath of our entire order.'")
                print("They then vanish into the shadows, leaving you with nothing but questions.")
            
            else:
                print("\nYou challenge the Veiled Priest, and a dark battle ensues.")
                outcome = combat(veiled_priest)
                if outcome == "success":
                    print("The Veiled Priest falls, and the Shard is left unguarded.")
                    drop = random_drop()
                    print(f"From the priest's fall, you recover: {drop['name']}.")
                    player_inventory.add_item(item_name=drop['name'], item_type=drop['type'], 
                                               damage=drop.get('attack', None), defense=drop.get('defense', None), 
                                               level=drop.get('level', None))
                else:
                    print("The Veiled Priest overwhelms you. Darkness envelops you as you fall.")

        # Decide to continue or leave the Vale
        print("\nThe Vale is full of darkness, and your choices will have consequences. Will you leave or continue?")
        continue_exploration = choose_action([
            "Continue exploring the Shadowed Vale.",
            "Leave the Vale and continue your journey."
        ])
        
        if continue_exploration == 2:
            print("You leave the Shadowed Vale, feeling the weight of your choices as you head toward an uncertain future.")
            break

def verdant_grove():
    # Introduce the Grove and the Elderwood
    print("You arrive at the Verdant Grove, a place of overwhelming beauty and tranquility. The air is filled with the scents of flowers and the sounds of mythical creatures.")
    print("In the heart of the Grove, you see the Elderwood, a towering, ancient tree. Its roots stretch deep into the earth, and its branches seem to touch the heavens.")
    print("\nThe Elderwood speaks in a deep, resonant voice, warning you: 'The Shard lies within my roots. If you take it, you will disturb the life force of Eldoria, and all will be at risk. Decide wisely.'")
    print("You must now choose your path—will you take the Shard, or leave it to protect Eldoria's balance?")

    while True:
        # First choice: How to approach the Elderwood
        choice1 = choose_action([
            "Take the Shard, regardless of the Elderwood's warning.",
            "Leave the Shard and respect the Elderwood’s wish to protect Eldoria.",
            "Speak further with the Elderwood to understand more of the consequences."
        ])

        if choice1 == 1:
            # Take the Shard despite the warning
            print("\nIgnoring the Elderwood’s warning, you reach into its roots and pull out the Shard.")
            print("The moment you touch it, a terrible surge of power pulses through you, and the air grows heavy. The balance of the Grove begins to shift, and creatures of the forest grow restless.")
            print("Suddenly, a massive roar echoes from the Grove, and a large, thorn-covered creature charges at you.")
            outcome = combat(thornbeast)
            
            if outcome == "success":
                drop = random_drop()
                print(f"The Thornbeast collapses, leaving behind: {drop['name']}.")
                player_inventory.add_item(item_name=drop['name'], item_type=drop['type'], 
                                           damage=drop.get('attack', None), defense=drop.get('defense', None), 
                                           level=drop.get('level', None))
                # Now the Elderwood Guardian appears
                print("\nThe Elderwood Guardian emerges, an enormous creature with bark-like armor and glowing green eyes. It will stop at nothing to protect the Shard.")
                outcome = combat(elderwood_guardian)
                if outcome == "success":
                    print("The Elderwood Guardian falls, but the Shard’s power begins to corrupt the land. The Grove withers around you.")
                else:
                    print("The Elderwood Guardian overpowers you. As darkness takes over, the Shard pulses ominously in your hand.")

        elif choice1 == 2:
            # Leave the Shard and respect the Elderwood
            print("\nYou decide to respect the Elderwood’s wishes and leave the Shard untouched.")
            print("The Elderwood nods approvingly, and the Grove seems to settle back into its peaceful state. The creatures of the Grove return to their natural harmony.")
            drop = random_drop()
            print(f"Grateful for your respect, the Elderwood grants you a boon: {drop['name']}.")
            player_inventory.add_item(item_name=drop['name'], item_type=drop['type'], 
                                       damage=drop.get('attack', None), defense=drop.get('defense', None), 
                                       level=drop.get('level', None))

        else:
            # Speak with the Elderwood to understand the consequences
            print("\nYou sit down at the base of the Elderwood and meditate, listening carefully to its words.")
            print("The Elderwood speaks of the balance of Eldoria, and how the Shard’s power can either heal or destroy the world depending on who wields it.")
            print("'If you take it, the land will suffer, but you may gain power beyond measure. If you leave it, the land will remain in harmony, but the Shard’s power will be forever contained.'")
            print("The Elderwood then warns you: 'But there is no telling who will come after you. The Shard calls to those who seek dominion.'")

            # Ask the player for more details on their choice
            choice2 = choose_action([
                "Ask the Elderwood what will happen if the Shard is taken.",
                "Ask if there is a way to use the Shard without destroying Eldoria.",
                "Thank the Elderwood and leave the Grove."
            ])

            if choice2 == 1:
                print("\nThe Elderwood warns that if the Shard is taken, it will disturb the life force of Eldoria, causing the land to become tainted and dark.")
                print("The consequences could be dire, but you may gain great power. However, the Grove itself will begin to fade, and its creatures will grow restless and hostile.")
            
            elif choice2 == 2:
                print("\nThe Elderwood says, 'There may be a way, but it requires great sacrifice. The Shard must be purified, or it will corrupt everything around it. But that may not be enough.'")
                print("The Elderwood's roots shift slightly, as if feeling the weight of your decision.")
            
            else:
                print("\nYou thank the Elderwood for its wisdom, and begin to leave the Grove, feeling the weight of your decision settle on you.")

        # Final choice to leave or stay
        print("\nThe Grove is still and quiet, the weight of your choices heavy on your mind. Do you wish to continue or leave?")
        continue_exploration = choose_action([
            "Continue exploring the Verdant Grove.",
            "Leave the Grove and continue your journey."
        ])
        
        if continue_exploration == 2:
            print("You leave the Verdant Grove, the Elderwood’s words lingering in your mind. The decision you’ve made will haunt you.")
            break

def fractured_pinnacle():
    print("You stand before the Fractured Pinnacle, a towering, jagged peak that seems to pierce the sky.")
    print("The mountain is surrounded by swirling winds and sharp cliffs, carved with glowing runes that pulse with an ancient power.")
    print("At the summit lies the final piece of the Shard, but the path is fraught with danger. You must climb the tower, facing both new and familiar foes.")
    print("As you ascend, your strength will be tested. The Warden waits at the top, and he knows the truth of your past...")

    # Random encounters during the ascent
    encounter_choices = [
        ice_wraith, cataclysmic_sentinel, fractured_hound, rune_warden
    ]
    
    floors = 5  # Number of floors before reaching the Warden
    current_floor = 1
    rest_used = False  # Flag to ensure the player can't rest more than once per floor

    while current_floor <= floors:
        print(f"\nYou ascend to floor {current_floor} of the Pinnacle.")
        
        # Resting and healing, but only once per floor
        choice1 = choose_action([
            "Continue climbing the tower.",
            "Search the area for supplies.",
            "Take a rest and regain strength."
        ])

        if choice1 == 1:
            # Random encounter while climbing
            print("\nYou continue climbing... but an enemy appears!")
            enemy = random.choice(encounter_choices)
            print(f"A {enemy.name} appears and blocks your path!")

            # Combat with the selected enemy
            outcome = combat(enemy)
            if outcome == "success":
                print(f"You defeated the {enemy.name} and continue your climb.")
                drop = random_drop()
                print(f"You find a health potion and {drop['name']}.")
                player_inventory.add_item(item_name="Healing Potion", item_type="Potion", level=1)
                player_inventory.add_item(item_name=drop['name'], item_type=drop['type'], 
                                           damage=drop.get('attack', None), defense=drop.get('defense', None), 
                                           level=drop.get('level', None))
                # Only increment the floor if the player fights and wins
                current_floor += 1  # Proceed to next floor after combat victory
            elif outcome == "fled":
                print(f"You manage to escape the {enemy.name}, but the climb is taking a toll on you.")
                # Floor doesn't increment if the player flees

        elif choice1 == 2:
            # Searching for supplies
            print("\nYou search the surrounding area, hoping to find more supplies to help you on your journey.")
            drop = random_drop()
            print(f"You find a stash of supplies: {drop['name']}.")
            player_inventory.add_item(item_name=drop['name'], item_type=drop['type'], 
                                       damage=drop.get('attack', None), defense=drop.get('defense', None), 
                                       level=drop.get('level', None))
            
            # Finding a potion
            if random.choice([True, False]):
                print("You find a health potion hidden beneath the rocks.")
                player_inventory.add_item(item_name="Healing Potion", item_type="Potion", level=1)
            else:
                print("You find only more broken shards and cold stone.")

        elif choice1 == 3:
            # Resting and regaining strength
            if rest_used:
                print("\nYou’ve already rested on this floor. Time to face your next challenge!")
            else:
                print("\nYou sit down to rest, hoping to regain some strength for the difficult climb ahead.")
                player.health = min(100, player.health + 50)  # Restores a portion of health (max 100)
                print(f"Your health is restored. You now have {player.health} health.")
                rest_used = True  # Prevent the player from resting again on this floor
        
    # Final stretch: Reaching the summit and facing the Warden
    print("\nThe summit is within sight. You prepare for the final confrontation.")
    choice2 = choose_action([
        "Climb to the top to face the Warden.",
        "Rest before the final climb."
    ])
    
    if choice2 == 1:
        # Final battle with the Warden
        print("\nYou reach the summit and find yourself face-to-face with the Warden.")
        print(f"The Warden, a being forged from the Cataclysm’s essence, stands before you. His presence is overwhelming.")
        print("The Warden speaks: 'You were once part of Eldoria’s ruling council. You helped create the Shard, and you were responsible for its shattering. Now you seek redemption. But redemption cannot come easily.'")
        
        outcome = combat(warden_of_pinnacle)

        if outcome == "success":
            print("\nWith a final, powerful strike, you defeat the Warden, claiming the last piece of the Shard.")
            print("As the Shard of Dawn reunites, you feel the weight of your past actions and the burden of your redemption lifted.")
            print("The world of Eldoria begins to heal, and the Cataclysm’s influence fades.")
        else:
            print("\nThe Warden overpowers you, and as you fall, the world around you crumbles. Your quest ends here, and the Shard remains shattered.")
    else:
        print("\nYou decide to rest before the final climb. No further rest is allowed before the Warden fight.")
        player.health = min(100, player.health + 50)  # Final health restoration
        rest_used = True  # This will prevent further resting
        print(f"Your health is restored to {player.health}. Prepare for the final climb!")
        # Proceed to final boss encounter
        outcome = combat(warden_of_pinnacle)

        if outcome == "success":
            print("\nWith a final, powerful strike, you defeat the Warden, claiming the last piece of the Shard.")
            print("As the Shard of Dawn reunites, you feel the weight of your past actions and the burden of your redemption lifted.")
            print("The world of Eldoria begins to heal, and the Cataclysm’s influence fades.")
        else:
            print("\nThe Warden overpowers you, and as you fall, the world around you crumbles. Your quest ends here, and the Shard remains shattered.")


# Run the welcome message
welcome_message()

# Run the character selection function from the imported module
player_class = characters.choose_class()  # Calls choose_class from characters module

player = player_class
player_inventory = Inventory()

intro_island_of_whispers()

island_of_whispers()

city_of_everlight()

shadowed_vale()

verdant_grove()

fractured_pinnacle()