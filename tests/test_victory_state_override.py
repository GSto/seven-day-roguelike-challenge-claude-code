"""Test that victory state is not overridden by other game state changes."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from game import Game
from monsters.devil import Devil
from items.weapons.dagger import Dagger

def test_victory_state_not_overridden():
    """Test that VICTORY state is preserved after equipment operations."""
    game = Game()
    
    # Set game to VICTORY state
    game.game_state = 'VICTORY'
    
    # Create a weapon to equip
    dagger = Dagger(0, 0)
    
    # Try to equip item - this should NOT change the game state from VICTORY
    game.equip_item(dagger)
    
    # Game state should still be VICTORY
    assert game.game_state == 'VICTORY', f"Expected VICTORY, got {game.game_state}"
    print("✓ Victory state preserved after equip_item")

def test_victory_after_devil_death_with_demon_slayer():
    """Test victory state with demon slayer weapon to actually kill devil."""
    game = Game()
    game.game_state = 'PLAYING'
    
    # Give player demon slayer weapon to ensure they can kill the devil
    from items.weapons.demon_slayer import DemonSlayer
    demon_slayer = DemonSlayer(0, 0)
    game.player.weapon = demon_slayer
    
    # Create devil
    devil = Devil(5, 5)
    game.level.monsters = [devil]
    
    # Set devil HP lower for faster test (but still high enough to be realistic)
    devil.hp = 50
    
    print(f"Initial state: {game.game_state}")
    print(f"Player attack: {game.player.get_total_attack()}")
    print(f"Devil HP: {devil.hp}")
    
    # Attack until devil dies
    attacks = 0
    while devil.is_alive() and attacks < 20:
        attacks += 1
        old_state = game.game_state
        game.player_attack_monster(devil)
        new_state = game.game_state
        
        print(f"Attack {attacks}: State {old_state} -> {new_state}, Devil HP: {devil.hp}")
        
        if new_state == 'VICTORY':
            break
    
    # Should have triggered victory
    assert game.game_state == 'VICTORY', f"Expected VICTORY, got {game.game_state}"
    assert not devil.is_alive(), "Devil should be dead"
    
    # Now test that the victory state persists through other operations
    old_state = game.game_state
    
    # Try equipping something (simulate what might happen after victory)
    test_item = Dagger(0, 0)
    game.equip_item(test_item)
    
    # State should still be VICTORY
    assert game.game_state == 'VICTORY', f"Victory state was overridden: {old_state} -> {game.game_state}"
    print("✓ Victory state preserved after post-victory operations")

if __name__ == "__main__":
    test_victory_state_not_overridden()
    print("---")
    test_victory_after_devil_death_with_demon_slayer()
    print("All tests passed!")