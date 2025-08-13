from enum import Enum, auto


class Trait(Enum):
    FIRE = auto()
    ICE = auto()
    HOLY = auto()
    DARK = auto()
    STRIKE = auto()
    SLASH = auto()
    DEMONSLAYER = auto()

    def __str__(self):
        return self.name.lower()