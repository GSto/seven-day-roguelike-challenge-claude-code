"""
Weapons package for the roguelike game.
"""

from .base import Weapon
from .wooden_stick import WoodenStick
from .dagger import Dagger
from .shield import Shield
from .tower_shield import TowerShield
from .sword import Sword
from .longsword import Longsword
from .war_scythe import WarScythe
from .axe import Axe
from .morning_star import MorningStar
from .war_hammer import WarHammer
from .katana import Katana
from .uchigatana import Uchigatana
from .rivers_of_blood import RiversOfBlood
from .clerics_staff import ClericsStaff
from .materia_staff import MateriaStaff
from .pickaxe import Pickaxe
from .gauntlets import Gauntlets
from .demon_slayer import DemonSlayer
from .snakes_fang import SnakesFang
from .rapier import Rapier
from .acid_dagger import AcidDagger
from .clair_obscur import ClairObscur
from .feu_glace import FeuGlace
from .big_stick import BigStick

# Event-driven weapons
from .defender import Defender
from .holy_avenger import HolyAvenger
from .backhand_blade import BackhandBlade

__all__ = [
    'Weapon',
    'WoodenStick',
    'Dagger', 
    'Shield',
    'TowerShield',
    'Sword',
    'Longsword',
    'WarScythe',
    'Axe',
    'MorningStar', 
    'WarHammer',
    'Katana',
    'Uchigatana',
    'RiversOfBlood',
    'ClericsStaff',
    'MateriaStaff',
    'Pickaxe',
    'Gauntlets',
    'DemonSlayer',
    'SnakesFang',
    'Rapier',
    'AcidDagger',
    'ClairObscur',
    'FeuGlace',
    'BigStick',
    
    # Event-driven weapons
    'Defender',
    'HolyAvenger',
    'BackhandBlade'
]