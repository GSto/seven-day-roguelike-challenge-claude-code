"""
Armor items for defense.
"""

from constants import COLOR_GREEN
from .base import Equipment
import random
from traits import Trait


class Armor(Equipment):
    """Armor equipment."""
    
    def __init__(self, x, y, name, char, defense_bonus, description="", 
                 attack_bonus=0, fov_bonus=0, health_aspect_bonus=0.0,
                 attack_multiplier_bonus=1.0, defense_multiplier_bonus=1.0, xp_multiplier_bonus=1.0,
                 evade_bonus=0.0, crit_bonus=0.0, crit_multiplier_bonus=0.0,
                 attack_traits=None, weaknesses=None, resistances=None,
                 xp_cost=5):
        self.enchantments = []
        self.base_name = name
        super().__init__(
            x=x, y=y,
            name=name,
            char=char,
            color=COLOR_GREEN,
            description=description,
            attack_bonus=attack_bonus,
            defense_bonus=defense_bonus,
            equipment_slot="armor",
            fov_bonus=fov_bonus,
            health_aspect_bonus=health_aspect_bonus,
            attack_multiplier_bonus=attack_multiplier_bonus,
            defense_multiplier_bonus=defense_multiplier_bonus,
            xp_multiplier_bonus=xp_multiplier_bonus,
            evade_bonus=evade_bonus,
            crit_bonus=crit_bonus,
            crit_multiplier_bonus=crit_multiplier_bonus,
            attack_traits=attack_traits,
            weaknesses=weaknesses,
            resistances=resistances,
            xp_cost=xp_cost
        )
    
    def add_enchantment(self, enchantment):
        """Add an enchantment to this armor (max 2 enchantments)."""
        if len(self.enchantments) >= 2:
            return False
        
        # Check if enchantment type already exists
        for existing_enchantment in self.enchantments:
            if existing_enchantment.type == enchantment.type:
                return False
        
        self.enchantments.append(enchantment)
        self._update_display_name()
        return True
    
    def get_total_resistances(self):
        """Get all resistances including enchantments."""
        return self.get_resistances()
    
    def _update_display_name(self):
        """Update the display name to include enchantments."""
        if not self.enchantments:
            self.name = self.base_name
        else:
            enchantment_names = [e.name for e in self.enchantments]
            self.name = f"{' '.join(enchantment_names)} {self.base_name}"


# Specific armor types
class WhiteTShirt(Armor):
    """Basic starting armor."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "White T-Shirt", '[', 0, "A plain white T-shirt", xp_cost=0)


class LeatherArmor(Armor):
    """Light armor for early game."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Leather Armor", '[', 1, description="Basic leather protection. Free to equip", xp_cost=0)

class SafetyVest(Armor):
    """Light armor for early game."""

    def __init__(self, x, y):
        super().__init__(x, y, "Safety Vest", '[', 2, description="Bright orange, easy to see", fov_bonus=2)

class Cloak(Armor):
    def __init__(self, x, y):
        super().__init__(x, y, "Cloak", '[', 1, description="Shadow black, hard to see", evade_bonus=0.05)

class NightCloak(Armor):
    def __init__(self, x, y):
        super().__init__(x, y, "Night Cloak", '[', 1, description="Vanta black, harder to see", evade_bonus=0.1)

class ShadowCloak(Armor):
    def __init__(self, x, y):
        super().__init__(x, y, "Shadow's Cloak", '[', 1, description="Wearer is transcluent, harder to see", evade_bonus=0.2)
class GamblersVest(Armor):
    def __init__(self, x, y):
        super().__init__(x, y, "Gambler's Vest", '[', 0, description="Double or 0.5x on defense")

    def get_defense_multiplier_bonus(self, player):
      rand = random.random()
      if rand <= 0.5:
        return 2
      else:
        return 0.5
      
class SkinSuit(Armor):
    def __init__(self, x, y):
        super().__init__(x, y, "Skin Suit", '[', 0, description="+1 DEF for every 4 enemies slain")

    def get_defense_bonus(self, player):
        return super().get_defense_bonus(player) + int(player.body_count / 4)
    

class MinimalSuit(Armor):
    def __init__(self, x, y):
        super().__init__(x, y, "Traveler's Garb", '[', 0, description="More evade the lighter you are")

    def get_evade_bonus(self, player):
        inventory_space = len(player.ininventory) - player.inventory_size
        return super().get_evade_bonus(player) + (inventory_space / 100)


class ChainMail(Armor):
    """Medium armor for mid-game."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Chain Mail", '[', 2, description="Flexible chain mail armor")


class PlateArmor(Armor):
    """Heavy armor for late game."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Plate Armor", '[', 3, description="Heavy plate armor")


class DragonScale(Armor):
    """Legendary armor from dragon materials."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Dragon Scale Armor", '[', 5, description="Legendary dragon scale armor")


class SpikedArmor(Armor):
    """Aggressive armor with spikes for extra protection and offense."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Spiked Armor", '[', 1, description="Menacing armor covered in spikes", attack_bonus=2)