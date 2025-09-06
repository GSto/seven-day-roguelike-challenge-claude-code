"""
Penny pickup - gives 1 XP instantly.
"""

from .pickup import Pickup
from constants import COLOR_ORANGE


class Penny(Pickup):
    """A penny that instantly grants 1 XP when picked up."""
    
    def __init__(self, x, y):
        """Initialize a Penny pickup."""
        super().__init__(
            x, y,
            name="Penny",
            char="¢",
            color=COLOR_ORANGE,
            description="A penny worth 1 XP",
            market_value=0
        )
        self.xp_amount = 1
    
    def on_pickup(self, player):
        """Grant XP to the player when picked up.
        
        Returns:
            tuple: (success, message)
        """
        # Calculate XP with multipliers
        xp_gained = int(self.xp_amount * player.get_total_xp_multiplier())
        
        # Grant the XP
        player.gain_xp(self.xp_amount)
        
        # Check if player can now level up
        if player.can_level_up():
            return True, f"The Penny grants you {xp_gained} XP! You can level up!"
        else:
            return True, f"The Penny grants you {xp_gained} XP!"