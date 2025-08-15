from enum import Enum, auto


class Trait(Enum):
    FIRE = auto()
    ICE = auto()
    HOLY = auto()
    DARK = auto()
    POISON = auto()
    STRIKE = auto()
    SLASH = auto()
    DEMONSLAYER = auto()
    MYSTIC = auto()

    def __str__(self):
        return self.name.lower()
    
    @property
    def is_elemental(self):
        """Return True if this trait is elemental (fire, ice, holy, dark, poison)."""
        return self in {Trait.FIRE, Trait.ICE, Trait.HOLY, Trait.DARK, Trait.POISON}
    
    @property
    def opposing_element(self):
        """Return the opposing elemental trait if this is elemental."""
        if not self.is_elemental:
            return None
        
        opposites = {
            Trait.FIRE: Trait.ICE,
            Trait.ICE: Trait.FIRE,
            Trait.HOLY: Trait.DARK,
            Trait.DARK: Trait.HOLY
        }
        return opposites.get(self)