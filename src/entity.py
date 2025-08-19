"""
Base Entity class for Player and Monster.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from traits import Trait
from status_effects import StatusEffects
from stats import Stats, StatType


@dataclass
class Entity:
    """Base class for all entities (Player and Monster)."""
    
    x: int
    y: int
    character: str
    color: Tuple[int, int, int]
    stats: Stats
    attack_traits: List[Trait] = field(default_factory=list)
    weaknesses: List[Trait] = field(default_factory=list)
    resistances: List[Trait] = field(default_factory=list)
    status_effects: StatusEffects = field(default_factory=StatusEffects)
    
    @property
    def max_hp(self):
        return self.stats.get_stat(StatType.MAX_HP)
    
    @max_hp.setter
    def max_hp(self, value):
        self.stats.set_stat(StatType.MAX_HP, value)
    
    @property
    def hp(self):
        return self.stats.get_stat(StatType.HP)
    
    @hp.setter
    def hp(self, value):
        self.stats.set_stat(StatType.HP, value)
    
    @property
    def attack(self):
        return self.stats.get_stat(StatType.ATTACK)
    
    @attack.setter
    def attack(self, value):
        self.stats.set_stat(StatType.ATTACK, value)
    
    @property
    def defense(self):
        return self.stats.get_stat(StatType.DEFENSE)
    
    @defense.setter
    def defense(self, value):
        self.stats.set_stat(StatType.DEFENSE, value)
    
    @property
    def evade(self):
        return self.stats.get_stat(StatType.EVADE)
    
    @evade.setter
    def evade(self, value):
        self.stats.set_stat(StatType.EVADE, value)
    
    @property
    def crit(self):
        return self.stats.get_stat(StatType.CRIT)
    
    @crit.setter
    def crit(self, value):
        self.stats.set_stat(StatType.CRIT, value)
    
    @property
    def crit_multiplier(self):
        return self.stats.get_stat(StatType.CRIT_MULTIPLIER)
    
    @crit_multiplier.setter
    def crit_multiplier(self, value):
        self.stats.set_stat(StatType.CRIT_MULTIPLIER, value)
    
    @property
    def attack_multiplier(self):
        return self.stats.get_stat(StatType.ATTACK_MULTIPLIER)
    
    @attack_multiplier.setter
    def attack_multiplier(self, value):
        self.stats.set_stat(StatType.ATTACK_MULTIPLIER, value)
    
    @property
    def defense_multiplier(self):
        return self.stats.get_stat(StatType.DEFENSE_MULTIPLIER)
    
    @defense_multiplier.setter
    def defense_multiplier(self, value):
        self.stats.set_stat(StatType.DEFENSE_MULTIPLIER, value)
    
    def take_damage(self, damage: int) -> int:
        """Take damage, accounting for defense."""
        actual_damage = max(1, damage - self.stats.get_stat(StatType.DEFENSE))
        self.stats.set_stat(StatType.HP, max(0, self.stats.get_stat(StatType.HP) - actual_damage))
        return actual_damage
    
    def take_damage_with_traits(self, damage: int, attack_traits: Optional[List[Trait]] = None) -> int:
        """Take damage with trait consideration for resistances/weaknesses."""
        if attack_traits is None:
            attack_traits = []
        
        # Check for trait interactions
        final_damage = damage
        
        for trait in attack_traits:
            if trait in self.resistances:
                final_damage = int(final_damage * 0.5)  # 50% damage if resistant
            elif trait in self.weaknesses:
                final_damage = int(final_damage * 2.0)  # 200% damage if weak
        
        # Apply normal damage calculation
        actual_damage = max(1, final_damage - self.stats.get_stat(StatType.DEFENSE))
        self.stats.set_stat(StatType.HP, max(0, self.stats.get_stat(StatType.HP) - actual_damage))
        return actual_damage
    
    def is_alive(self) -> bool:
        """Check if the entity is alive."""
        return self.stats.get_stat(StatType.HP) > 0
    
    def move(self, dx: int, dy: int) -> None:
        """Move the entity by dx, dy."""
        self.x += dx
        self.y += dy
    
    def render(self, console, fov) -> None:
        """Render the entity on the console."""
        if fov[self.x, self.y]:
            console.print(self.x, self.y, self.character, fg=self.color)