from typing import Optional, TYPE_CHECKING
from dataclasses import dataclass, field
import time

if TYPE_CHECKING:
    from player import Player
    from monsters.base import Monster
    from items.item import Item

@dataclass
class EventContext:
    player: 'Player'
    timestamp: float = field(default_factory=time.time)

@dataclass
class HealContext(EventContext):
    amount_healed: int = 0

@dataclass
class ConsumeContext(EventContext):
    item_type: str = ""
    item: Optional['Item'] = None

@dataclass
class AttackContext(EventContext):
    attacker: Optional['Player | Monster'] = None
    defender: Optional['Player | Monster'] = None
    damage: int = 0
    is_critical: bool = False
    is_miss: bool = False
    trait_interaction: Optional[str] = None

@dataclass
class DeathContext(EventContext):
    monster: Optional['Monster'] = None
    experience_gained: int = 0

@dataclass
class LevelUpContext(EventContext):
    new_level: int = 0
    stat_increases: dict = field(default_factory=dict)

@dataclass
class FloorContext(EventContext):
    floor_number: int = 0
    previous_floor: int = 0