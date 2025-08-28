"""
Backhand Blade weapon - counter-attacks on successful dodges.
"""

from .base import Weapon
from constants import COLOR_BLACK
from traits import Trait
from event_type import EventType
from event_context import AttackContext

class BackhandBlade(Weapon):
    """A weapon that counter-attacks when the player successfully dodges."""
    
    def __init__(self, x, y):
        super().__init__(
            x, y,
            name="Backhand Blade",
            char=")",
            description="Counter-attacks on successful dodges",
            attack_bonus=3,
            evade_bonus=0.05,  # +5% evade
            attack_traits=[Trait.DARK, Trait.SLASH],
        )
        self.color = COLOR_BLACK
        # Subscribe to successful dodge events
        self.event_subscriptions.add(EventType.SUCCESSFUL_DODGE)
    
    def on_event(self, event_type, context):
        """Handle successful dodge events."""
        if event_type == EventType.SUCCESSFUL_DODGE and isinstance(context, AttackContext):
            # Only trigger if this weapon is equipped and player dodged
            if context.player.weapon == self and context.defender == context.player:
                # Perform counter-attack
                if hasattr(context, 'attacker') and context.attacker:
                    counter_damage = context.player.get_total_attack()
                    actual_damage = context.attacker.take_damage_with_traits(
                        counter_damage, 
                        context.player.get_total_attack_traits()
                    )
                    # Note: We can't easily add UI messages from here, 
                    # but the effect will still work