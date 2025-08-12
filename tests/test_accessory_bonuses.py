"""
Tests for accessory bonus functionality.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from player import Player
from items.accessories import Rosary, HeadLamp


def test_rosary_health_aspect_bonus():
    """Test that Rosary provides health aspect bonus."""
    player = Player(5, 5)
    rosary = Rosary(0, 0)
    
    # Check base health aspect
    base_health_aspect = player.get_total_health_aspect()
    assert base_health_aspect == 0.3  # Player base health aspect
    
    # Equip rosary
    player.accessories.append(rosary)
    
    # Check health aspect with rosary equipped
    total_health_aspect = player.get_total_health_aspect()
    expected = 0.3 + 0.1  # Base + rosary bonus
    assert total_health_aspect == expected, f"Expected {expected}, got {total_health_aspect}"


def test_headlamp_fov_bonus():
    """Test that HeadLamp provides FOV bonus."""
    player = Player(5, 5)
    headlamp = HeadLamp(0, 0)
    
    # Check base FOV
    base_fov = player.get_total_fov()
    assert base_fov == 10  # Player base FOV
    
    # Equip headlamp
    player.accessories.append(headlamp)
    
    # Check FOV with headlamp equipped
    total_fov = player.get_total_fov()
    expected = 10 + 5  # Base + headlamp bonus
    assert total_fov == expected, f"Expected {expected}, got {total_fov}"


def test_accessory_attributes_exist():
    """Test that accessories have the correct bonus attributes."""
    rosary = Rosary(0, 0)
    headlamp = HeadLamp(0, 0)
    
    # Check rosary attributes
    assert hasattr(rosary, 'health_aspect_bonus')
    assert rosary.health_aspect_bonus == 0.1
    assert hasattr(rosary, 'fov_bonus')
    assert rosary.fov_bonus == 0
    
    # Check headlamp attributes
    assert hasattr(headlamp, 'fov_bonus')
    assert headlamp.fov_bonus == 5
    assert hasattr(headlamp, 'health_aspect_bonus')
    assert headlamp.health_aspect_bonus == 0


if __name__ == "__main__":
    test_rosary_health_aspect_bonus()
    test_headlamp_fov_bonus()
    test_accessory_attributes_exist()
    print("All accessory bonus tests passed!")