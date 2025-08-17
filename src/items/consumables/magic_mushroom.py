"""
All stats up +1.
"""

from constants import COLOR_RED
from ..consumable import Consumable


class MagicMushroom(Consumable): 
    """All stats up +1"""

    def __init__(self, x, y):
          super().__init__(
              x=x, y=y,
              name="Magic Mushroom",
              char='m',
              color=COLOR_RED,
              description="Permanently increases XP multiplier by 5%",
              effect_value=1,
              xp_multiplier_effect=1.05
          )
    
    def use(self, player): 
        player.max_hp += 1
        player.attack += 1
        player.defense += 1 
        player.xp += 1
        player.fov += 1
        player.evade += 0.01
        player.crit += 0.01
        player.crit_multiplier += 0.01
        player.health_aspect += 0.01
        player.attack_multiplier += 0.01
        player.defense_multiplier += 0.01
        player.xp_multiplier += 0.01 
        player.status_effects.apply_status('shields', 1)
        return (True, f"all stats up by 1")