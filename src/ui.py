"""
User interface rendering and management.
"""

from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, MAP_HEIGHT,
    COLOR_WHITE, COLOR_RED, COLOR_GREEN
)


class UI:
    """Handles user interface rendering."""
    
    def __init__(self):
        """Initialize the UI."""
        self.message_log = []
        self.max_messages = 5
    
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
            console.print(0, ui_y, f"HP: {player.hp}/{player.max_hp}", fg=hp_color)
            console.print(20, ui_y, f"Level: {player.level}", fg=COLOR_WHITE)
            console.print(35, ui_y, f"XP: {player.xp}/{player.xp_to_next}", fg=COLOR_WHITE)
            console.print(55, ui_y, f"Dungeon Level: {current_level}", fg=COLOR_WHITE)
            
            ui_y += 1
            
            # Combat stats
            if ui_y < SCREEN_HEIGHT:
                console.print(0, ui_y, f"Attack: {player.get_total_attack()}", fg=COLOR_WHITE)
                console.print(20, ui_y, f"Defense: {player.get_total_defense()}", fg=COLOR_WHITE)
                ui_y += 1
            
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
            
            # Show contextual prompts
            if level and level.get_item_at(player.x, player.y):
                item = level.get_item_at(player.x, player.y)
                pickup_prompt = f"Press 'g' to pick up {item.name}"
                console.print(0, ui_y, pickup_prompt, fg=COLOR_GREEN)
                ui_y += 1
            elif level and level.is_stairs_down(player.x, player.y):
                stairs_prompt = "Press arrow keys to descend to next level"
                console.print(0, ui_y, stairs_prompt, fg=COLOR_GREEN)
                ui_y += 1
            elif level and level.is_stairs_up(player.x, player.y):
                stairs_prompt = "Press arrow keys to ascend to previous level"
                console.print(0, ui_y, stairs_prompt, fg=COLOR_GREEN)
                ui_y += 1
            
            # Message log
            for i, (message, color) in enumerate(self.message_log):
                if ui_y + i < SCREEN_HEIGHT:
                    console.print(0, ui_y + i, message, fg=color)
            
            # Controls reminder at bottom
            controls_text = "Controls: [G]et items  [I]nventory  [ESC]ape/Quit"
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
            
            # Add stat information for equipment
            stat_info = ""
            if hasattr(item, 'attack_bonus') and item.attack_bonus > 0:
                stat_info = f" (+{item.attack_bonus} att)"
            elif hasattr(item, 'defense_bonus') and item.defense_bonus > 0:
                stat_info = f" (+{item.defense_bonus} def)"
            elif hasattr(item, 'heal_percentage'):
                stat_info = f" (heals {item.heal_percentage}%)"
            elif hasattr(item, 'heal_amount'):
                stat_info = f" (heals {item.heal_amount})"
            
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
                weapon_bonus = f" (+{player.weapon.attack_bonus})" if player.weapon.attack_bonus > 0 else ""
                weapon_text = f"{player.weapon.name}{weapon_bonus}"
            
            armor_text = "None"
            if player.armor:
                armor_bonus = f" (+{player.armor.defense_bonus})" if player.armor.defense_bonus > 0 else ""
                armor_text = f"{player.armor.name}{armor_bonus}"
            
            accessory_text = "None"
            if player.accessory:
                accessory_text = player.accessory.name
            
            console.print(0, eq_y, f"Weapon: {weapon_text}", fg=COLOR_WHITE)
            console.print(0, eq_y + 1, f"Armor: {armor_text}", fg=COLOR_WHITE)
            console.print(0, eq_y + 2, f"Accessory: {accessory_text}", fg=COLOR_WHITE)
            eq_y += 3  # Move past the equipment section
        
        # Show item description when an item is selected (always show when selected)
        # Place it AFTER the equipped items section
        if (selected_item_index is not None and 
            0 <= selected_item_index < len(player.inventory)):
            selected_item = player.inventory[selected_item_index]
            desc_y = eq_y + 1  # Place after equipped items
            console.print(0, desc_y, "Item Description:", fg=COLOR_GREEN)
            desc_y += 1
            
            # Detailed description (you can expand this based on item types)
            desc_lines = []
            if hasattr(selected_item, 'description'):
                desc_lines.append(selected_item.description)
            
            if hasattr(selected_item, 'attack_bonus') and selected_item.attack_bonus > 0:
                desc_lines.append(f"Attack Bonus: +{selected_item.attack_bonus}")
            
            if hasattr(selected_item, 'defense_bonus') and selected_item.defense_bonus > 0:
                desc_lines.append(f"Defense Bonus: +{selected_item.defense_bonus}")
            
            if hasattr(selected_item, 'heal_percentage'):
                desc_lines.append(f"Heals: {selected_item.heal_percentage}% of max HP")
            elif hasattr(selected_item, 'heal_amount'):
                desc_lines.append(f"Heals: {selected_item.heal_amount} HP")
            
            for line in desc_lines:
                console.print(0, desc_y, line, fg=COLOR_WHITE)
                desc_y += 1
        
        # Instructions with better formatting
        console.print(0, SCREEN_HEIGHT - 4, "Controls:", fg=COLOR_GREEN)
        console.print(0, SCREEN_HEIGHT - 3, "Arrow keys or letter to select item", fg=COLOR_WHITE)
        console.print(0, SCREEN_HEIGHT - 2, "[Enter] Use/Equip  [D] Drop", fg=COLOR_WHITE)
        console.print(0, SCREEN_HEIGHT - 1, "Press ESC to close inventory", fg=COLOR_WHITE)