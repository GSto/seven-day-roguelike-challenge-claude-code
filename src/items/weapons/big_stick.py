"""
Big Stick weapon for the roguelike game.
"""

import random
from .base import Weapon
from traits import Trait


class BigStick(Weapon):
    """Mid-game weapons. strike. 50% chance to apply stun. 50% chance to apply immobilized."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Big Stick", ')', 5, 
                        "Mid-game weapons. strike. 50% chance to apply stun. 50% chance to apply immobilized.",
                        attack_traits=[Trait.STRIKE])
        self.market_value = 45  # Mid game common weapon
    
    def on_hit(self, attacker, target):
        """Apply random status effects when hitting a target."""
        messages = []
        if hasattr(target, 'status_effects'):
            if random.random() < 0.5:  # 50% chance for stun
                if target.status_effects.apply_status('stun', 1, target):
                    messages.append(f"{target.name if hasattr(target, 'name') else 'The target'} is stunned!")
            if random.random() < 0.5:  # 50% chance for immobilized
                if target.status_effects.apply_status('immobilized', 1, target):
                    messages.append(f"{target.name if hasattr(target, 'name') else 'The target'} is immobilized!")
        return " ".join(messages) if messages else None