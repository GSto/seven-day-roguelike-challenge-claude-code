"""
AceOfSpades - Double Attack, Zero Defense.
"""
from .card import Card


class AceOfSpades(Card):
    """Increased Attack, Zero Defense"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Ace of Spades", attack_multiplier_bonus=1.5, defense_multiplier_bonus=0, description="Are you a gambling man? doubles attack, decimates defense")