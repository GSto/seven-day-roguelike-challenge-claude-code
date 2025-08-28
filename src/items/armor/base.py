"""
Base armor class for the roguelike game.
"""

from constants import COLOR_GREEN
from ..equipment import Equipment
import random
from traits import Trait


class Armor(Equipment):
    """Armor equipment."""
    
    def __init__(self, x, y, name, char, defense_bonus, description="", 
                 attack_bonus=0, fov_bonus=0, health_aspect_bonus=0.0,
                 attack_multiplier_bonus=1.0, defense_multiplier_bonus=1.0, xp_multiplier_bonus=1.0,
                 evade_bonus=0.0, crit_bonus=0.0, crit_multiplier_bonus=0.0,
                 attack_traits=None, weaknesses=None, resistances=None):
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
            resistances=resistances
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
            enchantment_names = [e.name.capitalize() for e in self.enchantments]
            self.name = f"{' '.join(enchantment_names)} {self.base_name}"