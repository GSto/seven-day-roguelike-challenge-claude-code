"""
Test cases for Transmutation consumable.
"""

import sys
sys.path.insert(0, 'src')

from player import Player
from items.consumables.transmutation import Transmutation
from items.armor.leather_armor import LeatherArmor
from items.armor.chain_mail import ChainMail
from items.consumables.shell_potion import ShellPotion


def test_transmutation_converts_unequipped_armor():
    """Test that Transmutation converts unequipped armor to shield potions"""
    player = Player(5, 5)
    
    # Add some armor to inventory (not equipped)
    leather_armor = LeatherArmor(0, 0)
    chain_mail = ChainMail(0, 0)
    player.add_item(leather_armor)
    player.add_item(chain_mail)
    
    # Verify initial state
    assert len(player.inventory) == 2
    assert leather_armor in player.inventory
    assert chain_mail in player.inventory
    
    # Use transmutation
    transmutation = Transmutation(0, 0)
    success, message = transmutation.use(player)
    
    # Verify success
    assert success == True
    assert "2 pieces of armor transform into protective potions!" in message
    
    # Verify armor is removed and shield potions are added
    assert leather_armor not in player.inventory
    assert chain_mail not in player.inventory
    assert len(player.inventory) == 2  # Same count, but now potions
    
    # Check that all items are shield potions
    shield_potions = [item for item in player.inventory if isinstance(item, ShellPotion)]
    assert len(shield_potions) == 2


def test_transmutation_ignores_equipped_armor():
    """Test that Transmutation does not convert equipped armor"""
    player = Player(5, 5)
    
    # Add armor to inventory
    leather_armor = LeatherArmor(0, 0)
    player.add_item(leather_armor)
    
    # Current equipped armor should not be converted
    equipped_armor = player.armor
    
    # Use transmutation
    transmutation = Transmutation(0, 0)
    success, message = transmutation.use(player)
    
    # Verify success
    assert success == True
    assert f"Your {leather_armor.name} transforms into a protective potion!" in message
    
    # Verify equipped armor is still equipped
    assert player.armor == equipped_armor
    assert equipped_armor not in player.inventory  # It's equipped, not in inventory
    
    # Verify unequipped armor is converted
    assert leather_armor not in player.inventory
    shield_potions = [item for item in player.inventory if isinstance(item, ShellPotion)]
    assert len(shield_potions) == 1


def test_transmutation_no_armor_to_convert():
    """Test that Transmutation fails when no unequipped armor is available"""
    player = Player(5, 5)
    
    # Don't add any armor to inventory (only equipped armor exists)
    
    # Use transmutation
    transmutation = Transmutation(0, 0)
    success, message = transmutation.use(player)
    
    # Verify failure
    assert success == False
    assert "You have no unequipped armor to transmute!" in message
    
    # Verify inventory is unchanged
    assert len(player.inventory) == 0


def test_transmutation_single_armor_conversion():
    """Test that Transmutation handles single armor piece correctly"""
    player = Player(5, 5)
    
    # Add single armor to inventory
    leather_armor = LeatherArmor(0, 0)
    player.add_item(leather_armor)
    
    # Use transmutation
    transmutation = Transmutation(0, 0)
    success, message = transmutation.use(player)
    
    # Verify success with singular message
    assert success == True
    assert f"Your {leather_armor.name} transforms into a protective potion!" in message
    
    # Verify conversion
    assert leather_armor not in player.inventory
    shield_potions = [item for item in player.inventory if isinstance(item, ShellPotion)]
    assert len(shield_potions) == 1


if __name__ == "__main__":
    test_transmutation_converts_unequipped_armor()
    test_transmutation_ignores_equipped_armor()
    test_transmutation_no_armor_to_convert()
    test_transmutation_single_armor_conversion()
    print("All Transmutation tests passed!")