"""
Boon consumables that apply enchantments to equipped items.
This file now imports from the new consumables/ directory for backward compatibility.
"""

# Import all boon-related consumables from the new structure
from .consumables.boon import Boon
from .consumables.barons_boon import BaronsBoon
from .consumables.jewelers_boon import JewelersBoon
from .consumables.miners_boon import MinersBoon
from .consumables.clerics_boon import ClericsBoon
from .consumables.jokers_boon import JokersBoon
from .consumables.reapers_boon import ReapersBoon
from .consumables.fire_boon import FireBoon
from .consumables.ice_boon import IceBoon
from .consumables.holy_boon import HolyBoon
from .consumables.dark_boon import DarkBoon

# Re-export for backward compatibility
__all__ = [
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
]