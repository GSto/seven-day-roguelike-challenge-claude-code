"""
Tests for the new items implemented from plans/new_items.md
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from player import Player
from items.consumables import PowerCatalyst, DefenseCatalyst, D6
from items.weapons import BrightSword, ClericsStaff
from items.armor import SpikedArmor


def test_power_catalyst():
    """Test that Power Catalyst permanently increases attack."""
    player = Player(5, 5)
    catalyst = PowerCatalyst(0, 0)
    
    initial_attack = player.attack
    result = catalyst.use(player)
    
    assert result == True, "Power Catalyst should be usable"
    assert player.attack == initial_attack + 1, f"Expected attack {initial_attack + 1}, got {player.attack}"
    print("✓ Power Catalyst increases attack by 1")


def test_defense_catalyst():
    """Test that Defense Catalyst permanently increases defense."""
    player = Player(5, 5)
    catalyst = DefenseCatalyst(0, 0)
    
    initial_defense = player.defense
    result = catalyst.use(player)
    
    assert result == True, "Defense Catalyst should be usable"
    assert player.defense == initial_defense + 1, f"Expected defense {initial_defense + 1}, got {player.defense}"
    print("✓ Defense Catalyst increases defense by 1")


def test_d6_effects():
    """Test that D6 provides one of the expected random effects."""
    import random
    
    # Test multiple rolls to see different effects
    effects_seen = set()
    for i in range(50):  # Run enough tests to likely see all effects
        player = Player(5, 5)
        d6 = D6(0, 0)
        
        # Store initial values
        initial_attack = player.attack
        initial_defense = player.defense
        initial_max_hp = player.max_hp
        initial_fov = player.fov
        initial_hp = player.hp
        
        result = d6.use(player)
        assert result == True, "D6 should always be usable"
        
        # Check which effect occurred
        if player.attack > initial_attack:
            effects_seen.add("attack_boost")
        elif player.defense > initial_defense:
            effects_seen.add("defense_boost")
        elif player.max_hp > initial_max_hp:
            effects_seen.add("hp_boost")
            # Should also heal when max HP increases
            assert player.hp > initial_hp, "HP should increase when max HP increases"
        elif player.fov > initial_fov:
            effects_seen.add("fov_boost")
        elif player.max_hp < initial_max_hp:
            effects_seen.add("hp_penalty")
            # HP should be capped to max HP
            assert player.hp <= player.max_hp, "HP should not exceed max HP"
    
    # We should see at least some different effects over 50 rolls
    assert len(effects_seen) >= 3, f"Expected to see multiple effects, only saw: {effects_seen}"
    print("✓ D6 provides various random effects")


def test_bright_sword():
    """Test that Bright Sword provides attack and FOV bonuses."""
    player = Player(5, 5)
    sword = BrightSword(0, 0)
    
    # Check sword attributes
    assert sword.attack_bonus == 6, f"Expected attack bonus 6, got {sword.attack_bonus}"
    assert sword.fov_bonus == 3, f"Expected FOV bonus 3, got {sword.fov_bonus}"
    
    # Test when equipped (replace the starting weapon)
    base_attack_raw = player.attack  # Raw attack without weapon
    base_fov = player.get_total_fov()
    
    player.weapon = sword
    
    total_attack = player.get_total_attack()
    total_fov = player.get_total_fov()
    
    # Total attack should be base + sword bonus
    expected_attack = base_attack_raw + sword.attack_bonus
    assert total_attack == expected_attack, f"Expected total attack {expected_attack}, got {total_attack}"
    assert total_fov == base_fov + 3, f"Expected total FOV {base_fov + 3}, got {total_fov}"
    print("✓ Bright Sword provides +6 attack and +3 FOV")


def test_clerics_staff():
    """Test that Cleric's Staff provides attack and health aspect bonuses."""
    player = Player(5, 5)
    staff = ClericsStaff(0, 0)
    
    # Check staff attributes
    assert staff.attack_bonus == 4, f"Expected attack bonus 4, got {staff.attack_bonus}"
    assert staff.health_aspect_bonus == 0.2, f"Expected health aspect bonus 0.2, got {staff.health_aspect_bonus}"
    
    # Test when equipped (replace the starting weapon)
    base_attack_raw = player.attack  # Raw attack without weapon
    base_health_aspect = player.get_total_health_aspect()
    
    player.weapon = staff
    
    total_attack = player.get_total_attack()
    total_health_aspect = player.get_total_health_aspect()
    
    # Total attack should be base + staff bonus
    expected_attack = base_attack_raw + staff.attack_bonus
    assert total_attack == expected_attack, f"Expected total attack {expected_attack}, got {total_attack}"
    assert abs(total_health_aspect - (base_health_aspect + 0.2)) < 0.001, f"Expected total health aspect {base_health_aspect + 0.2}, got {total_health_aspect}"
    print("✓ Cleric's Staff provides +4 attack and +0.2 health aspect")


