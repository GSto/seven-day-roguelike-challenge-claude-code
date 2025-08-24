"""
Devil monster - powerful final boss of the dungeon.
"""

from .base import Monster
from constants import COLOR_RED
from traits import Trait


class Devil(Monster):
    """Powerful devil - final boss of the dungeon."""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Ancient Devil",
            char='D',
            color=COLOR_RED,
            hp=666,      
            attack=30,   
            defense=12,   
            xp_value=666, # Massive XP reward
            evade=0.06,  
            crit=0.06,  
            crit_multiplier=2.06,
            attack_traits=[Trait.DARK, Trait.FIRE],
            weaknesses=[Trait.DEMONSLAYER]
        )
        # Mark this as the final boss
        self.is_final_boss = True