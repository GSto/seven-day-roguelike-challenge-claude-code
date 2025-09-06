"""
GodsEye - FOV +20, Holy attack trait.
"""
from .accessory import Accessory
from traits import Trait


class GodsEye(Accessory):
    """FOV +15, Holy attack trait"""
    
    def __init__(self, x, y):
        super().__init__(x, y, "God's Eye", '=',
        description="FOV +15, Holy attack trait",
                        fov_bonus=20,
                        attack_traits=[Trait.HOLY])
        self.market_value = 38  # Uncommon accessory (legendary)