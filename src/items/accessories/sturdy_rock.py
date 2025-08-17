"""
SturdyRock - Immunity to stun, immobilized, and off-guard.
"""
from .accessory import Accessory


class SturdyRock(Accessory):
    """Immunity to stun, immobilized, and off-guard."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Sturdy Rock", '=',
                        description="+1 DEF. Immunity to stun, immobilized, and off-guard",
                        defense_bonus=1)
    
    def blocks_status_effect(self, effect_name):
        """Check if this accessory blocks a specific status effect."""
        return effect_name in ['stun', 'immobilized', 'off_guard']