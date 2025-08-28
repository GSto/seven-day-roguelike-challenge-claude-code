"""
Main Game class - handles the core game loop and state management.
"""

import tcod
import tcod.event

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, TILE_WALL, COLOR_GREEN, COLOR_YELLOW
from items.factory import create_random_item_for_level
import random
from player import Player
from level.level import Level
from level.base import Base
from level_manager import LevelManager
from ui import UI
from traits import Trait
from event_emitter import EventEmitter
from event_type import EventType
from event_context import ConsumeContext, AttackContext, DeathContext, FloorContext
from shop_manager import ShopManager


class Game:
    """Main game class that manages the game state and loop."""
    
    def __init__(self):
        """Initialize the game."""
        # Set up the console
        self.console = tcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT, order="F")
        
        # Initialize level manager and game state
        self.level_manager = LevelManager()
        self.level = self.level_manager.get_current_area()
        
        # Place player at stairs up position (or first room if no stairs)
        if hasattr(self.level, 'stairs_up_pos') and self.level.stairs_up_pos:
            start_x, start_y = self.level.stairs_up_pos
        elif len(self.level.rooms) > 0:
            start_x, start_y = self.level.rooms[0].center()
        else:
            start_x, start_y = 10, 10
        
        self.player = Player(x=start_x, y=start_y)
        self.ui = UI()
        self.shop_manager = ShopManager()  # Initialize shop manager
        
        # Initialize FOV for starting position
        self.level.update_fov(self.player.x, self.player.y, self.player.get_total_fov())
        
        # Game state flags
        self.running = True
        self.player_turn = True
        self.just_changed_level = False  # Prevent immediate level transitions
        self.game_state = 'MENU'  # 'PLAYING', 'DEAD', 'INVENTORY', 'VICTORY', 'MENU', 'HELP', 'SHOP'
        self.highest_floor_reached = 1
        self.player_acted_this_frame = False  # Track if player took an action this frame
        
        # Inventory management
        self.selected_item_index = None
        self.selected_equipment_index = None  # For equipment/accessory selection
        self.selection_mode = "inventory"  # "inventory" or "equipment"
        self.pending_accessory_replacement = None  # For accessory slot replacement
        self.pending_boon_item = None  # For boon choice selection
        self.pending_boon_enchantment = None  # For boon enchantment type
        
        # ESC quit confirmation tracking
        self.esc_pressed_once = False
    
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
        elif self.game_state == 'SHOP':
            # Handle shop input
            action = self.shop_manager.handle_input(key)
            if action == "exit_shop":
                self.game_state = 'PLAYING'
                self.ui.add_message("You leave the shop.")
            elif action and action.startswith("buy:"):
                message = action.split(":", 1)[1]
                self.ui.add_message(message)
            elif action and action.startswith("sell:"):
                message = action.split(":", 1)[1]
                self.ui.add_message(message)
        elif self.game_state == 'INVENTORY':
            # Handle inventory screen input
            if key == tcod.event.KeySym.ESCAPE:
                self.game_state = 'PLAYING'
                self.selected_item_index = None
                self.selected_equipment_index = None
                self.selection_mode = "inventory"
            # Handle action keys FIRST (before letter selection)
            elif key == tcod.event.KeySym.RETURN:
                if self.selection_mode == "inventory" and self.selected_item_index is not None:
                    # Use/equip selected item with Enter key
                    self.use_inventory_item(self.selected_item_index)
                elif self.selection_mode == "equipment" and self.selected_equipment_index is not None:
                    # Unequip selected equipped item with Enter key
                    self.unequip_selected_item()
            elif key == ord('d') and self.selection_mode == "inventory" and self.selected_item_index is not None:
                # Drop selected item
                self.drop_inventory_item(self.selected_item_index)
            elif key == ord('u') and self.selection_mode == "equipment" and self.selected_equipment_index is not None:
                # Unequip selected equipped item
                self.unequip_selected_item()
            elif key == tcod.event.KeySym.UP or key == ord('k'):
                self.navigate_up()
            elif key == tcod.event.KeySym.DOWN or key == ord('j'):
                self.navigate_down()
            elif ord('1') <= key <= ord('5'):
                # Handle equipment slot keys 1-5 (highlight equipment)
                self.select_equipment_slot(key - ord('1'))
            elif ord('a') <= key <= ord('z'):
                # Select item by letter (but exclude action keys)
                if key not in [ord('d'), ord('k'), ord('j'), ord('u')]:
                    display_index = key - ord('a')  # Display position (newest = 0)
                    if 0 <= display_index < len(self.player.inventory):
                        # Convert display index to actual inventory index (reverse mapping)
                        actual_item_index = len(self.player.inventory) - 1 - display_index
                        # Switch to inventory mode and select item
                        self.selection_mode = "inventory"
                        self.selected_equipment_index = None
                        # If same item is selected again, reset selection
                        if self.selected_item_index == actual_item_index:
                            self.selected_item_index = None
                        else:
                            self.selected_item_index = actual_item_index
        elif self.game_state == 'ACCESSORY_REPLACEMENT':
            # Handle accessory replacement selection
            if key == tcod.event.KeySym.ESCAPE:
                self.game_state = 'INVENTORY'  # Return to inventory
                self.pending_accessory_replacement = None
            elif ord('3') <= key <= ord('5'):
                # Replace accessory at selected slot (slots 3-5 for accessories)
                slot_index = key - ord('3')  # Map 3->0, 4->1, 5->2
                if 0 <= slot_index < len(self.player.accessories):
                    # Unequip the old accessory and put it back in inventory
                    old_accessory = self.player.accessories[slot_index]
                    self.unregister_equipment_events(old_accessory)
                    self.player.add_item(old_accessory)
                    self.ui.add_message(f"You unequipped {old_accessory.name}.")
                    
                    # Equip the new accessory in that slot
                    self.player.accessories[slot_index] = self.pending_accessory_replacement
                    self.player.remove_item(self.pending_accessory_replacement)
                    
                    # Register events for new accessory
                    self.register_equipment_events(self.pending_accessory_replacement)
                    
                    self.ui.add_message(f"You equipped {self.pending_accessory_replacement.name}.")
                    
                    # Clear replacement state and return to inventory
                    self.pending_accessory_replacement = None
                    self.game_state = 'INVENTORY'
                    
                    # Update FOV after equipment change
                    self.level.update_fov(self.player.x, self.player.y, self.player.get_total_fov())
        elif self.game_state == 'BOON_CHOICE':
            # Handle boon enchantment choice selection
            if key == tcod.event.KeySym.ESCAPE:
                self.game_state = 'INVENTORY'  # Return to inventory
                self.pending_boon_item = None
                self.pending_boon_enchantment = None
                self.ui.add_message("Enchantment cancelled.")
            elif key == ord('w') or key == ord('W'):
                # Apply enchantment to weapon
                success, message = self.pending_boon_item.apply_to_weapon(self.player, self.pending_boon_enchantment)
                if success:
                    self.player.consumable_count += 1
                    self.player.remove_item(self.pending_boon_item)
                self.ui.add_message(message)
                self.pending_boon_item = None
                self.pending_boon_enchantment = None
                self.game_state = 'INVENTORY'
            elif key == ord('a') or key == ord('A'):
                # Apply enchantment to armor
                success, message = self.pending_boon_item.apply_to_armor(self.player, self.pending_boon_enchantment)
                if success:
                    self.player.consumable_count += 1
                    self.player.remove_item(self.pending_boon_item)
                self.ui.add_message(message)
                self.pending_boon_item = None
                self.pending_boon_enchantment = None
                self.game_state = 'INVENTORY'
        elif self.game_state == 'PLAYING':
            # Inventory key
            if key == ord('i'):
                self.esc_pressed_once = False  # Reset ESC confirmation
                self.game_state = 'INVENTORY'
                # Default to selecting newest item if inventory is not empty
                if len(self.player.inventory) > 0:
                    self.selected_item_index = len(self.player.inventory) - 1  # Newest item
                    self.selection_mode = "inventory"
                    self.selected_equipment_index = None
                else:
                    self.selected_item_index = None
                    # Start with equipment if no inventory items
                    self.selection_mode = "equipment"
                    self.selected_equipment_index = 0
            # Item pickup key
            elif key == ord('g'):
                self.esc_pressed_once = False  # Reset ESC confirmation
                self.try_pickup_item()
            # Movement keys using KeySym enum
            elif key == tcod.event.KeySym.UP or key == ord('k'):
                self.esc_pressed_once = False  # Reset ESC confirmation
                self.try_move_player(0, -1)
            elif key == tcod.event.KeySym.DOWN or key == ord('j'):
                self.esc_pressed_once = False  # Reset ESC confirmation
                self.try_move_player(0, 1)
            elif key == tcod.event.KeySym.LEFT or key == ord('h'):
                self.esc_pressed_once = False  # Reset ESC confirmation
                self.try_move_player(-1, 0)
            elif key == tcod.event.KeySym.RIGHT or key == ord('l'):
                self.esc_pressed_once = False  # Reset ESC confirmation
                self.try_move_player(1, 0)
            # Diagonal movement
            elif key == ord('y'):
                self.esc_pressed_once = False  # Reset ESC confirmation
                self.try_move_player(-1, -1)
            elif key == ord('u'):
                self.esc_pressed_once = False  # Reset ESC confirmation
                self.try_move_player(1, -1)
            elif key == ord('b'):
                self.esc_pressed_once = False  # Reset ESC confirmation
                self.try_move_player(-1, 1)
            elif key == ord('n'):
                self.esc_pressed_once = False  # Reset ESC confirmation
                self.try_move_player(1, 1)
            # Manual leveling
            elif key == ord('x'):
                self.esc_pressed_once = False  # Reset ESC confirmation
                self.handle_manual_level_up()
            # Quit game
            elif key == tcod.event.KeySym.ESCAPE or key == ord('q'):
                if self.esc_pressed_once:
                    # Second ESC press - quit the game
                    self.running = False
                else:
                    # First ESC press - show confirmation
                    self.esc_pressed_once = True
                    self.ui.add_message("Are you sure? Press ESC again to quit.")
            else:
                # Any other key cancels the ESC confirmation
                if self.esc_pressed_once:
                    self.esc_pressed_once = False
    
    def try_move_player(self, dx, dy):
        """Attempt to move the player by dx, dy."""
        new_x = self.player.x + dx
        new_y = self.player.y + dy
        
        # Check if there's a monster at the target position
        monster = self.level.get_monster_at(new_x, new_y)
        if monster and monster.is_alive():
            # Check if combat is allowed in this area
            if not self.level_manager.can_attack():
                self.ui.add_message("You cannot attack in a safe zone!")
                return
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
            
            # Check if player moved onto a shop
            if self.level.is_shop_at(new_x, new_y):
                self.open_shop()
                return
            
            # Add occasional movement messages to help clear old combat messages
            # This helps push out persistent XP/combat messages from the log
            if self.level.is_stairs_down(new_x, new_y):
                self.ui.add_message("You see stairs leading down.")
            elif self.level.is_stairs_up(new_x, new_y):
                self.ui.add_message("You see stairs leading up.")
    
    def calculate_aspect_damage_multiplier(self, attack_traits, target_weaknesses, target_resistances):
        """Calculate damage multiplier based on aspects vs weaknesses/resistances."""
        multiplier = 1.0
        
        for trait in attack_traits:
            if trait in target_weaknesses:
                multiplier *= 1.5  # 1.5x damage for weakness
            elif trait in target_resistances:
                multiplier *= 0.5  # 0.5x damage for resistance
        
        return multiplier
    
    def apply_elemental_status_effects(self, attack_traits, target):
        """Apply status effects based on elemental attack traits."""
        from traits import Trait
        import random
        
        for trait in attack_traits:
            # Only apply if target is not resistant to this trait
            if trait not in target.resistances:
                if trait == Trait.ICE:
                    if random.random() < 0.25:  # 25% chance
                        if target.status_effects.apply_status('stun', 3, target):
                            entity_name = target.name if hasattr(target, 'name') else 'You'
                            self.ui.add_message(f"{entity_name} become stunned!")
                        
                elif trait == Trait.FIRE:
                    if random.random() < 0.5:  # 50% chance
                        if target.status_effects.apply_status('burn', 4, target):
                            entity_name = target.name if hasattr(target, 'name') else 'You'
                            self.ui.add_message(f"{entity_name} start burning!")
                        
                elif trait == Trait.HOLY:
                    if random.random() < 0.5:  # 50% chance
                        if target.status_effects.apply_status('blinded', 3, target):
                            entity_name = target.name if hasattr(target, 'name') else 'You'
                            self.ui.add_message(f"{entity_name} become blinded!")
                        
                elif trait == Trait.DARK:
                    # DARK always applies (100% chance)
                    if target.status_effects.apply_status('frightened', 2, target):
                        entity_name = target.name if hasattr(target, 'name') else 'You'
                        self.ui.add_message(f"{entity_name} become frightened!")
                    
                elif trait == Trait.POISON:
                    # POISON always applies (100% chance)
                    if target.status_effects.apply_status('poison', 2, target):
                        entity_name = target.name if hasattr(target, 'name') else 'You'
                        self.ui.add_message(f"{entity_name} become poisoned!")
    
    def process_status_effects_turn_start(self, entity):
        """Process status effects at the start of an entity's turn."""
        # Check for stun skip turn
        if entity.status_effects.check_stun_skip_turn():
            entity_name = entity.name if hasattr(entity, 'name') else 'You'
            self.ui.add_message(f"{entity_name} are stunned and skip their turn!")
            return True  # Turn should be skipped
        
        # Process burn and poison damage
        damage_taken, messages = entity.status_effects.process_turn_start_effects(entity)
        for message in messages:
            self.ui.add_message(message)
        
        return False  # Turn should not be skipped
    
    def player_attack_monster(self, monster):
        """Player attacks a monster."""
        # Apply status effect modifiers to attack
        attack_modifier = self.player.status_effects.get_attack_modifier()
        miss_chance_increase = self.player.status_effects.get_miss_chance_increase()
        can_crit = self.player.status_effects.can_crit()
        
        # Check for miss (including blinded effect)
        base_miss_chance = 0.05  # 5% base miss chance
        total_miss_chance = min(0.95, base_miss_chance + (miss_chance_increase / 100.0))
        
        if random.random() < total_miss_chance:
            if miss_chance_increase > 0:
                self.ui.add_message(f"You attack {monster.name} blindly and miss!")
            else:
                self.ui.add_message(f"You try to attack {monster.name} and miss!")
            
            # Emit miss event
            event_emitter = EventEmitter()
            context = AttackContext(
                player=self.player,
                attacker=self.player,
                defender=monster,
                damage=0,
                is_critical=False,
                is_miss=True
            )
            event_emitter.emit(EventType.MISS, context)
            return
        
        # Check for evade
        if random.random() < monster.evade:
            self.ui.add_message(f"You try to attack {monster.name} and miss!")
            
            # Emit miss event
            event_emitter = EventEmitter()
            context = AttackContext(
                player=self.player,
                attacker=self.player,
                defender=monster,
                damage=0,
                is_critical=False,
                is_miss=True
            )
            event_emitter.emit(EventType.MISS, context)
            return
        
        # Calculate base damage (with frightened modifier)
        damage = self.player.get_total_attack() + attack_modifier
        damage = max(1, damage)  # Ensure minimum 1 damage
        
        # Check for critical hit (blocked by blinded)
        is_crit = can_crit and random.random() < self.player.get_total_crit()
        if is_crit:
            damage = int(damage * self.player.get_total_crit_multiplier())
            self.player.crit_count += 1
        
        # Apply aspect damage multipliers (after crit calculation)
        player_traits = self.player.get_total_attack_traits()
        aspect_multiplier = self.calculate_aspect_damage_multiplier(
            player_traits, monster.weaknesses, monster.resistances
        )
        damage = int(damage * aspect_multiplier)
        
        # Apply accessory damage bonuses (like PunishTheWeak)
        for accessory in self.player.equipped_accessories():
            if hasattr(accessory, 'get_damage_multiplier_vs_target'):
                accessory_multiplier = accessory.get_damage_multiplier_vs_target(monster)
                damage = int(damage * accessory_multiplier)
        
        # Check if weakness was exploited or resistance was applied
        weakness_exploited = any(trait in monster.weaknesses for trait in player_traits)
        resistance_applied = any(trait in monster.resistances for trait in player_traits)
        
        # Check if shields absorb the attack
        if monster.status_effects.absorb_attack():
            actual_damage = 0
            self.ui.add_message(f"The {monster.name}'s shields absorb the attack!")
        else:
            actual_damage = monster.take_damage_with_traits(damage, player_traits)
            
            # Apply elemental status effects if monster is not resistant to the trait
            self.apply_elemental_status_effects(player_traits, monster)
            
            # Apply weapon on-hit effects
            if self.player.weapon and hasattr(self.player.weapon, 'on_hit'):
                hit_message = self.player.weapon.on_hit(self.player, monster)
                if hit_message:
                    self.ui.add_message(hit_message)
        
        # Add weakness/resistance messages first if applicable
        if weakness_exploited and not resistance_applied:
            self.ui.add_message("Weakness exploited!")
        elif resistance_applied and not weakness_exploited:
            self.ui.add_message("Resistant!")
        # If both apply, don't add any extra message
        
        # Create appropriate message
        if is_crit:
            message = f"You critical hit on the {monster.name} for {actual_damage}!"
        else:
            message = f"You attack the {monster.name} for {actual_damage}!"
        
        self.ui.add_message(message)
        
        # Emit player attack event
        event_emitter = EventEmitter()
        trait_interaction = None
        if weakness_exploited and not resistance_applied:
            trait_interaction = "weakness"
        elif resistance_applied and not weakness_exploited:
            trait_interaction = "resistance"
        
        context = AttackContext(
            player=self.player,
            attacker=self.player,
            defender=monster,
            damage=actual_damage,
            is_critical=is_crit,
            is_miss=False,
            trait_interaction=trait_interaction
        )
        event_emitter.emit(EventType.PLAYER_ATTACK_MONSTER, context)
        
        # Emit trait-specific events
        if is_crit:
            event_emitter.emit(EventType.CRITICAL_HIT, context)
        if weakness_exploited and not resistance_applied:
            event_emitter.emit(EventType.WEAKNESS_HIT, context)
        elif resistance_applied and not weakness_exploited:
            event_emitter.emit(EventType.RESISTANCE_HIT, context)
        
        # Check if monster died
        if not monster.is_alive():
            death_message = f"The {monster.name} dies!"
            self.player.body_count += 1
            self.ui.add_message(death_message)
            
            # Give player XP
            leveled_up = self.player.gain_xp(monster.xp_value)
            xp_message = f"You gain {monster.xp_value} XP!"
            self.ui.add_message(xp_message, COLOR_GREEN)
            
            # Emit monster death event
            death_context = DeathContext(
                player=self.player,
                monster=monster,
                experience_gained=monster.xp_value
            )
            event_emitter.emit(EventType.MONSTER_DEATH, death_context)
            
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
            self.player.dodge_count += 1
            
            # Emit successful dodge event
            event_emitter = EventEmitter()
            context = AttackContext(
                player=self.player,
                attacker=monster,
                defender=self.player,
                damage=0,
                is_critical=False,
                is_miss=True
            )
            event_emitter.emit(EventType.SUCCESSFUL_DODGE, context)
            return
        
        # Calculate base damage
        damage = monster.attack
        
        # Check for critical hit
        is_crit = random.random() < monster.crit
        if is_crit:
            damage = int(damage * monster.crit_multiplier)
        
        # Apply aspect damage multipliers (after crit calculation)
        monster_traits = monster.attack_traits
        player_weaknesses = self.player.get_total_weaknesses()
        player_resistances = self.player.get_total_resistances()
        aspect_multiplier = self.calculate_aspect_damage_multiplier(
            monster_traits, player_weaknesses, player_resistances
        )
        damage = int(damage * aspect_multiplier)
        
        # Check if weakness was exploited or resistance was applied
        weakness_exploited = any(trait in player_weaknesses for trait in monster_traits)
        resistance_applied = any(trait in player_resistances for trait in monster_traits)
        
        # Check if shields absorb the attack
        if self.player.status_effects.absorb_attack():
            actual_damage = 0
            self.ui.add_message("Your shields absorb the attack!")
        else:
            # Apply status effect modifiers to defense and evade
            effective_defense = self.player.status_effects.get_effective_defense(self.player.get_total_defense())
            effective_evade = self.player.status_effects.get_effective_evade(self.player.get_total_evade())
            
            # Check for evade first
            if random.random() < effective_evade:
                actual_damage = 0
                self.player.dodge_count += 1
                self.ui.add_message("You dodged the attack!")
                
                # Emit successful dodge event
                event_emitter = EventEmitter()
                dodge_context = AttackContext(
                    player=self.player,
                    attacker=monster,
                    defender=self.player,
                    damage=0,
                    is_critical=False,
                    is_miss=True
                )
                event_emitter.emit(EventType.SUCCESSFUL_DODGE, dodge_context)
            else:
                # Apply damage with traits
                actual_damage = self.player.take_damage_with_traits(damage, monster_traits)
                
                # Apply elemental status effects if player is not resistant to the trait
                self.apply_elemental_status_effects(monster_traits, self.player)
        
        # Add weakness/resistance messages first if applicable
        if weakness_exploited and not resistance_applied:
            self.ui.add_message("Weakness exploited!")
        elif resistance_applied and not weakness_exploited:
            self.ui.add_message("Resistant!")
        # If both apply, don't add any extra message
        
        # Create appropriate message
        if is_crit:
            message = f"The {monster.name} critical hits you for {actual_damage}!"
        else:
            message = f"The {monster.name} attacks you for {actual_damage}!"
        
        self.ui.add_message(message)
        
        # Emit monster attack event
        event_emitter = EventEmitter()
        trait_interaction = None
        if weakness_exploited and not resistance_applied:
            trait_interaction = "weakness"
        elif resistance_applied and not weakness_exploited:
            trait_interaction = "resistance"
        
        attack_context = AttackContext(
            player=self.player,
            attacker=monster,
            defender=self.player,
            damage=actual_damage,
            is_critical=is_crit,
            is_miss=False,
            trait_interaction=trait_interaction
        )
        event_emitter.emit(EventType.MONSTER_ATTACK_PLAYER, attack_context)
        
        # Emit trait-specific events
        if is_crit:
            event_emitter.emit(EventType.CRITICAL_HIT, attack_context)
        if weakness_exploited and not resistance_applied:
            event_emitter.emit(EventType.WEAKNESS_HIT, attack_context)
        elif resistance_applied and not weakness_exploited:
            event_emitter.emit(EventType.RESISTANCE_HIT, attack_context)
        
        # Check if player died
        if not self.player.is_alive():
            death_message = "You have died!"
            self.ui.add_message(death_message)
            self.game_state = 'DEAD'
    
    def process_monster_turns(self):
        """Process AI turns for all monsters."""
        for monster in self.level.monsters:
            if monster.is_alive():
                # Process status effects at turn start
                should_skip_turn = self.process_status_effects_turn_start(monster)
                if not should_skip_turn:
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
        # Process player status effects at turn start
        if self.player.is_alive() and self.game_state == 'PLAYING':
            player_skips_turn = self.process_status_effects_turn_start(self.player)
            if player_skips_turn:
                # Player loses their turn, but monsters still get to act
                self.process_monster_turns()
                return
        
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
        result = self.level_manager.transition_down(self.player)
        
        if isinstance(result, tuple) and result[0]:  # Success with message
            success, message = result
            self.level = self.level_manager.get_current_area()
            self.current_level = self.level_manager.get_current_floor_number()
            self.highest_floor_reached = max(self.highest_floor_reached, self.current_level)
            
            # Add transition message
            if message:
                self.ui.add_message(message)
            
            # Update FOV for new area
            self.level.update_fov(self.player.x, self.player.y, self.player.get_total_fov())
            # Set flag to prevent immediate transition back
            self.just_changed_level = True
        elif result is True:  # Old format compatibility
            self.level = self.level_manager.get_current_area()
            self.current_level = self.level_manager.get_current_floor_number()
            self.highest_floor_reached = max(self.highest_floor_reached, self.current_level)
            
            # Update FOV for new area
            self.level.update_fov(self.player.x, self.player.y, self.player.get_total_fov())
            # Set flag to prevent immediate transition back
            self.just_changed_level = True
        else:
            # Floor 10 completed - should trigger victory
            if self.current_level >= 10:
                self.game_state = 'VICTORY'
    
    def register_equipment_events(self, equipment):
        """Register equipment with the event system."""
        if not hasattr(equipment, 'on_event'):
            return
        
        event_emitter = EventEmitter()
        subscribed_events = equipment.get_subscribed_events()
        
        for event_type in subscribed_events:
            event_emitter.subscribe(event_type, equipment.on_event)
    
    def unregister_equipment_events(self, equipment):
        """Unregister equipment from the event system."""
        if not hasattr(equipment, 'on_event'):
            return
        
        event_emitter = EventEmitter()
        subscribed_events = equipment.get_subscribed_events()
        
        for event_type in subscribed_events:
            event_emitter.unsubscribe(event_type, equipment.on_event)
    
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
        # Initialize level manager and game state
        self.level_manager = LevelManager()
        self.level = self.level_manager.get_current_area()
        self.current_level = self.level_manager.get_current_floor_number()
        self.highest_floor_reached = 1
        
        # Place player at stairs up position (or first room if no stairs)
        if hasattr(self.level, 'stairs_up_pos') and self.level.stairs_up_pos:
            start_x, start_y = self.level.stairs_up_pos
        elif hasattr(self.level, 'rooms') and len(self.level.rooms) > 0:
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
    
    def open_shop(self):
        """Open the shop interface when player enters a shop."""
        if self.level.shop:
            self.shop_manager.open_shop(self.level.shop, self.player)
            self.game_state = 'SHOP'
            self.ui.add_message("Welcome to the shop! Press TAB to switch between buying and selling.")
    
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
                    if success == "CHOICE_NEEDED":
                        # Boon needs player to choose between weapon and armor
                        enchantment_type = message  # message contains the enchantment type
                        self.pending_boon_item = item
                        self.pending_boon_enchantment = enchantment_type
                        self.ui.add_message(f"Choose enchantment target for {item.name}:")
                        self.ui.add_message(f"[W]eapon: {self.player.weapon.name}")
                        self.ui.add_message(f"[A]rmor: {self.player.armor.name}")
                        self.ui.add_message("Press W for weapon, A for armor, or ESC to cancel.")
                        self.game_state = 'BOON_CHOICE'
                    elif success:
                        self.player.consumable_count += 1
                        
                        # Emit consume event before removing item
                        event_emitter = EventEmitter()
                        context = ConsumeContext(
                            player=self.player,
                            item_type=type(item).__name__,
                            item=item
                        )
                        event_emitter.emit(EventType.PLAYER_CONSUME_ITEM, context)
                        
                        self.player.remove_item(item)
                        self.ui.add_message(message)
                        # Reset inventory pointer to first slot after consumable use
                        if len(self.player.inventory) > 0:
                            self.selected_item_index = len(self.player.inventory) - 1  # Newest item (first slot)
                        else:
                            self.selected_item_index = None
                    else:
                        self.ui.add_message(message)
                else:
                    # Legacy boolean format
                    if result:
                        # Emit consume event before removing item
                        event_emitter = EventEmitter()
                        context = ConsumeContext(
                            player=self.player,
                            item_type=type(item).__name__,
                            item=item
                        )
                        event_emitter.emit(EventType.PLAYER_CONSUME_ITEM, context)
                        
                        self.player.remove_item(item)
                        self.ui.add_message(f"You used a {item.name}.")
                        # Reset inventory pointer to first slot after consumable use
                        if len(self.player.inventory) > 0:
                            self.selected_item_index = len(self.player.inventory) - 1  # Newest item (first slot)
                        else:
                            self.selected_item_index = None
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
    
    def navigate_up(self):
        """Navigate up in the inventory, cycling between inventory and equipment."""
        if self.selection_mode == "inventory":
            if len(self.player.inventory) > 0:
                if self.selected_item_index is None:
                    # Start at newest item (last in actual list, first in display)
                    self.selected_item_index = len(self.player.inventory) - 1
                elif self.selected_item_index == len(self.player.inventory) - 1:
                    # At newest item (top of display), move to equipment section
                    self.selection_mode = "equipment" 
                    self.selected_item_index = None
                    self.selected_equipment_index = self.get_equipment_count() - 1  # Start at bottom of equipment
                else:
                    # Move to next newer item (higher actual index, up in display)
                    self.selected_item_index += 1
            else:
                # No inventory items, go to equipment
                self.selection_mode = "equipment"
                self.selected_equipment_index = self.get_equipment_count() - 1
        elif self.selection_mode == "equipment":
            equipment_count = self.get_equipment_count()
            if equipment_count > 0:
                if self.selected_equipment_index is None:
                    self.selected_equipment_index = 0
                elif self.selected_equipment_index == 0:
                    # Move to inventory section (top of display = newest item)
                    if len(self.player.inventory) > 0:
                        self.selection_mode = "inventory"
                        self.selected_equipment_index = None
                        self.selected_item_index = len(self.player.inventory) - 1  # Newest item
                    # If no inventory, stay in equipment
                else:
                    self.selected_equipment_index = (self.selected_equipment_index - 1) % equipment_count
    
    def navigate_down(self):
        """Navigate down in the inventory, cycling between inventory and equipment."""
        if self.selection_mode == "inventory":
            if len(self.player.inventory) > 0:
                if self.selected_item_index is None:
                    # Start at newest item (last in actual list, first in display)
                    self.selected_item_index = len(self.player.inventory) - 1
                elif self.selected_item_index == 0:
                    # At oldest item (bottom of display), move to equipment section
                    self.selection_mode = "equipment"
                    self.selected_item_index = None
                    self.selected_equipment_index = 0  # Start at top of equipment
                else:
                    # Move to next older item (lower actual index, down in display)
                    self.selected_item_index -= 1
            else:
                # No inventory items, go to equipment
                self.selection_mode = "equipment"
                self.selected_equipment_index = 0
        elif self.selection_mode == "equipment":
            equipment_count = self.get_equipment_count()
            if equipment_count > 0:
                if self.selected_equipment_index is None:
                    self.selected_equipment_index = 0
                elif self.selected_equipment_index == equipment_count - 1:
                    # Move to inventory section (top of display = newest item)
                    if len(self.player.inventory) > 0:
                        self.selection_mode = "inventory"
                        self.selected_equipment_index = None
                        self.selected_item_index = len(self.player.inventory) - 1  # Newest item
                    # If no inventory, stay in equipment
                else:
                    self.selected_equipment_index = (self.selected_equipment_index + 1) % equipment_count
    
    def get_equipment_count(self):
        """Get the number of equipment slots (weapon + armor + 3 accessories)."""
        return 5  # Weapon, Armor, 3 Accessory slots
    
    def get_selected_equipment_item(self):
        """Get the currently selected equipment item or None if slot is empty."""
        if self.selected_equipment_index is None:
            return None
        
        if self.selected_equipment_index == 0:  # Weapon
            return self.player.weapon
        elif self.selected_equipment_index == 1:  # Armor
            return self.player.armor
        elif 2 <= self.selected_equipment_index <= 4:  # Accessories
            accessory_index = self.selected_equipment_index - 2
            return self.player.accessories[accessory_index]
        
        return None
    
    def unequip_selected_item(self):
        """Unequip the currently selected equipment item."""
        if self.selected_equipment_index is None:
            return
        
        # Check if inventory has space first
        if len(self.player.inventory) >= self.player.inventory_size:
            self.ui.add_message("Cannot unequip. Inventory is full.")
            return
        
        item = self.get_selected_equipment_item()
        if item is None:
            self.ui.add_message("No item equipped in this slot.")
            return
        
        # Unregister events first
        self.unregister_equipment_events(item)
        
        # Unequip the item
        if self.selected_equipment_index == 0:  # Weapon
            self.player.weapon = None
        elif self.selected_equipment_index == 1:  # Armor  
            self.player.armor = None
        elif 2 <= self.selected_equipment_index <= 4:  # Accessories
            accessory_index = self.selected_equipment_index - 2
            self.player.accessories[accessory_index] = None
        
        # Add to inventory
        self.player.add_item(item)
        self.ui.add_message(f"You unequipped {item.name}.")
        
        # Update FOV if weapon/armor changed
        if self.selected_equipment_index <= 1:
            self.level.update_fov(self.player.x, self.player.y, self.player.get_total_fov())
    
    def handle_accessory_slot_key(self, slot_index):
        """Handle accessory slot keys 1-3 for equipping/unequipping accessories."""
        # Check if slot_index is valid (0-2 for slots 1-3)
        if not (0 <= slot_index < 3):
            return
        
        # Check if slot is currently occupied
        slot_occupied = self.player.accessories[slot_index] is not None
        
        if slot_occupied:
            # Slot is occupied - UNEQUIP the accessory
            accessory_to_unequip = self.player.accessories[slot_index]
            self.unregister_equipment_events(accessory_to_unequip)
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
            
            
            # Equip accessory to the specific slot
            # Note: accessories list should always have 3 slots initialized with None
            self.player.accessories[slot_index] = selected_item
            self.player.remove_item(selected_item)
            
            # Register events for new accessory
            self.register_equipment_events(selected_item)
            
            self.ui.add_message(f"You equipped {selected_item.name} to slot {slot_index + 1}.")
            
            # Update FOV after equipment change
            self.level.update_fov(self.player.x, self.player.y, self.player.get_total_fov())
            
            # Adjust selection after equipping (item was removed from inventory)
            if len(self.player.inventory) == 0:
                self.selected_item_index = None
            elif self.selected_item_index >= len(self.player.inventory):
                self.selected_item_index = len(self.player.inventory) - 1
    
    def select_equipment_slot(self, slot_index):
        """Select an equipment slot (0-4 for slots 1-5) and highlight it."""
        # Map slot numbers to equipment indices:
        # Slot 1 (index 0) = Weapon (equipment_index 0)
        # Slot 2 (index 1) = Armor (equipment_index 1) 
        # Slot 3 (index 2) = Accessory 1 (equipment_index 2)
        # Slot 4 (index 3) = Accessory 2 (equipment_index 3)
        # Slot 5 (index 4) = Accessory 3 (equipment_index 4)
        
        if 0 <= slot_index <= 4:  # Valid slot indices
            # Switch to equipment mode and select the slot
            self.selection_mode = "equipment"
            self.selected_item_index = None
            self.selected_equipment_index = slot_index
    
    def equip_item(self, item):
        """Equip an item and handle slot management."""
        
        slot = item.equipment_slot
        
        if slot == "weapon":
            # Check if we need to unequip current weapon and if there's space
            if self.player.weapon:
                old_weapon = self.player.weapon
                # Check if inventory has space for the old weapon
                if not self.player.add_item(old_weapon):
                    self.ui.add_message(f"Cannot equip {item.name}. Inventory is full.")
                    return
                # Unregister events for old weapon
                self.unregister_equipment_events(old_weapon)
                self.player.weapon = None
                self.ui.add_message(f"You unequipped {old_weapon.name}.")
            
            # Equip new weapon
            self.player.weapon = item
            self.player.remove_item(item)
            
            # Register events for new weapon
            self.register_equipment_events(item)
            self.ui.add_message(f"You equipped {item.name}.")
            
        elif slot == "armor":
            # Check if we need to unequip current armor and if there's space
            if self.player.armor:
                old_armor = self.player.armor
                # Check if inventory has space for the old armor
                if not self.player.add_item(old_armor):
                    self.ui.add_message(f"Cannot equip {item.name}. Inventory is full.")
                    return
                # Unregister events for old armor
                self.unregister_equipment_events(old_armor)
                self.player.armor = None
                self.ui.add_message(f"You unequipped {old_armor.name}.")
            
            # Equip new armor
            self.player.armor = item
            self.player.remove_item(item)
            
            # Register events for new armor
            self.register_equipment_events(item)
            self.ui.add_message(f"You equipped {item.name}.")
            
        elif slot == "accessory":
            # Check if there's an available accessory slot
            if len(self.player.equipped_accessories()) < self.player.accessory_slots:
                # Find first empty slot (None) and equip there
                for i in range(len(self.player.accessories)):
                    if self.player.accessories[i] is None:
                        self.player.accessories[i] = item
                        break
                self.player.remove_item(item)
                
                # Register events for new accessory
                self.register_equipment_events(item)
                
                self.ui.add_message(f"You equipped {item.name}.")
            else:
                # All slots are full - ask which one to replace
                self.ui.add_message("All accessory slots are full. Which accessory would you like to replace?")
                for i, accessory in enumerate(self.player.equipped_accessories()):
                    self.ui.add_message(f"{i+1}: {accessory.name}")
                self.ui.add_message("Press 1-3 to select which accessory to replace, or ESC to cancel.")
                self.pending_accessory_replacement = item
                self.game_state = 'ACCESSORY_REPLACEMENT'
        
        # Update FOV after equipment change (some items affect FOV)
        self.level.update_fov(self.player.x, self.player.y, self.player.get_total_fov())
        
        # Only return to playing if not in inventory mode and not in victory state
        if self.game_state not in ['INVENTORY', 'VICTORY']:
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
        elif self.game_state == 'SHOP':
            # Render shop interface
            self.level.render(self.console)
            self.player.render(self.console, self.level.fov)
            self.shop_manager.render(self.console)
            self.ui.render(self.console, self.player, self.level_manager.get_display_name(), self.level)
        elif self.game_state == 'INVENTORY':
            # Render inventory screen
            self.ui.render_inventory(self.console, self.player, self.selected_item_index, 
                                    self.selected_equipment_index, self.selection_mode, game_state=self.game_state)
        elif self.game_state == 'ACCESSORY_REPLACEMENT':
            # Render accessory replacement screen
            self.ui.render_inventory(self.console, self.player, self.selected_item_index, 
                                    self.selected_equipment_index, self.selection_mode, game_state=self.game_state)
        elif self.game_state == 'BOON_CHOICE':
            # Render boon choice screen
            self.ui.render_inventory(self.console, self.player, self.selected_item_index, 
                                    self.selected_equipment_index, self.selection_mode, 
                                    game_state=self.game_state, pending_boon=self.pending_boon_item)
        else:
            # Normal game rendering
            # Render the level
            self.level.render(self.console)
            
            # Render the player
            self.player.render(self.console, self.level.fov)
            
            # Render the UI
            self.ui.render(self.console, self.player, self.level_manager.get_display_name(), self.level)