"""
Base item class for the roguelike game.
"""

from constants import COLOR_WHITE


class Item:
    """Base class for all items."""
    
    def __init__(self, x, y, name, char, color, description="", market_value=10):
        """Initialize an item."""
        self.x = x
        self.y = y
        self.name = name
        self.char = char
        self.color = color
        self.description = description
        self.market_value = market_value

    def get_market_value(self):
        return self.market_value

    def render(self, console, fov):
        """Render the item on the console."""
        if fov[self.x, self.y]:
            console.print(self.x, self.y, self.char, fg=self.color)