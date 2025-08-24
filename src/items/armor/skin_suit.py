"""
Skin Suit armor for the roguelike game.
"""

from .base import Armor
from event_type import EventType
from event_context import DeathContext


class SkinSuit(Armor):
    """+1 DEF for every 4 enemies slain."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Skin Suit", '[', 0, description="+1 DEF for every 4 enemies slain")
        # Internal counter for enemies slain while equipped
        self.death_counter = 0
        # Subscribe to monster death events
        self.event_subscriptions.add(EventType.MONSTER_DEATH)

    def on_event(self, event_type, context):
        """Handle monster death events."""
        if event_type == EventType.MONSTER_DEATH and isinstance(context, DeathContext):
            # Increment internal counter when monsters die
            self.death_counter += 1

    def get_defense_bonus(self, player):
        # Use both the player's historical body count (for kills before equipping)
        # and the internal counter (for kills while equipped)
        total_kills = player.body_count + self.death_counter
        return super().get_defense_bonus(player) + int(total_kills / 4)