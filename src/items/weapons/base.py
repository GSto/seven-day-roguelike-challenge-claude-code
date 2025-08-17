"""
Base weapon class for the roguelike game.
"""

from constants import COLOR_YELLOW
from ..equipment import Equipment
from enchantments import Enchantment
from traits import Trait


class Weapon(Equipment):
    """Weapon equipment."""
    
    def __init__(self, x, y, name, char=')', attack_bonus=0, description="", 
                 fov_bonus=0, health_aspect_bonus=0.0, attack_multiplier_bonus=1.0, defense_multiplier_bonus=1.0, xp_multiplier_bonus=1.0,
                 evade_bonus=0.0, crit_bonus=0.0, crit_multiplier_bonus=0.0,
                 attack_traits=None, weaknesses=None, resistances=None,
                 xp_cost=5):
        self.enchantments = []
        self.base_name = name
        
        super().__init__(
            x=x, y=y,
            name=name,
            char=char,
            color=COLOR_YELLOW,
            description=description,
            attack_bonus=attack_bonus,
            equipment_slot="weapon",
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
        """Add an enchantment to this weapon (max 2 enchantments)."""
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
    
    def get_attack_multiplier_bonus(self, player):
        """Get attack multiplier bonus including enchantments."""
        total = super().get_attack_multiplier_bonus(player)
        for enchantment in self.enchantments:
            total += self.get_enchantment_bonus(enchantment, "attack_multiplier", player)
        return total
    
    def get_defense_multiplier_bonus(self, player):
        """Get defense multiplier bonus including enchantments."""
        total = super().get_defense_multiplier_bonus(player)
        for enchantment in self.enchantments:
            # Defense multiplier enchantments would be additive here if they existed
            pass
        return total
    
    def get_xp_multiplier_bonus(self, player):
        """Get XP multiplier bonus including enchantments."""
        total = super().get_xp_multiplier_bonus(player)
        for enchantment in self.enchantments:
            total += self.get_enchantment_bonus(enchantment, "xp_multiplier", player)
        return total
    
    def get_enchantment_bonus(self, enchantment, bonus_type, player):
        """
        Override method to customize enchantment effects for specific weapons.
        
        Args:
            enchantment: The enchantment to get bonus from
            bonus_type: Type of bonus ("attack", "defense", "fov", etc.)
            player: Player instance for context
            
        Returns:
            The bonus value for this enchantment and bonus type
        """
        # Default behavior - call the appropriate method on the enchantment
        weapon_method_name = f"get_weapon_{bonus_type}_bonus"
        shared_method_name = f"get_{bonus_type}_bonus"
        
        if hasattr(enchantment, weapon_method_name):
            return getattr(enchantment, weapon_method_name)()
        elif hasattr(enchantment, shared_method_name):
            return getattr(enchantment, shared_method_name)()
        return 0.0
    
    def get_evade_bonus(self, player):
        """Get evade bonus including enchantments."""
        total = super().get_evade_bonus(player)
        # No evade enchantments currently exist
        return total
    
    def get_crit_bonus(self, player):
        """Get crit bonus including enchantments."""
        total = super().get_crit_bonus(player)
        for enchantment in self.enchantments:
            total += self.get_enchantment_bonus(enchantment, "crit", player)
        return total
    
    def get_crit_multiplier_bonus(self, player):
        """Get crit multiplier bonus including enchantments."""
        total = super().get_crit_multiplier_bonus(player)
        # No crit multiplier enchantments currently exist
        return total
    
    def get_total_attack_traits(self):
        """Get all attack traits including enchantments."""
        return self.get_attack_traits()
    
    def _update_display_name(self):
        """Update the display name to include enchantments."""
        if not self.enchantments:
            self.name = self.base_name
        else:
            enchantment_names = [e.name for e in self.enchantments]
            self.name = f"{' '.join(enchantment_names)} {self.base_name}"