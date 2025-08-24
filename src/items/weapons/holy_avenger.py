"""
Holy Avenger weapon - counter-attacks when hit.
"""

import random
from .base import Weapon
from constants import COLOR_WHITE
from traits import Trait
from event_type import EventType
from event_context import AttackContext

class HolyAvenger(Weapon):
    """A weapon that counter-attacks when the player is hit."""
    
    def __init__(self, x, y):
        super().__init__(
            x, y,
            name="Holy Avenger",
            char=")",
            description="10% chance to counter-attack when hit",
            attack_bonus=8,
            attack_traits=[Trait.HOLY],
            xp_cost=30
        )
        self.color = COLOR_WHITE
        # Subscribe to monster attack events
        self.event_subscriptions.add(EventType.MONSTER_ATTACK_PLAYER)
    
    def on_event(self, event_type, context):
        """Handle monster attack events."""
        if event_type == EventType.MONSTER_ATTACK_PLAYER and isinstance(context, AttackContext):
            # Only trigger if this weapon is equipped and player took damage
            if context.player.weapon == self and context.damage > 0:
                # 10% chance to counter-attack
                if random.random() < 0.1:
                    # Perform counter-attack
                    if hasattr(context, 'attacker') and context.attacker:
                        counter_damage = context.player.get_total_attack()
                        actual_damage = context.attacker.take_damage_with_traits(
                            counter_damage, 
                            context.player.get_total_attack_traits()
                        )
                        # Note: We can't easily add UI messages from here, 
                        # but the effect will still work