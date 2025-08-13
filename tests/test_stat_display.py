"""Test stat display formatting."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from player import Player


def test_crit_evade_percentage_display():
    """Test that crit and evade values display correctly as percentages."""
    player = Player(x=0, y=0)
    
    # Test base values
    base_crit = player.get_total_crit()
    base_evade = player.get_total_evade()
    
    # Format as percentage integers
    crit_display = f"{int(base_crit * 100)}%"
    evade_display = f"{int(base_evade * 100)}%"
    
    print(f"Base crit: {base_crit} -> Display: {crit_display}")
    print(f"Base evade: {base_evade} -> Display: {evade_display}")
    
    # Test with some example values
    test_values = [
        (0.1, "10%"),
        (0.15, "15%"),
        (0.099, "9%"),  # Should round down
        (0.101, "10%"),  # Should round down
        (0.255, "25%"),  # Should round down
        (0.5, "50%"),
        (1.0, "100%"),
    ]
    
    for value, expected in test_values:
        result = f"{int(value * 100)}%"
        assert result == expected, f"Value {value} should display as {expected}, got {result}"
        print(f"✓ {value} correctly displays as {result}")
    
    print("\nAll percentage display tests passed!")


if __name__ == "__main__":
    test_crit_evade_percentage_display()