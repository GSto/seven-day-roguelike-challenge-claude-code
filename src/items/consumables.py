"""
Consumable items - now organized into subcategories.
This file imports all consumables for backward compatibility.
"""

# Import everything from the new consumables package
from .consumables import *

# Import the miscellaneous items that were originally in this file
from .consumables.d6 import D6
from .consumables.mayhems_boon import MayhemsBoon
from .consumables.compass import Compass
from .consumables.map import Map
from .consumables.bomb import Bomb
from .consumables.swords_to_plowshares import SwordsToPlowshares
from .consumables.transmutation import Transmutation

# For backward compatibility, also import from old structure
from .foods import *
from .catalysts import *
from .boons import *