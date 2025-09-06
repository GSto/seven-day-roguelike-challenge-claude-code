from .accessory import Accessory
from traits import Trait


class AceOfSwords(Accessory):
    def __init__(self, x, y):
        super().__init__(
            x=x, 
            y=y, 
            name="Ace of Swords",
            char="#",  # Card character
            fov_bonus=5,
            attack_traits=None,
            weaknesses=None,
            resistances=[Trait.MYSTIC],
            description="+5 FOV, resistant to mystic damage, immune to blindness"
        )
        self.market_value = 65  # Higher value due to multiple useful bonuses

    def blocks_status_effect(self, effect_name):
        """Check if this accessory blocks a specific status effect."""
        # Immune to blindness
        return effect_name == "blinded"