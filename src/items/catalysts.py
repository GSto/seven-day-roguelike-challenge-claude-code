"""
Catalyst consumables that permanently modify player stats and traits.
"""

from constants import COLOR_RED, COLOR_BLUE, COLOR_ORANGE, COLOR_SALMON, COLOR_WHITE, COLOR_YELLOW, COLOR_GREEN, COLOR_CYAN
from .base import Consumable
from traits import Trait

# ============================================================================
# BUFF CATALYSTS - Permanently increase stats
# ============================================================================
class Catalyst(Consumable):
    """Base class for catalysts that have HP costs based on catalyst tax."""
    
    def __init__(self, x, y, name, char, color, description="", effect_value=0,
                 attack_multiplier_effect=0.0, defense_multiplier_effect=0.0, xp_multiplier_effect=0.0,
                 attack_traits=None, weaknesses=None, resistances=None):
        super().__init__(x, y, name, char, color, description, effect_value,
                         attack_multiplier_effect, defense_multiplier_effect, xp_multiplier_effect,
                         attack_traits, weaknesses, resistances)
    
    def get_catalyst_hp_cost(self, player):
        """Calculate HP cost based on player's catalyst tax."""
        return int(player.max_hp * player.catalyst_tax)
    
    def get_description_with_cost(self, player):
        """Get description including HP cost information."""
        hp_cost = self.get_catalyst_hp_cost(player)
        cost_text = f" (Cost: {hp_cost} HP)"
        return self.description + cost_text
    
    def use(self, player):
        """Apply catalyst tax before using - override in subclasses."""
        hp_cost = self.get_catalyst_hp_cost(player)
        
        # Check if player has enough HP (must leave at least 1 HP)
        if player.hp <= hp_cost:
            return (False, f"You need at least {hp_cost + 1} HP to use this catalyst!")
        
        # Apply HP cost and increase tax
        player.hp -= hp_cost
        player.catalyst_tax += 0.05  # Increase tax by 5%
        
        # Call subclass implementation
        return self._apply_catalyst_effect(player, hp_cost)
    
    def _apply_catalyst_effect(self, player, hp_cost):
        """Override this method in subclasses to implement catalyst effects."""
        return (False, "Catalyst effect not implemented!")


class PowerCatalyst(Catalyst):
    """Permanently increases attack power"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Warrior's Catalyst",
            char='*',
            color=COLOR_RED,
            description="Permanently increases attack by 1",
            effect_value=1
        )
    
    def _apply_catalyst_effect(self, player, hp_cost):
        """Permanently increase player's attack"""
        player.attack += self.effect_value
        return (True, f"You feel more powerful! Attack +{self.effect_value} (Cost: {hp_cost} HP)")


class DefenseCatalyst(Catalyst):
    """Permanently increases defense"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Defender's Catalyst",
            char='*',
            color=COLOR_BLUE,
            description="Permanently increases defense by 1",
            effect_value=1
        )
    
    def _apply_catalyst_effect(self, player, hp_cost):
        """Permanently increase player's defense"""
        player.defense += self.effect_value
        return (True, f"You feel more protected! Defense +{self.effect_value} (Cost: {hp_cost} HP)")


class BaronCatalyst(Catalyst):
    """Permanently increases attack multiplier by 10%"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Baron's Catalyst",
            char='!',
            color=COLOR_YELLOW,
            description="Permanently increases attack multiplier by 10%",
            effect_value=0.1,
            attack_multiplier_effect=1.1
        )
    
    def _apply_catalyst_effect(self, player, hp_cost):
        """Permanently increase player's attack multiplier"""
        player.attack_multiplier *= self.attack_multiplier_effect
        return (True, f"Your attacks become more effective! Attack multiplier increased by {int((self.attack_multiplier_effect-1)*100)}% (Cost: {hp_cost} HP)")


class WardenCatalyst(Catalyst):
    """Permanently increases defense multiplier by 10%"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Warden's Catalyst",
            char='!',
            color=COLOR_BLUE,
            description="Permanently increases defense multiplier by 10%",
            effect_value=0.1,
            defense_multiplier_effect=1.1
        )
    
    def _apply_catalyst_effect(self, player, hp_cost):
        """Permanently increase player's defense multiplier"""
        player.defense_multiplier *= self.defense_multiplier_effect
        return (True, f"Your defenses become more effective! Defense multiplier increased by {int((self.defense_multiplier_effect-1)*100)}% (Cost: {hp_cost} HP)")


