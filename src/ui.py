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
    
    def render(self, console, player, current_level):
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
                console.print(0, ui_y, f"Weapon: {weapon_name}", fg=COLOR_WHITE)
                console.print(25, ui_y, f"Armor: {armor_name}", fg=COLOR_WHITE)
                ui_y += 1
            
            # Message log
            for i, (message, color) in enumerate(self.message_log):
                if ui_y + i < SCREEN_HEIGHT:
                    console.print(0, ui_y + i, message, fg=color)
    
    def render_inventory(self, console, player):
        """Render the inventory screen."""
        console.clear()
        
        # Title
        console.print(0, 0, "Inventory", fg=COLOR_WHITE)
        console.print(0, 1, "---------", fg=COLOR_WHITE)
        
        # List items
        y = 3
        for i, item in enumerate(player.inventory):
            letter = chr(ord('a') + i)
            console.print(0, y + i, f"{letter}) {item.name}", fg=COLOR_WHITE)
        
        if not player.inventory:
            console.print(0, y, "Empty", fg=COLOR_WHITE)
        
        # Instructions
        console.print(0, SCREEN_HEIGHT - 2, "Press ESC to close", fg=COLOR_WHITE)