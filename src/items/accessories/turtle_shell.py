"""
TurtleShell - +6 DEF -6 ATK.
"""
from .hat import Hat


class TurtleShell(Hat):
    """+6 DEF -6 ATK."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Turtle Shell", 
                        description="+6 DEF, -6 ATK")
    
    def get_attack_bonus(self, player):
        return super().get_attack_bonus(player) - 6
    
    def get_defense_bonus(self, player):
        return super().get_defense_bonus(player) + 6