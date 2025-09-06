from .accessory import Accessory


class AceOfCoins(Accessory):
    def __init__(self, x, y):
        super().__init__(
            x=x, 
            y=y, 
            name="Ace of Coins",
            char="#",  # Card character
            xp_multiplier_bonus=1.2,  # +20% XP multiplier (1.0 + 0.2)
            description="Provides +20% XP multiplier bonus"
        )
        self.market_value = 80  # High value due to powerful XP bonus