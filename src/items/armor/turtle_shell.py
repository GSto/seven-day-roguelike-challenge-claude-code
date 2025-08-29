"""
Stone Armor
"""

from .base import Armor
from event_type import EventType
from event_context import FloorContext
from event_context import LevelUpContext

class TurtleShell(Armor):
    def __init__(self, x, y):
        super().__init__(x, y, "Turtle Shell", '[', 6, 
        description="+6 DEF, -3 ATK. Gain a shield when level up or changing floors", attack_bonus=-3)
        self.market_value = 68  # Mid game uncommon armor
        
    def on_event(self, event_type, context):
      """Handle floor change events."""
      if event_type == EventType.FLOOR_CHANGE and isinstance(context, FloorContext):
          context.player.status_effects.shields += 1

      if event_type == EventType.LEVEL_UP and isinstance(context, LevelUpContext):
          context.player.status_effects.shields += 1
    