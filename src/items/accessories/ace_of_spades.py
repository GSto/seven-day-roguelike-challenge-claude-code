"""
AceOfSpades - Double Attack, Zero Defense.
"""
from .card import Card


class AceOfSpades(Card):
    """Double Attack, Zero Defense"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Ace of Spades", attack_multiplier_bonus=2.0, defense_multiplier_bonus=0.1, description="Are you a gambling man? doubles attack, decimates defense")