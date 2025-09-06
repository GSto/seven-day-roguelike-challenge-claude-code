"""
Tests for pickup item pool integration.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from items.pool import item_pool
from items.pickups import Snackie


def test_pickups_in_item_pool():
    """Test that pickups are properly configured in the item pool."""
    # Check that pickup_specs exists and contains Snackie
    assert hasattr(item_pool, 'pickup_specs')
    assert len(item_pool.pickup_specs) > 0
    
    # Check that Snackie is in the pickup specs
    snackie_spec = None
    for spec in item_pool.pickup_specs:
        if spec.item_class == Snackie:
            snackie_spec = spec
            break
    
    assert snackie_spec is not None
    assert snackie_spec.item_type == 'pickup'
    assert snackie_spec.min_level == 1
    assert snackie_spec.max_level is None  # Available at all levels


def test_pickup_weights_in_pool():
    """Test that pickups have appropriate weights at different levels."""
    # Test early game (level 1-2): 10% pickups
    weights_lvl1 = item_pool.get_item_type_weights(1)
    assert 'pickup' in weights_lvl1
    assert weights_lvl1['pickup'] == 0.10
    
    # Test mid game (level 3-5): 7% pickups
    weights_lvl4 = item_pool.get_item_type_weights(4)
    assert 'pickup' in weights_lvl4
    assert weights_lvl4['pickup'] == 0.07
    
    # Test late game (level 6-8): 6% pickups
    weights_lvl7 = item_pool.get_item_type_weights(7)
    assert 'pickup' in weights_lvl7
    assert weights_lvl7['pickup'] == 0.06
    
    # Test end game (level 9+): 5% pickups
    weights_lvl10 = item_pool.get_item_type_weights(10)
    assert 'pickup' in weights_lvl10
    assert weights_lvl10['pickup'] == 0.05


def test_pickup_generation():
    """Test that pickups can be generated from the pool."""
    # Reset pool state
    item_pool.start_new_floor(1)
    
    # Try to generate a pickup specifically
    item = item_pool.create_item_for_level(1, 5, 5, item_type='pickup')
    
    # Should get some pickup type
    assert item is not None
    from items.pickups import Pickup
    assert isinstance(item, Pickup)
    assert item.x == 5
    assert item.y == 5


def test_pickup_spawn_probability():
    """Test that pickups spawn at roughly the expected rate."""
    # Reset pool state
    item_pool.start_new_floor(1)
    
    # Generate many items and count pickups
    pickup_count = 0
    total_items = 1000
    
    for i in range(total_items):
        item = item_pool.create_item_for_level(1, 0, 0)
        from items.pickups import Pickup
        if isinstance(item, Pickup):
            pickup_count += 1
    
    # At level 1, pickups should be ~10% of items
    pickup_rate = pickup_count / total_items
    print(f"Pickup spawn rate at level 1: {pickup_rate:.2%} (expected ~10%)")
    
    # Allow some variance (between 5% and 15%)
    assert 0.05 <= pickup_rate <= 0.15


if __name__ == "__main__":
    test_pickups_in_item_pool()
    test_pickup_weights_in_pool()
    test_pickup_generation()
    test_pickup_spawn_probability()
    print("All pickup pool tests passed!")