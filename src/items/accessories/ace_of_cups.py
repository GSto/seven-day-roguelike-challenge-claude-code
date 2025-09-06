from .card import Card
from event_emitter import EventEmitter
from event_type import EventType
from event_context import ConsumeContext


class AceOfCups(Card):
    def __init__(self, x, y):
        super().__init__(x, y, "Ace of Cups", 
                        description="Heals 5 HP whenever the player consumes an item")
        self.market_value = 50  # Uncommon card accessory with healing utility
        self.event_subscriptions.add(EventType.PLAYER_CONSUME_ITEM)

    def on_event(self, event_type, context):
        """Handle subscribed events."""
        if event_type == EventType.PLAYER_CONSUME_ITEM and isinstance(context, ConsumeContext):
            # Heal 5 HP whenever the player consumes any item
            context.player.heal(5)