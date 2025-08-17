"""
Deals 30 damage to all enemies in a 3 block radius.
"""

from constants import COLOR_WHITE
from ..consumable import Consumable


class Bomb(Consumable):
    """Deals 30 damage to all enemies in a 3 block radius"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Bomb",
            char='o',
            color=COLOR_WHITE,
            description="Deals 30 damage to all enemies in a 3 block radius"
        )
    
    def use(self, player):
        """Deal damage to nearby enemies"""
        # This requires access to the current level's monsters
        # Since we don't have direct access to the level here, we'll need to check
        # if the player object has a reference to the current level/game state
        if not hasattr(player, '_current_level') or player._current_level is None:
            return (False, "Unable to detonate bomb - no enemies detected!")
        
        level = player._current_level
        damage_dealt = 30
        radius = 3
        enemies_hit = 0
        
        # Find all monsters within radius
        for monster in level.monsters:
            distance = monster.distance_to(player.x, player.y)
            if distance <= radius:
                monster.take_damage(damage_dealt)
                enemies_hit += 1
        
        # Remove dead monsters
        level.remove_dead_monsters()
        
        if enemies_hit == 0:
            return (True, "BOOM! The bomb explodes, but no enemies were in range.")
        elif enemies_hit == 1:
            return (True, f"BOOM! The bomb explodes, dealing {damage_dealt} damage to 1 enemy!")
        else:
            return (True, f"BOOM! The bomb explodes, dealing {damage_dealt} damage to {enemies_hit} enemies!")