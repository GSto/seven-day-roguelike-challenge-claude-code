"""
Food consumables that provide healing and nutrition.
This file now imports from the new consumables/ directory for backward compatibility.
"""

# Import all food-related consumables from the new structure
from .consumables.health_potion import HealthPotion
from .consumables.elixir import Elixir
from .consumables.beef import Beef
from .consumables.chicken import Chicken
from .consumables.carrot import Carrot
from .consumables.salmon_of_knowledge import SalmonOfKnowledge
from .consumables.antidote import Antidote
from .consumables.shell_potion import ShellPotion
from .consumables.mezzo_forte import MezzoForte
from .consumables.magic_mushroom import MagicMushroom

# Re-export for backward compatibility
__all__ = [
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
]