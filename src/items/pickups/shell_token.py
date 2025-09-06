"""
Shell Token pickup - gives +1 Defense instantly.
"""

from .pickup import Pickup
from constants import COLOR_CYAN


class ShellToken(Pickup):
    """A shell token that instantly grants +1 shield when picked up."""
    
    def __init__(self, x, y):
        """Initialize a Shell Token pickup."""
        super().__init__(
            x, y,
            name="Shell Token",
            char="○",
            color=COLOR_CYAN,
            description="A shell token that grants 1 protective shield",
            market_value=0
        )
        self.shield_amount = 1
    
    def on_pickup(self, player):
        """Grant shield to the player when picked up.
        
        Returns:
            tuple: (success, message)
        """
        # Apply shield status effect
        player.status_effects.apply_status('shields', self.shield_amount, player)
        
        return True, f"The Shell Token grants you {self.shield_amount} shield!"