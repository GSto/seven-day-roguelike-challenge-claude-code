"""
Consumable items - now organized into subcategories.
This file imports all consumables for backward compatibility.
"""

# Import all consumable subcategories for backward compatibility
from .foods import HealthPotion, Elixir, Beef, Chicken, Carrot, SalmonOfKnowledge, Antidote, ShellPotion, MezzoForte
from .catalysts import (
    PowerCatalyst, DefenseCatalyst, D6, BaronCatalyst, WardenCatalyst, 
    JewelerCatalyst, MagicMushroom, ReapersCatalyst, ShadowsCatalyst,
    FireAttackCatalyst, IceAttackCatalyst, HolyAttackCatalyst, DarkAttackCatalyst,
    FireResistanceCatalyst, IceResistanceCatalyst, HolyResistanceCatalyst, DarkResistanceCatalyst
)
from .boons import (
    BaronsBoon, JewelersBoon, MinersBoon, ClericsBoon, 
    JokersBoon, ReapersBoon
)