"""
Consumables package - exports all consumable classes.
"""

# Food consumables
from .health_potion import HealthPotion
from .elixir import Elixir
from .beef import Beef
from .chicken import Chicken
from .carrot import Carrot
from .salmon_of_knowledge import SalmonOfKnowledge
from .antidote import Antidote
from .shell_potion import ShellPotion
from .mezzo_forte import MezzoForte
from .magic_mushroom import MagicMushroom

# Catalyst consumables
from .catalyst import Catalyst
from .power_catalyst import PowerCatalyst
from .defense_catalyst import DefenseCatalyst
from .baron_catalyst import BaronCatalyst
from .warden_catalyst import WardenCatalyst
from .jeweler_catalyst import JewelerCatalyst
from .reapers_catalyst import ReapersCatalyst
from .shadows_catalyst import ShadowsCatalyst
from .fire_resistance_catalyst import FireResistanceCatalyst
from .ice_resistance_catalyst import IceResistanceCatalyst
from .holy_resistance_catalyst import HolyResistanceCatalyst
from .dark_resistance_catalyst import DarkResistanceCatalyst

# Boon consumables
from .boon import Boon
from .barons_boon import BaronsBoon
from .jewelers_boon import JewelersBoon
from .miners_boon import MinersBoon
from .clerics_boon import ClericsBoon
from .jokers_boon import JokersBoon
from .reapers_boon import ReapersBoon
from .fire_boon import FireBoon
from .ice_boon import IceBoon
from .holy_boon import HolyBoon
from .dark_boon import DarkBoon

# Miscellaneous consumables
from .d6 import D6
from .mayhems_boon import MayhemsBoon
from .swords_to_plowshares import SwordsToPlowshares
from .transmutation import Transmutation

__all__ = [
    # Food consumables
    'HealthPotion',
    'Elixir',
    'Beef',
    'Chicken',
    'Carrot',
    'SalmonOfKnowledge',
    'Antidote',
    'ShellPotion',
    'MezzoForte',
    'MagicMushroom',
    
    # Catalyst consumables
    'Catalyst',
    'PowerCatalyst',
    'DefenseCatalyst',
    'BaronCatalyst',
    'WardenCatalyst',
    'JewelerCatalyst',
    'ReapersCatalyst',
    'ShadowsCatalyst',
    'FireResistanceCatalyst',
    'IceResistanceCatalyst',
    'HolyResistanceCatalyst',
    'DarkResistanceCatalyst',
    
    # Boon consumables
    'Boon',
    'BaronsBoon',
    'JewelersBoon',
    'MinersBoon',
    'ClericsBoon',
    'JokersBoon',
    'ReapersBoon',
    'FireBoon',
    'IceBoon',
    'HolyBoon',
    'DarkBoon',
    
    # Miscellaneous consumables
    'D6',
    'MayhemsBoon',
    'SwordsToPlowshares',
    'Transmutation',
]