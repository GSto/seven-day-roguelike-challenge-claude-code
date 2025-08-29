from .base import Monster
from constants import COLOR_GRAY
from traits import Trait


class Bat(Monster):
    """Hard to hit, ephemeral creature."""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Bat",
            char='B',
            color=COLOR_GRAY,
            hp=6,
            attack=2,
            defense=0,
            xp_value=5,
            evade=0.4,
            attack_traits=[Trait.DARK]
        )