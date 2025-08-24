"""Test that pressing Enter on equipped items removes them."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import tcod.event
from game import Game
from items.weapons.dagger import Dagger
from items.armor.leather_armor import LeatherArmor
from items.accessories.protection_ring import ProtectionRing

def test_enter_unequips_weapon():
    """Test that pressing Enter on equipped weapon unequips it."""
    game = Game()
    
    # Equip a weapon
    sword = Dagger(0, 0)
    game.player.weapon = sword
    
    # Enter inventory mode
    game.game_state = 'INVENTORY'
    
    # Select weapon slot in equipment mode
    game.selection_mode = "equipment"
    game.selected_equipment_index = 0  # Weapon slot
    
    # Call unequip directly to test the functionality
    game.unequip_selected_item()
    
    # Weapon should be unequipped and in inventory
    assert game.player.weapon is None
    assert len(game.player.inventory) == 1
    assert game.player.inventory[0] == sword

def test_enter_unequips_armor():
    """Test that pressing Enter on equipped armor unequips it."""
    game = Game()
    
    # Equip armor
    armor = LeatherArmor(0, 0)
    game.player.armor = armor
    
    # Enter inventory mode
    game.game_state = 'INVENTORY'
    
    # Select armor slot in equipment mode
    game.selection_mode = "equipment"
    game.selected_equipment_index = 1  # Armor slot
    
    # Call unequip directly to test the functionality
    game.unequip_selected_item()
    
    # Armor should be unequipped and in inventory
    assert game.player.armor is None
    assert len(game.player.inventory) == 1
    assert game.player.inventory[0] == armor

def test_enter_unequips_accessory():
    """Test that pressing Enter on equipped accessory unequips it."""
    game = Game()
    
    # Equip an accessory
    ring = ProtectionRing(0, 0)
    game.player.accessories[0] = ring
    
    # Enter inventory mode
    game.game_state = 'INVENTORY'
    
    # Select first accessory slot in equipment mode
    game.selection_mode = "equipment"
    game.selected_equipment_index = 2  # First accessory slot
    
    # Call unequip directly to test the functionality
    game.unequip_selected_item()
    
    # Accessory should be unequipped and in inventory
    assert game.player.accessories[0] is None
    assert len(game.player.inventory) == 1
    assert game.player.inventory[0] == ring

def test_enter_does_nothing_on_empty_slot():
    """Test that pressing Enter on empty equipment slot does nothing harmful."""
    game = Game()
    
    # Make sure no equipment (reset in case it started with something)
    game.player.weapon = None
    
    # Enter inventory mode
    game.game_state = 'INVENTORY'
    
    # Select weapon slot in equipment mode
    game.selection_mode = "equipment"
    game.selected_equipment_index = 0  # Weapon slot
    
    # Call unequip directly to test the functionality
    game.unequip_selected_item()
    
    # Nothing should change
    assert game.player.weapon is None
    assert len(game.player.inventory) == 0

def test_enter_fails_when_inventory_full():
    """Test that unequip fails when inventory is full."""
    game = Game()
    
    # Fill inventory to max
    for i in range(game.player.inventory_size):
        game.player.add_item(Dagger(0, 0))
    
    # Equip a weapon
    sword = Dagger(0, 0)
    game.player.weapon = sword
    
    # Enter inventory mode
    game.game_state = 'INVENTORY'
    
    # Select weapon slot in equipment mode
    game.selection_mode = "equipment"
    game.selected_equipment_index = 0  # Weapon slot
    
    # Call unequip directly to test the functionality
    game.unequip_selected_item()
    
    # Weapon should still be equipped (unequip failed due to full inventory)
    assert game.player.weapon == sword
    assert len(game.player.inventory) == game.player.inventory_size

if __name__ == "__main__":
    test_enter_unequips_weapon()
    test_enter_unequips_armor()
    test_enter_unequips_accessory()
    test_enter_does_nothing_on_empty_slot()
    test_enter_fails_when_inventory_full()
    print("All tests passed!")