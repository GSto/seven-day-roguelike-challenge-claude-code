"""
Consumable items - now organized into subcategories.
This file imports all consumables for backward compatibility.
"""

# Import all consumable subcategories for backward compatibility
import random
from constants import COLOR_WHITE
from .foods import HealthPotion, Elixir, Beef, Chicken, Carrot, SalmonOfKnowledge, Antidote, ShellPotion, MezzoForte, MagicMushroom
from .catalysts import (
    PowerCatalyst, DefenseCatalyst, BaronCatalyst, WardenCatalyst, 
    JewelerCatalyst, ReapersCatalyst, ShadowsCatalyst,
    FireAttackCatalyst, IceAttackCatalyst, HolyAttackCatalyst, DarkAttackCatalyst,
    FireResistanceCatalyst, IceResistanceCatalyst, HolyResistanceCatalyst, DarkResistanceCatalyst
)
from .boons import (
    BaronsBoon, JewelersBoon, MinersBoon, ClericsBoon, 
    JokersBoon, ReapersBoon
)

from .base import Consumable
from .catalysts import Catalyst

class D6(Catalyst):
    """Random effect dice with 6 possible outcomes"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="D6",
            char='6',
            color=COLOR_WHITE,
            description="Roll for one of 6 random effects:\n +1 Attack, +1 Defense, +10 max HP, +1 FOV, or -20 max HP",
            effect_value=1
        )
    
    def _apply_catalyst_effect(self, player, hp_cost):
        """Apply one of 6 random effects"""
        roll = random.randint(1, 6)
        
        if roll == 5:
            # +1 Attack
            player.attack += 1
            return (True, f"Rolled {roll}! Attack +1 (Cost: {hp_cost} HP)")
        elif roll == 2:
            # +1 Defense
            player.defense += 1
            return (True, f"Rolled {roll}! Defense +1 (Cost: {hp_cost} HP)")
        elif roll == 3:
            # +10 max HP
            old_max = player.max_hp
            player.max_hp += 10
            player.hp += (player.max_hp - old_max)  # Heal the difference
            return (True, f"Rolled {roll}! Max HP +10 (Cost: {hp_cost} HP)")
        elif roll == 4:
            # +3 FOV
            player.fov += 1
            return (True, f"Rolled {roll}! FOV +3 (Cost: {hp_cost} HP)")
        elif roll == 1:
            # -20 max HP (but don't kill the player)
            if player.max_hp > 25:  # Ensure player doesn't die from this
                player.max_hp -= 20
                if player.hp > player.max_hp:
                    player.hp = player.max_hp
                return (True, f"Rolled {roll}! Max HP -20 (ouch!) (Cost: {hp_cost} HP)")
            else:
                return (True, f"Rolled {roll}! But you're too weak for the penalty to apply. (Cost: {hp_cost} HP)")
        else:  # roll == 6
            # Duplicate effect - +1 Attack (making it slightly more likely to be positive)
            player.attack += 1
            return (True, f"Rolled {roll}! Attack +1 (Cost: {hp_cost} HP)")