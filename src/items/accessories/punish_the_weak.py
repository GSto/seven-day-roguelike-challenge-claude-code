"""
PunishTheWeak - Deal 25% more damage to enemies with negative status effects.
"""
from .accessory import Accessory


class PunishTheWeak(Accessory):
    """Deal 25% more damage to enemies with negative status effects."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Punish the Weak", '=',
        description="-1 DEF. Deal 25% more damage to targets with negative status effects",
                        defense_bonus=-1)
        self.market_value = 25  # Common accessory
    
    def get_damage_multiplier_vs_target(self, target):
        """Get damage multiplier when attacking a specific target."""
        if hasattr(target, 'status_effects') and target.status_effects.has_negative_effects():
            return 1.25  # 25% more damage
        return 1.0