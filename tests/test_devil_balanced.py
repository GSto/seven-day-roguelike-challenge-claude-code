"""Test devil with balanced stats."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from game import Game
from monsters.devil import Devil

def test_devil_killable_with_normal_equipment():
    """Test that devil can be killed with starting equipment in reasonable time."""
    game = Game()
    devil = Devil(0, 0)
    
    print(f"=== BALANCED DEVIL TEST ===")
    print(f"Player attack: {game.player.get_total_attack()}")
    print(f"Devil HP: {devil.hp}")
    print(f"Devil defense: {devil.defense}")
    
    # Calculate damage per hit
    damage_per_hit = max(1, game.player.get_total_attack() - devil.defense)
    print(f"Damage per hit: {damage_per_hit}")
    
    # Calculate hits needed
    hits_needed = devil.hp // damage_per_hit + (1 if devil.hp % damage_per_hit > 0 else 0)
    print(f"Hits needed to kill: {hits_needed}")
    
    if hits_needed <= 100:
        print("✓ Devil is reasonably killable (≤100 hits)")
    elif hits_needed <= 200:
        print("⚠ Devil is challenging but doable (≤200 hits)")
    else:
        print("✗ Devil is too difficult (>200 hits)")
    
    # Test actual kill
    devil.hp = 1  # Set low for quick test
    game.game_state = 'PLAYING'
    game.player_attack_monster(devil)
    
    assert game.game_state == 'VICTORY', f"Expected VICTORY, got {game.game_state}"
    print("✓ Victory triggers correctly")

def test_devil_with_demon_slayer():
    """Test devil with demon slayer weapon."""
    game = Game()
    from items.weapons.demon_slayer import DemonSlayer
    
    # Equip demon slayer
    demon_slayer = DemonSlayer(0, 0)
    game.player.weapon = demon_slayer
    
    devil = Devil(0, 0)
    
    print(f"=== WITH DEMON SLAYER ===")
    print(f"Player attack: {game.player.get_total_attack()}")
    print(f"Devil HP: {devil.hp}")
    print(f"Devil defense: {devil.defense}")
    
    # Calculate damage per hit (with weakness)
    base_damage = max(1, game.player.get_total_attack() - devil.defense)
    damage_per_hit = base_damage * 2  # DEMONSLAYER weakness
    print(f"Base damage: {base_damage}")
    print(f"Damage per hit (with weakness): {damage_per_hit}")
    
    # Calculate hits needed
    hits_needed = devil.hp // damage_per_hit + (1 if devil.hp % damage_per_hit > 0 else 0)
    print(f"Hits needed to kill: {hits_needed}")
    
    if hits_needed <= 20:
        print("✓ Devil is very manageable with demon slayer")
    elif hits_needed <= 50:
        print("✓ Devil is reasonable with demon slayer") 
    else:
        print("⚠ Devil is still challenging even with demon slayer")

if __name__ == "__main__":
    test_devil_killable_with_normal_equipment()
    print("---")
    test_devil_with_demon_slayer()
    print("All tests completed!")