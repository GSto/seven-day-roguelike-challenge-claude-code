"""
Dodge Master Ring accessory - gains +1% CRT bonus on every successful dodge.
"""

from .accessory import Accessory
from constants import COLOR_YELLOW
from event_type import EventType
from event_context import AttackContext

class DodgeMasterRing(Accessory):
    """A ring that rewards evasive combat with increased critical hit chance."""
    
    def __init__(self, x, y):
        super().__init__(
            x, y,
            name="Dodge Master Ring",
            char="o",
            description="Gains +1% CRT bonus for each successful dodge",
        )
        self.market_value = 45  # Uncommon rarity
        self.color = COLOR_YELLOW
        
        # Track accumulated dodge bonus
        self.dodge_count = 0
        
        # Subscribe to dodge events
        self.event_subscriptions.add(EventType.SUCCESSFUL_DODGE)
    
    def on_event(self, event_type, context):
        """Handle successful dodge events."""
        if event_type == EventType.SUCCESSFUL_DODGE and isinstance(context, AttackContext):
            # Only count if the player is the one dodging
            if context.defender == context.player:
                self.dodge_count += 1
    
    def get_crit_bonus(self, player):
        """Return critical hit bonus based on dodge count."""
        return self.crit_bonus + (self.dodge_count * 0.01)  # 1% per dodge