"""
SongOfIceAndFire - If on floor 5 or lower, +6 ATK for Ice or fire damage.
"""
from .accessory import Accessory
from traits import Trait


class SongOfIceAndFire(Accessory):
    """If on floor 5 or lower, +6 ATK for Ice or fire damage"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Song of Ice and Fire", '=',
                        description="If on floor 5 or lower, +6 ATK for Ice or fire damage")
    
    def get_attack_bonus(self, player):
        """Get attack bonus based on floor and elemental traits."""
        base_bonus = super().get_attack_bonus(player)
        
        # Check if player is on floor 5 or lower
        current_floor = getattr(player, 'current_floor', 1)
        if current_floor > 5:
            return base_bonus
        
        # Check if player has ice or fire attack traits
        attack_traits = player.get_total_attack_traits()
        if Trait.ICE in attack_traits or Trait.FIRE in attack_traits:
            return base_bonus + 6
        
        return base_bonus