#!/usr/bin/env python3
"""
Test health potion percentage-based healing.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from game import Game
from player import Player
from items.consumables.health_potion import HealthPotion
from ui import UI

def test_percentage_healing():
    """Test that health potions heal 30% of max HP."""
    print("Testing percentage-based healing...")
    
    # Create a player with different max HP values
    player = Player(10, 10)
    
    # Test with default max HP (50)
    print(f"Player max HP: {player.max_hp}")
    
    # Damage the player to 20 HP
    player.hp = 20
    print(f"Player HP before potion: {player.hp}")
    
    # Create and use health potion
    potion = HealthPotion(0, 0)
    print(f"Potion description: {potion.description}")
    print(f"Potion heal percentage: {potion.heal_percentage}%")
    
    # Use the potion
    result = potion.use(player)
    
    print(f"Player HP after potion: {player.hp}")
    print(f"Potion use result: {result}")
    
    # Calculate expected healing (30% of 50 = 15)
    expected_healing = int(player.max_hp * 0.3)  # 30% of 50 = 15
    expected_final_hp = min(20 + expected_healing, player.max_hp)  # 20 + 15 = 35
    
    if player.hp == expected_final_hp:
        print(f"✓ Correct healing: {expected_healing} HP (30% of {player.max_hp})")
    else:
        print(f"✗ Incorrect healing: expected {expected_final_hp}, got {player.hp}")
        return False
    
    return True

def test_max_hp_cap():
    """Test that healing cannot exceed max HP."""
    print("\nTesting max HP cap...")
    
    player = Player(10, 10)
    
    # Set player to nearly full health
    player.hp = player.max_hp - 5  # 45/50 HP
    print(f"Player HP before potion: {player.hp}/{player.max_hp}")
    
    # Use health potion (should heal 15 HP but cap at max HP)
    potion = HealthPotion(0, 0)
    result = potion.use(player)
    
    print(f"Player HP after potion: {player.hp}/{player.max_hp}")
    
    if player.hp == player.max_hp:
        print("✓ Healing correctly capped at max HP")
        return True
    else:
        print(f"✗ Healing not capped: expected {player.max_hp}, got {player.hp}")
        return False

def test_full_health_rejection():
    """Test that potions cannot be used at full health."""
    print("\nTesting full health rejection...")
    
    player = Player(10, 10)
    
    # Player at full health
    player.hp = player.max_hp
    print(f"Player HP: {player.hp}/{player.max_hp} (full health)")
    
    # Try to use health potion
    potion = HealthPotion(0, 0)
    result = potion.use(player)
    
    print(f"Potion use result: {result}")
    print(f"Player HP after attempt: {player.hp}/{player.max_hp}")
    
    if not result and player.hp == player.max_hp:
        print("✓ Potion correctly rejected at full health")
        return True
    else:
        print("✗ Potion should be rejected at full health")
        return False

def test_different_max_hp_levels():
    """Test percentage healing with different max HP levels."""
    print("\nTesting with different max HP levels...")
    
    # Test with level 5 player (higher max HP)
    player = Player(10, 10)
    player.level = 5
    player.max_hp = 130  # Higher level player
    player.hp = 50  # Low health
    
    print(f"High-level player: {player.hp}/{player.max_hp} HP")
    
    potion = HealthPotion(0, 0)
    result = potion.use(player)
    
    expected_healing = int(player.max_hp * 0.3)  # 30% of 130 = 39
    expected_final_hp = 50 + expected_healing  # 50 + 39 = 89
    
    print(f"Expected healing: {expected_healing} HP")
    print(f"Player HP after potion: {player.hp}/{player.max_hp}")
    
    if player.hp == expected_final_hp:
        print(f"✓ Correct percentage healing for high-level player: {expected_healing} HP")
        return True
    else:
        print(f"✗ Incorrect healing: expected {expected_final_hp}, got {player.hp}")
        return False

def test_ui_display():
    """Test that UI displays percentage correctly."""
    print("\nTesting UI display...")
    
    # Create a mock console for testing
    class MockConsole:
        def __init__(self):
            self.printed_items = []
        
        def clear(self):
            self.printed_items = []
        
        def print(self, x, y, text, fg=None):
            self.printed_items.append((x, y, text, fg))
    
    # Create player with health potion
    game = Game()
    potion = HealthPotion(0, 0)
    game.player.add_item(potion)
    
    # Create UI and mock console
    ui = UI()
    console = MockConsole()
    
    # Render inventory with potion selected
    ui.render_inventory(console, game.player, 0)
    
    # Check for percentage display in item list
    percentage_in_list = [item for item in console.printed_items if "(heals 30%)" in item[2]]
    print(f"Found percentage in item list: {len(percentage_in_list) > 0}")
    
    # Check for percentage display in description
    percentage_in_desc = [item for item in console.printed_items if "30% of max HP" in item[2]]
    print(f"Found percentage in description: {len(percentage_in_desc) > 0}")
    
    if len(percentage_in_list) > 0 and len(percentage_in_desc) > 0:
        print("✓ UI correctly displays percentage healing")
        return True
    else:
        print("✗ UI does not display percentage correctly")
        return False

def run_all_tests():
    """Run all health potion percentage tests."""
    print("Running health potion percentage tests...")
    
    test1 = test_percentage_healing()
    test2 = test_max_hp_cap()
    test3 = test_full_health_rejection()
    test4 = test_different_max_hp_levels()
    test5 = test_ui_display()
    
    if test1 and test2 and test3 and test4 and test5:
        print("\n✓ All health potion percentage tests passed!")
    else:
        print("\n✗ Some health potion percentage tests failed")
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    run_all_tests()