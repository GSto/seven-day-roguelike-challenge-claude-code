"""
Snake's Fang weapon for the roguelike game.
"""

from .base import Weapon
from traits import Trait


class SnakesFang(Weapon):
    """Venomous blade that applies poison on hit."""

    def __init__(self, x, y):
        super().__init__(x, y, "Snake's Fang", ')', 4, "Deals slash & poison damage. Applies additional poison on hit", 
                         attack_traits=[Trait.SLASH, Trait.POISON])
        self.market_value = 68  # Mid game uncommon weapon
    
    def on_hit(self, player, target):
        """Apply additional poison when hitting a target."""
        if hasattr(target, 'status_effects'):
            if target.status_effects.apply_status('poison', 5, target):
                return f"The venom seeps into {target.name if hasattr(target, 'name') else 'the target'}!"
        return None