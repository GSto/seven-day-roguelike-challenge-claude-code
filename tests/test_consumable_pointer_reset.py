"""Test that inventory pointer resets to first slot after consumable use."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from game import Game
from items.consumables import HealthPotion

def test_inventory_pointer_resets_after_consumable_use():
    """Test that using a consumable in first slot resets pointer to first slot."""
    game = Game()
    
    # Add multiple items to inventory
    potion1 = HealthPotion(0, 0)
    potion2 = HealthPotion(0, 0)
    potion3 = HealthPotion(0, 0)
    
    game.player.add_item(potion1)
    game.player.add_item(potion2)
    game.player.add_item(potion3)
    
    # Damage player so potion can be used
    game.player.hp = 10
    
    # Select the first item (newest, index 2 in inventory list)
    game.selected_item_index = 2  
    
    # Use the potion
    game.use_inventory_item(2)
    
    # After using, pointer should reset to first slot (newest remaining item)
    # Since we removed one item, we now have 2 items
    # The newest item is at index 1 (last in list)
    assert game.selected_item_index == 1, f"Expected index 1, got {game.selected_item_index}"
    assert len(game.player.inventory) == 2
    
def test_inventory_pointer_resets_after_middle_consumable_use():
    """Test that using a consumable in middle slot resets pointer to first slot."""
    game = Game()
    
    # Add multiple items to inventory
    potion1 = HealthPotion(0, 0)
    potion2 = HealthPotion(0, 0)
    potion3 = HealthPotion(0, 0)
    
    game.player.add_item(potion1)
    game.player.add_item(potion2)
    game.player.add_item(potion3)
    
    # Damage player so potion can be used
    game.player.hp = 10
    
    # Select the middle item (index 1 in inventory list)
    game.selected_item_index = 1
    
    # Use the potion
    game.use_inventory_item(1)
    
    # After using, pointer should reset to first slot (newest remaining item)
    # Since we removed one item, we now have 2 items
    # The newest item is at index 1 (last in list)
    assert game.selected_item_index == 1, f"Expected index 1, got {game.selected_item_index}"
    assert len(game.player.inventory) == 2

def test_inventory_pointer_becomes_none_when_last_item_used():
    """Test that using the last consumable sets pointer to None."""
    game = Game()
    
    # Add single item to inventory
    potion = HealthPotion(0, 0)
    game.player.add_item(potion)
    
    # Damage player so potion can be used
    game.player.hp = 10
    
    # Select the only item
    game.selected_item_index = 0
    
    # Use the potion
    game.use_inventory_item(0)
    
    # After using last item, pointer should be None
    assert game.selected_item_index is None
    assert len(game.player.inventory) == 0

if __name__ == "__main__":
    test_inventory_pointer_resets_after_consumable_use()
    test_inventory_pointer_resets_after_middle_consumable_use()
    test_inventory_pointer_becomes_none_when_last_item_used()
    print("All tests passed!")