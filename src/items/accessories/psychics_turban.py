"""
PsychicsTurban - +1 ATK for every consumable used.
"""
from .hat import Hat


class PsychicsTurban(Hat):
    """+1 ATK for every consumable used."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Psychic's Turban", 
                        description="+1 ATK for each consumable used")
    
    def get_attack_bonus(self, player):
        return super().get_attack_bonus(player) + player.consumable_count