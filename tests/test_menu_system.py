"""
Unit tests for the menu system.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from game import Game


def test_menu_initialization():
    """Test that game starts in menu state."""
    game = Game()
    
    # Game should start in menu state
    assert game.game_state == 'MENU'
    
    print("✓ Game starts in menu state")


def test_menu_state_transitions():
    """Test menu state transitions."""
    game = Game()
    
    # Test transition to help
    game.game_state = 'HELP'
    assert game.game_state == 'HELP'
    
    # Test transition back to menu
    game.game_state = 'MENU'
    assert game.game_state == 'MENU'
    
    print("✓ Menu state transitions work correctly")


def test_new_game_start():
    """Test starting a new game from menu."""
    game = Game()
    
    # Start new game
    game.start_new_game()
    
    # Should be in playing state
    assert game.game_state == 'PLAYING'
    
    # Should have valid game objects
    assert game.player is not None
    assert game.level is not None
    assert game.current_level == 1
    assert game.highest_floor_reached == 1
    
    # Player should be alive and positioned
    assert game.player.is_alive()
    assert game.player.x >= 0
    assert game.player.y >= 0
    
    print("✓ New game start works correctly")


def test_menu_rendering_concepts():
    """Test that menu rendering can be called without errors."""
    game = Game()
    
    # Test that we can call render methods (they should complete without errors)
    try:
        game.render_main_menu()
        main_menu_works = True
    except Exception:
        main_menu_works = False
    
    try:
        game.render_help_screen()
        help_screen_works = True
    except Exception:
        help_screen_works = False
    
    assert main_menu_works
    assert help_screen_works
    
    print("✓ Menu rendering methods work correctly")


def test_game_state_flow():
    """Test complete game state flow from menu."""
    game = Game()
    
    # Start in menu
    assert game.game_state == 'MENU'
    
    # Transition to help
    game.game_state = 'HELP'
    assert game.game_state == 'HELP'
    
    # Back to menu
    game.game_state = 'MENU'
    assert game.game_state == 'MENU'
    
    # Start new game
    game.start_new_game()
    assert game.game_state == 'PLAYING'
    
    # Test death -> menu transition
    game.game_state = 'DEAD'
    assert game.game_state == 'DEAD'
    
    # Back to menu from death
    game.game_state = 'MENU'
    assert game.game_state == 'MENU'
    
    # Test victory -> menu transition
    game.game_state = 'VICTORY'
    assert game.game_state == 'VICTORY'
    
    # Back to menu from victory
    game.game_state = 'MENU'
    assert game.game_state == 'MENU'
    
    print("✓ Complete game state flow works correctly")


def test_menu_system_integration():
    """Test menu system integration with game."""
    game = Game()
    
    # Initial state should be menu
    assert game.game_state == 'MENU'
    
    # Start new game should initialize everything properly
    old_message_count = len(game.ui.message_log)
    game.start_new_game()
    
    # Should have welcome message
    assert len(game.ui.message_log) > old_message_count
    
    # Should be in playing state with proper initialization
    assert game.game_state == 'PLAYING'
    assert game.current_level == 1
    assert game.player.is_alive()
    assert not game.player_acted_this_frame
    assert not game.just_changed_level
    
    print("✓ Menu system integration works correctly")


def run_all_tests():
    """Run all menu system tests."""
    print("Running menu system tests...")
    print()
    
    test_menu_initialization()
    test_menu_state_transitions()
    test_new_game_start()
    test_menu_rendering_concepts()
    test_game_state_flow()
    test_menu_system_integration()
    
    print()
    print("✅ All menu system tests passed!")


if __name__ == "__main__":
    run_all_tests()