"""
Shell Token pickup - gives +1 Defense instantly.
"""

from .pickup import Pickup
from constants import COLOR_CYAN


class ShellToken(Pickup):
    """A shell token that instantly grants +1 Defense when picked up."""
    
    def __init__(self, x, y):
        """Initialize a Shell Token pickup."""
        super().__init__(
            x, y,
            name="Shell Token",
            char="○",
            color=COLOR_CYAN,
            description="A shell token that permanently increases Defense by 1",
            market_value=0
        )
        self.defense_amount = 1
    
    def on_pickup(self, player):
        """Grant Defense to the player when picked up.
        
        Returns:
            tuple: (success, message)
        """
        # Increase base defense permanently
        player.stats.defense += self.defense_amount
        
        return True, f"The Shell Token increases your Defense by {self.defense_amount}!"