class JewelerCatalyst(Catalyst):
    """Permanently increases XP multiplier by 20%"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Jeweler's Catalyst",
            char='!',
            color=COLOR_WHITE,
            description="Permanently increases XP multiplier by 5%",
            effect_value=0.05,
            xp_multiplier_effect=1.05
        )
    
    def _apply_catalyst_effect(self, player, hp_cost):
        """Permanently increase player's XP multiplier"""
        player.xp_multiplier *= self.xp_multiplier_effect
        return (True, f"You learn more efficiently! XP multiplier increased by {int((self.xp_multiplier_effect-1)*100)}% (Cost: {hp_cost} HP)")

class ReapersCatalyst(Catalyst):
    """Permanently increases crit chance"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Reaper's Catalyst",
            char='*',
            color=COLOR_RED,
            description="Permanently increases crit chance by 5%",
            effect_value=0.05
        )
    
    def _apply_catalyst_effect(self, player, hp_cost):
        """Permanently increase player's crit chance"""
        player.crit += self.effect_value
        return (True, f"You feel deadlier! Crit chance +{int(self.effect_value * 100)}% (Cost: {hp_cost} HP)")

class ShadowsCatalyst(Catalyst):
    """Permanently increases evade chance"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Shadow's Catalyst",
            char='*',
            color=COLOR_BLUE,
            description="Permanently increases evade chance by 5%",
            effect_value=0.05
        )
    
    def _apply_catalyst_effect(self, player, hp_cost):
        """Permanently increase player's evade chance"""
        player.evade += self.effect_value
        return (True, f"You feel more agile! Evade chance +{int(self.effect_value * 100)}% (Cost: {hp_cost} HP)")




# ============================================================================
# ELEMENTAL RESISTANCE CATALYSTS - Permanently add resistance traits
# ============================================================================

class FireResistanceCatalyst(Catalyst):
    """Permanently adds Fire resistance"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Salamander Catalyst",
            char='*',
            color=COLOR_ORANGE,
            description="Permanently adds Fire resistance",
            effect_value=1
        )
    
    def _apply_catalyst_effect(self, player, hp_cost):
        """Add Fire resistance to player"""
        if Trait.FIRE not in player.resistances:
            player.resistances.append(Trait.FIRE)
        return (True, f"You feel protected against fire! (Cost: {hp_cost} HP)")


class IceResistanceCatalyst(Catalyst):
    """Permanently adds Ice resistance"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Yeti Catalyst",
            char='*',
            color=COLOR_BLUE,
            description="Permanently adds Ice resistance",
            effect_value=1
        )
    
    def _apply_catalyst_effect(self, player, hp_cost):
        """Add Ice resistance to player"""
        if Trait.ICE not in player.resistances:
            player.resistances.append(Trait.ICE)
        return (True, f"You feel protected against ice! (Cost: {hp_cost} HP)")


class HolyResistanceCatalyst(Catalyst):
    """Permanently adds Holy resistance"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Angel Catalyst",
            char='*',
            color=COLOR_WHITE,
            description="Permanently adds Holy resistance",
            effect_value=1
        )
    
    def _apply_catalyst_effect(self, player, hp_cost):
        """Add Holy resistance to player"""
        if Trait.HOLY not in player.resistances:
            player.resistances.append(Trait.HOLY)
        return (True, f"You feel protected against holy light! (Cost: {hp_cost} HP)")


class DarkResistanceCatalyst(Catalyst):
    """Permanently adds Dark resistance"""
    
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            name="Demon Catalyst",
            char='*',
            color=COLOR_SALMON,
            description="Permanently adds Dark resistance",
            effect_value=1
        )
    
    def _apply_catalyst_effect(self, player, hp_cost):
        """Add Dark resistance to player"""
        if Trait.DARK not in player.resistances:
            player.resistances.append(Trait.DARK)
        return (True, f"You feel protected against darkness! (Cost: {hp_cost} HP)")