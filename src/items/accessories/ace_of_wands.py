from .card import Card
from event_emitter import EventEmitter
from event_type import EventType
from event_context import HealContext


class AceOfWands(Card):
    def __init__(self, x, y):
        super().__init__(x, y, "Ace of Wands", 
                        description="Grants +10 XP whenever the player heals")
        self.market_value = 45  # Uncommon card accessory
        self.event_subscriptions.add(EventType.PLAYER_HEAL)

    def on_event(self, event_type, context):
        """Handle subscribed events."""
        if event_type == EventType.PLAYER_HEAL and isinstance(context, HealContext):
            # Award 10 XP whenever the player heals
            context.player.gain_xp(10)