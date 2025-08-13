"""Test ESC confirmation functionality."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import tcod.event
from game import Game
from unittest.mock import Mock, MagicMock


def test_esc_confirmation_first_press():
    """Test that first ESC press shows confirmation message."""
    game = Game()
    game.game_state = 'PLAYING'
    game.esc_pressed_once = False
    
    # Mock the UI to track messages
    game.ui = Mock()
    game.ui.add_message = MagicMock()
    
    # Create a mock ESC key event
    event = Mock()
    event.sym = tcod.event.KeySym.ESCAPE
    
    # Handle the keydown event
    game.handle_keydown(event)
    
    # Check that confirmation was requested
    assert game.esc_pressed_once == True
    assert game.running == True  # Game should still be running
    game.ui.add_message.assert_called_with("Are you sure? Press ESC again to quit.")


def test_esc_confirmation_second_press():
    """Test that second ESC press quits the game."""
    game = Game()
    game.game_state = 'PLAYING'
    game.esc_pressed_once = True  # Already pressed once
    
    # Mock the UI
    game.ui = Mock()
    
    # Create a mock ESC key event
    event = Mock()
    event.sym = tcod.event.KeySym.ESCAPE
    
    # Handle the keydown event
    game.handle_keydown(event)
    
    # Check that game is now stopping
    assert game.running == False


def test_esc_confirmation_reset_on_movement():
    """Test that ESC confirmation is reset when player moves."""
    game = Game()
    game.game_state = 'PLAYING'
    game.esc_pressed_once = True  # ESC was pressed once
    
    # Mock necessary components
    game.ui = Mock()
    game.level = Mock()
    game.level.get_monster_at = Mock(return_value=None)
    game.level.is_walkable = Mock(return_value=True)
    game.level.update_fov = Mock()
    game.level.is_stairs_down = Mock(return_value=False)
    game.level.is_stairs_up = Mock(return_value=False)
    game.player = Mock()
    game.player.x = 5
    game.player.y = 5
    game.player.move = Mock()
    game.player.get_total_fov = Mock(return_value=8)
    
    # Create a mock movement key event (arrow up)
    event = Mock()
    event.sym = tcod.event.KeySym.UP
    
    # Handle the keydown event
    game.handle_keydown(event)
    
    # Check that ESC confirmation was reset
    assert game.esc_pressed_once == False
    assert game.running == True


def test_esc_confirmation_reset_on_action():
    """Test that ESC confirmation is reset when player performs action."""
    game = Game()
    game.game_state = 'PLAYING'
    game.esc_pressed_once = True  # ESC was pressed once
    
    # Mock necessary components
    game.ui = Mock()
    game.try_pickup_item = Mock()
    
    # Create a mock 'g' key event (get item)
    event = Mock()
    event.sym = ord('g')
    
    # Handle the keydown event
    game.handle_keydown(event)
    
    # Check that ESC confirmation was reset
    assert game.esc_pressed_once == False
    assert game.running == True


def test_inventory_esc_no_confirmation():
    """Test that ESC in inventory screen doesn't need confirmation."""
    game = Game()
    game.game_state = 'INVENTORY'
    game.esc_pressed_once = False
    
    # Mock the UI
    game.ui = Mock()
    
    # Create a mock ESC key event
    event = Mock()
    event.sym = tcod.event.KeySym.ESCAPE
    
    # Handle the keydown event
    game.handle_keydown(event)
    
    # Check that we returned to playing without quit confirmation
    assert game.game_state == 'PLAYING'
    assert game.running == True
    assert game.esc_pressed_once == False


if __name__ == "__main__":
    test_esc_confirmation_first_press()
    print("✓ First ESC press shows confirmation")
    
    test_esc_confirmation_second_press()
    print("✓ Second ESC press quits game")
    
    test_esc_confirmation_reset_on_movement()
    print("✓ ESC confirmation resets on movement")
    
    test_esc_confirmation_reset_on_action()
    print("✓ ESC confirmation resets on action")
    
    test_inventory_esc_no_confirmation()
    print("✓ ESC in inventory closes without confirmation")
    
    print("\nAll ESC confirmation tests passed!")