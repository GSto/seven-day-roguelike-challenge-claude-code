"""
User interface rendering and management.
"""

from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, MAP_HEIGHT,
    COLOR_WHITE, COLOR_RED, COLOR_GREEN, COLOR_YELLOW, COLOR_GRAY
)


class UI:
    """Handles user interface rendering."""
    
    def __init__(self):
        """Initialize the UI."""
        self.message_log = []
        self.max_messages = 6
    
    def add_message(self, message, color=COLOR_WHITE):
        """Add a message to the message log."""
        self.message_log.append((message, color))
        
        # Keep only the most recent messages
        if len(self.message_log) > self.max_messages:
            self.message_log.pop(0)
    
    def render(self, console, player, current_level, level=None):
        """Render the UI elements."""
        # UI panel starts below the map
        ui_y = MAP_HEIGHT
        
        # Draw a horizontal line to separate the map from UI
        if ui_y < SCREEN_HEIGHT:
            for x in range(SCREEN_WIDTH):
                console.print(x, ui_y, '-', fg=COLOR_WHITE)
        
        ui_y += 1
        
        # Only render UI elements if we have space
        if ui_y < SCREEN_HEIGHT:
            # Player stats
            hp_color = COLOR_GREEN if player.hp > player.max_hp * 0.3 else COLOR_RED
            console.print(0, ui_y, f"HP:  {player.hp}/{player.max_hp}", fg=hp_color)
            console.print(20, ui_y, f"LVL: {player.level}", fg=COLOR_WHITE)
            console.print(35, ui_y, f"XP: {player.xp}", fg=COLOR_WHITE)
            console.print(50, ui_y, f"Floor: {current_level}", fg=COLOR_WHITE)
            
            # Add "Next Lvl:" under dungeon level with level up indicator
            level_up_color = COLOR_YELLOW if player.can_level_up() else COLOR_WHITE
            level_up_text = f"Next Lvl: {player.xp_to_next}"
            if player.can_level_up():
                level_up_text += " (Press X)"
            console.print(50, ui_y + 1, level_up_text, fg=level_up_color)
            
            ui_y += 1  # Account for the extra "Next Lvl:" line
            
            # Combat stats
            if ui_y < SCREEN_HEIGHT:
                console.print(0, ui_y, f"ATK: {player.get_total_attack()}", fg=COLOR_WHITE)
                console.print(20, ui_y, f"DEF: {player.get_total_defense()}", fg=COLOR_WHITE)
                ui_y += 2
            
            # Equipment
            if ui_y < SCREEN_HEIGHT:
                weapon_name = player.weapon.name if player.weapon else "None"
                armor_name = player.armor.name if player.armor else "None"
                weapon_text = f"Weapon: {weapon_name}"
                
                # Dynamic positioning: place armor text with padding after weapon text
                console.print(0, ui_y, weapon_text, fg=COLOR_WHITE)
                armor_x = len(weapon_text) + 3  # 3 character padding
                console.print(armor_x, ui_y, f"Armor: {armor_name}", fg=COLOR_WHITE)
                ui_y += 1
                
                # # Show accessories (up to 3)
                # if ui_y < SCREEN_HEIGHT:
                #     accessories_text = "Accessories: "
                #     equipped_accessories = player.equipped_accessories()
                #     if len(equipped_accessories) == 0:
                #         accessories_text += "None"
                #     else:
                #         accessory_names = [acc.name for acc in equipped_accessories]
                #         accessories_text += ", ".join(accessory_names)
                #         # Add empty slot indicators
                #         empty_slots = player.accessory_slots - len(equipped_accessories)
                #         if empty_slots > 0:
                #             accessories_text += f" (+{empty_slots} empty)"
                #     console.print(0, ui_y, accessories_text, fg=COLOR_WHITE)
                #     ui_y += 1
            
            # Message log (reserve space for 6 lines, but only show actual messages)
            log_start_y = ui_y
            for i, (message, color) in enumerate(self.message_log):
                if log_start_y + i < SCREEN_HEIGHT - 3:  # Leave space for prompts and controls
                    console.print(0, log_start_y + i, message, fg=color)
            
            # Calculate where action prompts should go (ensure they fit on screen)
            # Leave at least 2 lines for prompts + controls at bottom
            max_log_space = SCREEN_HEIGHT - log_start_y - 3  # 3 lines for prompts/controls
            actual_log_lines = min(len(self.message_log), max_log_space)
            ui_y = log_start_y + actual_log_lines
            
            # Show contextual prompts on their own line
            if level and level.get_item_at(player.x, player.y):
                item = level.get_item_at(player.x, player.y)
                pickup_prompt = f"Press 'g' to pick up {item.name}"
                if ui_y < SCREEN_HEIGHT - 1:
                    console.print(0, ui_y, pickup_prompt, fg=COLOR_GREEN)
                    ui_y += 1
            elif level and level.is_stairs_down(player.x, player.y):
                stairs_prompt = "Press arrow keys to descend to next level"
                if ui_y < SCREEN_HEIGHT - 1:
                    console.print(0, ui_y, stairs_prompt, fg=COLOR_GREEN)
                    ui_y += 1
            elif level and level.is_stairs_up(player.x, player.y):
                stairs_prompt = "Press arrow keys to ascend to previous level"
                if ui_y < SCREEN_HEIGHT - 1:
                    console.print(0, ui_y, stairs_prompt, fg=COLOR_GREEN)
                    ui_y += 1
            
            # Controls reminder at bottom
            controls_text = "Controls: [G]et items  [I]nventory  [L]evel up  [ESC]ape/Quit"
            if SCREEN_HEIGHT - 1 >= 0:
                console.print(0, SCREEN_HEIGHT - 1, controls_text, fg=COLOR_WHITE)
    
    def render_inventory(self, console, player, selected_item_index=None):
        """Render the inventory screen."""
        console.clear()
        
        # Title
        console.print(0, 0, "Inventory", fg=COLOR_WHITE)
        console.print(0, 1, "---------", fg=COLOR_WHITE)
        
        # Show inventory size
        inventory_info = f"Items: {len(player.inventory)}/{player.inventory_size}"
        console.print(0, 2, inventory_info, fg=COLOR_WHITE)
        
        # List items
        y = 4
        for i, item in enumerate(player.inventory):
            letter = chr(ord('a') + i)
            # Show item type indicator
            if hasattr(item, 'equipment_slot'):
                type_indicator = f"[{item.equipment_slot[0].upper()}]"
            elif hasattr(item, 'use'):
                type_indicator = "[C]"
            else:
                type_indicator = "[?]"
            
            # Add comprehensive stat information for equipment
            stat_info_parts = []
            if hasattr(item, 'attack_bonus') and item.attack_bonus > 0:
                stat_info_parts.append(f"+{item.attack_bonus} att")
            if hasattr(item, 'defense_bonus') and item.defense_bonus > 0:
                stat_info_parts.append(f"+{item.defense_bonus} def")
            if hasattr(item, 'fov_bonus') and item.fov_bonus > 0:
                stat_info_parts.append(f"+{item.fov_bonus} fov")
            if hasattr(item, 'health_aspect_bonus') and item.health_aspect_bonus > 0:
                heal_percent = int(item.health_aspect_bonus * 100)
                stat_info_parts.append(f"{heal_percent}% heal")
            if hasattr(item, 'attack_multiplier_bonus') and item.attack_multiplier_bonus > 1.0:
                att_mult_percent = int(item.attack_multiplier_bonus * 100)
                stat_info_parts.append(f"{att_mult_percent}% att")
            if hasattr(item, 'defense_multiplier_bonus') and item.defense_multiplier_bonus > 1.0:
                def_mult_percent = int(item.defense_multiplier_bonus * 100)
                stat_info_parts.append(f"{def_mult_percent}% def")
            if hasattr(item, 'xp_multiplier_bonus') and item.xp_multiplier_bonus > 1.0:
                xp_mult_percent = int(item.xp_multiplier_bonus * 100)
                stat_info_parts.append(f"{xp_mult_percent}% xp")
            if hasattr(item, 'heal_percentage'):
                stat_info_parts.append(f"heals {item.heal_percentage}%")
            if hasattr(item, 'heal_amount'):
                stat_info_parts.append(f"heals {item.heal_amount}")
            
            stat_info = f" ({', '.join(stat_info_parts)})" if stat_info_parts else ""
            
            # Highlight selected item
            fg_color = COLOR_GREEN if i == selected_item_index else COLOR_WHITE
            item_text = f"{letter}) {type_indicator} {item.name}{stat_info}"
            console.print(0, y + i, item_text, fg=fg_color)
        
        if not player.inventory:
            console.print(0, y, "Empty", fg=COLOR_WHITE)
        
        # Show currently equipped items
        eq_y = y + len(player.inventory) + 2
        if eq_y < SCREEN_HEIGHT - 8:  # Leave more space for description
            console.print(0, eq_y, "Currently Equipped:", fg=COLOR_GREEN)
            eq_y += 1
            # Show equipped items with stat bonuses
            weapon_text = "None"
            if player.weapon:
                weapon_bonus = f" (+{player.weapon.get_attack_bonus(player)})" if player.weapon.get_attack_bonus(player) != 0 else ""
                weapon_text = f"{player.weapon.name}{weapon_bonus}"
            
            armor_text = "None"
            if player.armor:
                armor_bonus = f" (+{player.armor.get_defense_bonus(player)})" if player.armor.defense_bonus != 0 else ""
                armor_text = f"{player.armor.name}{armor_bonus}"
            
            console.print(0, eq_y, f"Weapon: {weapon_text}", fg=COLOR_WHITE)
            console.print(0, eq_y + 1, f"Armor: {armor_text}", fg=COLOR_WHITE)
            eq_y += 2
            
            # Show all accessories
            console.print(0, eq_y, "Accessories:", fg=COLOR_WHITE)
            eq_y += 1

            for i, accessory in enumerate(player.accessories):
                slot_num = i + 1
                if(accessory is None):
                    console.print(2, eq_y, f"Slot {slot_num}: Empty", fg=COLOR_GRAY)
                else: 
                  console.print(2, eq_y, f"Slot {i+1}: {accessory.name}", fg=COLOR_WHITE)
                eq_y += 1
        
        # Show item description when an item is selected (always show when selected)
        # Place it AFTER the equipped items section
        if (selected_item_index is not None and 
            0 <= selected_item_index < len(player.inventory)):
            selected_item = player.inventory[selected_item_index]
            desc_y = eq_y + 1  # Place after equipped items
            console.print(0, desc_y, "Item Description:", fg=COLOR_GREEN)
            desc_y += 1
            
            # Detailed description with comprehensive bonuses
            desc_lines = []
            if hasattr(selected_item, 'description'):
                desc_lines.append(selected_item.description)
            
            # Equipment bonuses
            if hasattr(selected_item, 'attack_bonus') and selected_item.attack_bonus > 0:
                desc_lines.append(f"Attack Bonus: +{selected_item.get_attack_bonus(player)}")
            
            if hasattr(selected_item, 'defense_bonus') and selected_item.defense_bonus > 0:
                desc_lines.append(f"Defense Bonus: +{selected_item.get_defense_bonus(player)}")
            
            if hasattr(selected_item, 'fov_bonus') and selected_item.fov_bonus > 0:
                desc_lines.append(f"FOV Bonus: +{selected_item.get_fov_bonus(player)}")
            
            if hasattr(selected_item, 'health_aspect_bonus') and selected_item.health_aspect_bonus > 0:
                healing_bonus_percent = int(selected_item.get_health_aspect_bonus(player) * 100)
                desc_lines.append(f"Healing Bonus: {healing_bonus_percent}%")
            
            # Multiplier bonuses (displayed as percentages)
            if hasattr(selected_item, 'attack_multiplier_bonus') and selected_item.attack_multiplier_bonus > 1.0:
                attack_mult_percent = int(selected_item.get_attack_multiplier_bonus(player) * 100)
                desc_lines.append(f"Attack Multiplier: {attack_mult_percent}%")
            
            if hasattr(selected_item, 'defense_multiplier_bonus') and selected_item.defense_multiplier_bonus > 1.0:
                defense_mult_percent = int(selected_item.get_defense_multiplier_bonus(player) * 100)
                desc_lines.append(f"Defense Multiplier: {defense_mult_percent}%")
            
            if hasattr(selected_item, 'xp_multiplier_bonus') and selected_item.xp_multiplier_bonus > 1.0:
                xp_mult_percent = int(selected_item.get_xp_multiplier_bonus(player) * 100)
                desc_lines.append(f"XP Multiplier: {xp_mult_percent}%")
            
            # Consumable effects
            if hasattr(selected_item, 'heal_percentage'):
                desc_lines.append(f"Heals: {selected_item.heal_percentage}% of max HP")
            if hasattr(selected_item, 'heal_amount'):
                desc_lines.append(f"Heals: {selected_item.heal_amount} HP")
            # Show effect value for consumables that use dynamic healing
            elif (hasattr(selected_item, 'effect_value') and 
                  hasattr(selected_item, 'use') and 
                  selected_item.effect_value > 0 and
                  'Health Potion' in selected_item.name):
                desc_lines.append(f"Healing Factor: {selected_item.effect_value}x (scales with health aspect)")
            
            # Show enchantments for weapons
            if hasattr(selected_item, 'enchantments') and selected_item.enchantments:
                enchant_names = [e.name for e in selected_item.enchantments]
                desc_lines.append(f"Enchantments: {', '.join(enchant_names)}")
            
            for line in desc_lines:
                console.print(0, desc_y, line, fg=COLOR_WHITE)
                desc_y += 1
            
            desc_y += 1  # Add space between description and player summary
        
        # Player summary section (always show when in inventory)
        # Position it after item description or after equipped items if no item selected
        summary_y = desc_y if (selected_item_index is not None and 
                              0 <= selected_item_index < len(player.inventory)) else eq_y + 1
        
        if summary_y < SCREEN_HEIGHT - 6:  # Leave space for controls
            console.print(0, summary_y, "Player Summary:", fg=COLOR_GREEN)
            summary_y += 1
            
            # HP
            hp_color = COLOR_GREEN if player.hp > player.max_hp * 0.3 else COLOR_RED
            console.print(0, summary_y, f"HP: {player.hp}/{player.max_hp}", fg=hp_color)
            summary_y += 1
            
            # XP and level
            console.print(0, summary_y, f"Level: {player.level}  XP: {player.xp}", fg=COLOR_WHITE)
            summary_y += 1
            
            # Combat stats
            console.print(0, summary_y, f"ATK: {player.get_total_attack()}", fg=COLOR_WHITE)
            summary_y += 1

            console.print(0, summary_y, f"DEF: {player.get_total_defense()}", fg=COLOR_WHITE)
            summary_y += 1

            console.print(0, summary_y, f"CRT: {int(player.get_total_crit() * 100)}%", fg=COLOR_WHITE)
            summary_y += 1

            console.print(0, summary_y, f"EVD: {int(player.get_total_evade() * 100)}%", fg=COLOR_WHITE)
            summary_y += 1
            
            # Healing aspect and multipliers (displayed as percentages, one per line)
            healing_percent = int(player.get_total_health_aspect() * 100)
            console.print(0, summary_y, f"Healing: {healing_percent}%", fg=COLOR_WHITE)
            summary_y += 1
            
            attack_mult_percent = int(player.get_total_attack_multiplier() * 100)
            console.print(0, summary_y, f"Attack Mult: {attack_mult_percent}%", fg=COLOR_WHITE)
            summary_y += 1
            
            defense_mult_percent = int(player.get_total_defense_multiplier() * 100)
            console.print(0, summary_y, f"Defense Mult: {defense_mult_percent}%", fg=COLOR_WHITE)
            summary_y += 1
            
            xp_mult_percent = int(player.get_total_xp_multiplier() * 100)
            console.print(0, summary_y, f"XP Mult: {xp_mult_percent}%", fg=COLOR_WHITE)
        
        # Instructions with better formatting
        console.print(0, SCREEN_HEIGHT - 5, "Controls:", fg=COLOR_GREEN)
        console.print(0, SCREEN_HEIGHT - 4, "Arrow keys or letter to select item", fg=COLOR_WHITE)
        console.print(0, SCREEN_HEIGHT - 3, "[Enter] Use/Equip  [D] Drop", fg=COLOR_WHITE)
        console.print(0, SCREEN_HEIGHT - 2, "1-3: Manage accessory slots", fg=COLOR_WHITE)
        console.print(0, SCREEN_HEIGHT - 1, "Press ESC to close inventory", fg=COLOR_WHITE)