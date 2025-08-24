"""Detailed test of devil victory trigger including update loop."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from game import Game
from monsters.devil import Devil

def test_devil_victory_with_updates():
    """Test that devil victory persists through game updates."""
    game = Game()
    game.game_state = 'PLAYING'
    
    # Create a devil and add it to the level
    devil = Devil(10, 10)
    game.level.monsters = [devil]
    
    print(f"Initial game state: {game.game_state}")
    print(f"Devil HP: {devil.hp}")
    print(f"Devil is final boss: {getattr(devil, 'is_final_boss', 'NO ATTRIBUTE')}")
    
    # Set devil's HP to 1 for easy kill
    devil.hp = 1
    
    # Attack the devil
    game.player_attack_monster(devil)
    
    print(f"Game state after attack: {game.game_state}")
    print(f"Devil HP after attack: {devil.hp}")
    print(f"Devil is alive: {devil.is_alive()}")
    
    # Simulate what happens in the game loop
    game.player_acted_this_frame = True
    
    # Check if update() changes the game state
    print(f"About to call update(), game state: {game.game_state}")
    game.update()
    print(f"Game state after update(): {game.game_state}")
    
    # The game state should still be VICTORY
    assert game.game_state == 'VICTORY', f"Expected VICTORY, got {game.game_state}"

def test_victory_state_isolation():
    """Test that VICTORY state prevents normal game updates."""
    game = Game()
    
    # Set game state to VICTORY manually
    game.game_state = 'VICTORY'
    
    print(f"Game state before update: {game.game_state}")
    
    # Call update - should not change anything
    game.update()
    
    print(f"Game state after update: {game.game_state}")
    
    # Should still be VICTORY
    assert game.game_state == 'VICTORY', f"VICTORY state should be preserved, got {game.game_state}"

def test_debug_victory_logic():
    """Debug the exact victory logic step by step."""
    game = Game()
    devil = Devil(5, 5)
    game.level.monsters = [devil]
    
    print("=== STEP BY STEP DEBUG ===")
    print(f"1. Initial state: {game.game_state}")
    print(f"2. Devil alive: {devil.is_alive()}")
    print(f"3. Devil has is_final_boss: {hasattr(devil, 'is_final_boss')}")
    print(f"4. Devil is_final_boss value: {getattr(devil, 'is_final_boss', None)}")
    
    # Reduce devil HP to 1
    devil.hp = 1
    
    # Manually trigger the death logic from player_attack_monster
    print(f"5. About to attack devil with HP: {devil.hp}")
    
    # This should kill the devil and set VICTORY
    old_state = game.game_state  
    game.player_attack_monster(devil)
    new_state = game.game_state
    
    print(f"6. State changed from {old_state} to {new_state}")
    print(f"7. Devil alive after attack: {devil.is_alive()}")
    
    # Check if the victory condition was met
    if hasattr(devil, 'is_final_boss') and devil.is_final_boss and not devil.is_alive():
        print("8. Victory conditions met - devil is dead and is final boss")
    else:
        print("8. Victory conditions NOT met!")

if __name__ == "__main__":
    test_debug_victory_logic()
    print("---")
    test_victory_state_isolation() 
    print("---")
    test_devil_victory_with_updates()
    print("All tests passed!")