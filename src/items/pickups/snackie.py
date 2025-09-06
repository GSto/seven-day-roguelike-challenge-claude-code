"""
Snackie pickup - instant healing item.
"""

from .pickup import Pickup
from constants import COLOR_SALMON


class Snackie(Pickup):
    """Small snack that instantly heals 5 HP when picked up."""
    
    def __init__(self, x, y):
        """Initialize a Snackie pickup."""
        super().__init__(
            x, y,
            name="Snackie",
            char="*",
            color=COLOR_SALMON,
            description="A tasty snack that restores 5 HP instantly",
            market_value=0
        )
        self.heal_amount = 5
    
    def on_pickup(self, player):
        """Heal the player when picked up.
        
        Returns:
            tuple: (success, message)
        """
        if player.stats.hp >= player.stats.max_hp:
            return False, "You're already at full health!"
        
        # Calculate actual healing amount
        old_hp = player.stats.hp
        player.stats.hp = min(player.stats.hp + self.heal_amount, player.stats.max_hp)
        healed = player.stats.hp - old_hp
        
        return True, f"The Snackie heals you for {healed} HP!"