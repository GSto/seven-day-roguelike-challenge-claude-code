"""
Nickel pickup - gives 5 XP instantly.
"""

from .pickup import Pickup
from constants import COLOR_GRAY


class Nickel(Pickup):
    """A nickel that instantly grants 5 XP when picked up."""
    
    def __init__(self, x, y):
        """Initialize a Nickel pickup."""
        super().__init__(
            x, y,
            name="Nickel",
            char="¢",
            color=COLOR_GRAY,
            description="A nickel worth 5 XP",
            market_value=0
        )
        self.xp_amount = 5
    
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
            return True, f"The Nickel grants you {xp_gained} XP! You can level up!"
        else:
            return True, f"The Nickel grants you {xp_gained} XP!"