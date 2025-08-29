"""
PsychicsTurban - +1 ATK for every consumable used.
"""
from .hat import Hat
from event_type import EventType
from event_context import ConsumeContext


class PsychicsTurban(Hat):
    """+1 ATK for every consumable used."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Psychic's Turban", 
        description="+1 ATK for each consumable used")
        self.market_value = 38  # Uncommon accessory
        # Internal counter for consumables used while equipped
        self.consumable_counter = 0
        # Subscribe to consume events
        self.event_subscriptions.add(EventType.PLAYER_CONSUME_ITEM)
    
    def on_event(self, event_type, context):
        """Handle consumable use events."""
        if event_type == EventType.PLAYER_CONSUME_ITEM and isinstance(context, ConsumeContext):
            # Increment internal counter when consumables are used
            self.consumable_counter += 1
    
    def get_attack_bonus(self, player):
        # Use both the player's historical consumable count (for items used before equipping)
        # and the internal counter (for items used while equipped)
        return super().get_attack_bonus(player) + player.consumable_count + self.consumable_counter