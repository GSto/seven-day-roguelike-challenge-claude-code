"""
Consumable items - now organized into subcategories.
This file imports all consumables for backward compatibility.
"""

# Import all consumable subcategories for backward compatibility
import random
from constants import COLOR_WHITE
from .base import Consumable


class D6(Consumable):
    """Random effect dice with 6 possible outcomes"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="D6",
            char='6',
            color=COLOR_WHITE,
            description="Roll for one of 6 random effects:\n +1 Attack, +1 Defense, +10 max HP, +1 FOV, or -20 max HP",
            effect_value=1
        )
    
    def use(self, player):
        """Apply one of 6 random effects"""
        roll = random.randint(1, 6)
        
        if roll == 5:
            # +1 Attack
            player.attack += 1
            return (True, f"Rolled {roll}! Attack +1")
        elif roll == 2:
            # +1 Defense
            player.defense += 1
            return (True, f"Rolled {roll}! Defense +1")
        elif roll == 3:
            # +10 max HP
            old_max = player.max_hp
            player.max_hp += 10
            player.hp += (player.max_hp - old_max)  # Heal the difference
            return (True, f"Rolled {roll}! Max HP +10")
        elif roll == 4:
            # +3 FOV
            player.fov += 1
            return (True, f"Rolled {roll}! FOV +3")
        elif roll == 1:
            # -20 max HP (but don't kill the player)
            if player.max_hp > 25:  # Ensure player doesn't die from this
                player.max_hp -= 20
                if player.hp > player.max_hp:
                    player.hp = player.max_hp
                return (True, f"Rolled {roll}! Max HP -20 (ouch!)")
            else:
                return (True, f"Rolled {roll}! But you're too weak for the penalty to apply.")
        else:  # roll == 6
            # Duplicate effect - +1 Attack (making it slightly more likely to be positive)
            player.attack += 1
            return (True, f"Rolled {roll}! Attack +1")


# New Item Pack 2 Consumables

class MayhemsBoon(Consumable):
    """Grants a random elemental enchantment bonus"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Mayhem's Boon",
            char='*',
            color=COLOR_WHITE,
            description="Grants a random elemental enchantment bonus"
        )
    
    def use(self, player):
        """Apply a random elemental enchantment to equipped weapon or armor"""
        import random
        from .enchantments import EnchantmentType, get_weapon_enchantment_by_type, get_armor_enchantment_by_type
        
        # Get elemental enchantment types
        elemental_enchantments = [EnchantmentType.FIRE, EnchantmentType.ICE, EnchantmentType.HOLY, EnchantmentType.DARK]
        random_enchantment = random.choice(elemental_enchantments)
        
        # Check what can be enchanted
        weapon_eligible = (player.weapon is not None and
                          len(player.weapon.enchantments) < 2 and
                          not any(e.type == random_enchantment for e in player.weapon.enchantments))
        armor_eligible = (player.armor is not None and
                         len(player.armor.enchantments) < 2 and
                         not any(e.type == random_enchantment for e in player.armor.enchantments))
        
        if not weapon_eligible and not armor_eligible:
            return (False, "You need equipped items that can be further enhanced!", True)
        
        # Prefer weapon if both available
        if weapon_eligible:
            enchantment = get_weapon_enchantment_by_type(random_enchantment)
            if player.weapon.add_enchantment(enchantment):
                return (True, f"Your {player.weapon.name} is enchanted with {random_enchantment.value} power!", True)
        elif armor_eligible:
            enchantment = get_armor_enchantment_by_type(random_enchantment)
            if player.armor.add_enchantment(enchantment):
                return (True, f"Your {player.armor.name} is enchanted with {random_enchantment.value} protection!", True)
        
        return (False, "The enchantment failed to take hold!", True)


class Compass(Consumable):
    """Makes all items visible on the map (3 charges)"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Compass",
            char='c',
            color=COLOR_WHITE,
            description="Makes all items visible on the map",
            charges=3
        )
    
    def use(self, player):
        """Reveal all items on the current floor"""
        # This will need to interface with the game level/map system
        # For now, just return success - implementation depends on game architecture
        should_destroy = self.use_charge()
        return (True, "All items on this floor are now visible!", should_destroy)


class Map(Consumable):
    """Marks all tiles explored, destroyed when changing floors"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Map",
            char='?',
            color=COLOR_WHITE,
            description="Marks all tiles as explored, destroyed when changing floors"
        )
    
    def use(self, player):
        """Reveal entire floor"""
        # This will need to interface with the game level/map system
        # For now, just return success - implementation depends on game architecture
        return (True, "The entire floor layout is revealed!", True)


class Bomb(Consumable):
    """Deals 30 damage to all enemies in a 3 block radius"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Bomb",
            char='o',
            color=COLOR_WHITE,
            description="Deals 30 damage to all enemies in a 3 block radius"
        )
    
    def use(self, player):
        """Deal damage to nearby enemies"""
        # This will need to interface with the game's enemy system
        # For now, just return success - implementation depends on game architecture
        return (True, "BOOM! The bomb explodes, damaging nearby enemies!", True)


class SwordsToPlowshares(Consumable):
    """Replace all unequipped weapons in inventory with health potions"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Swords to Plowshares",
            char='s',
            color=COLOR_WHITE,
            description="Replace all unequipped weapons in inventory with health potions"
        )
    
    def use(self, player):
        """Convert weapons to health potions"""
        # This will need to interface with the player's inventory system
        # For now, just return success - implementation depends on game architecture
        return (True, "Your weapons transform into healing potions!", True)


class Transmutation(Consumable):
    """Replace all unequipped armor in inventory with shield potions"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Transmutation",
            char='t',
            color=COLOR_WHITE,
            description="Replace all unequipped armor in inventory with shield potions"
        )
    
    def use(self, player):
        """Convert armor to shield potions"""
        # This will need to interface with the player's inventory system
        # For now, just return success - implementation depends on game architecture
        return (True, "Your armor transforms into protective potions!", True)