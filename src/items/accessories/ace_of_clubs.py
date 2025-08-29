"""
AceOfClubs - +5 Def if 20% HP or less.
"""
from .card import Card


class AceOfClubs(Card):
        def __init__(self, x, y):
          super().__init__(x, y, "Ace of Clubs", description="+5 Def if low HP")
          self.market_value = 38  # Uncommon accessory (card)

        def get_defense_bonus(self, player):
          if(player.has_low_hp()):
              return 5
          else:
              return 0