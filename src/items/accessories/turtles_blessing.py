"""
Turtle's Blessing accessory - gains shield when changing floors.
"""

from .accessory import Accessory
from constants import COLOR_YELLOW
from event_type import EventType
from event_context import FloorContext

class TurtlesBlessing(Accessory):
    """An accessory that gives the player a shield when changing floors."""
    
    def __init__(self, x, y):
        super().__init__(
            x, y,
            name="Turtle's Blessing",
            char="♦",
            description="Gain 1 shield when changing floors",
            xp_cost=15
        )
        self.color = COLOR_YELLOW
        # Subscribe to floor change events
        self.event_subscriptions.add(EventType.FLOOR_CHANGE)
    
    def on_event(self, event_type, context):
        """Handle floor change events."""
        if event_type == EventType.FLOOR_CHANGE and isinstance(context, FloorContext):
            # Add one shield to the player
            context.player.status_effects.shields += 1