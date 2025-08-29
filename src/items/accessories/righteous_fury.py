"""
RighteousFury - Holy attacks also apply 4 burn damage.
"""
from .accessory import Accessory
from traits import Trait


class RighteousFury(Accessory):
    """Holy attacks also apply 4 burn damage"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Righteous Fury", '=',
        description="Holy attacks also apply 4 burn damage")
        self.market_value = 38  # Uncommon accessory
    
    def on_hit(self, player, target):
        """Apply burn damage when making holy attacks."""

        if hasattr(target, 'status_effects') and Trait.HOLY in player.attack_traits:
            if target.status_effects.apply_status('burn', 4, target):
                return f"{target.name if hasattr(target, 'name') else 'The target'} is burned by righteous fire!"
        return None