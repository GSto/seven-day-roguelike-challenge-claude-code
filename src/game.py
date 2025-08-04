"""
Main Game class - handles the core game loop and state management.
"""

import tcod
import tcod.event

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, TILE_WALL, COLOR_GREEN, COLOR_YELLOW
from items import HealthPotion, create_random_item_for_level
import random
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
        self.just_changed_level = False  # Prevent immediate level transitions
    
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
            # Explicitly ignore mouse events to prevent unwanted behavior
            elif isinstance(event, (tcod.event.MouseMotion, tcod.event.MouseButtonDown, tcod.event.MouseButtonUp)):
                pass  # Ignore mouse events
    
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
        
        # Check if there's a monster at the target position
        monster = self.level.get_monster_at(new_x, new_y)
        if monster and monster.is_alive():
            # Attack the monster instead of moving
            self.player_attack_monster(monster)
            return
        
        # Check if the move is valid (no walls, no monsters)
        if self.level.is_walkable(new_x, new_y):
            self.player.move(dx, dy)
            # Update FOV immediately after movement
            self.level.update_fov(self.player.x, self.player.y)
            # Movement successful
    
    def player_attack_monster(self, monster):
        """Player attacks a monster."""
        # Calculate damage
        damage = self.player.get_total_attack()
        actual_damage = monster.take_damage(damage)
        
        # Add combat message
        message = f"You attack the {monster.name} for {actual_damage} damage!"
        self.ui.add_message(message)
        
        # Check if monster died
        if not monster.is_alive():
            death_message = f"The {monster.name} dies!"
            self.ui.add_message(death_message)
            
            # Give player XP
            leveled_up = self.player.gain_xp(monster.xp_value)
            xp_message = f"You gain {monster.xp_value} XP!"
            self.ui.add_message(xp_message, COLOR_GREEN)
            
            # Show level up message if player leveled up
            if leveled_up:
                level_up_message = f"You reached level {self.player.level}!"
                self.ui.add_message(level_up_message, COLOR_YELLOW)
            
            # Chance for monster to drop an item
            if random.random() < 0.3:  # 30% chance to drop an item
                dropped_item = create_random_item_for_level(self.current_level, monster.x, monster.y)
                self.level.add_item_drop(monster.x, monster.y, dropped_item)
                drop_message = f"The {monster.name} dropped a {dropped_item.name}!"
                self.ui.add_message(drop_message)
            
            # Remove dead monster from level
            self.level.remove_dead_monsters()
    
    def monster_attack_player(self, monster):
        """Monster attacks the player."""
        # Calculate damage
        damage = monster.attack
        actual_damage = self.player.take_damage(damage)
        
        # Add combat message
        message = f"The {monster.name} attacks you for {actual_damage} damage!"
        self.ui.add_message(message)
        
        # Check if player died
        if not self.player.is_alive():
            death_message = "You have died! Press ESC to exit."
            self.ui.add_message(death_message)
            # Could add game over screen here
    
    def process_monster_turns(self):
        """Process AI turns for all monsters."""
        for monster in self.level.monsters:
            if monster.is_alive():
                self.monster_take_turn(monster)
    
    def monster_take_turn(self, monster):
        """Process a single monster's turn."""
        # Check if monster can see player
        if monster.can_see_player(self.player.x, self.player.y, self.level.fov):
            monster.has_seen_player = True
            monster.target_x = self.player.x
            monster.target_y = self.player.y
            monster.turns_since_seen_player = 0
        elif monster.has_seen_player:
            # Continue tracking for a few turns even if player goes out of sight
            monster.turns_since_seen_player += 1
            if monster.turns_since_seen_player > 5:
                monster.has_seen_player = False
                monster.target_x = None
                monster.target_y = None
        
        # If monster knows where player is, move toward them
        if monster.has_seen_player and monster.target_x is not None:
            # Simple AI: move directly toward target
            dx = 0
            dy = 0
            
            if monster.x < monster.target_x:
                dx = 1
            elif monster.x > monster.target_x:
                dx = -1
                
            if monster.y < monster.target_y:
                dy = 1
            elif monster.y > monster.target_y:
                dy = -1
            
            # Try to move toward player
            new_x = monster.x + dx
            new_y = monster.y + dy
            
            # Check if player is at target position (attack!)
            if new_x == self.player.x and new_y == self.player.y:
                self.monster_attack_player(monster)
            # Otherwise try to move there
            elif self.level.tiles[new_x, new_y] != TILE_WALL and not self.level.is_position_occupied(new_x, new_y):  # Not a wall and not occupied
                monster.move(dx, dy)
    
    def update(self):
        """Update game state."""
        # Reset level change flag if player moved away from stairs
        if (not self.level.is_stairs_down(self.player.x, self.player.y) and 
            not self.level.is_stairs_up(self.player.x, self.player.y)):
            self.just_changed_level = False
        
        # Process monster turns (only if player is alive)
        if self.player.is_alive():
            self.process_monster_turns()
        
        # Check for level transitions (only if we didn't just change levels)
        if not self.just_changed_level:
            if self.level.is_stairs_down(self.player.x, self.player.y):
                self.descend_level()
            elif self.level.is_stairs_up(self.player.x, self.player.y):
                self.ascend_level()
    
    def descend_level(self):
        """Move to the next level down."""
        self.current_level += 1
        self.level = Level(level_number=self.current_level)
        # Place player at stairs up position
        stairs_up_x, stairs_up_y = self.level.get_stairs_up_position()
        self.player.x = stairs_up_x
        self.player.y = stairs_up_y
        # Update FOV for new level
        self.level.update_fov(self.player.x, self.player.y)
        # Set flag to prevent immediate transition back
        self.just_changed_level = True
    
    def ascend_level(self):
        """Move to the previous level up."""
        if self.current_level > 1:
            self.current_level -= 1
            self.level = Level(level_number=self.current_level)
            # Place player at stairs down position
            stairs_down_x, stairs_down_y = self.level.get_stairs_down_position()
            self.player.x = stairs_down_x
            self.player.y = stairs_down_y
            # Update FOV for new level
            self.level.update_fov(self.player.x, self.player.y)
            # Set flag to prevent immediate transition back
            self.just_changed_level = True
    
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