"""
Healing Dodge accessory - heals when successfully dodging attacks.
"""

from .accessory import Accessory
from constants import COLOR_GREEN
from event_type import EventType
from event_context import AttackContext

class HealingDodge(Accessory):
    """An accessory that heals the player when they successfully dodge an attack."""
    
    def __init__(self, x, y):
        super().__init__(
            x, y,
            name="Healing Dodge",
            char="♦",
            description="Heals 5% max health when successfully dodging attacks",
        )
        self.color = COLOR_GREEN
        # Subscribe to dodge events
        self.event_subscriptions.add(EventType.SUCCESSFUL_DODGE)
    
    def on_event(self, event_type, context):
        """Handle successful dodge events."""
        if event_type == EventType.SUCCESSFUL_DODGE and isinstance(context, AttackContext):
            # Only heal if the player is the one dodging
            if context.defender == context.player:
                heal_amount = int(context.player.max_hp * 0.05)  # 5% max health
                if heal_amount > 0:
                    context.player.heal(heal_amount)