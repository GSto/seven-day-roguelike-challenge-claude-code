"""
Ghost Pepper - Extremely spicy pepper that increases max HP but causes burn.
"""

from constants import COLOR_RED
from ..consumable import Consumable


class GhostPepper(Consumable):
    """Ghost Pepper - Increases max HP but applies burn damage."""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Ghost Pepper",
            char='p',
            color=COLOR_RED,
            description="An extremely spicy pepper that burns the tongue. +7 Max HP but applies 3 burn damage.",
            effect_value=7,
            market_value=65  # Rare consumable value
        )
    
    def use(self, player):
        """Increase the player's max HP but apply burn status effect."""
        # Apply the max HP bonus
        player.max_hp += self.effect_value
        
        # Apply burn status effect (3 turns of burn damage)
        player.status_effects.apply_status('burn', 3, player)
        
        return (True, f"You eat the ghost pepper! Max HP +{self.effect_value}, but you're burning! (3 burn applied)")