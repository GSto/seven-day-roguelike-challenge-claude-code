"""
Base item classes for the roguelike game.
"""

from constants import COLOR_WHITE
from traits import Trait


class Item:
    """Base class for all items."""
    
    def __init__(self, x, y, name, char, color, description=""):
        """Initialize an item."""
        self.x = x
        self.y = y
        self.name = name
        self.char = char
        self.color = color
        self.description = description
    
    def render(self, console, fov):
        """Render the item on the console."""
        if fov[self.x, self.y]:
            console.print(self.x, self.y, self.char, fg=self.color)


class Consumable(Item):
    """Base class for consumable items like potions."""
    
    def __init__(self, x, y, name, char, color, description="", effect_value=0,
                 attack_multiplier_effect=0.0, defense_multiplier_effect=0.0, xp_multiplier_effect=0.0,
                 attack_traits=None, weaknesses=None, resistances=None):
        super().__init__(x, y, name, char, color, description)
        self.effect_value = effect_value
        
        # Multiplier effects (additive to current multipliers)
        self.attack_multiplier_effect = attack_multiplier_effect
        self.defense_multiplier_effect = defense_multiplier_effect
        self.xp_multiplier_effect = xp_multiplier_effect
        
        # Traits system
        self.attack_traits = attack_traits or []
        self.weaknesses = weaknesses or []
        self.resistances = resistances or []
    
    def use(self, player):
        """Use the consumable item. Returns True if successfully used."""
        return False  # Override in subclasses


class Equipment(Item):
    """Base class for equippable items."""
    
    def __init__(self, x, y, name, char, color, description="", 
                 attack_bonus=0, defense_bonus=0, equipment_slot="", 
                 fov_bonus=0, health_aspect_bonus=0.0,
                 attack_multiplier_bonus=1.0, defense_multiplier_bonus=1.0, xp_multiplier_bonus=1.0,
                 evade_bonus=0.0, crit_bonus=0.0, crit_multiplier_bonus=0.0,
                 attack_traits=None, weaknesses=None, resistances=None,
                 xp_cost=5):
        super().__init__(x, y, name, char, color, description)
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.equipment_slot = equipment_slot  # "weapon", "armor", "accessory"
        self.fov_bonus = fov_bonus  # Bonus to field of view radius
        self.health_aspect_bonus = health_aspect_bonus  # Bonus to health potion effectiveness
        
        # Multiplier bonuses (additive to base multiplier of 1.0)
        self.attack_multiplier_bonus = attack_multiplier_bonus
        self.defense_multiplier_bonus = defense_multiplier_bonus
        self.xp_multiplier_bonus = xp_multiplier_bonus
        
        # Combat modifiers
        self.evade_bonus = evade_bonus  # Bonus to evade chance
        self.crit_bonus = crit_bonus  # Bonus to critical hit chance
        self.crit_multiplier_bonus = crit_multiplier_bonus  # Bonus to critical hit multiplier
        
        # XP cost to equip this item
        self.xp_cost = xp_cost
        
        # Traits system
        self.attack_traits = attack_traits or []
        self.weaknesses = weaknesses or []
        self.resistances = resistances or []
    
    def get_attack_bonus(self, player):
          return self.attack_bonus
    
    def get_defense_bonus(self, player):
        return self.defense_bonus
    
    def get_fov_bonus(self, player):
        return self.fov_bonus
    
    def get_health_aspect_bonus(self, player):
        return self.health_aspect_bonus
    
    def get_attack_multiplier_bonus(self, player):
        return self.attack_multiplier_bonus
    
    def get_defense_multiplier_bonus(self, player):
        return self.defense_multiplier_bonus
    
    def get_xp_multiplier_bonus(self, player):
        return self.xp_multiplier_bonus
    
    def get_evade_bonus(self, player):
        return self.evade_bonus
    
    def get_crit_bonus(self, player):
        return self.crit_bonus
    
    def get_crit_multiplier_bonus(self, player):
        return self.crit_multiplier_bonus
    

    def get_attack_traits(self):
        """Get all attack traits including those from enchantments."""
        traits = list(self.attack_traits)  # Copy base traits
        
        # Add traits from enchantments if this item has them
        if hasattr(self, 'enchantments'):
            for enchantment in self.enchantments:
                if hasattr(enchantment, 'attack_traits'):
                    traits.extend(enchantment.attack_traits)
        
        return traits
    
    def get_weaknesses(self):
        """Get all weaknesses including those from enchantments."""
        weaknesses = list(self.weaknesses)  # Copy base weaknesses
        
        # Add weaknesses from enchantments if this item has them
        if hasattr(self, 'enchantments'):
            for enchantment in self.enchantments:
                if hasattr(enchantment, 'weaknesses'):
                    weaknesses.extend(enchantment.weaknesses)
        
        return weaknesses
    
    def get_resistances(self):
        """Get all resistances including those from enchantments."""
        resistances = list(self.resistances)  # Copy base resistances
        
        # Add resistances from enchantments if this item has them
        if hasattr(self, 'enchantments'):
            for enchantment in self.enchantments:
                if hasattr(enchantment, 'resistances'):
                    resistances.extend(enchantment.resistances)
        
        return resistances
  
    
    def can_equip(self, player):
        """Check if player can equip this item."""
        # Check if player has enough XP to equip this item
        return player.xp >= self.xp_cost