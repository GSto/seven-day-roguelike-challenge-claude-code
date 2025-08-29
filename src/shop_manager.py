"""
Shop UI manager for handling shop interface and transactions.
"""

from typing import Optional
import tcod.event
from shop import Shop


class ShopManager:
    """Manages shop UI state and interactions."""
    
    def __init__(self):
        """Initialize the shop manager."""
        self.current_shop: Optional[Shop] = None
        self.ui_mode: Optional[str] = None  # 'buy' or 'sell'
        self.selected_index: int = 0
        self.player = None
        self.is_open: bool = False
        
    def open_shop(self, shop: Shop, player):
        """Initialize shop interface."""
        self.current_shop = shop
        self.player = player
        self.ui_mode = 'buy'
        self.selected_index = 0
        self.is_open = True
        
    def close_shop(self):
        """Close the shop interface."""
        self.current_shop = None
        self.player = None
        self.ui_mode = None
        self.selected_index = 0
        self.is_open = False
    
    def handle_input(self, key) -> Optional[str]:
        """
        Process keyboard input in shop UI.
        
        Returns:
            Action string or None
        """
        if not self.is_open:
            return None
        
        # Handle navigation
        if key == tcod.event.K_UP:
            self.move_selection(-1)
            return "navigate"
        elif key == tcod.event.K_DOWN:
            self.move_selection(1)
            return "navigate"
        
        # Handle mode switching
        elif key == tcod.event.K_TAB:
            self.toggle_mode()
            return "mode_switch"
        
        # Handle buy/sell
        elif key == tcod.event.K_RETURN or key == tcod.event.K_KP_ENTER:
            if self.ui_mode == 'buy':
                return self.handle_buy()
            else:
                return self.handle_sell()
        
        # Handle exit
        elif key == tcod.event.K_ESCAPE:
            self.close_shop()
            return "exit_shop"
        
        return None
    
    def move_selection(self, delta: int):
        """Move the selection cursor up or down."""
        if self.ui_mode == 'buy':
            # Navigate through shop inventory
            max_index = len([i for i in self.current_shop.inventory if i is not None]) - 1
            if max_index >= 0:
                self.selected_index = max(0, min(max_index, self.selected_index + delta))
        else:
            # Navigate through player inventory
            max_index = len(self.player.inventory) - 1
            if max_index >= 0:
                self.selected_index = max(0, min(max_index, self.selected_index + delta))
    
    def toggle_mode(self):
        """Switch between buy and sell modes."""
        if self.ui_mode == 'buy':
            self.ui_mode = 'sell'
        else:
            self.ui_mode = 'buy'
        self.selected_index = 0
    
    def handle_buy(self) -> Optional[str]:
        """Process a buy transaction."""
        if not self.current_shop or not self.player:
            return None
        
        # Find the actual item at selected index (skip None slots)
        actual_index = 0
        items_seen = 0
        for i, item in enumerate(self.current_shop.inventory):
            if item is not None:
                if items_seen == self.selected_index:
                    actual_index = i
                    break
                items_seen += 1
        
        success, message = self.current_shop.buy_item(actual_index, self.player)
        
        # Adjust selection if needed
        if success:
            # Check if we need to move selection
            non_empty_items = [i for i in self.current_shop.inventory if i is not None]
            if self.selected_index >= len(non_empty_items) and self.selected_index > 0:
                self.selected_index -= 1
        
        return f"buy:{message}"
    
    def handle_sell(self) -> Optional[str]:
        """Process a sell transaction."""
        if not self.current_shop or not self.player:
            return None
        
        if self.selected_index >= len(self.player.inventory):
            return "sell:No item selected."
        
        item = self.player.inventory[self.selected_index]
        success, message = self.current_shop.sell_item(item, self.player)
        
        # Adjust selection if needed
        if success and self.selected_index >= len(self.player.inventory) and self.selected_index > 0:
            self.selected_index -= 1
        
        return f"sell:{message}"
    
    def get_display_items(self):
        """Get items to display based on current mode."""
        if self.ui_mode == 'buy':
            # Return shop inventory (excluding None slots)
            return [(i, item) for i, item in enumerate(self.current_shop.inventory) if item is not None]
        else:
            # Return player inventory with sell prices
            return [(i, item) for i, item in enumerate(self.player.inventory)]
    
    def get_selected_item(self):
        """Get the currently selected item for description display."""
        items = self.get_display_items()
        if 0 <= self.selected_index < len(items):
            _, item = items[self.selected_index]
            return item
        return None
    
    def render(self, console):
        """Render the shop UI."""
        if not self.is_open:
            return
        
        # Calculate UI dimensions
        width = 70
        height = 30
        x = (console.width - width) // 2
        y = (console.height - height) // 2
        
        # Draw background
        console.draw_frame(x, y, width, height, 
                          title=f"═══ SHOP - Floor {self.current_shop.floor_level} ═══",
                          clear=True,
                          fg=(255, 255, 255),
                          bg=(0, 0, 0))
        
        # Draw header info
        mode_text = "[BUY MODE]" if self.ui_mode == 'buy' else "[SELL MODE]"
        console.print(x + 2, y + 2, f"Current XP: {self.player.xp}", fg=(255, 215, 0))
        console.print(x + width - 12, y + 2, mode_text, fg=(0, 255, 0) if self.ui_mode == 'buy' else (255, 165, 0))
        
        # Draw items
        items = self.get_display_items()
        start_y = y + 4
        
        if self.ui_mode == 'buy':
            console.print(x + 2, start_y, "Items for Sale:", fg=(255, 255, 255))
            start_y += 2
            
            for i, (_, item) in enumerate(items):
                item_y = start_y + i
                if item_y >= y + height - 9:  # Leave room for description and controls
                    break
                
                # Highlight selected item
                fg_color = (255, 255, 0) if i == self.selected_index else (200, 200, 200)
                prefix = "> " if i == self.selected_index else "  "
                
                # Format item line
                item_name = item.name[:35]  # Truncate long names
                price_text = f"{item.market_value} XP"
                
                console.print(x + 2, item_y, f"{prefix}{item_name}", fg=fg_color)
                console.print(x + width - 10, item_y, price_text, fg=fg_color)
        else:
            console.print(x + 2, start_y, "Your Inventory:", fg=(255, 255, 255))
            start_y += 2
            
            if not items:
                console.print(x + 4, start_y, "No items to sell", fg=(128, 128, 128))
            else:
                for i, (_, item) in enumerate(items):
                    item_y = start_y + i
                    if item_y >= y + height - 9:  # Leave room for description and controls
                        break
                    
                    # Highlight selected item
                    fg_color = (255, 255, 0) if i == self.selected_index else (200, 200, 200)
                    prefix = "> " if i == self.selected_index else "  "
                    
                    # Format item line
                    item_name = item.name[:35]
                    sell_price = self.current_shop.get_sell_price(item)
                    price_text = f"{sell_price} XP"
                    
                    console.print(x + 2, item_y, f"{prefix}{item_name}", fg=fg_color)
                    console.print(x + width - 10, item_y, price_text, fg=fg_color)
        
        # Draw item description
        selected_item = self.get_selected_item()
        description_y = y + height - 7
        
        # Draw separator line
        console.print(x + 1, description_y, "─" * (width - 2), fg=(128, 128, 128))
        description_y += 1
        
        if selected_item:
            # Draw item description
            console.print(x + 2, description_y, "Description:", fg=(255, 255, 255))
            description_y += 1
            
            # Word wrap the description to fit in the box
            description = selected_item.description if selected_item.description else "No description available."
            words = description.split()
            lines = []
            current_line = ""
            max_width = width - 4  # Leave margin
            
            for word in words:
                if len(current_line + word) + 1 <= max_width:
                    current_line += (" " if current_line else "") + word
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            
            if current_line:
                lines.append(current_line)
            
            # Display description lines (max 3 lines)
            for i, line in enumerate(lines[:3]):
                console.print(x + 2, description_y + i, line, fg=(200, 200, 200))
        else:
            console.print(x + 2, description_y + 1, "Select an item to see its description", fg=(128, 128, 128))
        
        # Draw controls
        controls_y = y + height - 2
        control_text = "[↑↓] Navigate [ENTER] Buy [TAB] Sell Mode [ESC] Exit" if self.ui_mode == 'buy' \
                      else "[↑↓] Navigate [ENTER] Sell [TAB] Buy Mode [ESC] Exit"
        console.print(x + (width - len(control_text)) // 2, controls_y, control_text, fg=(128, 128, 128))