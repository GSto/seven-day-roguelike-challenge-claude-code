"""
Defender weapon - trades attack for defense when monsters die.
"""

from .base import Weapon
from constants import COLOR_BLUE
from event_type import EventType
from event_context import DeathContext

class Defender(Weapon):
    """A weapon that trades attack for defense when monsters die."""
    
    def __init__(self, x, y):
        super().__init__(
            x, y,
            name="Defender",
            char=")",
            description="Trades ATK for DEF when monsters die (min 1 ATK)",
            attack_bonus=7,
        )
        self.color = COLOR_BLUE
        # Subscribe to monster death events
        self.event_subscriptions.add(EventType.MONSTER_DEATH)
    
    def on_event(self, event_type, context):
        """Handle monster death events."""
        if event_type == EventType.MONSTER_DEATH and isinstance(context, DeathContext):
            # Only trigger if this weapon is equipped
            if context.player.weapon == self:
                # Decrease attack by 1 (minimum 1) and increase defense by 1
                if self.attack_bonus > 1:
                    self.attack_bonus -= 1
                    context.player.defense += 1