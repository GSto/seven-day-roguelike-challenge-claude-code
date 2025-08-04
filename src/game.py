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
        self.game_state = 'PLAYING'  # 'PLAYING', 'DEAD', 'INVENTORY', 'DEAD', 'MENU'
        self.highest_floor_reached = 1
        self.player_acted_this_frame = False  # Track if player took an action this frame
    
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
                # Reset player action flag
                self.player_acted_this_frame = False
                
                # Handle events
                self.handle_events(context)
                
                # Update game state only if player acted
                if self.player_acted_this_frame:
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
        
        if self.game_state == 'DEAD':
            # Handle death screen input
            if key == ord('r') or key == ord('R'):
                self.restart_game()
            elif key == tcod.event.KeySym.ESCAPE or key == ord('q'):
                self.running = False
        elif self.game_state == 'INVENTORY':
            # Handle inventory screen input
            if key == tcod.event.KeySym.ESCAPE:
                self.game_state = 'PLAYING'
            elif ord('a') <= key <= ord('z'):
                # Use/equip item by letter
                item_index = key - ord('a')
                self.use_inventory_item(item_index)
        elif self.game_state == 'PLAYING':
            # Inventory key
            if key == ord('i'):
                self.game_state = 'INVENTORY'
            # Item pickup key
            elif key == ord('g'):
                self.try_pickup_item()
            # Movement keys using KeySym enum
            elif key == tcod.event.KeySym.UP or key == ord('k'):
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
            self.player_acted_this_frame = True  # Player took an action
            return
        
        # Check if the move is valid (no walls, no monsters)
        if self.level.is_walkable(new_x, new_y):
            self.player.move(dx, dy)
            # Update FOV immediately after movement
            self.level.update_fov(self.player.x, self.player.y)
            self.player_acted_this_frame = True  # Player took an action
    
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
            death_message = "You have died!"
            self.ui.add_message(death_message)
            self.game_state = 'DEAD'
    
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
        
        # Process monster turns (only if player is alive and game is playing)
        if self.player.is_alive() and self.game_state == 'PLAYING':
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
        self.highest_floor_reached = max(self.highest_floor_reached, self.current_level)
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
    
    def restart_game(self):
        """Restart the game with a new character."""
        # Initialize game state
        self.current_level = 1
        self.highest_floor_reached = 1
        self.level = Level(level_number=self.current_level)
        
        # Place player at stairs up position (or first room if no stairs)
        if hasattr(self.level, 'stairs_up_pos') and self.level.stairs_up_pos:
            start_x, start_y = self.level.stairs_up_pos
        elif len(self.level.rooms) > 0:
            start_x, start_y = self.level.rooms[0].center()
        else:
            start_x, start_y = 10, 10
        
        self.player = Player(x=start_x, y=start_y)
        
        # Initialize FOV for starting position
        self.level.update_fov(self.player.x, self.player.y)
        
        # Reset game state flags
        self.player_turn = True
        self.just_changed_level = False
        self.game_state = 'PLAYING'
        self.player_acted_this_frame = False
        
        # Clear UI messages
        self.ui.message_log = []
        self.ui.add_message("Welcome back, adventurer!")
    
    def try_pickup_item(self):
        """Try to pick up an item at the player's current position."""
        item = self.level.get_item_at(self.player.x, self.player.y)
        if item:
            # Try to add item to inventory
            if self.player.add_item(item):
                self.level.remove_item(item)
                self.ui.add_message(f"You picked up a {item.name}.")
                self.player_acted_this_frame = True
            else:
                self.ui.add_message("Your inventory is full!")
        else:
            self.ui.add_message("There's nothing here to pick up.")
    
    def use_inventory_item(self, item_index):
        """Use or equip an item from inventory by index."""
        if 0 <= item_index < len(self.player.inventory):
            item = self.player.inventory[item_index]
            
            # Check if it's a consumable
            if hasattr(item, 'use') and callable(item.use):
                if item.use(self.player):
                    self.player.remove_item(item)
                    self.ui.add_message(f"You used a {item.name}.")
                    self.game_state = 'PLAYING'  # Return to game after use
                else:
                    self.ui.add_message(f"You can't use the {item.name} right now.")
            
            # Check if it's equipment
            elif hasattr(item, 'equipment_slot'):
                self.equip_item(item)
            
            else:
                self.ui.add_message(f"You can't use the {item.name}.")
    
    def equip_item(self, item):
        """Equip an item and handle slot management."""
        slot = item.equipment_slot
        
        if slot == "weapon":
            # Unequip current weapon if any
            if self.player.weapon:
                old_weapon = self.player.weapon
                self.player.weapon = None
                self.player.add_item(old_weapon)  # Put back in inventory
                self.ui.add_message(f"You unequipped {old_weapon.name}.")
            
            # Equip new weapon
            self.player.weapon = item
            self.player.remove_item(item)
            self.ui.add_message(f"You equipped {item.name}.")
            
        elif slot == "armor":
            # Unequip current armor if any
            if self.player.armor:
                old_armor = self.player.armor
                self.player.armor = None
                self.player.add_item(old_armor)
                self.ui.add_message(f"You unequipped {old_armor.name}.")
            
            # Equip new armor
            self.player.armor = item
            self.player.remove_item(item)
            self.ui.add_message(f"You equipped {item.name}.")
            
        elif slot == "accessory":
            # Unequip current accessory if any
            if self.player.accessory:
                old_accessory = self.player.accessory
                self.player.accessory = None
                self.player.add_item(old_accessory)
                self.ui.add_message(f"You unequipped {old_accessory.name}.")
            
            # Equip new accessory
            self.player.accessory = item
            self.player.remove_item(item)
            self.ui.add_message(f"You equipped {item.name}.")
        
        self.game_state = 'PLAYING'  # Return to game after equipping
    
    def render_death_screen(self):
        """Render the death screen with stats and restart option."""
        from constants import COLOR_RED, COLOR_WHITE, COLOR_YELLOW
        
        # Get screen dimensions
        screen_width = self.console.width
        screen_height = self.console.height
        
        # Calculate center positions
        center_x = screen_width // 2
        center_y = screen_height // 2
        
        # Render "YOU DIED" in large red text
        death_text = "YOU DIED"
        text_x = center_x - len(death_text) // 2
        self.console.print(text_x, center_y - 4, death_text, fg=COLOR_RED)
        
        # Render player stats
        stats_lines = [
            f"Final Level: {self.player.level}",
            f"Highest Floor Reached: {self.highest_floor_reached}",
            f"Experience Points: {self.player.xp}",
            f"Damage Dealt: {self.player.get_total_attack()}",
            f"Defense: {self.player.get_total_defense()}"
        ]
        
        for i, line in enumerate(stats_lines):
            line_x = center_x - len(line) // 2
            self.console.print(line_x, center_y - 1 + i, line, fg=COLOR_WHITE)
        
        # Render restart instructions
        restart_text = "Press 'R' to restart or 'ESC' to quit"
        restart_x = center_x - len(restart_text) // 2
        self.console.print(restart_x, center_y + 6, restart_text, fg=COLOR_YELLOW)
    
    def render(self):
        """Render the game to the console."""
        # Clear the console
        self.console.clear()
        
        if self.game_state == 'DEAD':
            # Render death screen
            self.render_death_screen()
        elif self.game_state == 'INVENTORY':
            # Render inventory screen
            self.ui.render_inventory(self.console, self.player)
        else:
            # Normal game rendering
            # Render the level
            self.level.render(self.console)
            
            # Render the player
            self.player.render(self.console, self.level.fov)
            
            # Render the UI
            self.ui.render(self.console, self.player, self.current_level, self.level)