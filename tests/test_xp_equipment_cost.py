"""
Test XP cost system for equipment.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from player import Player
from items import Dagger, Sword, LeatherArmor, PowerRing, WhiteTShirt, WoodenStick
from items.base import Equipment
from game import Game
import level


def test_equipment_has_xp_cost():
    """Test that equipment items have an xp_cost attribute."""
    # Test weapons
    dagger = Dagger(5, 5)
    assert hasattr(dagger, 'xp_cost')
    assert dagger.xp_cost == 5  # Default cost
    
    # Test armor
    leather = LeatherArmor(5, 5)
    assert hasattr(leather, 'xp_cost')
    assert leather.xp_cost == 5  # Default cost
    
    # Test accessories
    ring = PowerRing(5, 5)
    assert hasattr(ring, 'xp_cost')
    assert ring.xp_cost == 5  # Default cost


def test_starting_equipment_has_zero_cost():
    """Test that starting equipment costs 0 XP."""
    stick = WoodenStick(5, 5)
    assert stick.xp_cost == 0
    
    shirt = WhiteTShirt(5, 5)
    assert shirt.xp_cost == 0


def test_can_equip_with_sufficient_xp():
    """Test that player can equip items when they have enough XP."""
    player = Player(5, 5)
    player.xp = 10  # Enough for default cost of 5
    
    dagger = Dagger(5, 5)
    assert dagger.can_equip(player) == True


def test_cannot_equip_with_insufficient_xp():
    """Test that player cannot equip items when they don't have enough XP."""
    player = Player(5, 5)
    player.xp = 3  # Not enough for default cost of 5
    
    dagger = Dagger(5, 5)
    assert dagger.can_equip(player) == False


def test_can_equip_starting_equipment():
    """Test that player can always equip starting equipment (0 cost)."""
    player = Player(5, 5)
    player.xp = 0  # No XP
    
    stick = WoodenStick(5, 5)
    assert stick.can_equip(player) == True
    
    shirt = WhiteTShirt(5, 5)
    assert shirt.can_equip(player) == True


def test_xp_deduction_on_successful_equip():
    """Test that XP is properly deducted when equipping items."""
    # Create a mock level for the game
    test_level = level.Level(1)
    
    game = Game()
    game.level = test_level
    game.player.x = 5
    game.player.y = 5
    game.player.xp = 20
    game.player.add_item(Dagger(0, 0))
    
    initial_xp = game.player.xp
    dagger = game.player.inventory[0]
    
    # Equip the dagger
    game.equip_item(dagger)
    
    # Check XP was deducted
    assert game.player.xp == initial_xp - dagger.xp_cost
    assert game.player.weapon == dagger


def test_no_xp_deduction_for_free_equipment():
    """Test that no XP is deducted for equipment with 0 cost."""
    test_level = level.Level(1)
    
    game = Game()
    game.level = test_level
    game.player.x = 5
    game.player.y = 5
    game.player.xp = 10
    game.player.add_item(WoodenStick(0, 0))
    
    initial_xp = game.player.xp
    stick = game.player.inventory[0]
    
    # Equip the stick
    game.equip_item(stick)
    
    # Check no XP was deducted
    assert game.player.xp == initial_xp
    assert game.player.weapon == stick


def test_equip_blocked_with_insufficient_xp():
    """Test that equipping is blocked when player doesn't have enough XP."""
    test_level = level.Level(1)
    
    game = Game()
    game.level = test_level
    game.player.x = 5
    game.player.y = 5
    game.player.xp = 3  # Less than required 5
    game.player.add_item(Dagger(0, 0))
    
    initial_xp = game.player.xp
    initial_weapon = game.player.weapon
    dagger = game.player.inventory[0]
    
    # Try to equip the dagger
    game.equip_item(dagger)
    
    # Check equipping was blocked
    assert game.player.xp == initial_xp  # No XP deducted
    assert game.player.weapon == initial_weapon  # Weapon unchanged
    assert dagger in game.player.inventory  # Item still in inventory


def test_different_equipment_slots_xp_costs():
    """Test XP costs work for all equipment slots."""
    test_level = level.Level(1)
    
    game = Game()
    game.level = test_level
    game.player.x = 5
    game.player.y = 5
    game.player.xp = 50  # Plenty of XP
    
    # Test weapon
    game.player.add_item(Dagger(0, 0))
    initial_xp = game.player.xp
    game.equip_item(game.player.inventory[0])
    assert game.player.xp == initial_xp - 5
    
    # Test armor
    armor = LeatherArmor(0, 0)
    game.player.add_item(armor)
    initial_xp = game.player.xp
    game.equip_item(armor)
    assert game.player.xp == initial_xp - 5
    
    # Test accessory
    ring = PowerRing(0, 0)
    game.player.add_item(ring)
    initial_xp = game.player.xp
    game.equip_item(ring)  # Equip the specific ring
    assert game.player.xp == initial_xp - 5


def test_custom_xp_cost():
    """Test that custom XP costs can be set."""
    # Create equipment with custom cost
    expensive_item = Equipment(5, 5, "Expensive Item", '!', (255, 255, 255), 
                              "Very expensive", equipment_slot="weapon", xp_cost=15)
    
    player = Player(5, 5)
    
    # Player can't afford it
    player.xp = 10
    assert expensive_item.can_equip(player) == False
    
    # Player can afford it
    player.xp = 20
    assert expensive_item.can_equip(player) == True


def test_unequipping_does_not_refund_xp():
    """Test that unequipping items does not refund XP."""
    test_level = level.Level(1)
    
    game = Game()
    game.level = test_level
    game.player.x = 5
    game.player.y = 5
    game.player.xp = 20
    
    # Equip a dagger
    game.player.add_item(Dagger(0, 0))
    dagger = game.player.inventory[0]
    game.equip_item(dagger)
    
    xp_after_equip = game.player.xp
    
    # Equip something else to unequip the dagger
    game.player.add_item(Sword(0, 0))
    sword = game.player.inventory[0]
    game.equip_item(sword)  # This should unequip dagger and equip sword
    
    # XP should be further reduced by sword cost, not refunded for dagger
    assert game.player.xp == xp_after_equip - sword.xp_cost
    assert dagger in game.player.inventory  # Dagger back in inventory


if __name__ == "__main__":
    # Run all tests
    test_equipment_has_xp_cost()
    test_starting_equipment_has_zero_cost()
    test_can_equip_with_sufficient_xp()
    test_cannot_equip_with_insufficient_xp()
    test_can_equip_starting_equipment()
    test_xp_deduction_on_successful_equip()
    test_no_xp_deduction_for_free_equipment()
    test_equip_blocked_with_insufficient_xp()
    test_different_equipment_slots_xp_costs()
    test_custom_xp_cost()
    test_unequipping_does_not_refund_xp()
    print("All XP equipment cost tests passed!")