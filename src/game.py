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
        self.level.update_fov(self.player.x, self.player.y, self.player.get_total_fov())
        
        # Game state flags
        self.running = True
        self.player_turn = True
        self.just_changed_level = False  # Prevent immediate level transitions
        self.game_state = 'MENU'  # 'PLAYING', 'DEAD', 'INVENTORY', 'VICTORY', 'MENU', 'HELP'
        self.highest_floor_reached = 1
        self.player_acted_this_frame = False  # Track if player took an action this frame
        
        # Inventory management
        self.selected_item_index = None
        self.pending_accessory_replacement = None  # For accessory slot replacement
    
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
                self.game_state = 'MENU'
            elif key == tcod.event.KeySym.ESCAPE or key == ord('q'):
                self.running = False
        elif self.game_state == 'MENU':
            # Handle main menu input
            if key == ord('n') or key == ord('N'):
                self.start_new_game()
            elif key == ord('h') or key == ord('H'):
                self.game_state = 'HELP'
            elif key == tcod.event.KeySym.ESCAPE or key == ord('q'):
                self.running = False
        elif self.game_state == 'HELP':
            # Handle help screen input - any key returns to menu
            self.game_state = 'MENU'
        elif self.game_state == 'VICTORY':
            # Handle victory screen input
            if key == ord('r') or key == ord('R'):
                self.game_state = 'MENU'
            elif key == tcod.event.KeySym.ESCAPE or key == ord('q'):
                self.running = False
        elif self.game_state == 'INVENTORY':
            # Handle inventory screen input
            if key == tcod.event.KeySym.ESCAPE:
                self.game_state = 'PLAYING'
                self.selected_item_index = None
            # Handle action keys FIRST (before letter selection)
            elif key == tcod.event.KeySym.RETURN and self.selected_item_index is not None:
                # Use/equip selected item with Enter key
                self.use_inventory_item(self.selected_item_index)
            elif key == ord('d') and self.selected_item_index is not None:
                # Drop selected item
                self.drop_inventory_item(self.selected_item_index)
            elif key == tcod.event.KeySym.UP or key == ord('k'):
                # Navigate up in inventory
                if len(self.player.inventory) > 0:
                    if self.selected_item_index is None:
                        self.selected_item_index = 0
                    else:
                        self.selected_item_index = (self.selected_item_index - 1) % len(self.player.inventory)
            elif key == tcod.event.KeySym.DOWN or key == ord('j'):
                # Navigate down in inventory
                if len(self.player.inventory) > 0:
                    if self.selected_item_index is None:
                        self.selected_item_index = 0
                    else:
                        self.selected_item_index = (self.selected_item_index + 1) % len(self.player.inventory)
            elif ord('1') <= key <= ord('3'):
                # Handle accessory slot keys 1-3
                self.handle_accessory_slot_key(key - ord('1'))
            elif ord('a') <= key <= ord('z'):
                # Select item by letter (but exclude action keys)
                if key not in [ord('d'), ord('k'), ord('j')]:  # Removed 'u' and 'e'
                    item_index = key - ord('a')
                    if 0 <= item_index < len(self.player.inventory):
                        # If same item is selected again, reset selection
                        if self.selected_item_index == item_index:
                            self.selected_item_index = None
                        else:
                            self.selected_item_index = item_index
        elif self.game_state == 'ACCESSORY_REPLACEMENT':
            # Handle accessory replacement selection
            if key == tcod.event.KeySym.ESCAPE:
                self.game_state = 'INVENTORY'  # Return to inventory
                self.pending_accessory_replacement = None
            elif ord('1') <= key <= ord('3'):
                # Replace accessory at selected slot
                slot_index = key - ord('1')
                if 0 <= slot_index < len(self.player.accessories):
                    # Unequip the old accessory and put it back in inventory
                    old_accessory = self.player.accessories[slot_index]
                    self.player.add_item(old_accessory)
                    self.ui.add_message(f"You unequipped {old_accessory.name}.")
                    
                    # Equip the new accessory in that slot
                    self.player.accessories[slot_index] = self.pending_accessory_replacement
                    self.player.remove_item(self.pending_accessory_replacement)
                    self.player.xp -= self.pending_accessory_replacement.xp_cost
                    
                    if self.pending_accessory_replacement.xp_cost > 0:
                        self.ui.add_message(f"You equipped {self.pending_accessory_replacement.name} for {self.pending_accessory_replacement.xp_cost} XP.")
                    else:
                        self.ui.add_message(f"You equipped {self.pending_accessory_replacement.name}.")
                    
                    # Clear replacement state and return to inventory
                    self.pending_accessory_replacement = None
                    self.game_state = 'INVENTORY'
                    
                    # Update FOV after equipment change
                    self.level.update_fov(self.player.x, self.player.y, self.player.get_total_fov())
        elif self.game_state == 'PLAYING':
            # Inventory key
            if key == ord('i'):
                self.game_state = 'INVENTORY'
                # Default to selecting first item if inventory is not empty
                self.selected_item_index = 0 if len(self.player.inventory) > 0 else None
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
            # Manual leveling
            elif key == ord('x'):
                self.handle_manual_level_up()
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
            self.level.update_fov(self.player.x, self.player.y, self.player.get_total_fov())
            self.player_acted_this_frame = True  # Player took an action
            
            # Add occasional movement messages to help clear old combat messages
            # This helps push out persistent XP/combat messages from the log
            if self.level.is_stairs_down(new_x, new_y):
                self.ui.add_message("You see stairs leading down.")
            elif self.level.is_stairs_up(new_x, new_y):
                self.ui.add_message("You see stairs leading up.")
    
    def player_attack_monster(self, monster):
        """Player attacks a monster."""
        # Check for evade
        if random.random() < monster.evade:
            self.ui.add_message(f"You try to attack {monster.name} and miss!")
            return
        
        # Calculate base damage
        damage = self.player.get_total_attack()
        
        # Check for critical hit
        if random.random() < self.player.get_total_crit():
            damage = int(damage * self.player.get_total_crit_multiplier())
            actual_damage = monster.take_damage(damage)
            message = f"You critical hit on the {monster.name} for {actual_damage}!"
        else:
            actual_damage = monster.take_damage(damage)
            message = f"You attack the {monster.name} for {actual_damage}!"
        
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
            
            # Check if this was the final boss
            if hasattr(monster, 'is_final_boss') and monster.is_final_boss:
                self.ui.add_message("You have defeated the Ancient Devil!")
                self.ui.add_message("The dungeon is cleared! You are victorious!")
                self.game_state = 'VICTORY'
                return  # Don't process item drops or removal for boss
            
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
        # Check for evade
        if random.random() < self.player.get_total_evade():
            self.ui.add_message(f"The {monster.name} tries to attack you and misses!")
            return
        
        # Calculate base damage
        damage = monster.attack
        
        # Check for critical hit
        if random.random() < monster.crit:
            damage = int(damage * monster.crit_multiplier)
            actual_damage = self.player.take_damage(damage)
            message = f"The {monster.name} critical hits you for {actual_damage}!"
        else:
            actual_damage = self.player.take_damage(damage)
            message = f"The {monster.name} attacks you for {actual_damage}!"
        
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
            # removed down stairs, this is a one-way journey
            # if self.level.is_stairs_up(self.player.x, self.player.y):
            #     self.ascend_level()
    
    
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
        self.level.update_fov(self.player.x, self.player.y, self.player.get_total_fov())
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
            self.level.update_fov(self.player.x, self.player.y, self.player.get_total_fov())
            # Set flag to prevent immediate transition back
            self.just_changed_level = True
    
    def start_new_game(self):
        """Start a new game from the main menu."""
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
        self.level.update_fov(self.player.x, self.player.y, self.player.get_total_fov())
        
        # Reset game state flags
        self.player_turn = True
        self.just_changed_level = False
        self.game_state = 'PLAYING'
        self.player_acted_this_frame = False
        
        # Clear UI messages
        self.ui.message_log = []
        self.ui.add_message("Welcome to the Devil's Den!")
        
        # Reset inventory state
        self.selected_item_index = None
    
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
            # Don't add a message for empty pickup attempts - this was causing message spam
            pass
    
    def use_inventory_item(self, item_index):
        """Use or equip an item from inventory by index."""
        if 0 <= item_index < len(self.player.inventory):
            item = self.player.inventory[item_index]
            
            # Check if it's a consumable
            if hasattr(item, 'use') and callable(item.use):
                result = item.use(self.player)
                # Handle both old format (boolean) and new format (tuple)
                if isinstance(result, tuple):
                    success, message = result
                    if success:
                        self.player.remove_item(item)
                        self.ui.add_message(message)
                        
                    else:
                        self.ui.add_message(message)
                else:
                    # Legacy boolean format
                    if result:
                        self.player.remove_item(item)
                        self.ui.add_message(f"You used a {item.name}.")
                    else:
                        self.ui.add_message(f"You can't use the {item.name} right now.")
            
            # Check if it's equipment
            elif hasattr(item, 'equipment_slot'):
                self.equip_item(item)
                # Adjust selection after equipping (item was removed)
                if len(self.player.inventory) == 0:
                    self.selected_item_index = None
                elif self.selected_item_index >= len(self.player.inventory):
                    self.selected_item_index = len(self.player.inventory) - 1
            
            else:
                self.ui.add_message(f"You can't use the {item.name}.")
    
    def drop_inventory_item(self, item_index):
        """Drop an item from inventory onto the current map position."""
        if 0 <= item_index < len(self.player.inventory):
            item = self.player.inventory[item_index]
            # Update the item's position to the player's current location
            item.x = self.player.x
            item.y = self.player.y
            # Add the item to the current level's item list
            self.level.add_item_drop(item.x, item.y, item)
            # Remove the item from player's inventory
            self.player.remove_item(item)
            self.ui.add_message(f"You dropped the {item.name}.")
            
            # Adjust selection after dropping
            if len(self.player.inventory) == 0:
                self.selected_item_index = None
            elif self.selected_item_index >= len(self.player.inventory):
                self.selected_item_index = len(self.player.inventory) - 1
    
    def handle_accessory_slot_key(self, slot_index):
        """Handle accessory slot keys 1-3 for equipping/unequipping accessories."""
        # Check if slot_index is valid (0-2 for slots 1-3)
        if not (0 <= slot_index < 3):
            return
        
        # Check if slot is currently occupied
        slot_occupied = (slot_index < len(self.player.accessories) and 
                        self.player.accessories[slot_index] is not None)
        
        if slot_occupied:
            # Slot is occupied - UNEQUIP the accessory
            accessory_to_unequip = self.player.accessories[slot_index]
            self.player.accessories[slot_index] = None
            self.player.add_item(accessory_to_unequip)
            self.ui.add_message(f"You unequipped {accessory_to_unequip.name} from slot {slot_index + 1}.")
            
            # Update FOV after equipment change
            self.level.update_fov(self.player.x, self.player.y, self.player.get_total_fov())
            
        else:
            # Slot is empty - try to EQUIP selected accessory
            if self.selected_item_index is None:
                self.ui.add_message("No item selected. Select an accessory first.")
                return
            
            if self.selected_item_index >= len(self.player.inventory):
                self.ui.add_message("Invalid item selected.")
                return
            
            selected_item = self.player.inventory[self.selected_item_index]
            
            # Check if selected item is an accessory
            if not (hasattr(selected_item, 'equipment_slot') and 
                   selected_item.equipment_slot == "accessory"):
                self.ui.add_message("Selected item is not an accessory.")
                return
            
            # Check if player can afford the XP cost
            if not selected_item.can_equip(self.player):
                self.ui.add_message(f"Cannot equip {selected_item.name}. Need {selected_item.xp_cost} XP (you have {self.player.xp}).")
                return
            
            # Equip accessory to the specific slot
            # Ensure accessories list is long enough
            while len(self.player.accessories) <= slot_index:
                self.player.accessories.append(None)
            
            # Equip the accessory
            self.player.accessories[slot_index] = selected_item
            self.player.remove_item(selected_item)
            self.player.xp -= selected_item.xp_cost
            
            if selected_item.xp_cost > 0:
                self.ui.add_message(f"You equipped {selected_item.name} to slot {slot_index + 1} for {selected_item.xp_cost} XP.")
            else:
                self.ui.add_message(f"You equipped {selected_item.name} to slot {slot_index + 1}.")
            
            # Update FOV after equipment change
            self.level.update_fov(self.player.x, self.player.y, self.player.get_total_fov())
            
            # Adjust selection after equipping (item was removed from inventory)
            if len(self.player.inventory) == 0:
                self.selected_item_index = None
            elif self.selected_item_index >= len(self.player.inventory):
                self.selected_item_index = len(self.player.inventory) - 1
    
    def equip_item(self, item):
        """Equip an item and handle slot management."""
        # Check if player can afford the XP cost
        if not item.can_equip(self.player):
            self.ui.add_message(f"Cannot equip {item.name}. Need {item.xp_cost} XP (you have {self.player.xp}).")
            return
        
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
            self.player.xp -= item.xp_cost
            if item.xp_cost > 0:
                self.ui.add_message(f"You equipped {item.name} for {item.xp_cost} XP.")
            else:
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
            self.player.xp -= item.xp_cost
            if item.xp_cost > 0:
                self.ui.add_message(f"You equipped {item.name} for {item.xp_cost} XP.")
            else:
                self.ui.add_message(f"You equipped {item.name}.")
            
        elif slot == "accessory":
            # Check if there's an available accessory slot
            if len(self.player.accessories) < self.player.accessory_slots:
                # Find first available slot and equip
                self.player.accessories.append(item)
                self.player.remove_item(item)
                self.player.xp -= item.xp_cost
                if item.xp_cost > 0:
                    self.ui.add_message(f"You equipped {item.name} for {item.xp_cost} XP.")
                else:
                    self.ui.add_message(f"You equipped {item.name}.")
            else:
                # All slots are full - ask which one to replace
                self.ui.add_message("All accessory slots are full. Which accessory would you like to replace?")
                for i, accessory in enumerate(self.player.accessories):
                    self.ui.add_message(f"{i+1}: {accessory.name}")
                self.ui.add_message("Press 1-3 to select which accessory to replace, or ESC to cancel.")
                self.pending_accessory_replacement = item
                self.game_state = 'ACCESSORY_REPLACEMENT'
        
        # Update FOV after equipment change (some items affect FOV)
        self.level.update_fov(self.player.x, self.player.y, self.player.get_total_fov())
        
        # Only return to playing if not in inventory mode
        if self.game_state != 'INVENTORY':
            self.game_state = 'PLAYING'  # Return to game after equipping
    
    def handle_manual_level_up(self):
        """Handle manual level up when L key is pressed."""
        if self.player.attempt_level_up():
            self.ui.add_message(f"Level up! You are now level {self.player.level}.")
            self.ui.add_message(f"HP increased to {self.player.max_hp}!")
            self.ui.add_message(f"Attack increased to {self.player.attack}!")
            self.ui.add_message(f"Defense increased to {self.player.defense}!")
            self.player_acted_this_frame = True  # Count as an action
        else:
            self.ui.add_message("Not enough XP to level up!")
    
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
        
        # Render menu instructions
        menu_text = "Press 'R' to return to main menu or 'ESC' to quit"
        menu_x = center_x - len(menu_text) // 2
        self.console.print(menu_x, center_y + 6, menu_text, fg=COLOR_YELLOW)
    
    def render_victory_screen(self):
        """Render the victory screen with congratulations and stats."""
        from constants import COLOR_YELLOW, COLOR_WHITE, COLOR_GREEN
        
        # Get screen dimensions
        screen_width = self.console.width
        screen_height = self.console.height
        
        # Calculate center positions
        center_x = screen_width // 2
        center_y = screen_height // 2
        
        # Render "VICTORY!" in large yellow text
        victory_text = "VICTORY!"
        text_x = center_x - len(victory_text) // 2
        self.console.print(text_x, center_y - 6, victory_text, fg=COLOR_YELLOW)
        
        # Render congratulations message
        congrats_lines = [
            "Congratulations, brave adventurer!",
            "You have conquered the Devil's Den",
            "and defeated the Ancient Devil!"
        ]
        
        for i, line in enumerate(congrats_lines):
            line_x = center_x - len(line) // 2
            self.console.print(line_x, center_y - 4 + i, line, fg=COLOR_WHITE)
        
        # Render final stats
        stats_lines = [
            f"Final Character Level: {self.player.level}",
            f"Floors Conquered: {self.highest_floor_reached}/10",
            f"Total Experience: {self.player.xp}",
            f"Final Attack Power: {self.player.get_total_attack()}",
            f"Final Defense: {self.player.get_total_defense()}"
        ]
        
        for i, line in enumerate(stats_lines):
            line_x = center_x - len(line) // 2
            self.console.print(line_x, center_y + 1 + i, line, fg=COLOR_GREEN)
        
        # Render menu instructions
        menu_text = "Press 'R' to return to main menu or 'ESC' to quit"
        menu_x = center_x - len(menu_text) // 2
        self.console.print(menu_x, center_y + 8, menu_text, fg=COLOR_YELLOW)
    
    def render_main_menu(self):
        """Render the main menu screen."""
        from constants import COLOR_YELLOW, COLOR_WHITE, COLOR_GREEN
        
        # Get screen dimensions
        screen_width = self.console.width
        screen_height = self.console.height
        
        # Calculate center positions
        center_x = screen_width // 2
        center_y = screen_height // 2
        
        # Render game title
        title_text = "DEVIL'S DEN"
        title_x = center_x - len(title_text) // 2
        self.console.print(title_x, center_y - 8, title_text, fg=COLOR_YELLOW)
        
        # Render subtitle
        subtitle_text = "Conquer the dungeon and defeat the Ancient Demon!"
        subtitle_x = center_x - len(subtitle_text) // 2
        self.console.print(subtitle_x, center_y - 6, subtitle_text, fg=COLOR_WHITE)
        
        # Render menu options
        menu_options = [
            "Press 'N' to start a New Game",
            "Press 'H' for Help and Controls",
            "Press 'ESC' to Quit"
        ]
        
        for i, option in enumerate(menu_options):
            option_x = center_x - len(option) // 2
            self.console.print(option_x, center_y - 2 + i * 2, option, fg=COLOR_GREEN)
        
        # Render credits
        credits_text = "Made for the Seven-Day Roguelike Challenge"
        credits_x = center_x - len(credits_text) // 2
        self.console.print(credits_x, center_y + 6, credits_text, fg=COLOR_WHITE)
    
    def render_help_screen(self):
        """Render the help/controls screen."""
        from constants import COLOR_YELLOW, COLOR_WHITE, COLOR_GREEN
        
        # Get screen dimensions
        screen_width = self.console.width
        screen_height = self.console.height
        
        # Calculate center positions
        center_x = screen_width // 2
        center_y = screen_height // 2
        
        # Render help title
        title_text = "CONTROLS & HELP"
        title_x = center_x - len(title_text) // 2
        self.console.print(title_x, center_y - 12, title_text, fg=COLOR_YELLOW)
        
        # Render control instructions
        controls = [
            "MOVEMENT:",
            "  Arrow Keys or HJKL - Move/Attack",
            "  YUBN - Diagonal movement",
            "",
            "ACTIONS:",
            "  G - Pick up items",
            "  I - Open inventory",
            "  A-Z - Use/equip items in inventory",
            "  ESC - Close menus or quit",
            "",
            "GAME OBJECTIVE:",
            "  Explore 10 levels of the dungeon",
            "  Fight monsters and collect items",
            "  Defeat the Ancient Devil on level 10",
            "",
            "Press any key to return to menu"
        ]
        
        start_y = center_y - 10
        for i, line in enumerate(controls):
            if line.startswith("  "):
                # Indented lines in white
                self.console.print(center_x - len(line) // 2, start_y + i, line, fg=COLOR_WHITE)
            elif line.endswith(":"):
                # Section headers in green
                self.console.print(center_x - len(line) // 2, start_y + i, line, fg=COLOR_GREEN)
            elif line == "Press any key to return to menu":
                # Footer instruction in yellow
                self.console.print(center_x - len(line) // 2, start_y + i, line, fg=COLOR_YELLOW)
            else:
                # Regular text in white
                self.console.print(center_x - len(line) // 2, start_y + i, line, fg=COLOR_WHITE)
    
    def render(self):
        """Render the game to the console."""
        # Clear the console
        self.console.clear()
        
        if self.game_state == 'MENU':
            # Render main menu
            self.render_main_menu()
        elif self.game_state == 'HELP':
            # Render help screen
            self.render_help_screen()
        elif self.game_state == 'DEAD':
            # Render death screen  
            self.render_death_screen()
        elif self.game_state == 'VICTORY':
            # Render victory screen
            self.render_victory_screen()
        elif self.game_state == 'INVENTORY':
            # Render inventory screen
            self.ui.render_inventory(self.console, self.player, self.selected_item_index)
        elif self.game_state == 'ACCESSORY_REPLACEMENT':
            # Render accessory replacement screen
            self.ui.render_inventory(self.console, self.player, self.selected_item_index)
        else:
            # Normal game rendering
            # Render the level
            self.level.render(self.console)
            
            # Render the player
            self.player.render(self.console, self.level.fov)
            
            # Render the UI
            self.ui.render(self.console, self.player, self.current_level, self.level)