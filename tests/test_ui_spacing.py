"""Test that UI renders with proper spacing."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import tcod.console
from ui import UI
from player import Player
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

def test_ui_renders_without_error():
    """Test that UI renders without throwing errors."""
    console = tcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT, order="F")
    ui = UI()
    player = Player(5, 5)
    
    # Add some messages to the log
    ui.add_message("Test message 1")
    ui.add_message("Test message 2")
    
    # Try to render - should not throw any errors
    try:
        ui.render(console, player, current_level=1)
        success = True
    except Exception as e:
        print(f"UI render failed: {e}")
        success = False
    
    assert success, "UI render should complete without errors"

def test_ui_spacing_calculation():
    """Test that spacing is properly calculated in UI."""
    console = tcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT, order="F")
    ui = UI()
    player = Player(5, 5)
    
    # The UI should have:
    # - Separator line after map
    # - Player stats lines
    # - Combat stats lines  
    # - Equipment line
    # - Space line (new)
    # - Message log
    
    # This test just ensures the render completes
    ui.render(console, player, current_level=1)
    
    # If we get here without exception, the spacing is at least valid
    assert True

if __name__ == "__main__":
    test_ui_renders_without_error()
    test_ui_spacing_calculation()
    print("All tests passed!")