"""
Enchantment class for the roguelike game.
"""

from .enchantment_type import EnchantmentType
from traits import Trait


class Enchantment:
    """Represents an enchantment that can be applied to weapons or armor."""
    
    def __init__(self, enchantment_type, target_type="weapon"):
        self.type = enchantment_type
        self.target_type = target_type  # "weapon" or "armor"
        if target_type == "weapon":
            self.name = enchantment_type.get_weapon_label()
        else:
            self.name = enchantment_type.get_armor_label()
        self.attack_traits = self._get_attack_traits()
        self.resistances = self._get_resistances()
    
    def get_weapon_attack_bonus(self):
        """Get the attack bonus when applied to weapons."""
        if self.type == EnchantmentType.QUALITY:
            return 3
        elif self.type == EnchantmentType.BALANCED:
            return 0  # Defense bonus, not attack
        return 0
    
    def get_armor_attack_bonus(self):
        """Get the attack bonus when applied to armor."""
        if self.type == EnchantmentType.BALANCED:
            return 1  # Spiked armor gives attack
        return 0
    
    def get_weapon_defense_bonus(self):
        """Get the defense bonus when applied to weapons."""
        if self.type == EnchantmentType.BALANCED:
            return 1  # Bolstered weapon gives defense
        return 0
    
    def get_armor_defense_bonus(self):
        """Get the defense bonus when applied to armor."""
        if self.type == EnchantmentType.QUALITY:
            return 3
        return 0
    
    def get_weapon_fov_bonus(self):
        """Get the FOV bonus when applied to weapons."""
        if self.type == EnchantmentType.GLOWING:
            return 3
        return 0
    
    def get_armor_fov_bonus(self):
        """Get the FOV bonus when applied to armor."""  
        if self.type == EnchantmentType.GLOWING:
            return 3
        return 0
    
    def get_weapon_attack_multiplier_bonus(self):
        """Get the attack multiplier bonus when applied to weapons."""
        if self.type == EnchantmentType.SHINY:
            return 0.25  # 25% bonus = 1.25x attack
        return 0.0
    
    def get_armor_defense_multiplier_bonus(self):
        """Get the defense multiplier bonus when applied to armor."""
        if self.type == EnchantmentType.SHINY:
            return 0.25  # 25% bonus = 1.25x defense
        return 0.0
    
    def get_xp_multiplier_bonus(self):
        """Get the XP multiplier bonus (same for weapon/armor)."""
        if self.type == EnchantmentType.GILDED:
            return 0.05  # 5% bonus
        return 0.0
    
    def get_health_aspect_bonus(self):
        """Get the health aspect bonus (same for weapon/armor)."""
        if self.type == EnchantmentType.BLESSED:
            return 0.10  # 10% bonus
        return 0.0
    
    def get_weapon_crit_bonus(self):
        """Get the crit chance bonus when applied to weapons."""
        if self.type == EnchantmentType.RENDING:
            return 0.05  # 5% crit chance bonus
        return 0.0
    
    def get_armor_evade_bonus(self):
        """Get the evade chance bonus when applied to armor."""
        if self.type == EnchantmentType.SHADOW:
            return 0.05  # 5% evade chance bonus
        return 0.0
    
    def _get_attack_traits(self):
        """Get the attack traits provided by this enchantment."""
        if self.target_type != "weapon":
            return []
        
        trait_map = {
            EnchantmentType.FIRE: [Trait.FIRE],
            EnchantmentType.ICE: [Trait.ICE],
            EnchantmentType.HOLY: [Trait.HOLY],
            EnchantmentType.DARK: [Trait.DARK]
        }
        return trait_map.get(self.type, [])
    
    def _get_resistances(self):
        """Get the resistances provided by this enchantment."""
        if self.target_type != "armor":
            return []
        
        resistance_map = {
            EnchantmentType.FIRE: [Trait.FIRE],
            EnchantmentType.ICE: [Trait.ICE],
            EnchantmentType.HOLY: [Trait.HOLY],
            EnchantmentType.DARK: [Trait.DARK]
        }
        return resistance_map.get(self.type, [])