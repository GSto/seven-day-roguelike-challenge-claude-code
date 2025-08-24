"""Test that Map, Compass, and Bomb consumables have been removed."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_consumables_removed_from_imports():
    """Test that Map, Compass, and Bomb are not importable."""
    from items import consumables
    
    # These should not be in the module
    assert not hasattr(consumables, 'Map'), "Map should be removed"
    assert not hasattr(consumables, 'Compass'), "Compass should be removed"
    assert not hasattr(consumables, 'Bomb'), "Bomb should be removed"
    
    # These should not be in __all__
    assert 'Map' not in consumables.__all__, "Map should not be exported"
    assert 'Compass' not in consumables.__all__, "Compass should not be exported"
    assert 'Bomb' not in consumables.__all__, "Bomb should not be exported"

def test_factory_doesnt_reference_removed_items():
    """Test that the factory doesn't reference removed items."""
    from items.factory import BASE_CONSUMABLES, EARLY_GAME_CONSUMABLES
    
    # Check that removed items are not in any consumable pools
    for pool in [BASE_CONSUMABLES, EARLY_GAME_CONSUMABLES]:
        for item_class in pool:
            assert item_class.__name__ != 'Map', f"Map found in pool"
            assert item_class.__name__ != 'Compass', f"Compass found in pool"
            assert item_class.__name__ != 'Bomb', f"Bomb found in pool"

def test_files_removed():
    """Test that the files have been removed."""
    import os
    base_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'items', 'consumables')
    
    assert not os.path.exists(os.path.join(base_path, 'map.py')), "map.py should be removed"
    assert not os.path.exists(os.path.join(base_path, 'compass.py')), "compass.py should be removed"
    assert not os.path.exists(os.path.join(base_path, 'bomb.py')), "bomb.py should be removed"

if __name__ == "__main__":
    test_consumables_removed_from_imports()
    test_factory_doesnt_reference_removed_items()
    test_files_removed()
    print("All tests passed!")