"""
Black Belt accessory - provides dynamic bonuses based on combat performance.
"""

from .accessory import Accessory
from constants import COLOR_BLACK
from event_type import EventType
from event_context import AttackContext

class BlackBelt(Accessory):
    """A martial arts belt that grows stronger through combat mastery."""
    
    def __init__(self, x, y):
        super().__init__(
            x, y,
            name="Black Belt",
            char="⌐",
            description="Gains +1% Critical chance per dodge, +1% EVD per critical hit",
            evade_bonus=0.0,
            crit_bonus=0.0
        )
        self.market_value = 75  # Rare accessory
        self.color = COLOR_BLACK
        
        # Track accumulated bonuses (stored on the item)
        self.dodge_count = 0  # Number of successful dodges
        self.crit_count = 0   # Number of critical hits
        
        # Store base description for dynamic updates
        self._base_description = self.description
        
        # Subscribe to combat events
        self.event_subscriptions.add(EventType.SUCCESSFUL_DODGE)
        self.event_subscriptions.add(EventType.CRITICAL_HIT)
    
    def on_event(self, event_type, context):
        """Handle combat events to accumulate bonuses."""
        if not isinstance(context, AttackContext):
            return
            
        if event_type == EventType.SUCCESSFUL_DODGE:
            # Check if the player (wearing this belt) is the one dodging
            if context.defender == context.player and self in context.player.equipment_list:
                self.dodge_count += 1
                # Update the critical bonus based on dodge count
                self.crit_bonus = self.dodge_count * 0.01  # +1% per dodge
                self._update_description()
                
        elif event_type == EventType.CRITICAL_HIT:
            # Check if the player (wearing this belt) is the one scoring the critical
            if context.attacker == context.player and self in context.player.equipment_list:
                self.crit_count += 1
                # Update the evade bonus based on critical hit count
                self.evade_bonus = self.crit_count * 0.01  # +1% EVD per crit
                self._update_description()
    
    def _update_description(self):
        """Update the description with current bonus counts."""
        if self.dodge_count > 0 or self.crit_count > 0:
            bonus_desc = f" (Dodges: {self.dodge_count}, Crits: {self.crit_count})"
            self.description = self._base_description + bonus_desc
        else:
            self.description = self._base_description