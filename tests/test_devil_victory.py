"""Test that killing the devil triggers victory screen."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from game import Game
from monsters.devil import Devil

def test_devil_death_triggers_victory():
    """Test that killing the devil sets game state to VICTORY."""
    game = Game()
    game.game_state = 'PLAYING'
    
    # Create a devil and add it to the level
    devil = Devil(5, 5)
    game.level.monsters = [devil]
    
    # Verify devil has final boss flag
    assert hasattr(devil, 'is_final_boss'), "Devil should have is_final_boss attribute"
    assert devil.is_final_boss == True, "Devil should be marked as final boss"
    
    # Set devil's HP to very low so it dies easily
    devil.hp = 1
    
    # Attack the devil (should kill it)
    initial_state = game.game_state
    game.player_attack_monster(devil)
    
    # Check that game state changed to VICTORY
    assert game.game_state == 'VICTORY', f"Expected VICTORY, got {game.game_state}"
    print(f"Victory triggered successfully! State changed from {initial_state} to {game.game_state}")

def test_devil_properties():
    """Test that devil has correct properties."""
    devil = Devil(0, 0)
    
    print(f"Devil name: {devil.name}")
    print(f"Devil has is_final_boss: {hasattr(devil, 'is_final_boss')}")
    if hasattr(devil, 'is_final_boss'):
        print(f"Devil is_final_boss value: {devil.is_final_boss}")
    print(f"Devil HP: {devil.hp}")
    print(f"Devil is_alive: {devil.is_alive()}")

def test_devil_death_logic():
    """Test the devil death detection logic step by step."""
    game = Game()
    devil = Devil(5, 5)
    
    print(f"Devil initial HP: {devil.hp}")
    print(f"Devil is_alive(): {devil.is_alive()}")
    
    # Kill the devil
    devil.hp = 0
    print(f"Devil HP after setting to 0: {devil.hp}")
    print(f"Devil is_alive() after HP=0: {devil.is_alive()}")
    
    # Check final boss attribute
    print(f"hasattr(devil, 'is_final_boss'): {hasattr(devil, 'is_final_boss')}")
    if hasattr(devil, 'is_final_boss'):
        print(f"devil.is_final_boss: {devil.is_final_boss}")

if __name__ == "__main__":
    test_devil_properties()
    test_devil_death_logic()
    test_devil_death_triggers_victory()
    print("All tests passed!")