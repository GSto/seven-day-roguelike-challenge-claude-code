"""
Test that all pickup types can spawn from the pool.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from items.pool import item_pool
from items.pickups import Snackie, Nickel, Penny, ShellToken


def test_all_pickup_types_can_spawn():
    """Test that all pickup types can spawn from the pool."""
    # Reset pool state
    item_pool.start_new_floor(1)
    
    # Track which pickup types we've seen
    pickup_types_seen = set()
    
    # Generate many items to find all pickup types
    max_attempts = 5000
    for i in range(max_attempts):
        item = item_pool.create_item_for_level(1, 0, 0, item_type='pickup')
        if item:
            pickup_types_seen.add(type(item).__name__)
        
        # Stop early if we've seen all types
        if len(pickup_types_seen) >= 4:
            break
    
    print(f"Pickup types found: {pickup_types_seen}")
    
    # Should have found all 4 pickup types
    expected_types = {'Snackie', 'Nickel', 'Penny', 'ShellToken'}
    assert pickup_types_seen == expected_types, f"Missing types: {expected_types - pickup_types_seen}"


def test_pickup_type_distribution():
    """Test the distribution of different pickup types."""
    # Reset pool state
    item_pool.start_new_floor(1)
    
    # Count occurrences of each pickup type
    pickup_counts = {}
    total_pickups = 1000
    
    for i in range(total_pickups):
        item = item_pool.create_item_for_level(1, 0, 0, item_type='pickup')
        if item:
            pickup_type = type(item).__name__
            pickup_counts[pickup_type] = pickup_counts.get(pickup_type, 0) + 1
    
    print("Pickup type distribution:")
    for pickup_type, count in pickup_counts.items():
        percentage = (count / total_pickups) * 100
        print(f"  {pickup_type}: {count} ({percentage:.1f}%)")
    
    # All pickup types should appear
    expected_types = {'Snackie', 'Nickel', 'Penny', 'ShellToken'}
    actual_types = set(pickup_counts.keys())
    assert actual_types == expected_types, f"Missing types: {expected_types - actual_types}"
    
    # Snackie should be most common (highest rarity multiplier)
    assert pickup_counts['Snackie'] > pickup_counts['Nickel'], "Snackie should be more common than Nickel"
    assert pickup_counts['Penny'] > pickup_counts['Nickel'], "Penny should be more common than Nickel"
    assert pickup_counts['Nickel'] > pickup_counts['ShellToken'], "Nickel should be more common than ShellToken (rare)"


if __name__ == "__main__":
    test_all_pickup_types_can_spawn()
    test_pickup_type_distribution()
    print("All pickup spawn tests passed!")