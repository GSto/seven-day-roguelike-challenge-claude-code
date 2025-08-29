"""
Base class for catalysts that have HP costs based on catalyst tax.
"""

from ..consumable import Consumable


class Catalyst(Consumable):
    """Base class for catalysts that have HP costs based on catalyst tax."""
    
    def __init__(self, x, y, name, char, color, description="", effect_value=0,
                 attack_multiplier_effect=0.0, defense_multiplier_effect=0.0, xp_multiplier_effect=0.0,
                 attack_traits=None, weaknesses=None, resistances=None, market_value=35):
        super().__init__(x, y, name, char, color, description, effect_value,
                         attack_multiplier_effect, defense_multiplier_effect, xp_multiplier_effect,
                         attack_traits, weaknesses, resistances, market_value)
    
    def get_catalyst_hp_cost(self, player):
        """Calculate HP cost based on player's catalyst tax."""
        return int(player.max_hp * player.catalyst_tax)
    
    def get_description_with_cost(self, player):
        """Get description including HP cost information."""
        hp_cost = self.get_catalyst_hp_cost(player)
        cost_text = f" (Cost: {hp_cost} HP)"
        return self.description + cost_text
    
    def use(self, player):
        """Apply catalyst tax before using - override in subclasses."""
        hp_cost = self.get_catalyst_hp_cost(player)
        
        # Check if player has enough HP (must leave at least 1 HP)
        if player.hp <= hp_cost:
            return (False, f"You need at least {hp_cost + 1} HP to use this catalyst!")
        
        # Apply HP cost and increase tax
        player.hp -= hp_cost
        player.catalyst_tax += 0.05  # Increase tax by 5%
        
        # Call subclass implementation
        return self._apply_catalyst_effect(player, hp_cost)
    
    def _apply_catalyst_effect(self, player, hp_cost):
        """Override this method in subclasses to implement catalyst effects."""
        return (False, "Catalyst effect not implemented!")