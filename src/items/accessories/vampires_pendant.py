"""
Vampire's Pendant accessory - heals when monsters die.
"""

from .accessory import Accessory
from constants import COLOR_RED
from event_type import EventType
from event_context import DeathContext
from traits import Trait

class VampiresPendant(Accessory):
    """An accessory that heals the player when monsters die."""
    
    def __init__(self, x, y):
        super().__init__(
            x, y,
            name="Vampire's Pendant",
            char="♦",
            description="Heals 5% max health when a monster dies",
            
            attack_traits=[Trait.DARK]
        )
        self.market_value = 50  # Rare accessory
        self.color = COLOR_RED
        # Subscribe to monster death events
        self.event_subscriptions.add(EventType.MONSTER_DEATH)
    
    def on_event(self, event_type, context):
        """Handle monster death events."""
        if event_type == EventType.MONSTER_DEATH and isinstance(context, DeathContext):
            heal_amount = int(context.player.max_hp * 0.05)  # 5% max health
            if heal_amount > 0:
                context.player.heal(heal_amount)