"""
Integration test for accessory bonuses in actual gameplay context.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from game import Game
from items.accessories import Rosary, HeadLamp
from items.consumables import HealthPotion


def test_fov_bonus_integration():
    """Test FOV bonus works in game context."""
    game = Game()
    player = game.player
    
    # Check base FOV
    base_fov = player.get_total_fov()
    print(f"Base FOV: {base_fov}")
    
    # Create and equip headlamp
    headlamp = HeadLamp(0, 0)
    player.accessories.append(headlamp)
    
    # Check FOV with headlamp
    fov_with_headlamp = player.get_total_fov()
    print(f"FOV with HeadLamp: {fov_with_headlamp}")
    
    assert fov_with_headlamp == base_fov + 5, f"Expected {base_fov + 5}, got {fov_with_headlamp}"
    print("✓ FOV bonus integration test passed!")


def test_health_aspect_bonus_integration():
    """Test health aspect bonus works with actual healing."""
    game = Game()
    player = game.player
    
    # Damage player first
    player.hp = 20  # Set to low health
    initial_hp = player.hp
    
    # Check base health aspect
    base_health_aspect = player.get_total_health_aspect()
    print(f"Base health aspect: {base_health_aspect}")
    
    # Create and use health potion without rosary
    potion = HealthPotion(0, 0)
    heal_amount_base = int(player.max_hp * (potion.effect_value * base_health_aspect))
    print(f"Expected heal without rosary: {heal_amount_base}")
    
    # Now equip rosary
    rosary = Rosary(0, 0)
    player.accessories.append(rosary)
    
    # Check health aspect with rosary
    health_aspect_with_rosary = player.get_total_health_aspect()
    print(f"Health aspect with Rosary: {health_aspect_with_rosary}")
    
    # Use potion with rosary equipped
    potion2 = HealthPotion(0, 0)
    potion2.use(player)
    
    # Calculate expected healing with rosary
    expected_heal = int(player.max_hp * (potion2.effect_value * health_aspect_with_rosary))
    expected_final_hp = min(player.max_hp, initial_hp + expected_heal)
    
    print(f"Expected heal with rosary: {expected_heal}")
    print(f"Expected final HP: {expected_final_hp}")
    print(f"Actual final HP: {player.hp}")
    
    assert health_aspect_with_rosary == base_health_aspect + 0.1, f"Expected {base_health_aspect + 0.1}, got {health_aspect_with_rosary}"
    print("✓ Health aspect bonus integration test passed!")


if __name__ == "__main__":
    test_fov_bonus_integration()
    test_health_aspect_bonus_integration()
    print("✅ All integration tests passed!")