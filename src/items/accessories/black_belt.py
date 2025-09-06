"""
Black Belt accessory - gains +1% EVD bonus on every critical hit.
"""

from .accessory import Accessory
from constants import COLOR_WHITE
from event_type import EventType
from event_context import AttackContext

class BlackBelt(Accessory):
    """An accessory that gains EVD bonus from critical hits."""
    
    def __init__(self, x, y):
        super().__init__(
            x, y,
            name="Black Belt",
            char="=",
            description="Gains +1% EVD bonus per critical hit",
        )
        self.market_value = 25  # Common rarity
        self.color = COLOR_WHITE
        
        # Track accumulated bonus
        self.crit_count = 0
        
        # Subscribe to critical hit events
        self.event_subscriptions.add(EventType.CRITICAL_HIT)
    
    def on_event(self, event_type, context):
        """Handle critical hit events."""
        if event_type == EventType.CRITICAL_HIT and isinstance(context, AttackContext):
            # Only count if the player is the one getting the critical hit
            if context.attacker == context.player:
                self.crit_count += 1
    
    def get_evade_bonus(self, player):
        """Return evade bonus based on critical hit count."""
        return self.evade_bonus + (self.crit_count * 0.01)  # 1% per critical hit