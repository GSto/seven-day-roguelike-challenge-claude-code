"""
Test for status effects display in inventory screen.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import tcod
from player import Player
from ui import UI

def test_status_effects_display():
    """Test that status effects are displayed in the inventory screen."""
    # Create a player with some status effects
    player = Player(5, 5)
    player.status_effects.burn = 3
    player.status_effects.shields = 2
    player.status_effects.poison = 1
    
    # Create UI and a console for testing
    ui = UI()
    console = tcod.console.Console(80, 50)
    
    # Render the inventory screen
    ui.render_inventory(console, player)
    
    # Convert console to string representation for testing
    console_text = ""
    for y in range(console.height):
        for x in range(console.width):
            char_info = console.tiles[y, x]
            if char_info['ch'] != 0:  # If there's a character at this position
                console_text += chr(char_info['ch'])
            else:
                console_text += " "
        console_text += "\n"
    
    # Check that status effects are displayed
    assert "Status Effects:" in console_text, "Status Effects should be displayed when player has effects"
    assert "Burn: 3" in console_text, "Burn effect should be displayed"
    assert "Poison: 1" in console_text, "Poison effect should be displayed"
    assert "Shields: 2" in console_text, "Shields effect should be displayed"
    
    print("✓ Status effects are properly displayed in inventory screen")
    print(f"  - Status effects: {str(player.status_effects)}")

def test_status_effects_none():
    """Test that status effects display correctly when none are active."""
    player = Player(5, 5)
    # All status effects should start at 0
    
    ui = UI()
    console = tcod.console.Console(80, 50)
    ui.render_inventory(console, player)
    
    # Convert console to string representation for testing
    console_text = ""
    for y in range(console.height):
        for x in range(console.width):
            char_info = console.tiles[y, x]
            if char_info['ch'] != 0:
                console_text += chr(char_info['ch'])
            else:
                console_text += " "
        console_text += "\n"
    
    # Check that status effects are not displayed when none are active
    assert "Status Effects:" not in console_text, "Status Effects should not be displayed when no effects are active"
    
    print("✓ Status effects correctly hidden when no effects are active")

def test_status_effects_mixed():
    """Test status effects display with a mix of positive and negative effects."""
    player = Player(5, 5)
    player.status_effects.shields = 5       # Positive
    player.status_effects.frightened = 2    # Negative
    player.status_effects.stun = 1          # Negative
    
    ui = UI()
    console = tcod.console.Console(80, 50)
    ui.render_inventory(console, player)
    
    # Convert console to string representation for testing
    console_text = ""
    for y in range(console.height):
        for x in range(console.width):
            char_info = console.tiles[y, x]
            if char_info['ch'] != 0:
                console_text += chr(char_info['ch'])
            else:
                console_text += " "
        console_text += "\n"
    
    # Check that all active effects are displayed
    assert "Status Effects:" in console_text, "Status Effects should be displayed"
    assert "Shields: 5" in console_text, "Shields should be displayed"
    assert "Frightened: 2" in console_text, "Frightened should be displayed"
    assert "Stun: 1" in console_text, "Stun should be displayed"
    
    print("✓ Mixed positive and negative status effects displayed correctly")
    print(f"  - Status effects: {str(player.status_effects)}")

if __name__ == "__main__":
    test_status_effects_display()
    test_status_effects_none()
    test_status_effects_mixed()
    print("All status effects display tests passed!")