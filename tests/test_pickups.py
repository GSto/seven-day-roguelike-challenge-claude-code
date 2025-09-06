"""
Tests for pickup items with instant effects.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from items.pickups import Pickup, Snackie
from player import Player
from stats import Stats


def test_pickup_base_class():
    """Test the base Pickup class."""
    pickup = Pickup(5, 5, "Test Pickup", "*", (255, 255, 255))
    assert pickup.x == 5
    assert pickup.y == 5
    assert pickup.name == "Test Pickup"
    assert pickup.char == "*"
    assert pickup.market_value == 0  # Pickups have no market value
    
    # Test default on_pickup behavior
    player = Player(0, 0)
    success, message = pickup.on_pickup(player)
    assert success == False
    assert message == "Nothing happens."


def test_snackie_initialization():
    """Test Snackie pickup initialization."""
    snackie = Snackie(10, 10)
    assert snackie.x == 10
    assert snackie.y == 10
    assert snackie.name == "Snackie"
    assert snackie.char == "*"
    assert snackie.heal_amount == 5
    assert snackie.market_value == 0


def test_snackie_heals_player():
    """Test that Snackie heals the player when picked up."""
    player = Player(0, 0)
    player.stats.max_hp = 50
    player.stats.hp = 30  # Damaged player
    
    snackie = Snackie(0, 0)
    success, message = snackie.on_pickup(player)
    
    assert success == True
    assert player.stats.hp == 35  # 30 + 5
    assert "heals you for 5 HP" in message


def test_snackie_healing_caps_at_max_hp():
    """Test that Snackie healing doesn't exceed max HP."""
    player = Player(0, 0)
    player.stats.max_hp = 50
    player.stats.hp = 48  # Nearly full HP
    
    snackie = Snackie(0, 0)
    success, message = snackie.on_pickup(player)
    
    assert success == True
    assert player.stats.hp == 50  # Capped at max
    assert "heals you for 2 HP" in message  # Only healed 2 HP


def test_snackie_fails_at_full_health():
    """Test that Snackie pickup fails when player is at full health."""
    player = Player(0, 0)
    player.stats.max_hp = 50
    player.stats.hp = 50  # Full health
    
    snackie = Snackie(0, 0)
    success, message = snackie.on_pickup(player)
    
    assert success == False
    assert player.stats.hp == 50  # No change
    assert "already at full health" in message


def test_pickup_instant_effect_not_added_to_inventory():
    """Test that pickups don't get added to inventory (tested via game logic)."""
    # This is tested in the game.py try_pickup_item method
    # Pickups should apply their effect immediately and not be added to inventory
    # This test documents the expected behavior
    player = Player(0, 0)
    initial_inventory_size = len(player.inventory)
    
    snackie = Snackie(0, 0)
    # When picked up via game.try_pickup_item, it should NOT be in inventory
    # Just applying the effect here to verify it doesn't modify inventory
    success, message = snackie.on_pickup(player)
    
    # Inventory should remain unchanged
    assert len(player.inventory) == initial_inventory_size


if __name__ == "__main__":
    test_pickup_base_class()
    test_snackie_initialization()
    test_snackie_heals_player()
    test_snackie_healing_caps_at_max_hp()
    test_snackie_fails_at_full_health()
    test_pickup_instant_effect_not_added_to_inventory()
    print("All pickup tests passed!")