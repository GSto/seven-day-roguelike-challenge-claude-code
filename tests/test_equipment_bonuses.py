"""
Test that all equipment types can be created with evade, crit, and crit_multiplier bonuses.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from items.weapons import Weapon, Katana, Uchigatana, RiversOfBlood
from items.armor import Armor, NinjaSuit, AssassinLeathers, Cloak
from items.accessories import Accessory, ShadowRing, RingOfPrecision, BrutalityAmulet, AssassinsMask
from player import Player


def test_weapon_evade_crit_bonuses():
    """Test that weapons can be created with evade, crit, and crit_multiplier bonuses."""
    # Create a weapon with all bonuses
    weapon = Weapon(0, 0, "Test Weapon", ')', 5, "A test weapon", 
                   evade_bonus=0.05, crit_bonus=0.10, crit_multiplier_bonus=0.5)
    
    assert weapon.evade_bonus == 0.05
    assert weapon.crit_bonus == 0.10
    assert weapon.crit_multiplier_bonus == 0.5
    
    # Test existing weapons that use crit bonuses
    katana = Katana(0, 0)
    assert katana.crit_bonus == 0.25
    
    uchigatana = Uchigatana(0, 0)
    assert uchigatana.crit_bonus == 0.20
    
    rivers_of_blood = RiversOfBlood(0, 0)
    assert rivers_of_blood.crit_bonus == 0.20
    assert rivers_of_blood.crit_multiplier_bonus == 0.25
    
    print("✓ Weapons can be created with evade/crit bonuses")


def test_armor_evade_crit_bonuses():
    """Test that armor can be created with evade, crit, and crit_multiplier bonuses."""
    # Create armor with all bonuses
    armor = Armor(0, 0, "Test Armor", '[', 2, "Test armor",
                 evade_bonus=0.08, crit_bonus=0.05, crit_multiplier_bonus=0.3)
    
    assert armor.evade_bonus == 0.08
    assert armor.crit_bonus == 0.05
    assert armor.crit_multiplier_bonus == 0.3
    
    # Test specific armor types
    ninja_suit = NinjaSuit(0, 0)
    assert ninja_suit.evade_bonus == 0.15
    
    assassin_leathers = AssassinLeathers(0, 0)
    assert assassin_leathers.evade_bonus == 0.08
    assert assassin_leathers.crit_bonus == 0.12
    
    cloak = Cloak(0, 0)
    assert cloak.evade_bonus == 0.05
    
    print("✓ Armor can be created with evade/crit bonuses")


def test_accessory_evade_crit_bonuses():
    """Test that accessories can be created with evade, crit, and crit_multiplier bonuses."""
    # Create accessory with all bonuses
    accessory = Accessory(0, 0, "Test Accessory", '&', 1, 1, "Test accessory",
                         evade_bonus=0.06, crit_bonus=0.08, crit_multiplier_bonus=0.4)
    
    assert accessory.evade_bonus == 0.06
    assert accessory.crit_bonus == 0.08
    assert accessory.crit_multiplier_bonus == 0.4
    
    # Test specific accessory types
    shadow_ring = ShadowRing(0, 0)
    assert shadow_ring.evade_bonus == 0.10
    
    precision_ring = RingOfPrecision(0, 0)
    assert precision_ring.crit_bonus == 0.12
    
    brutality_amulet = BrutalityAmulet(0, 0)
    assert brutality_amulet.crit_multiplier_bonus == 0.5
    
    assassin_mask = AssassinsMask(0, 0)
    assert assassin_mask.evade_bonus == 0.08
    assert assassin_mask.crit_bonus == 0.08
    
    print("✓ Accessories can be created with evade/crit bonuses")


def test_equipment_bonuses_with_player():
    """Test that equipment bonuses are properly added to player stats."""
    player = Player(0, 0)
    
    # Check base stats
    base_evade = player.get_total_evade()
    base_crit = player.get_total_crit()
    base_crit_mult = player.get_total_crit_multiplier()
    
    # Equip items with bonuses
    katana = Katana(0, 0)  # +25% crit
    ninja_suit = NinjaSuit(0, 0)  # +15% evade
    shadow_ring = ShadowRing(0, 0)  # +10% evade
    
    player.weapon = katana
    player.armor = ninja_suit
    player.accessory = shadow_ring
    
    # Check that bonuses are applied
    total_evade = player.get_total_evade()
    total_crit = player.get_total_crit()
    
    assert total_evade > base_evade  # Should be higher due to ninja suit + ring
    assert total_crit > base_crit   # Should be higher due to katana
    
    # Check specific values (with caps)
    expected_evade = min(0.75, base_evade + 0.15 + 0.10)  # base + ninja_suit + ring
    expected_crit = min(0.75, base_crit + 0.25)           # base + katana
    
    assert total_evade == expected_evade
    assert total_crit == expected_crit
    
    print("✓ Equipment bonuses are properly applied to player stats")


def test_no_bonuses_default():
    """Test that equipment without specified bonuses defaults to 0."""
    # Create equipment without specifying bonuses
    weapon = Weapon(0, 0, "Plain Sword", ')', 5, "A plain sword")
    armor = Armor(0, 0, "Plain Armor", '[', 2, "Plain armor")
    accessory = Accessory(0, 0, "Plain Ring", '=', 0, 0, "A plain ring")
    
    # All should default to 0
    assert weapon.evade_bonus == 0.0
    assert weapon.crit_bonus == 0.0  
    assert weapon.crit_multiplier_bonus == 0.0
    
    assert armor.evade_bonus == 0.0
    assert armor.crit_bonus == 0.0
    assert armor.crit_multiplier_bonus == 0.0
    
    assert accessory.evade_bonus == 0.0
    assert accessory.crit_bonus == 0.0
    assert accessory.crit_multiplier_bonus == 0.0
    
    print("✓ Equipment defaults to 0 bonuses when not specified")


if __name__ == "__main__":
    print("Testing equipment evade/crit bonus arguments...")
    print()
    
    test_weapon_evade_crit_bonuses()
    test_armor_evade_crit_bonuses()
    test_accessory_evade_crit_bonuses()
    test_equipment_bonuses_with_player()
    test_no_bonuses_default()
    
    print()
    print("✅ All equipment bonus tests passed!")