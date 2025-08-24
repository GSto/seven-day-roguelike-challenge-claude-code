"""Test that enchantment modifiers are properly capitalized."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from items.weapons.dagger import Dagger
from items.armor.leather_armor import LeatherArmor
from enchantments import get_weapon_enchantment_by_type, get_armor_enchantment_by_type
from enchantments.enchantment_type import EnchantmentType

def test_weapon_enchantment_capitalized():
    """Test that weapon enchantments are capitalized in display name."""
    weapon = Dagger(0, 0)
    
    # Add fire enchantment (displayed as 'flaming')
    fire = get_weapon_enchantment_by_type(EnchantmentType.FIRE)
    weapon.add_enchantment(fire)
    
    # Check that 'flaming' is capitalized to 'Flaming'
    assert "Flaming" in weapon.name, f"Expected 'Flaming' in name, got: {weapon.name}"
    assert "flaming" not in weapon.name, f"Lowercase 'flaming' found in name: {weapon.name}"

def test_multiple_weapon_enchantments_capitalized():
    """Test that multiple weapon enchantments are all capitalized."""
    weapon = Dagger(0, 0)
    
    # Add fire and ice enchantments (displayed as 'flaming' and 'chilling')
    fire = get_weapon_enchantment_by_type(EnchantmentType.FIRE)
    ice = get_weapon_enchantment_by_type(EnchantmentType.ICE)
    weapon.add_enchantment(fire)
    weapon.add_enchantment(ice)
    
    # Check that both are capitalized
    assert "Flaming" in weapon.name, f"Expected 'Flaming' in name, got: {weapon.name}"
    assert "Chilling" in weapon.name, f"Expected 'Chilling' in name, got: {weapon.name}"
    assert "flaming" not in weapon.name, f"Lowercase 'flaming' found in name: {weapon.name}"
    assert "chilling" not in weapon.name, f"Lowercase 'chilling' found in name: {weapon.name}"

def test_armor_enchantment_capitalized():
    """Test that armor enchantments are capitalized in display name."""
    armor = LeatherArmor(0, 0)
    
    # Add blessed enchantment
    blessed = get_armor_enchantment_by_type(EnchantmentType.BLESSED)
    armor.add_enchantment(blessed)
    
    # Check that 'blessed' is capitalized to 'Blessed'
    assert "Blessed" in armor.name, f"Expected 'Blessed' in name, got: {armor.name}"
    assert "blessed" not in armor.name.replace("Blessed", ""), f"Lowercase 'blessed' found in name: {armor.name}"

def test_multiple_armor_enchantments_capitalized():
    """Test that multiple armor enchantments are all capitalized."""
    armor = LeatherArmor(0, 0)
    
    # Add blessed and shadow enchantments
    blessed = get_armor_enchantment_by_type(EnchantmentType.BLESSED)
    shadow = get_armor_enchantment_by_type(EnchantmentType.SHADOW)
    armor.add_enchantment(blessed)
    armor.add_enchantment(shadow)
    
    # Check that both are capitalized
    assert "Blessed" in armor.name, f"Expected 'Blessed' in name, got: {armor.name}"
    assert "Shadow" in armor.name, f"Expected 'Shadow' in name, got: {armor.name}"
    assert "blessed" not in armor.name.replace("Blessed", ""), f"Lowercase 'blessed' found in name: {armor.name}"
    assert "shadow" not in armor.name.replace("Shadow", ""), f"Lowercase 'shadow' found in name: {armor.name}"

if __name__ == "__main__":
    test_weapon_enchantment_capitalized()
    test_multiple_weapon_enchantments_capitalized()
    test_armor_enchantment_capitalized()
    test_multiple_armor_enchantments_capitalized()
    print("All tests passed!")