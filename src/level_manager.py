"""
Level Manager for handling floor and base transitions.
"""

from level.level import Level
from level.base import Base
from event_emitter import EventEmitter
from event_type import EventType
from event_context import FloorContext


class LevelManager:
    """Manages progression between floors and bases."""
    
    def __init__(self):
        """Initialize the level manager."""
        self.current_floor = 1  # The actual floor number (1-10)
        self.current_area = None  # Either a Level or Base instance
        self.in_base = False  # Track if currently in a base
        
        # Start on Floor 1
        self.current_area = Level(level_number=1)
    
    def get_current_area(self):
        """Return the current area (Level or Base)."""
        return self.current_area
    
    def is_in_base(self):
        """Check if currently in a base."""
        return self.in_base
    
    def get_display_name(self):
        """Get the display name for current area."""
        if self.in_base:
            return f"Base {self.current_floor - 1}"
        else:
            return f"Floor {self.current_floor}"
    
    def get_current_floor_number(self):
        """Get the actual floor number (for compatibility)."""
        return self.current_floor
    
    def transition_down(self, player):
        """Handle transition when going down stairs."""
        previous_floor = self.current_floor
        message = None
        
        if self.in_base:
            # Transitioning from base to next floor
            self.current_area = Level(level_number=self.current_floor)
            self.in_base = False
            message = f"You enter Floor {self.current_floor}. Danger awaits!"
            
            # Emit FLOOR_START event
            event_emitter = EventEmitter()
            context = FloorContext(
                player=player,
                floor_number=self.current_floor,
                previous_floor=previous_floor - 1  # Previous actual floor
            )
            event_emitter.emit(EventType.FLOOR_START, context)
            
        else:
            # Transitioning from floor to base
            if self.current_floor < 10:  # No base after floor 10
                self.current_area = Base(base_number=self.current_floor)
                self.in_base = True
                self.current_floor += 1  # Increment for next floor
                message = f"You enter Base {previous_floor}. A safe haven with a shop nearby."
                
                # Emit FLOOR_END event
                event_emitter = EventEmitter()
                context = FloorContext(
                    player=player,
                    floor_number=previous_floor,
                    previous_floor=previous_floor
                )
                event_emitter.emit(EventType.FLOOR_END, context)
            else:
                # Floor 10 boss defeated - game should end
                return False
        
        # Place player at stairs up position in new area
        stairs_up_x, stairs_up_y = self.current_area.get_stairs_up_position()
        player.x = stairs_up_x
        player.y = stairs_up_y
        
        # Return success flag and message
        return (True, message)
    
    def transition_up(self, player):
        """Handle transition when going up stairs (if implemented)."""
        # Currently not implemented as per original design
        # Could be added for future base-to-previous-floor navigation
        pass
    
    def can_attack(self):
        """Check if combat is allowed in current area."""
        if self.in_base:
            return False  # No combat in bases
        return True
    
    def get_safe_zone_status(self):
        """Check if current area is a safe zone."""
        if hasattr(self.current_area, 'is_safe_zone'):
            return self.current_area.is_safe_zone()
        return False