"""
AceOfClubs - +5 Def if 20% HP or less.
"""
from .card import Card


class AceOfClubs(Card):
        def __init__(self, x, y):
          super().__init__(x, y, "Ace of Clubs", description="+5 Def if 20% HP or less")

        def get_defense_bonus(self, player):
          if(player.hp <= (player.max_hp / 5)):
              return 5
          else:
              return 0