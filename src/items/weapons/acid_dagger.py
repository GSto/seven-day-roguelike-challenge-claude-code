"""
Acid Dagger weapon for the roguelike game.
"""

from .base import Weapon
from traits import Trait


class AcidDagger(Weapon):
    """6 dmg. Apply 4 burn and 4 poison on every hit. Slash, Fire, Poison damage."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Acid Dagger", ')', 6, 
                        "Mid game weapon. 6 dmg. Apply 4 burn and 4 poison on every hit. Slash, Fire, Poison damage.",
                        attack_traits=[Trait.SLASH, Trait.FIRE, Trait.POISON])
    
    def on_hit(self, attacker, target):
        """Apply burn and poison when hitting a target."""
        messages = []
        if hasattr(target, 'status_effects'):
            if target.status_effects.apply_status('burn', 4, target):
                messages.append(f"{target.name if hasattr(target, 'name') else 'The target'} is burned by acid!")
            if target.status_effects.apply_status('poison', 4, target):
                messages.append(f"{target.name if hasattr(target, 'name') else 'The target'} is poisoned!")
        return " ".join(messages) if messages else None