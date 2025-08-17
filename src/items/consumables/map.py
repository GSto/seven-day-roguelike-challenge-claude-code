"""
Marks all tiles explored, destroyed when changing floors.
"""

from constants import COLOR_WHITE
from ..consumable import Consumable


class Map(Consumable):
    """Marks all tiles explored, destroyed when changing floors"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Map",
            char='?',
            color=COLOR_WHITE,
            description="Marks all tiles as explored, destroyed when changing floors"
        )
    
    def use(self, player):
        """Reveal entire floor"""
        # This requires access to the current level's explored map
        if not hasattr(player, '_current_level') or player._current_level is None:
            return (False, "Unable to reveal map - no floor detected!")
        
        level = player._current_level
        
        # Mark all tiles as explored
        level.explored.fill(True)
        
        return (True, "The entire floor layout is revealed!")