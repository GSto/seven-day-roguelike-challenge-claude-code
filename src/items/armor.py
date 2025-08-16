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
    
    def get_attack_bonus(self, player):
        """Get attack bonus including enchantments."""
        total = super().get_attack_bonus(player)
        for enchantment in self.enchantments:
            total += self.get_enchantment_bonus(enchantment, "attack", player)
        return total
    
    def get_defense_bonus(self, player):
        """Get defense bonus including enchantments."""
        total = super().get_defense_bonus(player)
        for enchantment in self.enchantments:
            total += self.get_enchantment_bonus(enchantment, "defense", player)
        return total
    
    def get_fov_bonus(self, player):
        """Get FOV bonus including enchantments."""
        total = super().get_fov_bonus(player)
        for enchantment in self.enchantments:
            total += self.get_enchantment_bonus(enchantment, "fov", player)
        return total
    
    def get_health_aspect_bonus(self, player):
        """Get health aspect bonus including enchantments."""
        total = super().get_health_aspect_bonus(player)
        for enchantment in self.enchantments:
            total += self.get_enchantment_bonus(enchantment, "health_aspect", player)
        return total
    
    def get_defense_multiplier_bonus(self, player):
        """Get defense multiplier bonus including enchantments."""
        total = super().get_defense_multiplier_bonus(player)
        for enchantment in self.enchantments:
            total += self.get_enchantment_bonus(enchantment, "defense_multiplier", player)
        return total
    
    def get_xp_multiplier_bonus(self, player):
        """Get XP multiplier bonus including enchantments."""
        total = super().get_xp_multiplier_bonus(player)
        for enchantment in self.enchantments:
            total += self.get_enchantment_bonus(enchantment, "xp_multiplier", player)
        return total
    
    def get_evade_bonus(self, player):
        """Get evade bonus including enchantments."""
        total = super().get_evade_bonus(player)
        for enchantment in self.enchantments:
            total += self.get_enchantment_bonus(enchantment, "evade", player)
        return total
    
    def get_enchantment_bonus(self, enchantment, bonus_type, player):
        """
        Override method to customize enchantment effects for specific armor.
        
        Args:
            enchantment: The enchantment to get bonus from
            bonus_type: Type of bonus ("attack", "defense", "fov", etc.)
            player: Player instance for context
            
        Returns:
            The bonus value for this enchantment and bonus type
        """
        # Default behavior - call the appropriate method on the enchantment
        armor_method_name = f"get_armor_{bonus_type}_bonus"
        shared_method_name = f"get_{bonus_type}_bonus"
        
        if hasattr(enchantment, armor_method_name):
            return getattr(enchantment, armor_method_name)()
        elif hasattr(enchantment, shared_method_name):
            return getattr(enchantment, shared_method_name)()
        return 0.0
    
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
      base = super().get_defense_multiplier_bonus(player)
      rand = random.random()
      if rand <= 0.5:
        return base + 1.0  # 2x total (base 1.0 + 1.0 bonus)
      else:
        return base - 0.5  # 0.5x total (base 1.0 - 0.5 penalty)
      
class SkinSuit(Armor):
    def __init__(self, x, y):
        super().__init__(x, y, "Skin Suit", '[', 0, description="+1 DEF for every 4 enemies slain")

    def get_defense_bonus(self, player):
        return super().get_defense_bonus(player) + int(player.body_count / 4)
    

class MinimalSuit(Armor):
    def __init__(self, x, y):
        super().__init__(x, y, "Traveler's Garb", '[', 0, description="More evade the lighter you are")

    def get_evade_bonus(self, player):
        inventory_space =  player.inventory_size - len(player.inventory)
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


# New Item Pack 2 Armor

class CoatedPlate(Armor):
    """Mid-game+ armor. +4 DEF. Immune to poison, burn, stun."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Coated Plate", '[', 4, 
                        description="Mid-game+ armor. +4 DEF. Immune to poison, burn, stun")
    
    def blocks_status_effect(self, effect_name):
        """Check if this armor blocks a specific status effect."""
        return effect_name in ['poison', 'burn', 'stun']


class AntiAngelTechnology(Armor):
    """Mid-game armor. +4 DEF. Holy resistance, immune to blindness."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Anti-Angel Technology", '[', 4, 
                        description="Mid-game armor. +4 DEF. Holy resistance, immune to blindness",
                        resistances=[Trait.HOLY])
    
    def blocks_status_effect(self, effect_name):
        """Check if this armor blocks a specific status effect."""
        return effect_name in ['blindness']


class SpikedCuirass(Armor):
    """Mid-game+ armor. +4 DEF, +2 ATK"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Spiked Cuirass", '[', 4, 
                        description="Mid-game+ armor. +4 DEF, +2 ATK",
                        attack_bonus=2)


class UtilityBelt(Armor):
    """Mid-game+ armor. +3 DEF, +10% healing, +10% XP, +3 FOV"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Utility Belt", '[', 3, 
                        description="Mid-game+ armor. +3 DEF, +10% healing, +10% XP, +3 FOV",
                        fov_bonus=3,
                        health_aspect_bonus=0.1,
                        xp_multiplier_bonus=1.1)


class SOSArmor(Armor):
    """+2 DEF. +6 DEF if HP is 20% or less of max HP"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "SOS Armor", '[', 2, 
                        description="+2 DEF. +6 DEF if HP is 20% or less of max HP")
    
    def get_defense_bonus(self, player):
        """Get defense bonus with conditional extra defense at low HP."""
        base_defense = super().get_defense_bonus(player)
        if player.hp <= (player.max_hp * 0.2):  # 20% or less HP
            return base_defense + 6
        return base_defense