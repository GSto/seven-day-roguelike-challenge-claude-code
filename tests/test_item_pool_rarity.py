#!/usr/bin/env python
"""Test the item pool system uses only rarity for drop rates."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.items.pool import ItemPool, ItemSpec, RARITY_COMMON, RARITY_UNCOMMON, RARITY_RARE
from collections import Counter


def test_item_pool_uses_rarity_only():
    """Test that item pool drop rates are based only on rarity."""
    pool = ItemPool()
    
    # Test that calculate_spawn_weight doesn't use difficulty_rating
    # (it shouldn't even exist anymore)
    assert not hasattr(ItemSpec, 'difficulty_rating'), "ItemSpec should not have difficulty_rating attribute"
    
    # Create a test spec to verify weight calculation
    test_spec = pool.weapon_specs[0]  # Get first weapon spec
    
    # Check that the spec doesn't have difficulty_rating
    assert not hasattr(test_spec, 'difficulty_rating'), "ItemSpec instances should not have difficulty_rating"
    
    # Test weight calculation at different levels
    level = 3
    weight = pool.calculate_spawn_weight(test_spec, level)
    
    # Weight should be based on rarity and level constraints, not difficulty
    if test_spec.min_level <= level <= (test_spec.max_level or float('inf')):
        assert weight > 0, "Weight should be positive when item is in level range"
    else:
        assert weight == 0, "Weight should be zero when item is out of level range"
    
    print("✓ Item pool correctly uses only rarity for drop rates")


def test_rarity_distribution():
    """Test that rarity values affect drop rates correctly."""
    pool = ItemPool()
    
    # Test at level 2 where common items should dominate
    level = 2
    item_counts = Counter()
    rarity_counts = {RARITY_COMMON: 0, RARITY_UNCOMMON: 0, RARITY_RARE: 0}
    
    # Spawn many items and count rarity distribution
    for _ in range(1000):
        pool.start_new_floor(level)  # Reset floor tracking
        item = pool.create_item_for_level(level, 0, 0, item_type='weapon')
        
        # Find the spec for this item
        for spec in pool.weapon_specs:
            if isinstance(item, spec.item_class):
                rarity_counts[spec.rarity] = rarity_counts.get(spec.rarity, 0) + 1
                break
    
    # At early levels, common items should appear more frequently
    # The exact ratio depends on what items are available at each level
    total = sum(rarity_counts.values())
    common_pct = rarity_counts[RARITY_COMMON] / total * 100
    uncommon_pct = rarity_counts[RARITY_UNCOMMON] / total * 100
    rare_pct = rarity_counts[RARITY_RARE] / total * 100
    
    # Test that rarity weights are being applied (not just counting available items)
    assert common_pct > 30, f"Common items should be a significant portion (got {common_pct:.1f}%)"
    
    # Test at level 8 with rare items
    level = 8
    rarity_counts = {RARITY_COMMON: 0, RARITY_UNCOMMON: 0, RARITY_RARE: 0}
    
    for _ in range(1000):
        pool.start_new_floor(level)  # Reset floor tracking
        item = pool.create_item_for_level(level, 0, 0, item_type='weapon')
        
        # Find the spec for this item
        for spec in pool.weapon_specs:
            if isinstance(item, spec.item_class):
                rarity_counts[spec.rarity] = rarity_counts.get(spec.rarity, 0) + 1
                break
    
    # Verify rare items can spawn but are less common than others
    assert rarity_counts[RARITY_RARE] > 0, "Rare items should be able to spawn at level 8"
    assert rarity_counts[RARITY_RARE] < rarity_counts[RARITY_UNCOMMON], "Rare items should be less common than uncommon"
    
    print(f"✓ Rarity distribution working - Level 2: Common={common_pct:.1f}%, "
          f"Level 8: Rare items spawned {rarity_counts[RARITY_RARE]} times")


def test_level_constraints_still_work():
    """Test that level constraints still work without difficulty factor."""
    pool = ItemPool()
    
    # Test early game (level 1)
    pool.start_new_floor(1)
    for _ in range(20):
        item = pool.create_item_for_level(1, 0, 0, item_type='weapon')
        # Find the spec
        for spec in pool.weapon_specs:
            if isinstance(item, spec.item_class):
                assert spec.min_level <= 1, f"{spec.item_class.__name__} should not spawn at level 1"
                if spec.max_level is not None:
                    assert 1 <= spec.max_level, f"{spec.item_class.__name__} should be able to spawn at level 1"
                break
    
    # Test late game (level 9)
    pool.start_new_floor(9)
    late_game_items = []
    for _ in range(20):
        item = pool.create_item_for_level(9, 0, 0, item_type='weapon')
        late_game_items.append(item.__class__.__name__)
    
    # Should see some late-game weapons at level 9
    from src.items.weapons import RiversOfBlood, WarHammer, WarScythe
    late_game_weapons = {'RiversOfBlood', 'WarHammer', 'WarScythe'}
    spawned_late_weapons = set(late_game_items) & late_game_weapons
    assert len(spawned_late_weapons) > 0, f"Should spawn some late-game weapons at level 9, got: {set(late_game_items)}"
    
    print("✓ Level constraints working correctly")


if __name__ == "__main__":
    test_item_pool_uses_rarity_only()
    test_rarity_distribution()
    test_level_constraints_still_work()
    print("\n✅ All item pool rarity tests passed!")