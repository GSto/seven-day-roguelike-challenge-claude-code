"""
Base item class for the roguelike game.
"""

from constants import COLOR_WHITE


class Item:
    """Base class for all items."""
    
    def __init__(self, x, y, name, char, color, description=""):
        """Initialize an item."""
        self.x = x
        self.y = y
        self.name = name
        self.char = char
        self.color = color
        self.description = description
    
    def render(self, console, fov):
        """Render the item on the console."""
        if fov[self.x, self.y]:
            console.print(self.x, self.y, self.char, fg=self.color)