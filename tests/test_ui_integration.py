"""
Test UI integration with manual leveling changes
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from game import Game
import tcod


def test_ui_render_without_crash():
    """Test that UI renders without crashing with new leveling system."""
    game = Game()
    
    # Create a mock console for testing
    console = tcod.console.Console(80, 50)
    
    # Test rendering UI with no XP
    game.ui.render(console, game.player, 1)
    print("✓ UI renders correctly with no XP")
    
    # Test rendering with some XP but can't level up
    game.player.gain_xp(25)
    game.ui.render(console, game.player, 1)
    print("✓ UI renders correctly with partial XP")
    
    # Test rendering when can level up
    game.player.gain_xp(25)  # Total 50, can level up
    game.ui.render(console, game.player, 1)
    print("✓ UI renders correctly when can level up")
    
    # Test rendering after manual level up
    game.player.attempt_level_up()
    game.ui.render(console, game.player, 1)
    print("✓ UI renders correctly after level up")


def test_level_up_messages():
    """Test that level up messages work correctly."""
    game = Game()
    
    # Give XP and attempt level up
    game.player.gain_xp(50)
    
    # Clear any existing messages
    game.ui.message_log = []
    
    # Test manual level up
    game.handle_manual_level_up()
    
    # Should have level up messages
    assert len(game.ui.message_log) > 0
    level_up_found = any("Level up!" in msg[0] for msg in game.ui.message_log)
    assert level_up_found, f"Level up message not found in: {[msg[0] for msg in game.ui.message_log]}"
    
    print("✓ Level up messages work correctly")
    
    # Test insufficient XP message
    game.ui.message_log = []
    game.handle_manual_level_up()  # Should fail
    
    assert len(game.ui.message_log) > 0
    insufficient_found = any("Not enough XP" in msg[0] for msg in game.ui.message_log)
    assert insufficient_found, f"Insufficient XP message not found in: {[msg[0] for msg in game.ui.message_log]}"
    
    print("✓ Insufficient XP message works correctly")


if __name__ == "__main__":
    test_ui_render_without_crash()
    test_level_up_messages()
    print("✅ All UI integration tests passed!")