"""Test that Anaglyph accessory correctly balances attack and defense."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from player import Player
from items.accessories.anaglyph import Anaglyph

def test_anaglyph_balances_stats():
    """Test that Anaglyph properly balances attack and defense."""
    player = Player(5, 5)
    
    # Set up initial stats
    player.attack = 8
    player.defense = 12
    
    # Check initial values (no Anaglyph)
    initial_attack = player.get_total_attack()
    initial_defense = player.get_total_defense()
    print(f"Initial: ATK={initial_attack}, DEF={initial_defense}")
    
    # Equip Anaglyph
    anaglyph = Anaglyph(0, 0)
    player.accessories[0] = anaglyph
    
    # Get balanced values
    balanced_attack = player.get_total_attack()
    balanced_defense = player.get_total_defense()
    print(f"With Anaglyph: ATK={balanced_attack}, DEF={balanced_defense}")
    
    # Both should be the average of the original values
    expected = (initial_attack + initial_defense) // 2
    assert balanced_attack == expected, f"Expected attack {expected}, got {balanced_attack}"
    assert balanced_defense == expected, f"Expected defense {expected}, got {balanced_defense}"

def test_anaglyph_with_equipment():
    """Test that Anaglyph balances stats including equipment bonuses."""
    player = Player(5, 5)
    
    # Remove starting equipment
    player.weapon = None
    player.armor = None
    
    # Set base stats
    player.attack = 5
    player.defense = 5
    
    # Add weapon with +3 attack
    from items.weapons.dagger import Dagger
    weapon = Dagger(0, 0)  # +3 attack
    player.weapon = weapon
    
    # Add armor with +2 defense  
    from items.armor.leather_armor import LeatherArmor
    armor = LeatherArmor(0, 0)  # +2 defense
    player.armor = armor
    
    # Check values before Anaglyph
    pre_attack = player.get_total_attack()  # 5 + 3 = 8
    pre_defense = player.get_total_defense()  # 5 + 2 = 7
    print(f"With equipment: ATK={pre_attack}, DEF={pre_defense}")
    
    # Equip Anaglyph
    anaglyph = Anaglyph(0, 0)
    player.accessories[0] = anaglyph
    
    # Get balanced values
    balanced_attack = player.get_total_attack()
    balanced_defense = player.get_total_defense()
    print(f"With Anaglyph: ATK={balanced_attack}, DEF={balanced_defense}")
    
    # Both should be the average
    expected = (pre_attack + pre_defense) // 2  # (8 + 7) // 2 = 7
    assert balanced_attack == expected, f"Expected attack {expected}, got {balanced_attack}"
    assert balanced_defense == expected, f"Expected defense {expected}, got {balanced_defense}"

def test_anaglyph_display_values():
    """Test that displayed values match the calculated values."""
    player = Player(5, 5)
    
    # Set specific stats
    player.attack = 8
    player.defense = 12
    
    # Equip Anaglyph
    anaglyph = Anaglyph(0, 0)
    player.accessories[0] = anaglyph
    
    # The UI displays player.get_total_attack() and player.get_total_defense()
    displayed_attack = player.get_total_attack()
    displayed_defense = player.get_total_defense()
    
    # With base ATK=8 and DEF=12, the average is 10
    # But we need to account for starting equipment
    print(f"Displayed: ATK={displayed_attack}, DEF={displayed_defense}")
    
    # Both values should be equal (balanced)
    assert displayed_attack == displayed_defense, f"Attack {displayed_attack} should equal Defense {displayed_defense}"

if __name__ == "__main__":
    test_anaglyph_balances_stats()
    test_anaglyph_with_equipment()
    test_anaglyph_display_values()
    print("All tests passed!")