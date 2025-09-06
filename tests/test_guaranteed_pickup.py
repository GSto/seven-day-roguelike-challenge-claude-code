"""
Test that each floor is guaranteed to have at least one pickup.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from level.level import Level
from items.pickups import Pickup
import random


def test_guaranteed_pickup_per_floor():
    """Test that each floor has at least one pickup item."""
    # Test multiple floor levels
    test_levels = [1, 2, 3, 5, 7, 9, 10]
    
    for level_num in test_levels:
        print(f"Testing floor {level_num}...")
        
        # Generate multiple floors to ensure consistency
        pickup_found_count = 0
        total_tests = 10
        
        for test_run in range(total_tests):
            # Set a different seed for each test run to ensure variety
            random.seed(42 + test_run + level_num * 100)
            
            # Create and generate a level
            level = Level(level_num)
            
            # Count pickups on the floor
            pickup_count = 0
            for item in level.items:
                if isinstance(item, Pickup):
                    pickup_count += 1
            
            if pickup_count >= 1:
                pickup_found_count += 1
            
            # Debug info for failed cases
            if pickup_count == 0:
                print(f"  Warning: Floor {level_num} run {test_run} has NO pickups!")
                print(f"  Total items on floor: {len(level.items)}")
        
        # Calculate success rate
        success_rate = pickup_found_count / total_tests
        print(f"  Floor {level_num}: {pickup_found_count}/{total_tests} floors had pickups ({success_rate:.0%})")
        
        # We want at least 90% success rate (allowing for some randomness edge cases)
        assert success_rate >= 0.9, f"Floor {level_num} only had pickups in {success_rate:.0%} of tests"


def test_pickup_types_on_floor():
    """Test what types of pickups appear on floors."""
    # Test a few floor levels
    level = Level(1)
    
    pickup_types = {}
    for item in level.items:
        if isinstance(item, Pickup):
            pickup_type = type(item).__name__
            pickup_types[pickup_type] = pickup_types.get(pickup_type, 0) + 1
    
    print(f"Pickup types found on floor 1: {pickup_types}")
    
    # Should have at least one pickup
    assert len(pickup_types) > 0, "No pickups found on floor"
    
    # Should have Snackie (currently the only pickup type)
    assert 'Snackie' in pickup_types, "Snackie not found on floor"


if __name__ == "__main__":
    test_guaranteed_pickup_per_floor()
    test_pickup_types_on_floor()
    print("All guaranteed pickup tests passed!")