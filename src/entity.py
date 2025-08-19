"""
Base Entity class for Player and Monster.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from traits import Trait
from status_effects import StatusEffects


@dataclass
class Entity:
    """Base class for all entities (Player and Monster)."""
    
    x: int
    y: int
    character: str
    color: Tuple[int, int, int]
    max_hp: int
    hp: int
    attack: int
    defense: int
    evade: float = 0.05
    crit: float = 0.05
    crit_multiplier: float = 2.0
    attack_multiplier: float = 1.0
    defense_multiplier: float = 1.0
    attack_traits: List[Trait] = field(default_factory=list)
    weaknesses: List[Trait] = field(default_factory=list)
    resistances: List[Trait] = field(default_factory=list)
    status_effects: StatusEffects = field(default_factory=StatusEffects)
    
    def take_damage(self, damage: int) -> int:
        """Take damage, accounting for defense."""
        actual_damage = max(1, damage - self.defense)
        self.hp = max(0, self.hp - actual_damage)
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
        actual_damage = max(1, final_damage - self.defense)
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage
    
    def is_alive(self) -> bool:
        """Check if the entity is alive."""
        return self.hp > 0
    
    def move(self, dx: int, dy: int) -> None:
        """Move the entity by dx, dy."""
        self.x += dx
        self.y += dy
    
    def render(self, console, fov) -> None:
        """Render the entity on the console."""
        if fov[self.x, self.y]:
            console.print(self.x, self.y, self.character, fg=self.color)