"""Test precise damage calculation against devil."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import random
from game import Game
from monsters.devil import Devil

def test_manual_damage_calculation():
    """Manually calculate and apply damage to see what's happening."""
    game = Game()
    devil = Devil(5, 5)
    
    # Set predictable state
    random.seed(42)  # For consistent results
    
    print(f"=== MANUAL DAMAGE CALCULATION ===")
    print(f"Player total attack: {game.player.get_total_attack()}")
    print(f"Devil defense: {devil.stats.get_stat(devil.stats.StatType.DEFENSE) if hasattr(devil.stats, 'StatType') else devil.defense}")
    
    # Calculate damage as the game does
    base_damage = game.player.get_total_attack()
    print(f"Base damage: {base_damage}")
    
    # Set devil HP to ensure death
    devil.hp = 1
    print(f"Devil HP set to: {devil.hp}")
    
    # Manually call take_damage_with_traits
    actual_damage = devil.take_damage_with_traits(base_damage, game.player.get_total_attack_traits())
    print(f"Actual damage dealt: {actual_damage}")
    print(f"Devil HP after manual damage: {devil.hp}")
    print(f"Devil is alive: {devil.is_alive()}")

def test_step_by_step_attack():
    """Test the attack step by step with debug prints."""
    game = Game()
    devil = Devil(5, 5) 
    game.level.monsters = [devil]
    
    # Monkey patch the take_damage_with_traits method to add debug
    original_take_damage = devil.take_damage_with_traits
    
    def debug_take_damage(damage, attack_traits=None):
        print(f"    take_damage_with_traits called with damage={damage}")
        print(f"    Devil HP before: {devil.hp}")
        result = original_take_damage(damage, attack_traits)
        print(f"    Actual damage dealt: {result}")
        print(f"    Devil HP after: {devil.hp}")
        return result
    
    devil.take_damage_with_traits = debug_take_damage
    
    # Set devil HP low
    devil.hp = 2
    print(f"Starting devil HP: {devil.hp}")
    
    # Attack
    game.game_state = 'PLAYING'
    print("Calling player_attack_monster...")
    game.player_attack_monster(devil)
    
    print(f"Final game state: {game.game_state}")
    print(f"Final devil HP: {devil.hp}")
    print(f"Devil alive: {devil.is_alive()}")

def test_devil_weaknesses():
    """Check if devil has any weaknesses that might affect damage."""
    devil = Devil(0, 0)
    
    print(f"=== DEVIL TRAITS ===")
    print(f"Devil weaknesses: {devil.weaknesses}")
    print(f"Devil resistances: {devil.resistances}")
    
    # Check player attack traits
    game = Game()
    player_traits = game.player.get_total_attack_traits()
    print(f"Player attack traits: {player_traits}")
    
    # Check for trait interactions
    for trait in player_traits:
        if trait in devil.weaknesses:
            print(f"Player has weakness exploit: {trait} (2x damage)")
        elif trait in devil.resistances:
            print(f"Devil resists: {trait} (0.5x damage)")

if __name__ == "__main__":
    test_devil_weaknesses()
    print("---")
    test_manual_damage_calculation()
    print("---")
    test_step_by_step_attack()
    print("Tests completed!")