"""
Joker - Double or nothing on Everything.
"""
import random
from .card import Card


class Joker(Card):
        def __init__(self, x, y):
          super().__init__(x, y, "Joker", description="Double or nothing on Everything")

        def get_attack_multiplier_bonus(self, player):
            rand = random.random()
            if rand <= 0.5:
              return 2
            else:
              return 0.5
            
        def get_defense_multiplier_bonus(self, player):
            rand = random.random()
            if rand <= 0.5:
              return 2
            else:
              return 0.5
            
        def get_xp_multiplier_bonus(self, player):
            rand = random.random()
            if rand <= 0.5:
              return 2
            else:
              return 0.5