"""
Tests for the new number key functionality in accessory management.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from game import Game
from items.accessories import Rosary, HeadLamp, PowerRing, ProtectionRing
from items.weapons import Sword  
from items.consumables import HealthPotion


def test_equip_accessory_to_specific_slot():
    """Test equipping accessories to specific slots using number keys 1-3."""
    print("Testing equip accessory to specific slot...")
    
    game = Game()
    player = game.player
    
    # Add some accessories to inventory
    rosary = Rosary(0, 0)
    headlamp = HeadLamp(0, 0) 
    power_ring = PowerRing(0, 0)
    
    player.add_item(rosary)
    player.add_item(headlamp)
    player.add_item(power_ring)
    
    # Ensure player has enough XP
    player.xp = 100
    
    # Set game to inventory state
    game.game_state = 'INVENTORY'
    
    # Select rosary (index 0) and equip to slot 1
    game.selected_item_index = 0
    game.handle_accessory_slot_key(0)  # Slot 1 (index 0)
    
    assert len(player.accessories) >= 1, "Player should have at least 1 accessory equipped"
    assert player.accessories[0] == rosary, "Rosary should be equipped in slot 1"
    assert rosary not in player.inventory, "Rosary should be removed from inventory"
    
    # Select headlamp (now index 0) and equip to slot 2  
    game.selected_item_index = 0
    game.handle_accessory_slot_key(1)  # Slot 2 (index 1)
    
    assert len(player.accessories) >= 2, "Player should have at least 2 accessories equipped"
    assert player.accessories[1] == headlamp, "HeadLamp should be equipped in slot 2"
    assert headlamp not in player.inventory, "HeadLamp should be removed from inventory"
    
    print("✓ Equip accessory to specific slot test passed!")


def test_unequip_accessory_from_specific_slot():
    """Test unequipping accessories from specific slots using number keys."""
    print("Testing unequip accessory from specific slot...")
    
    game = Game()
    player = game.player
    
    # Add some accessories directly to equipped slots
    rosary = Rosary(0, 0)
    headlamp = HeadLamp(0, 0)
    
    # Manually equip accessories (bypassing inventory)
    player.accessories = [rosary, headlamp, None]
    
    # Set game to inventory state
    game.game_state = 'INVENTORY'
    
    initial_inventory_size = len(player.inventory)
    
    # Unequip from slot 1
    game.handle_accessory_slot_key(0)  # Slot 1 (index 0)
    
    assert player.accessories[0] is None, "Slot 1 should be empty after unequipping"
    assert rosary in player.inventory, "Rosary should be back in inventory"
    assert len(player.inventory) == initial_inventory_size + 1, "Inventory should have one more item"
    
    # Unequip from slot 2
    game.handle_accessory_slot_key(1)  # Slot 2 (index 1)
    
    assert player.accessories[1] is None, "Slot 2 should be empty after unequipping"
    assert headlamp in player.inventory, "HeadLamp should be back in inventory"
    assert len(player.inventory) == initial_inventory_size + 2, "Inventory should have two more items"
    
    print("✓ Unequip accessory from specific slot test passed!")


def test_number_keys_only_work_on_accessories():
    """Test that number keys don't work on non-accessory items."""
    print("Testing number keys only work on accessories...")
    
    game = Game()
    player = game.player
    
    # Add non-accessory items to inventory
    sword = Sword(0, 0)
    potion = HealthPotion(0, 0)
    
    player.add_item(sword)
    player.add_item(potion)
    
    # Set game to inventory state
    game.game_state = 'INVENTORY'
    
    initial_accessories_count = len([a for a in player.accessories if a is not None])
    initial_inventory_size = len(player.inventory)
    
    # Try to use number key on sword (index 0)
    game.selected_item_index = 0
    game.handle_accessory_slot_key(0)  # Should not work
    
    # Check that nothing changed
    assert len([a for a in player.accessories if a is not None]) == initial_accessories_count, "No accessories should be equipped"
    assert len(player.inventory) == initial_inventory_size, "Inventory size should be unchanged"
    assert sword in player.inventory, "Sword should still be in inventory"
    
    # Try to use number key on potion (index 1)
    game.selected_item_index = 1
    game.handle_accessory_slot_key(1)  # Should not work
    
    # Check that nothing changed
    assert len([a for a in player.accessories if a is not None]) == initial_accessories_count, "No accessories should be equipped"
    assert len(player.inventory) == initial_inventory_size, "Inventory size should be unchanged"
    assert potion in player.inventory, "Potion should still be in inventory"
    
    print("✓ Number keys only work on accessories test passed!")


