"""
Test the new player multiplier system including attack_multiplier, defense_multiplier, and xp_multiplier.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from player import Player
from items import (BaronCatalyst, WardenCatalyst, JewelerCatalyst, 
                   WoodenStick, WhiteTShirt, PowerRing)
from items.base import Equipment


def test_player_default_multipliers():
    """Test that player starts with default multiplier values of 1.0"""
    player = Player(5, 5)
    
    assert player.attack_multiplier == 1.0
    assert player.defense_multiplier == 1.0
    assert player.xp_multiplier == 1.0


def test_multiplier_calculations():
    """Test that multipliers are applied correctly to attack, defense, and XP calculations"""
    player = Player(5, 5)
    base_attack = player.attack
    base_defense = player.defense
    
    # Test base calculations (should be unchanged with 1.0 multipliers)
    assert player.get_total_attack() == base_attack + player.weapon.attack_bonus
    assert player.get_total_defense() == base_defense + player.armor.defense_bonus
    
    # Test XP gain with base multiplier
    initial_xp = player.xp
    player.gain_xp(100)
    assert player.xp == initial_xp + 100
    
    # Test with modified multipliers
    player.attack_multiplier = 1.5
    player.defense_multiplier = 2.0
    player.xp_multiplier = 1.2
    
    expected_attack = int((base_attack + player.weapon.attack_bonus) * 1.5)
    expected_defense = int((base_defense + player.armor.defense_bonus) * 2.0)
    
    assert player.get_total_attack() == expected_attack
    assert player.get_total_defense() == expected_defense
    
    # Test XP gain with modified multiplier
    initial_xp = player.xp
    player.gain_xp(100)
    assert player.xp == initial_xp + int(100 * 1.2)


def test_equipment_multiplier_bonuses():
    """Test that equipment can provide multiplier bonuses"""
    player = Player(5, 5)
    
    # Create equipment with multiplier bonuses
    magic_weapon = Equipment(
        0, 0, "Magic Sword", '/', (255, 255, 255), 
        "A magical sword that enhances combat prowess",
        attack_bonus=5, equipment_slot="weapon",
        attack_multiplier_bonus=0.2, defense_multiplier_bonus=0.1, xp_multiplier_bonus=0.3
    )
    
    magic_armor = Equipment(
        0, 0, "Magic Armor", '[', (200, 200, 200),
        "Magical armor that enhances defenses", 
        defense_bonus=3, equipment_slot="armor",
        defense_multiplier_bonus=0.15
    )
    
    # Equip the magical items
    player.weapon = magic_weapon
    player.armor = magic_armor
    
    # Test that total multipliers include equipment bonuses
    assert player.get_total_attack_multiplier() == 1.0 + 0.2  # base + weapon bonus
    assert player.get_total_defense_multiplier() == 1.0 + 0.1 + 0.15  # base + weapon + armor
    assert player.get_total_xp_multiplier() == 1.0 + 0.3  # base + weapon bonus
    
    # Test that calculations use total multipliers
    base_attack = player.attack + magic_weapon.attack_bonus
    base_defense = player.defense + magic_armor.defense_bonus
    
    expected_attack = int(base_attack * (1.0 + 0.2))
    expected_defense = int(base_defense * (1.0 + 0.1 + 0.15))
    
    assert player.get_total_attack() == expected_attack
    assert player.get_total_defense() == expected_defense
    
    # Test XP gain with equipment bonus
    initial_xp = player.xp
    player.gain_xp(100)
    expected_xp_gain = int(100 * (1.0 + 0.3))
    assert player.xp == initial_xp + expected_xp_gain


def test_damage_calculation_with_multipliers():
    """Test that damage calculation uses the total defense including multipliers"""
    player = Player(5, 5)
    base_defense = player.get_total_defense()  # Should include equipment
    
    # Take damage with base multipliers
    damage_taken = player.take_damage(10)
    expected_damage = max(1, 10 - base_defense)
    assert damage_taken == expected_damage
    
    # Reset health and modify defense multiplier
    player.hp = player.max_hp
    player.defense_multiplier = 2.0
    
    new_total_defense = player.get_total_defense()
    damage_taken = player.take_damage(10)
    expected_damage = max(1, 10 - new_total_defense)
    assert damage_taken == expected_damage


def test_multiplier_stacking():
    """Test that player base multipliers and equipment multiplier bonuses stack correctly"""
    player = Player(5, 5)
    
    # Modify player base multipliers
    player.attack_multiplier = 1.3
    player.defense_multiplier = 1.4
    player.xp_multiplier = 1.5
    
    # Create equipment with bonuses
    equipment = Equipment(
        0, 0, "Stacking Item", '*', (255, 255, 255),
        attack_multiplier_bonus=0.2,
        defense_multiplier_bonus=0.3,
        xp_multiplier_bonus=0.1
    )
    player.weapon = equipment
    
    # Test that they stack additively
    assert player.get_total_attack_multiplier() == 1.3 + 0.2  # 1.5
    assert player.get_total_defense_multiplier() == 1.4 + 0.3  # 1.7
    assert player.get_total_xp_multiplier() == 1.5 + 0.1  # 1.6


if __name__ == "__main__":
    # Run all tests
    test_player_default_multipliers()
    print("✓ test_player_default_multipliers passed")
    
    test_multiplier_calculations()
    print("✓ test_multiplier_calculations passed")
    
    test_equipment_multiplier_bonuses()
    print("✓ test_equipment_multiplier_bonuses passed")
    
    test_consumable_multiplier_effects()
    print("✓ test_consumable_multiplier_effects passed")
    
    test_damage_calculation_with_multipliers()
    print("✓ test_damage_calculation_with_multipliers passed")
    
    test_multiplier_stacking()
    print("✓ test_multiplier_stacking passed")
    
    print("\nAll tests passed! ✅")