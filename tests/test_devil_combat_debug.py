"""Debug devil combat to understand why it's not dying."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from game import Game
from monsters.devil import Devil

def test_devil_combat_damage():
    """Test the actual damage calculation against devil."""
    game = Game()
    devil = Devil(5, 5)
    
    print(f"=== COMBAT DEBUG ===")
    print(f"Player attack: {game.player.get_total_attack()}")
    print(f"Devil defense: {devil.defense}")
    print(f"Devil HP: {devil.hp}")
    
    # Calculate expected damage
    expected_damage = max(1, game.player.get_total_attack() - devil.defense)
    print(f"Expected damage: {expected_damage}")
    
    # Set devil HP to expected damage so it should die
    devil.hp = expected_damage
    print(f"Set devil HP to: {devil.hp}")
    
    # Attack the devil
    game.game_state = 'PLAYING'
    initial_state = game.game_state
    game.player_attack_monster(devil)
    
    print(f"Devil HP after attack: {devil.hp}")
    print(f"Devil alive: {devil.is_alive()}")
    print(f"Game state changed from {initial_state} to {game.game_state}")

def test_direct_victory_trigger():
    """Test direct victory trigger by manually killing devil."""
    game = Game() 
    devil = Devil(5, 5)
    game.game_state = 'PLAYING'
    
    # Manually set devil to dead
    devil.hp = 0
    
    # The victory logic should be in the player_attack_monster function
    # Let's check if the logic runs when monster is already dead
    print(f"Devil HP: {devil.hp}")
    print(f"Devil alive: {devil.is_alive()}")  
    print(f"Initial game state: {game.game_state}")
    
    # Try attacking dead devil
    game.player_attack_monster(devil)
    print(f"Game state after attack: {game.game_state}")

def test_victory_condition_check():
    """Test the victory condition check in isolation."""
    game = Game()
    devil = Devil(5, 5)
    
    # Set devil to barely alive
    devil.hp = 1
    
    print(f"=== VICTORY CONDITION TEST ===")
    print(f"hasattr(devil, 'is_final_boss'): {hasattr(devil, 'is_final_boss')}")
    print(f"devil.is_final_boss: {getattr(devil, 'is_final_boss', None)}")
    print(f"devil.is_alive() before: {devil.is_alive()}")
    
    # Kill devil
    devil.hp = 0
    print(f"devil.is_alive() after setting HP=0: {devil.is_alive()}")
    
    # Check victory condition
    if hasattr(devil, 'is_final_boss') and devil.is_final_boss:
        print("Devil is final boss ✓")
        if not devil.is_alive():
            print("Devil is dead ✓")
            print("Victory conditions met!")
        else:
            print("Devil still alive ✗")
    else:
        print("Devil is not final boss ✗")

if __name__ == "__main__":
    test_victory_condition_check()
    print("---")
    test_devil_combat_damage()
    print("---") 
    test_direct_victory_trigger()
    print("Tests completed!")