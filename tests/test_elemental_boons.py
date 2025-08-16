"""
Test the new elemental boons that replace attack catalysts.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from player import Player
from items.boons import FireBoon, IceBoon, HolyBoon, DarkBoon
from items.weapons import Sword
from items.armor import LeatherArmor
from items.enchantments import EnchantmentType
from traits import Trait


def test_fire_boon_on_weapon():
    """Test that FireBoon applies Fire attack trait to weapon"""
    player = Player(5, 5)
    player.weapon = Sword(0, 0)
    player.armor = None
    
    fire_boon = FireBoon(0, 0)
    success, message = fire_boon.use(player)
    
    assert success, f"FireBoon should succeed, got: {message}"
    assert len(player.weapon.enchantments) == 1, "Weapon should have one enchantment"
    assert player.weapon.enchantments[0].type == EnchantmentType.FIRE, "Should be Fire enchantment"
    
    # Test that weapon now has Fire attack trait
    attack_traits = player.weapon.get_attack_traits()
    assert Trait.FIRE in attack_traits, f"Weapon should have Fire attack trait, got: {attack_traits}"


def test_fire_boon_on_armor():
    """Test that FireBoon applies Fire resistance to armor"""
    player = Player(5, 5)
    player.weapon = None
    player.armor = LeatherArmor(0, 0)
    
    fire_boon = FireBoon(0, 0)
    success, message = fire_boon.use(player)
    
    assert success, f"FireBoon should succeed, got: {message}"
    assert len(player.armor.enchantments) == 1, "Armor should have one enchantment"
    assert player.armor.enchantments[0].type == EnchantmentType.FIRE, "Should be Fire enchantment"
    
    # Test that armor now has Fire resistance
    resistances = player.armor.get_resistances()
    assert Trait.FIRE in resistances, f"Armor should have Fire resistance, got: {resistances}"


def test_ice_boon_on_weapon():
    """Test that IceBoon applies Ice attack trait to weapon"""
    player = Player(5, 5)
    player.weapon = Sword(0, 0)
    player.armor = None
    
    ice_boon = IceBoon(0, 0)
    success, message = ice_boon.use(player)
    
    assert success, f"IceBoon should succeed, got: {message}"
    assert len(player.weapon.enchantments) == 1, "Weapon should have one enchantment"
    assert player.weapon.enchantments[0].type == EnchantmentType.ICE, "Should be Ice enchantment"
    
    # Test that weapon now has Ice attack trait
    attack_traits = player.weapon.get_attack_traits()
    assert Trait.ICE in attack_traits, f"Weapon should have Ice attack trait, got: {attack_traits}"


def test_ice_boon_on_armor():
    """Test that IceBoon applies Ice resistance to armor"""
    player = Player(5, 5)
    player.weapon = None
    player.armor = LeatherArmor(0, 0)
    
    ice_boon = IceBoon(0, 0)
    success, message = ice_boon.use(player)
    
    assert success, f"IceBoon should succeed, got: {message}"
    assert len(player.armor.enchantments) == 1, "Armor should have one enchantment"
    assert player.armor.enchantments[0].type == EnchantmentType.ICE, "Should be Ice enchantment"
    
    # Test that armor now has Ice resistance
    resistances = player.armor.get_resistances()
    assert Trait.ICE in resistances, f"Armor should have Ice resistance, got: {resistances}"


def test_holy_boon_on_weapon():
    """Test that HolyBoon applies Holy attack trait to weapon"""
    player = Player(5, 5)
    player.weapon = Sword(0, 0)
    player.armor = None
    
    holy_boon = HolyBoon(0, 0)
    success, message = holy_boon.use(player)
    
    assert success, f"HolyBoon should succeed, got: {message}"
    assert len(player.weapon.enchantments) == 1, "Weapon should have one enchantment"
    assert player.weapon.enchantments[0].type == EnchantmentType.HOLY, "Should be Holy enchantment"
    
    # Test that weapon now has Holy attack trait
    attack_traits = player.weapon.get_attack_traits()
    assert Trait.HOLY in attack_traits, f"Weapon should have Holy attack trait, got: {attack_traits}"


def test_holy_boon_on_armor():
    """Test that HolyBoon applies Holy resistance to armor"""
    player = Player(5, 5)
    player.weapon = None
    player.armor = LeatherArmor(0, 0)
    
    holy_boon = HolyBoon(0, 0)
    success, message = holy_boon.use(player)
    
    assert success, f"HolyBoon should succeed, got: {message}"
    assert len(player.armor.enchantments) == 1, "Armor should have one enchantment"
    assert player.armor.enchantments[0].type == EnchantmentType.HOLY, "Should be Holy enchantment"
    
    # Test that armor now has Holy resistance
    resistances = player.armor.get_resistances()
    assert Trait.HOLY in resistances, f"Armor should have Holy resistance, got: {resistances}"


def test_dark_boon_on_weapon():
    """Test that DarkBoon applies Dark attack trait to weapon"""
    player = Player(5, 5)
    player.weapon = Sword(0, 0)
    player.armor = None
    
    dark_boon = DarkBoon(0, 0)
    success, message = dark_boon.use(player)
    
    assert success, f"DarkBoon should succeed, got: {message}"
    assert len(player.weapon.enchantments) == 1, "Weapon should have one enchantment"
    assert player.weapon.enchantments[0].type == EnchantmentType.DARK, "Should be Dark enchantment"
    
    # Test that weapon now has Dark attack trait
    attack_traits = player.weapon.get_attack_traits()
    assert Trait.DARK in attack_traits, f"Weapon should have Dark attack trait, got: {attack_traits}"


def test_dark_boon_on_armor():
    """Test that DarkBoon applies Dark resistance to armor"""
    player = Player(5, 5)
    player.weapon = None
    player.armor = LeatherArmor(0, 0)
    
    dark_boon = DarkBoon(0, 0)
    success, message = dark_boon.use(player)
    
    assert success, f"DarkBoon should succeed, got: {message}"
    assert len(player.armor.enchantments) == 1, "Armor should have one enchantment"
    assert player.armor.enchantments[0].type == EnchantmentType.DARK, "Should be Dark enchantment"
    
    # Test that armor now has Dark resistance
    resistances = player.armor.get_resistances()
    assert Trait.DARK in resistances, f"Armor should have Dark resistance, got: {resistances}"


def test_boon_prefers_weapon_when_both_available():
    """Test that boons prefer weapon when both weapon and armor are available"""
    player = Player(5, 5)
    player.weapon = Sword(0, 0)
    player.armor = LeatherArmor(0, 0)
    
    fire_boon = FireBoon(0, 0)
    success, message = fire_boon.use(player)
    
    assert success, f"FireBoon should succeed, got: {message}"
    assert len(player.weapon.enchantments) == 1, "Weapon should have one enchantment"
    assert len(player.armor.enchantments) == 0, "Armor should have no enchantments"
    assert player.weapon.enchantments[0].type == EnchantmentType.FIRE, "Should be Fire enchantment on weapon"


def test_boon_fails_when_no_equipment():
    """Test that boons fail when player has no equipment"""
    player = Player(5, 5)
    player.weapon = None
    player.armor = None
    
    fire_boon = FireBoon(0, 0)
    success, message = fire_boon.use(player)
    
    assert not success, "FireBoon should fail when no equipment available"
    assert "need equipped items" in message.lower(), f"Should mention need for equipment, got: {message}"


if __name__ == "__main__":
    print("Testing elemental boons...")
    
    test_fire_boon_on_weapon()
    print("✓ FireBoon on weapon works")
    
    test_fire_boon_on_armor()
    print("✓ FireBoon on armor works")
    
    test_ice_boon_on_weapon()
    print("✓ IceBoon on weapon works")
    
    test_ice_boon_on_armor()
    print("✓ IceBoon on armor works")
    
    test_holy_boon_on_weapon()
    print("✓ HolyBoon on weapon works")
    
    test_holy_boon_on_armor()
    print("✓ HolyBoon on armor works")
    
    test_dark_boon_on_weapon()
    print("✓ DarkBoon on weapon works")
    
    test_dark_boon_on_armor()
    print("✓ DarkBoon on armor works")
    
    test_boon_prefers_weapon_when_both_available()
    print("✓ Boon prefers weapon when both available")
    
    test_boon_fails_when_no_equipment()
    print("✓ Boon fails when no equipment")
    
    print("\nAll elemental boon tests passed! ✅")