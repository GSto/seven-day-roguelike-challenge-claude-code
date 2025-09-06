from .accessory import Accessory
from event_emitter import EventEmitter
from event_type import EventType
from event_context import AttackContext


class BrutalityExpertise(Accessory):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            name="Brutality Expertise",
            char="⚔",
            description="A bloodstained belt that grows stronger with each critical strike. +5% critical multiplier per critical hit.",
            market_value=75
        )
        # Override the default market value set by parent constructor
        self.market_value = 75
        self.event_subscriptions.add(EventType.CRITICAL_HIT)
        self.crit_count = 0

    def on_event(self, event_type, context):
        """Handle subscribed events."""
        if event_type == EventType.CRITICAL_HIT and isinstance(context, AttackContext):
            if context.attacker == context.player:  # Only count player critical hits
                self.crit_count += 1

    def get_crit_multiplier_bonus(self, player):
        """Provide +5% critical multiplier per critical hit landed."""
        return self.crit_multiplier_bonus + (self.crit_count * 0.05)

