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
            return (False, "You need equipped items that can be further enhanced!")
        
        # Prefer weapon if both available
        if weapon_eligible:
            enchantment = get_weapon_enchantment_by_type(random_enchantment)
            if player.weapon.add_enchantment(enchantment):
                return (True, f"Your {player.weapon.name} is enchanted with {random_enchantment.value} power!")
        elif armor_eligible:
            enchantment = get_armor_enchantment_by_type(random_enchantment)
            if player.armor.add_enchantment(enchantment):
                return (True, f"Your {player.armor.name} is enchanted with {random_enchantment.value} protection!")
        
        return (False, "The enchantment failed to take hold!")


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
        # This requires access to the current level's items
        if not hasattr(player, '_current_level') or player._current_level is None:
            self.use_charge()
            return (False, "Unable to detect items - no floor detected!")
        
        level = player._current_level
        
        # Mark all item positions as visible in FOV
        # This creates a temporary "sight" of all items
        items_revealed = 0
        for item in level.items:
            # Set FOV to true for item positions to make them visible
            level.fov[item.x, item.y] = True
            items_revealed += 1
        
        self.use_charge()
        
        if items_revealed == 0:
            return (True, "No items detected on this floor.")
        elif items_revealed == 1:
            return (True, "1 item is now visible on this floor!")
        else:
            return (True, f"{items_revealed} items are now visible on this floor!")


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
        # This requires access to the current level's explored map
        if not hasattr(player, '_current_level') or player._current_level is None:
            return (False, "Unable to reveal map - no floor detected!")
        
        level = player._current_level
        
        # Mark all tiles as explored
        level.explored.fill(True)
        
        return (True, "The entire floor layout is revealed!")


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
        # This requires access to the current level's monsters
        # Since we don't have direct access to the level here, we'll need to check
        # if the player object has a reference to the current level/game state
        if not hasattr(player, '_current_level') or player._current_level is None:
            return (False, "Unable to detonate bomb - no enemies detected!")
        
        level = player._current_level
        damage_dealt = 30
        radius = 3
        enemies_hit = 0
        
        # Find all monsters within radius
        for monster in level.monsters:
            distance = monster.distance_to(player.x, player.y)
            if distance <= radius:
                monster.take_damage(damage_dealt)
                enemies_hit += 1
        
        # Remove dead monsters
        level.remove_dead_monsters()
        
        if enemies_hit == 0:
            return (True, "BOOM! The bomb explodes, but no enemies were in range.")
        elif enemies_hit == 1:
            return (True, f"BOOM! The bomb explodes, dealing {damage_dealt} damage to 1 enemy!")
        else:
            return (True, f"BOOM! The bomb explodes, dealing {damage_dealt} damage to {enemies_hit} enemies!")


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
        from .foods import HealthPotion
        from .weapons import Weapon
        
        # Find all unequipped weapons in inventory
        weapon_items = []
        for item in player.inventory:
            if isinstance(item, Weapon) and item != player.weapon:
                weapon_items.append(item)
        
        if not weapon_items:
            return (False, "You have no unequipped weapons to convert!")
        
        # Convert each weapon to a health potion
        for weapon in weapon_items:
            player.remove_item(weapon)
            health_potion = HealthPotion(0, 0)
            player.add_item(health_potion)
        
        count = len(weapon_items)
        if count == 1:
            return (True, f"Your {weapon_items[0].name} transforms into a healing potion!")
        else:
            return (True, f"{count} weapons transform into healing potions!")


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
        from .foods import ShellPotion
        from .armor import Armor
        
        # Find all unequipped armor in inventory
        armor_items = []
        for item in player.inventory:
            if isinstance(item, Armor) and item != player.armor:
                armor_items.append(item)
        
        if not armor_items:
            return (False, "You have no unequipped armor to transmute!")
        
        # Convert each armor piece to a shield potion
        for armor in armor_items:
            player.remove_item(armor)
            shield_potion = ShellPotion(0, 0)
            player.add_item(shield_potion)
        
        count = len(armor_items)
        if count == 1:
            return (True, f"Your {armor_items[0].name} transforms into a protective potion!")
        else:
            return (True, f"{count} pieces of armor transform into protective potions!")