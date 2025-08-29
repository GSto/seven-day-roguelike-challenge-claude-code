"""
Rapier weapon for the roguelike game.
"""

from .base import Weapon
from traits import Trait


class Rapier(Weapon):
    """Elegant blade that leaves enemies off-guard."""

    def __init__(self, x, y):
        super().__init__(x, y, "Rapier", ')', 6, "Mid-game weapon that applies off-guard on attack", 
                         attack_traits=[Trait.SLASH])
        self.market_value = 68  # Mid game uncommon weapon
    
    def on_hit(self, attacker, target):
        """Apply off-guard status when hitting a target."""
        if hasattr(target, 'status_effects'):
            if target.status_effects.apply_status('off_guard', 1, target):
                return f"{target.name if hasattr(target, 'name') else 'The target'} is caught off-guard!"
        return None