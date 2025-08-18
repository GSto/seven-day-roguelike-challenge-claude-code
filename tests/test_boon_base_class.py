"""
Test for the new base Boon class and updated boon inheritance.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from player import Player
from items.consumables.barons_boon import BaronsBoon
from items.consumables.jewelers_boon import JewelersBoon
from items.consumables.miners_boon import MinersBoon
from items.consumables.clerics_boon import ClericsBoon
from items.consumables.jokers_boon import JokersBoon
from items.consumables.reapers_boon import ReapersBoon
from items.consumables.boon import Boon
from items.weapons.sword import Sword
from items.armor.leather_armor import LeatherArmor

def test_base_boon_class():
    """Test that the base Boon class has all required methods."""
    player = Player(5, 5)
    boon = Boon(0, 0, "Test Boon", description="Test boon")
    
    # Check that all required methods exist
    assert hasattr(boon, 'apply_enchantment_with_choice'), "Base Boon should have apply_enchantment_with_choice method"
    assert hasattr(boon, 'can_enchant_weapon'), "Base Boon should have can_enchant_weapon method"
    assert hasattr(boon, 'can_enchant_armor'), "Base Boon should have can_enchant_armor method"
    assert hasattr(boon, 'apply_to_weapon'), "Base Boon should have apply_to_weapon method"
    assert hasattr(boon, 'apply_to_armor'), "Base Boon should have apply_to_armor method"
    
    print("✓ Base Boon class has all required methods")

def test_boon_inheritance():
    """Test that all boon classes inherit from the base Boon class."""
    boon_classes = [BaronsBoon, JewelersBoon, MinersBoon, ClericsBoon, JokersBoon, ReapersBoon]
    
    for boon_class in boon_classes:
        boon = boon_class(0, 0)
        assert isinstance(boon, Boon), f"{boon_class.__name__} should inherit from Boon"
        
        # Check that all required methods are available
        assert hasattr(boon, 'apply_enchantment_with_choice'), f"{boon_class.__name__} should have apply_enchantment_with_choice method"
        assert hasattr(boon, 'can_enchant_weapon'), f"{boon_class.__name__} should have can_enchant_weapon method"
        assert hasattr(boon, 'can_enchant_armor'), f"{boon_class.__name__} should have can_enchant_armor method"
        assert hasattr(boon, 'apply_to_weapon'), f"{boon_class.__name__} should have apply_to_weapon method"
        assert hasattr(boon, 'apply_to_armor'), f"{boon_class.__name__} should have apply_to_armor method"
    
    print("✓ All boon classes inherit from base Boon class and have required methods")

def test_barons_boon_weapon_armor_choice():
    """Test that Baron's Boon can enchant both weapons and armor."""
    player = Player(5, 5)
    player.weapon = Sword(0, 0)
    player.armor = LeatherArmor(0, 0)
    
    barons_boon = BaronsBoon(0, 0)
    success, message = barons_boon.use(player)
    
    assert success, f"Baron's Boon should succeed when player has equipment: {message}"
    # Should have enchanted either weapon or armor
    weapon_enchanted = len(player.weapon.enchantments) > 0
    armor_enchanted = len(player.armor.enchantments) > 0
    assert weapon_enchanted or armor_enchanted, "Baron's Boon should enchant either weapon or armor"
    
    print("✓ Baron's Boon uses weapon/armor choice logic correctly")

def test_other_boons_use_choice_logic():
    """Test that other boons now use the choice logic from base class."""
    player = Player(5, 5)
    player.weapon = Sword(0, 0)
    player.armor = LeatherArmor(0, 0)
    
    choice_logic_boons = [JewelersBoon, MinersBoon, ClericsBoon, ReapersBoon]
    
    for boon_class in choice_logic_boons:
        # Reset enchantments
        player.weapon.enchantments = []
        player.armor.enchantments = []
        
        boon = boon_class(0, 0)
        success, message = boon.use(player)
        
        assert success, f"{boon_class.__name__} should succeed: {message}"
        # Should enchant either weapon or armor (default is weapon when both available)
        weapon_enchanted = len(player.weapon.enchantments) > 0
        armor_enchanted = len(player.armor.enchantments) > 0
        assert weapon_enchanted or armor_enchanted, f"{boon_class.__name__} should enchant something"
    
    print("✓ Boons use choice logic correctly")

def test_jokers_boon_random_enchantment():
    """Test that Joker's Boon applies a random enchantment with choice logic."""
    player = Player(5, 5)
    player.weapon = Sword(0, 0)
    player.armor = LeatherArmor(0, 0)
    
    jokers_boon = JokersBoon(0, 0)
    success, message = jokers_boon.use(player)
    
    assert success, f"Joker's Boon should succeed: {message}"
    # Should enchant either weapon or armor
    weapon_enchanted = len(player.weapon.enchantments) > 0
    armor_enchanted = len(player.armor.enchantments) > 0
    assert weapon_enchanted or armor_enchanted, "Joker's Boon should enchant something"
    assert "enchanted with" in message, "Joker's Boon should mention the enchantment name"
    
    print("✓ Joker's Boon applies random enchantments with choice logic correctly")

def test_boons_no_equipment_failure():
    """Test that boons fail appropriately when no equipment is available."""
    player = Player(5, 5)
    player.weapon = None  # No weapon equipped
    player.armor = None   # No armor equipped
    
    all_boons = [BaronsBoon, JewelersBoon, MinersBoon, ClericsBoon, ReapersBoon, JokersBoon]
    
    for boon_class in all_boons:
        boon = boon_class(0, 0)
        success, message = boon.use(player)
        
        assert not success, f"{boon_class.__name__} should fail when no equipment equipped"
        assert "equipped items" in message.lower() or "weapon equipped" in message.lower(), f"{boon_class.__name__} should mention needing equipment"
    
    print("✓ Boons fail correctly when no equipment is available")

if __name__ == "__main__":
    test_base_boon_class()
    test_boon_inheritance()
    test_barons_boon_weapon_armor_choice()
    test_other_boons_use_choice_logic()
    test_jokers_boon_random_enchantment()
    test_boons_no_equipment_failure()
    print("All boon base class tests passed!")