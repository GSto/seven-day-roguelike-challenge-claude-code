"""
Catalyst consumables that permanently modify player stats and traits.
This file now imports from the new consumables/ directory for backward compatibility.
"""

# Import all catalyst-related consumables from the new structure
from .consumables.catalyst import Catalyst
from .consumables.power_catalyst import PowerCatalyst
from .consumables.defense_catalyst import DefenseCatalyst
from .consumables.baron_catalyst import BaronCatalyst
from .consumables.warden_catalyst import WardenCatalyst
from .consumables.jeweler_catalyst import JewelerCatalyst
from .consumables.reapers_catalyst import ReapersCatalyst
from .consumables.shadows_catalyst import ShadowsCatalyst
from .consumables.fire_resistance_catalyst import FireResistanceCatalyst
from .consumables.ice_resistance_catalyst import IceResistanceCatalyst
from .consumables.holy_resistance_catalyst import HolyResistanceCatalyst
from .consumables.dark_resistance_catalyst import DarkResistanceCatalyst

# Re-export for backward compatibility
__all__ = [
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
]