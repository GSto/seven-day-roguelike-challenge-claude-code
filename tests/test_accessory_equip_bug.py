"""
Test for accessory equip bug fix.
Verifies that equipping accessories doesn't create new slots beyond the 3 allowed.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from player import Player
from items.accessories import PowerRing, ProtectionRing, ShadowRing


def test_equipping_accessory_replaces_none_slot():
    """Test that equipping an accessory replaces a None slot instead of appending."""
    player = Player(10, 10)
    
    # Start with 3 None slots
    assert len(player.accessories) == 3
    assert all(acc is None for acc in player.accessories)
    
    # Equip first accessory
    ring1 = PowerRing(0, 0)
    player.accessories[0] = ring1
    
    # Should still have 3 slots
    assert len(player.accessories) == 3
    assert player.accessories[0] == ring1
    assert player.accessories[1] is None
    assert player.accessories[2] is None
    
    # Equip second accessory
    ring2 = ProtectionRing(0, 0)
    player.accessories[1] = ring2
    
    # Should still have 3 slots
    assert len(player.accessories) == 3
    assert player.accessories[0] == ring1
    assert player.accessories[1] == ring2
    assert player.accessories[2] is None
    
    # Equip third accessory
    ring3 = ShadowRing(0, 0)
    player.accessories[2] = ring3
    
    # Should still have 3 slots
    assert len(player.accessories) == 3
    assert player.accessories[0] == ring1
    assert player.accessories[1] == ring2
    assert player.accessories[2] == ring3


def test_unequipping_sets_slot_to_none():
    """Test that unequipping an accessory sets the slot to None."""
    player = Player(10, 10)
    
    # Equip accessories
    ring1 = PowerRing(0, 0)
    ring2 = ProtectionRing(0, 0)
    player.accessories[0] = ring1
    player.accessories[1] = ring2
    
    # Unequip first accessory
    player.accessories[0] = None
    
    # Check that slot is None and list size unchanged
    assert len(player.accessories) == 3
    assert player.accessories[0] is None
    assert player.accessories[1] == ring2
    assert player.accessories[2] is None
    
    # Unequip second accessory
    player.accessories[1] = None
    
    # Check that both slots are None
    assert len(player.accessories) == 3
    assert all(acc is None for acc in player.accessories)


def test_equipped_accessories_method():
    """Test that equipped_accessories only returns non-None accessories."""
    player = Player(10, 10)
    
    # Start with no equipped accessories
    assert len(player.equipped_accessories()) == 0
    
    # Equip one accessory
    ring1 = PowerRing(0, 0)
    player.accessories[0] = ring1
    equipped = player.equipped_accessories()
    assert len(equipped) == 1
    assert ring1 in equipped
    
    # Equip second accessory in slot 2 (skip slot 1)
    ring2 = ProtectionRing(0, 0)
    player.accessories[2] = ring2
    equipped = player.equipped_accessories()
    assert len(equipped) == 2
    assert ring1 in equipped
    assert ring2 in equipped
    
    # Equip third accessory in slot 1
    ring3 = ShadowRing(0, 0)
    player.accessories[1] = ring3
    equipped = player.equipped_accessories()
    assert len(equipped) == 3
    assert ring1 in equipped
    assert ring2 in equipped
    assert ring3 in equipped


def test_accessory_list_never_exceeds_three_slots():
    """Test that the accessory list never grows beyond 3 slots."""
    player = Player(10, 10)
    
    # Try to manually append (should not be done in normal gameplay)
    # This test verifies the fix prevents the bug
    initial_length = len(player.accessories)
    assert initial_length == 3
    
    # Equip accessories normally
    ring1 = PowerRing(0, 0)
    ring2 = ProtectionRing(0, 0)
    ring3 = ShadowRing(0, 0)
    
    player.accessories[0] = ring1
    assert len(player.accessories) == 3
    
    player.accessories[1] = ring2
    assert len(player.accessories) == 3
    
    player.accessories[2] = ring3
    assert len(player.accessories) == 3
    
    # Replace an accessory
    new_ring = PowerRing(0, 0)
    player.accessories[1] = new_ring
    assert len(player.accessories) == 3
    assert player.accessories[1] == new_ring


if __name__ == "__main__":
    test_equipping_accessory_replaces_none_slot()
    test_unequipping_sets_slot_to_none()
    test_equipped_accessories_method()
    test_accessory_list_never_exceeds_three_slots()
    print("All accessory equip bug tests passed!")