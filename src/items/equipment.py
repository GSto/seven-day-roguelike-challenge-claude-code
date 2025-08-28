"""
Equipment item class for the roguelike game.
"""

from .item import Item
from typing import Set, TYPE_CHECKING

if TYPE_CHECKING:
    from event_type import EventType
    from event_context import EventContext


class Equipment(Item):
    """Base class for equippable items."""
    
    def __init__(self, x, y, name, char, color, description="", 
                 attack_bonus=0, defense_bonus=0, equipment_slot="", 
                 fov_bonus=0, health_aspect_bonus=0.0,
                 attack_multiplier_bonus=1.0, defense_multiplier_bonus=1.0, xp_multiplier_bonus=1.0,
                 evade_bonus=0.0, crit_bonus=0.0, crit_multiplier_bonus=0.0,
                 attack_traits=None, weaknesses=None, resistances=None,
                 xp_cost=5, is_cleanup=False):
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
        
        # Cleanup step - if True, effects are calculated after all other equipment
        self.is_cleanup = is_cleanup
        
        # Set proper market value for equipment
        self.market_value = self.get_default_market_value()
        
        # Traits system
        self.attack_traits = attack_traits or []
        self.weaknesses = weaknesses or []
        self.resistances = resistances or []
        
        # Event system
        self.event_subscriptions: Set['EventType'] = set()  # Events this equipment listens to
    
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
    
    def on_event(self, event_type: 'EventType', context: 'EventContext') -> None:
        """Handle an event. Override in subclasses to implement specific behavior."""
        pass
    
    def get_subscribed_events(self) -> Set['EventType']:
        """Get the events this equipment wants to listen to. Override in subclasses."""
        return self.event_subscriptions.copy()
    
    def get_default_market_value(self):
        """Get the default market value for equipment."""
        return 25