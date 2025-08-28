"""
Anaglyph - Balances stats. ATK = (ATK+DEF)/2, DEF = (DEF+ATK)/2.
"""
from .accessory import Accessory


class Anaglyph(Accessory):
    """Balances stats. ATK = (ATK+DEF)/2, DEF = (DEF+ATK)/2"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Anaglyph", '=',
                        description="Balances ATK and DEF",
                        is_cleanup=True)
    
    def apply_cleanup_effect(self, player, current_attack, current_defense):
        """Apply the stat balancing effect during cleanup phase."""
        balanced_value = (current_attack + current_defense) // 4
        return balanced_value, balanced_value  # new_attack, new_defense