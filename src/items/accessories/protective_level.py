"""
Protective Level accessory - gains shield when leveling up.
"""

from .accessory import Accessory
from constants import COLOR_CYAN
from event_type import EventType
from event_context import LevelUpContext

class ProtectiveLevel(Accessory):
    """An accessory that gives the player a shield when leveling up."""
    
    def __init__(self, x, y):
        super().__init__(
            x, y,
            name="Protective Level",
            char="♦",
            description="Gain 1 shield when leveling up",
            xp_cost=20
        )
        self.color = COLOR_CYAN
        # Subscribe to level up events
        self.event_subscriptions.add(EventType.LEVEL_UP)
    
    def on_event(self, event_type, context):
        """Handle level up events."""
        if event_type == EventType.LEVEL_UP and isinstance(context, LevelUpContext):
            # Add one shield to the player
            context.player.status_effects.shields += 1