def test_number_keys_when_no_item_selected():
    """Test number keys when no item is selected."""
    print("Testing number keys when no item selected...")
    
    game = Game()
    player = game.player
    
    # Add accessory to inventory
    rosary = Rosary(0, 0)
    player.add_item(rosary)
    
    # Set game to inventory state but don't select any item
    game.game_state = 'INVENTORY'
    game.selected_item_index = None
    
    initial_accessories_count = len([a for a in player.accessories if a is not None])
    initial_inventory_size = len(player.inventory)
    
    # Try to use number key with no item selected
    game.handle_accessory_slot_key(0)  # Should not work
    
    # Check that nothing changed
    assert len([a for a in player.accessories if a is not None]) == initial_accessories_count, "No accessories should be equipped"
    assert len(player.inventory) == initial_inventory_size, "Inventory size should be unchanged"
    assert rosary in player.inventory, "Rosary should still be in inventory"
    
    print("✓ Number keys when no item selected test passed!")


def test_xp_validation_for_equipping():
    """Test XP validation when equipping accessories."""
    print("Testing XP validation for equipping...")
    
    game = Game()
    player = game.player
    
    # Add accessory with XP cost to inventory
    rosary = Rosary(0, 0)
    player.add_item(rosary)
    
    # Set player XP to less than required
    player.xp = 2  # Rosary costs 5 XP by default
    
    # Set game to inventory state
    game.game_state = 'INVENTORY'
    game.selected_item_index = 0
    
    initial_accessories_count = len([a for a in player.accessories if a is not None])
    initial_inventory_size = len(player.inventory)
    initial_xp = player.xp
    
    # Try to equip rosary without enough XP
    game.handle_accessory_slot_key(0)  # Should not work
    
    # Check that nothing changed
    assert len([a for a in player.accessories if a is not None]) == initial_accessories_count, "No accessories should be equipped"
    assert len(player.inventory) == initial_inventory_size, "Inventory size should be unchanged"
    assert player.xp == initial_xp, "XP should be unchanged"
    assert rosary in player.inventory, "Rosary should still be in inventory"
    
    # Now give player enough XP
    player.xp = 10
    
    # Try to equip rosary with enough XP
    game.handle_accessory_slot_key(0)  # Should work now
    
    # Check that it worked
    assert len([a for a in player.accessories if a is not None]) == initial_accessories_count + 1, "One accessory should be equipped"
    assert player.xp == 10 - rosary.xp_cost, "XP should be reduced by accessory cost"
    assert rosary not in player.inventory, "Rosary should be removed from inventory"
    
    print("✓ XP validation for equipping test passed!")


def test_inventory_state_management():
    """Test inventory state management after equip/unequip operations."""
    print("Testing inventory state management...")
    
    game = Game()
    player = game.player
    
    # Add accessories to inventory
    rosary = Rosary(0, 0)
    headlamp = HeadLamp(0, 0)
    power_ring = PowerRing(0, 0)
    
    player.add_item(rosary)
    player.add_item(headlamp) 
    player.add_item(power_ring)
    
    # Give player enough XP
    player.xp = 50
    
    # Set game to inventory state
    game.game_state = 'INVENTORY'
    
    # Equip all accessories
    game.selected_item_index = 0
    game.handle_accessory_slot_key(0)  # Equip to slot 1
    
    game.selected_item_index = 0  # Index shifts down after previous item removed
    game.handle_accessory_slot_key(1)  # Equip to slot 2
    
    game.selected_item_index = 0  # Index shifts down again
    game.handle_accessory_slot_key(2)  # Equip to slot 3
    
    # Check that all slots are filled and inventory is empty of accessories
    equipped_count = len([a for a in player.accessories if a is not None])
    assert equipped_count == 3, f"Expected 3 accessories equipped, got {equipped_count}"
    
    accessory_count_in_inventory = len([item for item in player.inventory if hasattr(item, 'equipment_slot') and item.equipment_slot == 'accessory'])
    assert accessory_count_in_inventory == 0, "No accessories should remain in inventory"
    
    # Now unequip them all
    game.handle_accessory_slot_key(0)  # Unequip from slot 1
    game.handle_accessory_slot_key(1)  # Unequip from slot 2  
    game.handle_accessory_slot_key(2)  # Unequip from slot 3
    
    # Check that all slots are empty and accessories are back in inventory
    equipped_count = len([a for a in player.accessories if a is not None])
    assert equipped_count == 0, f"Expected 0 accessories equipped, got {equipped_count}"
    
    accessory_count_in_inventory = len([item for item in player.inventory if hasattr(item, 'equipment_slot') and item.equipment_slot == 'accessory'])
    assert accessory_count_in_inventory == 3, "All 3 accessories should be back in inventory"
    
    print("✓ Inventory state management test passed!")


if __name__ == "__main__":
    print("Running inventory accessory management tests...")
    test_equip_accessory_to_specific_slot()
    test_unequip_accessory_from_specific_slot() 
    test_number_keys_only_work_on_accessories()
    test_number_keys_when_no_item_selected()
    test_xp_validation_for_equipping()
    test_inventory_state_management()
    print("✅ All inventory accessory management tests passed!")