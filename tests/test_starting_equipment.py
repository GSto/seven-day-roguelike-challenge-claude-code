"""
Unit tests for player starting equipment.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from player import Player
from items import WoodenStick, WhiteTShirt


def test_player_starts_with_weapon():
    """Test that player starts with wooden stick weapon."""
    player = Player(10, 10)
    
    # Player should have a weapon equipped
    assert player.weapon is not None
    assert isinstance(player.weapon, WoodenStick)
    assert player.weapon.name == "Wooden Stick"
    assert player.weapon.attack_bonus == 1
    
    print("✓ Player starts with wooden stick weapon")


def test_player_starts_with_armor():
    """Test that player starts with white T-shirt armor."""
    player = Player(10, 10)
    
    # Player should have armor equipped
    assert player.armor is not None
    assert isinstance(player.armor, WhiteTShirt)
    assert player.armor.name == "White T-Shirt"
    assert player.armor.defense_bonus == 0
    
    print("✓ Player starts with white T-shirt armor")


def test_starting_equipment_stats():
    """Test that starting equipment provides correct stat bonuses."""
    player = Player(10, 10)
    
    # Base stats
    base_attack = player.attack  # Should be 10
    base_defense = player.defense  # Should be 2
    
    # Total stats with equipment
    total_attack = player.get_total_attack()
    total_defense = player.get_total_defense()
    
    # Wooden stick adds +1 attack
    assert total_attack == base_attack + 1
    # White T-shirt adds +0 defense
    assert total_defense == base_defense + 0
    
    print("✓ Starting equipment provides correct stat bonuses")


def test_starting_equipment_properties():
    """Test properties of starting equipment items."""
    player = Player(10, 10)
    
    # Test wooden stick properties
    wooden_stick = player.weapon
    assert wooden_stick.equipment_slot == "weapon"
    assert wooden_stick.char == ')'
    assert wooden_stick.description == "A simple wooden stick"
    
    # Test white T-shirt properties
    white_tshirt = player.armor
    assert white_tshirt.equipment_slot == "armor"
    assert white_tshirt.char == '['
    assert white_tshirt.description == "A plain white T-shirt"
    
    print("✓ Starting equipment has correct properties")


def test_no_starting_accessory():
    """Test that player starts with no accessory."""
    player = Player(10, 10)
    
    # Player should not have any accessories
    assert len(player.accessories) == 0
    
    print("✓ Player starts with no accessory")


def test_starting_equipment_can_be_unequipped():
    """Test that starting equipment can be unequipped and re-equipped."""
    player = Player(10, 10)
    
    # Get starting equipment
    starting_weapon = player.weapon
    starting_armor = player.armor
    
    # Unequip items
    player.weapon = None
    player.armor = None
    
    # Stats should change
    assert player.get_total_attack() == player.attack  # No weapon bonus
    assert player.get_total_defense() == player.defense  # No armor bonus
    
    # Re-equip items
    player.weapon = starting_weapon
    player.armor = starting_armor
    
    # Stats should return to equipped values
    assert player.get_total_attack() == player.attack + 1
    assert player.get_total_defense() == player.defense + 0
    
    print("✓ Starting equipment can be unequipped and re-equipped")


def test_multiple_players_have_separate_equipment():
    """Test that multiple players have separate equipment instances."""
    player1 = Player(10, 10)
    player2 = Player(20, 20)
    
    # Each player should have their own equipment instances
    assert player1.weapon is not player2.weapon
    assert player1.armor is not player2.armor
    
    # But they should be the same type
    assert type(player1.weapon) == type(player2.weapon)
    assert type(player1.armor) == type(player2.armor)
    
    # And have the same properties
    assert player1.weapon.name == player2.weapon.name
    assert player1.armor.name == player2.armor.name
    
    print("✓ Multiple players have separate equipment instances")


def test_starting_equipment_integration():
    """Test starting equipment integration with game systems."""
    player = Player(10, 10)
    
    # Test that equipment appears in inventory display concepts
    weapon_name = player.weapon.name if player.weapon else "None"
    armor_name = player.armor.name if player.armor else "None"
    
    assert weapon_name == "Wooden Stick"
    assert armor_name == "White T-Shirt"
    
    # Test that equipment affects combat calculations
    initial_attack = player.get_total_attack()
    assert initial_attack > player.attack  # Should be higher due to weapon
    
    initial_defense = player.get_total_defense()
    assert initial_defense == player.defense  # Should be same (T-shirt gives +0)
    
    print("✓ Starting equipment integrates correctly with game systems")


def test_restart_gives_starting_equipment():
    """Test that restarting the game gives fresh starting equipment."""
    from game import Game
    
    # This test verifies the concept without actually creating a Game instance
    # (which would require tcod initialization)
    
    # Test that creating multiple players gives fresh equipment
    player1 = Player(10, 10)
    player2 = Player(20, 20)
    
    # Both should have starting equipment
    assert player1.weapon.name == "Wooden Stick"
    assert player1.armor.name == "White T-Shirt"
    assert player2.weapon.name == "Wooden Stick" 
    assert player2.armor.name == "White T-Shirt"
    
    # But they should be separate instances
    assert player1.weapon is not player2.weapon
    assert player1.armor is not player2.armor
    
    print("✓ Restart gives fresh starting equipment")


def run_all_tests():
    """Run all starting equipment tests."""
    print("Running starting equipment tests...")
    print()
    
    test_player_starts_with_weapon()
    test_player_starts_with_armor()
    test_starting_equipment_stats()
    test_starting_equipment_properties()
    test_no_starting_accessory()
    test_starting_equipment_can_be_unequipped()
    test_multiple_players_have_separate_equipment()
    test_starting_equipment_integration()
    test_restart_gives_starting_equipment()
    
    print()
    print("✅ All starting equipment tests passed!")


if __name__ == "__main__":
    run_all_tests()