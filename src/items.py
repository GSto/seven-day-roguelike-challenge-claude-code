"""
Item system - weapons, armor, potions, and other items.
"""

import random
from constants import COLOR_WHITE, COLOR_GREEN, COLOR_BLUE, COLOR_YELLOW, COLOR_RED


class Item:
    """Base class for all items."""
    
    def __init__(self, x, y, name, char, color, description=""):
        """Initialize an item."""
        self.x = x
        self.y = y
        self.name = name
        self.char = char
        self.color = color
        self.description = description
    
    def render(self, console, fov):
        """Render the item on the console."""
        if fov[self.x, self.y]:
            console.print(self.x, self.y, self.char, fg=self.color)


class Consumable(Item):
    """Base class for consumable items like potions."""
    
    def __init__(self, x, y, name, char, color, description="", effect_value=0):
        super().__init__(x, y, name, char, color, description)
        self.effect_value = effect_value
    
    def use(self, player):
        """Use the consumable item. Returns True if successfully used."""
        return False  # Override in subclasses


class HealthPotion(Consumable):
    """Health restoration potion."""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Health Potion",
            char='!',
            color=COLOR_RED,
            description="Restores health when consumed",
            effect_value=30
        )
    
    def use(self, player):
        """Restore player health."""
        if player.hp >= player.max_hp:
            return False  # Already at full health
        
        old_hp = player.hp
        player.heal(self.effect_value)
        actual_healing = player.hp - old_hp
        return actual_healing > 0


class ManaPotion(Consumable):
    """Mana restoration potion (for future magic system)."""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Mana Potion",
            char='!',
            color=COLOR_BLUE,
            description="Restores mana when consumed",
            effect_value=20
        )
    
    def use(self, player):
        """Restore player mana (placeholder for future magic system)."""
        # For now, just return True to indicate successful use
        return True


class Equipment(Item):
    """Base class for equippable items."""
    
    def __init__(self, x, y, name, char, color, description="", 
                 attack_bonus=0, defense_bonus=0, equipment_slot=""):
        super().__init__(x, y, name, char, color, description)
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.equipment_slot = equipment_slot  # "weapon", "armor", "accessory"
    
    def can_equip(self, player):
        """Check if player can equip this item."""
        return True  # Basic check, can be overridden


class Weapon(Equipment):
    """Weapon equipment."""
    
    def __init__(self, x, y, name, char, attack_bonus, description=""):
        super().__init__(
            x=x, y=y,
            name=name,
            char=char,
            color=COLOR_YELLOW,
            description=description,
            attack_bonus=attack_bonus,
            equipment_slot="weapon"
        )


class Armor(Equipment):
    """Armor equipment."""
    
    def __init__(self, x, y, name, char, defense_bonus, description=""):
        super().__init__(
            x=x, y=y,
            name=name,
            char=char,
            color=COLOR_GREEN,
            description=description,
            defense_bonus=defense_bonus,
            equipment_slot="armor"
        )


class Accessory(Equipment):
    """Accessory equipment (rings, amulets, etc.)."""
    
    def __init__(self, x, y, name, char, attack_bonus=0, defense_bonus=0, description=""):
        super().__init__(
            x=x, y=y,
            name=name,
            char=char,
            color=COLOR_WHITE,
            description=description,
            attack_bonus=attack_bonus,
            defense_bonus=defense_bonus,
            equipment_slot="accessory"
        )


# Specific weapon types
class WoodenStick(Weapon):
    def __init__(self, x, y):
        super().__init__(x, y, "Wooden Stick", ')', 1, "A simple wooden stick")

class Dagger(Weapon):
    def __init__(self, x, y):
        super().__init__(x, y, "Dagger", ')', 3, "A sharp dagger")


class Sword(Weapon):
    def __init__(self, x, y):
        super().__init__(x, y, "Sword", ')', 5, "A well-balanced sword")


class Longsword(Weapon):
    def __init__(self, x, y):
        super().__init__(x, y, "Longsword", ')', 8, "A two-handed longsword")


class WarHammer(Weapon):
    def __init__(self, x, y):
        super().__init__(x, y, "War Hammer", ')', 12, "A heavy war hammer")


# Specific armor types
class WhiteTShirt(Armor):
    def __init__(self, x, y):
        super().__init__(x, y, "White T-Shirt", '[', 0, "A plain white T-shirt")

class LeatherArmor(Armor):
    def __init__(self, x, y):
        super().__init__(x, y, "Leather Armor", '[', 2, "Basic leather protection")


class ChainMail(Armor):
    def __init__(self, x, y):
        super().__init__(x, y, "Chain Mail", '[', 4, "Flexible chain mail armor")


class PlateArmor(Armor):
    def __init__(self, x, y):
        super().__init__(x, y, "Plate Armor", '[', 6, "Heavy plate armor")


class DragonScale(Armor):
    def __init__(self, x, y):
        super().__init__(x, y, "Dragon Scale Armor", '[', 10, "Legendary dragon scale armor")


# Specific accessory types
class Ring(Accessory):
    def __init__(self, x, y, name, attack_bonus=0, defense_bonus=0):
        super().__init__(x, y, name, '=', attack_bonus, defense_bonus, f"A magical ring")


class PowerRing(Ring):
    def __init__(self, x, y):
        super().__init__(x, y, "Ring of Power", attack_bonus=3, defense_bonus=1)


class ProtectionRing(Ring):
    def __init__(self, x, y):
        super().__init__(x, y, "Ring of Protection", defense_bonus=3)


def create_random_item_for_level(level_number, x, y):
    """Create a random item appropriate for the given dungeon level."""
    # Item rarity based on level
    rand = random.random()
    
    # 40% chance for consumables, 60% for equipment
    if rand < 0.4:
        # Consumables
        if random.random() < 0.8:
            return HealthPotion(x, y)
        else:
            return ManaPotion(x, y)
    
    else:
        # Equipment - scale quality with level
        if level_number <= 2:
            # Early game items
            item_type = random.choice(['weapon', 'armor'])
            if item_type == 'weapon':
                return random.choice([Dagger, Sword])(x, y)
            else:
                return LeatherArmor(x, y)
        
        elif level_number <= 5:
            # Mid game items
            item_type = random.choice(['weapon', 'armor', 'accessory'])
            if item_type == 'weapon':
                return random.choice([Sword, Longsword])(x, y)
            elif item_type == 'armor':
                return random.choice([LeatherArmor, ChainMail])(x, y)
            else:
                return PowerRing(x, y)
        
        elif level_number <= 8:
            # Late game items
            item_type = random.choice(['weapon', 'armor', 'accessory'])
            if item_type == 'weapon':
                return random.choice([Longsword, WarHammer])(x, y)
            elif item_type == 'armor':
                return random.choice([ChainMail, PlateArmor])(x, y)
            else:
                return random.choice([PowerRing, ProtectionRing])(x, y)
        
        else:
            # End game items
            item_type = random.choice(['weapon', 'armor', 'accessory'])
            if item_type == 'weapon':
                return WarHammer(x, y)
            elif item_type == 'armor':
                return random.choice([PlateArmor, DragonScale])(x, y)
            else:
                return random.choice([PowerRing, ProtectionRing])(x, y)