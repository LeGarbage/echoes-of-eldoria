class Enemy:
    def __init__(self, name, description, health, attack):
        """
        Initialize an enemy with a name, description, health, and attack power.
        
        Args:
            name (str): The name of the enemy.
            description (str): A brief description of the enemy.
            health (int): The health of the enemy.
            attack (int): The attack power of the enemy.
        """
        self.name = name
        self.description = description
        self.health = health
        self.attack = attack

# Create specific enemy instances
spectral_warrior = Enemy(
    name="Spectral Warrior",
    description="A ghostly figure of a long-lost warrior, wielding an ethereal sword.",
    health=50,
    attack=15
)

shadow_guardian = Enemy(
    name="Shadow Guardian",
    description="A dark, shadowy creature summoned to protect the Oracle.",
    health=40,
    attack=12
)

mist_stalker = Enemy(
    name="Mist Stalker",
    description="A creature formed from the mist itself, with a haunting gaze.",
    health=30,
    attack=10
)

radiant_guard = Enemy("Radiant Guard", "A heavily armored soldier of the Radiant Order, tasked with guarding their stronghold.", 120, 15)
betrayed_scholar = Enemy("Betrayed Scholar", "A former ally of Lira, now serving the Radiant Order. They guide you to a trap.", 100, 10)
lira = Enemy("Lira", "The exiled Keeper of Knowledge, once a trusted figure in the City of Everlight. She holds part of the Shard of Dawn.", 200, 25)

shadow_guard = Enemy("Shadow Guard", "A dark figure, draped in shadows and wielding a cursed sword. They protect the corrupted Shard fragment.", 130, 18)
veiled_priest = Enemy("Veiled Priest", "A follower of the Veiled Ones, they channel dark energies and have a mysterious, unsettling aura.", 110, 14)
corrupted_veiled_one = Enemy("Corrupted Veiled One", "A former leader of the Veiled Ones, now fully corrupted by the dark power of the Shard fragment.", 180, 20)

thornbeast = Enemy("Thornbeast", "A hulking, plant-like creature with thorns covering its body, it defends the Elderwood fiercely.", 150, 20)
elderwood_guardian = Enemy("Elderwood Guardian", "A powerful, ancient guardian of the Elderwood, bound to protect the Shard.", 200, 25)

rune_warden = Enemy("Rune Warden", "A guardian formed from the runes that protect the Pinnacle. It wields the power of the Cataclysm.", 250, 40)
ice_wraith = Enemy("Ice Wraith", "A chilling wraith that haunts the mountain, frozen by the ancient magic of the Fractured Pinnacle.", 180, 25)
cataclysmic_sentinel = Enemy("Cataclysmic Sentinel", "A hulking construct of stone and energy, powered by the remnants of the Cataclysm.", 300, 45)
fractured_hound = Enemy("Fractured Hound", "A twisted, monstrous creature made of fractured stone and shadows, roaming the icy peaks.", 220, 30)
warden_of_pinnacle = Enemy("Warden of the Pinnacle", "The final guardian of the Shard, a powerful being forged from the Cataclysm itself, with unmatched strength.", 500, 60)