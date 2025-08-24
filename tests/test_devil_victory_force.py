"""Force kill devil to test victory screen logic."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from game import Game
from monsters.devil import Devil

def test_force_kill_devil():
    """Force kill devil by setting HP to 0 and attacking."""
    game = Game()
    game.game_state = 'PLAYING'
    
    # Create devil and add to level
    devil = Devil(5, 5)
    game.level.monsters = [devil]
    
    print(f"Initial state: {game.game_state}")
    print(f"Devil HP: {devil.hp}")
    
    # Set devil HP to 1 so next attack will kill it
    devil.hp = 1
    
    # Attack the devil - this should kill it and trigger victory
    game.player_attack_monster(devil)
    
    print(f"After attack - Devil HP: {devil.hp}")
    print(f"Devil alive: {devil.is_alive()}")
    print(f"Game state: {game.game_state}")
    
    # Verify victory was triggered
    assert game.game_state == 'VICTORY', f"Expected VICTORY, got {game.game_state}"
    print("✓ Victory screen triggered correctly when devil dies!")

def test_give_player_demon_slayer():
    """Test with demon slayer weapon to see if victory works in more realistic scenario."""
    game = Game()
    game.game_state = 'PLAYING'
    
    # Give player Demon Slayer weapon
    from items.weapons.demon_slayer import DemonSlayer
    demon_slayer = DemonSlayer(0, 0)
    game.player.weapon = demon_slayer
    
    # Create devil
    devil = Devil(5, 5)
    game.level.monsters = [devil]
    
    print(f"=== WITH DEMON SLAYER WEAPON ===")
    print(f"Player attack: {game.player.get_total_attack()}")
    print(f"Player attack traits: {game.player.get_total_attack_traits()}")
    print(f"Devil HP: {devil.hp}")
    print(f"Devil weaknesses: {devil.weaknesses}")
    
    # Calculate expected damage
    base_damage = game.player.get_total_attack()  # Should include demon slayer bonus
    # Devil is weak to DEMONSLAYER, so 2x damage
    expected_damage = max(1, base_damage - devil.defense) * 2
    print(f"Expected damage per hit: {expected_damage}")
    
    # Reduce devil HP so it can be killed in one hit
    devil.hp = expected_damage
    print(f"Set devil HP to: {devil.hp}")
    
    # Attack
    game.player_attack_monster(devil)
    
    print(f"After attack - Game state: {game.game_state}")
    print(f"Devil HP: {devil.hp}")
    print(f"Devil alive: {devil.is_alive()}")

if __name__ == "__main__":
    test_force_kill_devil()
    print("---")
    test_give_player_demon_slayer()
    print("All tests completed!")