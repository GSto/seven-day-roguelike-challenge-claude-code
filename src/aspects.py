from enum import Enum

class AspectType(Enum):
  """aspects that can apply to weapons, armor, accessories, consumables, and monsters"""
  # Physical Damage Types
  SLASH = "Slash"
  STRIKE = "Strike"
  # Elemental Damage Types
  FIRE = "Fire"
  ICE = "Ice"
  DARK = "Dark"
  HOLY = "Holy"
