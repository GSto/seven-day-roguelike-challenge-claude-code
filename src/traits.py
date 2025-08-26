from enum import Enum, auto


class Trait(Enum):
    # elemental types
    FIRE = auto()
    ICE = auto()
    HOLY = auto()
    DARK = auto()
    POISON = auto()
    # physical 
    STRIKE = auto()
    SLASH = auto()
    THWACK = auto()

    # specialty types
    MYSTIC = auto()
    DEMONSLAYER = auto()

    def __str__(self):
        return self.name.lower()
    
    @property
    def is_elemental(self):
        """Return True if this trait is elemental (fire, ice, holy, dark, poison)."""
        return self in {Trait.FIRE, Trait.ICE, Trait.HOLY, Trait.DARK, Trait.POISON}
    
    @property
    def is_physical(self):
        return self in {Trait.SLASH, Trait.STRIKE, Trait.THWACK}
    
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