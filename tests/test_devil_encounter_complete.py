"""Complete test of devil encounter including victory screen."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from game import Game
from monsters.devil import Devil

def test_complete_devil_encounter():
    """Test a complete devil encounter from start to victory."""
    game = Game()
    game.game_state = 'PLAYING'
    
    # Create devil
    devil = Devil(5, 5)
    game.level.monsters = [devil]
    
    print(f"=== COMPLETE DEVIL ENCOUNTER ===")
    print(f"Initial game state: {game.game_state}")
    print(f"Devil HP: {devil.hp}")
    print(f"Devil is final boss: {getattr(devil, 'is_final_boss', False)}")
    
    # Calculate how many hits needed
    damage_per_hit = max(1, game.player.get_total_attack() - devil.defense)
    hits_needed = (devil.hp + damage_per_hit - 1) // damage_per_hit  # Ceiling division
    
    print(f"Player damage per hit: {damage_per_hit}")
    print(f"Hits needed: {hits_needed}")
    
    # Attack until devil dies
    hit_count = 0
    while devil.is_alive() and hit_count < hits_needed + 5:  # +5 safety buffer
        hit_count += 1
        old_hp = devil.hp
        game.player_attack_monster(devil)
        new_hp = devil.hp
        print(f"Hit {hit_count}: Devil HP {old_hp} -> {new_hp}")
        
        if game.game_state == 'VICTORY':
            print(f"✓ VICTORY triggered after {hit_count} hits!")
            break
    
    # Verify final state
    assert game.game_state == 'VICTORY', f"Expected VICTORY, got {game.game_state}"
    assert not devil.is_alive(), f"Devil should be dead"
    
    print(f"Final game state: {game.game_state}")
    print(f"Devil final HP: {devil.hp}")
    print(f"Total hits taken: {hit_count}")
    
    return True

if __name__ == "__main__":
    test_complete_devil_encounter()
    print("Complete devil encounter test passed!")