def test_spiked_armor():
    """Test that Spiked Armor provides defense and attack bonuses."""
    player = Player(5, 5)
    armor = SpikedArmor(0, 0)
    
    # Check armor attributes
    assert armor.defense_bonus == 4, f"Expected defense bonus 4, got {armor.defense_bonus}"
    assert armor.attack_bonus == 2, f"Expected attack bonus 2, got {armor.attack_bonus}"
    
    # Test when equipped (replace the starting armor)
    base_defense_raw = player.defense  # Raw defense without armor
    base_attack_raw = player.attack    # Raw attack without armor
    
    player.armor = armor
    
    total_defense = player.get_total_defense()
    total_attack = player.get_total_attack()
    
    # Total defense should be base + armor bonus
    expected_defense = base_defense_raw + armor.defense_bonus
    # Total attack should include starting weapon (+1) + armor bonus (+2)
    expected_attack = base_attack_raw + 1 + armor.attack_bonus
    
    assert total_defense == expected_defense, f"Expected total defense {expected_defense}, got {total_defense}"
    assert total_attack == expected_attack, f"Expected total attack {expected_attack}, got {total_attack}"
    print("✓ Spiked Armor provides +4 defense and +2 attack")


def test_new_items_attributes():
    """Test that all new items have correct basic attributes."""
    # Test consumables
    power_catalyst = PowerCatalyst(0, 0)
    assert power_catalyst.name == "Power Catalyst"
    assert power_catalyst.char == '*'
    
    defense_catalyst = DefenseCatalyst(0, 0)
    assert defense_catalyst.name == "Defense Catalyst"
    assert defense_catalyst.char == '*'
    
    d6 = D6(0, 0)
    assert d6.name == "D6"
    assert d6.char == '6'
    
    # Test weapons
    bright_sword = BrightSword(0, 0)
    assert bright_sword.name == "Bright Sword"
    assert bright_sword.equipment_slot == "weapon"
    
    clerics_staff = ClericsStaff(0, 0)
    assert clerics_staff.name == "Cleric's Staff"
    assert clerics_staff.equipment_slot == "weapon"
    
    # Test armor
    spiked_armor = SpikedArmor(0, 0)
    assert spiked_armor.name == "Spiked Armor"
    assert spiked_armor.equipment_slot == "armor"
    
    print("✓ All new items have correct basic attributes")


def test_d6_hp_penalty_safety():
    """Test that D6's HP penalty doesn't kill the player."""
    player = Player(5, 5)
    player.max_hp = 25  # Set to minimum safe threshold
    player.hp = 25
    
    d6 = D6(0, 0)
    
    # Force the HP penalty effect (this is a bit hacky but ensures we test the safety)
    import random
    original_randint = random.randint
    
    def mock_randint(a, b):
        return 5  # Force the HP penalty effect
    
    random.randint = mock_randint
    
    try:
        result = d6.use(player)
        # With max_hp = 25, the HP penalty should not trigger
        assert player.max_hp == 25, "HP penalty should not trigger when max_hp <= 25"
        assert result == True, "D6 should still be usable"
    finally:
        random.randint = original_randint
    
    print("✓ D6 HP penalty has safety mechanism")


if __name__ == "__main__":
    test_power_catalyst()
    test_defense_catalyst() 
    test_d6_effects()
    test_bright_sword()
    test_clerics_staff()
    test_spiked_armor()
    test_new_items_attributes()
    test_d6_hp_penalty_safety()
    print("✅ All new item tests passed!")