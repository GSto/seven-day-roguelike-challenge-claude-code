"""
Main Game class - handles the core game loop and state management.
"""

import tcod
import tcod.event

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE
from player import Player
from level import Level
from ui import UI


class Game:
    """Main game class that manages the game state and loop."""
    
    def __init__(self):
        """Initialize the game."""
        # Set up the console
        self.console = tcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT, order="F")
        
        # Initialize game state
        self.current_level = 1
        self.level = Level(level_number=self.current_level)
        
        # Place player at stairs up position (or first room if no stairs)
        if hasattr(self.level, 'stairs_up_pos') and self.level.stairs_up_pos:
            start_x, start_y = self.level.stairs_up_pos
        elif len(self.level.rooms) > 0:
            start_x, start_y = self.level.rooms[0].center()
        else:
            start_x, start_y = 10, 10
        
        self.player = Player(x=start_x, y=start_y)
        self.ui = UI()
        
        # Initialize FOV for starting position
        self.level.update_fov(self.player.x, self.player.y)
        
        # Game state flags
        self.running = True
        self.player_turn = True
    
    def run(self):
        """Main game loop."""
        # Create the tcod context for rendering
        with tcod.context.new_terminal(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            tileset=None,
            title=TITLE,
            vsync=True,
        ) as context:
            
            while self.running:
                # Handle events
                self.handle_events(context)
                
                # Update game state
                if self.player_turn:
                    self.update()
                
                # Render the game
                self.render()
                context.present(self.console)
    
    def handle_events(self, context):
        """Handle input events."""
        for event in tcod.event.wait():
            if isinstance(event, tcod.event.Quit):
                self.running = False
            elif isinstance(event, tcod.event.KeyDown):
                self.handle_keydown(event)
    
    def handle_keydown(self, event):
        """Handle keyboard input."""
        key = event.sym
        
        # Movement keys using KeySym enum
        if key == tcod.event.KeySym.UP or key == ord('k'):
            self.try_move_player(0, -1)
        elif key == tcod.event.KeySym.DOWN or key == ord('j'):
            self.try_move_player(0, 1)
        elif key == tcod.event.KeySym.LEFT or key == ord('h'):
            self.try_move_player(-1, 0)
        elif key == tcod.event.KeySym.RIGHT or key == ord('l'):
            self.try_move_player(1, 0)
        # Diagonal movement
        elif key == ord('y'):
            self.try_move_player(-1, -1)
        elif key == ord('u'):
            self.try_move_player(1, -1)
        elif key == ord('b'):
            self.try_move_player(-1, 1)
        elif key == ord('n'):
            self.try_move_player(1, 1)
        # Quit game
        elif key == tcod.event.KeySym.ESCAPE or key == ord('q'):
            self.running = False
    
    def try_move_player(self, dx, dy):
        """Attempt to move the player by dx, dy."""
        new_x = self.player.x + dx
        new_y = self.player.y + dy
        
        # Check if the move is valid
        if self.level.is_walkable(new_x, new_y):
            self.player.move(dx, dy)
            self.player_turn = False  # End player turn
    
    def update(self):
        """Update game state."""
        # Update field of view
        self.level.update_fov(self.player.x, self.player.y)
        
        # Check for level transitions
        if self.level.is_stairs_down(self.player.x, self.player.y):
            self.descend_level()
        elif self.level.is_stairs_up(self.player.x, self.player.y):
            self.ascend_level()
        
        # Reset player turn
        self.player_turn = True
    
    def descend_level(self):
        """Move to the next level down."""
        self.current_level += 1
        self.level = Level(level_number=self.current_level)
        # Place player at stairs up position
        stairs_up_x, stairs_up_y = self.level.get_stairs_up_position()
        self.player.x = stairs_up_x
        self.player.y = stairs_up_y
    
    def ascend_level(self):
        """Move to the previous level up."""
        if self.current_level > 1:
            self.current_level -= 1
            self.level = Level(level_number=self.current_level)
            # Place player at stairs down position
            stairs_down_x, stairs_down_y = self.level.get_stairs_down_position()
            self.player.x = stairs_down_x
            self.player.y = stairs_down_y
    
    def render(self):
        """Render the game to the console."""
        # Clear the console
        self.console.clear()
        
        # Render the level
        self.level.render(self.console)
        
        # Render the player
        self.player.render(self.console, self.level.fov)
        
        # Render the UI
        self.ui.render(self.console, self.player, self.current_level)