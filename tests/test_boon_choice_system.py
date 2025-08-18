"""
Test cases for the boon choice system integration.
"""

import sys
sys.path.insert(0, 'src')

from player import Player
from items.consumables.barons_boon import BaronsBoon
from items.consumables.fire_boon import FireBoon
from items.consumables.jokers_boon import JokersBoon
from enchantments import EnchantmentType
from game import Game
import tcod.event


class MockContext:
    """Mock context for testing"""
    def __init__(self):
        pass
    
    def present(self, console):
        pass


def test_boon_triggers_choice_when_both_eligible():
    """Test that using a boon triggers choice state when both weapon and armor are eligible"""
    # Create a mock game
    game = Game()
    game.game_state = 'INVENTORY'
    
    # Add a boon to player inventory
    boon = BaronsBoon(0, 0)
    game.player.add_item(boon)
    
    # Both weapon and armor should be eligible for SHINY enchantment
    assert len(game.player.weapon.enchantments) == 0
    assert len(game.player.armor.enchantments) == 0
    
    # Use the boon
    game.use_inventory_item(0)  # Use first item (the boon)
    
    # Should trigger choice state
    assert game.game_state == 'BOON_CHOICE'
    assert game.pending_boon_item == boon
    assert game.pending_boon_enchantment == EnchantmentType.SHINY
    assert boon in game.player.inventory  # Boon should still be in inventory until choice is made


def test_boon_weapon_choice_works():
    """Test that choosing weapon applies enchantment correctly"""
    game = Game()
    game.game_state = 'BOON_CHOICE'
    
    # Set up pending boon state
    boon = BaronsBoon(0, 0)
    game.player.add_item(boon)
    game.pending_boon_item = boon
    game.pending_boon_enchantment = EnchantmentType.SHINY
    
    # Simulate pressing 'w' for weapon
    event = tcod.event.KeyDown(sym=ord('w'), scancode=0, mod=0)
    game.handle_keydown(event)
    
    # Should apply to weapon and return to inventory
    assert game.game_state == 'INVENTORY'
    assert len(game.player.weapon.enchantments) == 1
    assert game.player.weapon.enchantments[0].type == EnchantmentType.SHINY
    assert len(game.player.armor.enchantments) == 0
    assert boon not in game.player.inventory  # Boon should be consumed
    assert game.pending_boon_item is None
    assert game.pending_boon_enchantment is None


def test_boon_armor_choice_works():
    """Test that choosing armor applies enchantment correctly"""
    game = Game()
    game.game_state = 'BOON_CHOICE'
    
    # Set up pending boon state
    boon = FireBoon(0, 0)  # Fire boon can go on armor for resistance
    game.player.add_item(boon)
    game.pending_boon_item = boon
    game.pending_boon_enchantment = EnchantmentType.FIRE
    
    # Simulate pressing 'a' for armor
    event = tcod.event.KeyDown(sym=ord('a'), scancode=0, mod=0)
    game.handle_keydown(event)
    
    # Should apply to armor and return to inventory
    assert game.game_state == 'INVENTORY'
    assert len(game.player.armor.enchantments) == 1
    assert game.player.armor.enchantments[0].type == EnchantmentType.FIRE
    assert len(game.player.weapon.enchantments) == 0
    assert boon not in game.player.inventory  # Boon should be consumed
    assert game.pending_boon_item is None
    assert game.pending_boon_enchantment is None


def test_boon_choice_cancellation():
    """Test that ESC cancels the boon choice"""
    game = Game()
    game.game_state = 'BOON_CHOICE'
    
    # Set up pending boon state
    boon = BaronsBoon(0, 0)
    game.player.add_item(boon)
    game.pending_boon_item = boon
    game.pending_boon_enchantment = EnchantmentType.SHINY
    
    # Simulate pressing ESC
    event = tcod.event.KeyDown(sym=tcod.event.KeySym.ESCAPE, scancode=0, mod=0)
    game.handle_keydown(event)
    
    # Should cancel and return to inventory
    assert game.game_state == 'INVENTORY'
    assert len(game.player.weapon.enchantments) == 0
    assert len(game.player.armor.enchantments) == 0
    assert boon in game.player.inventory  # Boon should still be in inventory
    assert game.pending_boon_item is None
    assert game.pending_boon_enchantment is None


def test_boon_automatic_choice_when_only_weapon_eligible():
    """Test that boon applies automatically when only weapon is eligible"""
    game = Game()
    game.game_state = 'INVENTORY'
    
    # Fill armor with enchantments so it can't be further enchanted
    from enchantments import get_armor_enchantment_by_type
    enchant1 = get_armor_enchantment_by_type(EnchantmentType.FIRE)
    enchant2 = get_armor_enchantment_by_type(EnchantmentType.ICE)
    game.player.armor.add_enchantment(enchant1)
    game.player.armor.add_enchantment(enchant2)
    
    # Add a boon
    boon = BaronsBoon(0, 0)
    game.player.add_item(boon)
    
    # Use the boon
    game.use_inventory_item(0)
    
    # Should apply automatically to weapon, no choice needed
    assert game.game_state == 'INVENTORY'  # Should stay in inventory, no choice state
    assert len(game.player.weapon.enchantments) == 1
    assert game.player.weapon.enchantments[0].type == EnchantmentType.SHINY
    assert boon not in game.player.inventory  # Boon should be consumed


def test_boon_automatic_choice_when_only_armor_eligible():
    """Test that boon applies automatically when only armor is eligible"""
    game = Game()
    game.game_state = 'INVENTORY'
    
    # Fill weapon with enchantments so it can't be further enchanted
    from enchantments import get_weapon_enchantment_by_type
    enchant1 = get_weapon_enchantment_by_type(EnchantmentType.FIRE)
    enchant2 = get_weapon_enchantment_by_type(EnchantmentType.ICE)
    game.player.weapon.add_enchantment(enchant1)
    game.player.weapon.add_enchantment(enchant2)
    
    # Add a boon
    boon = BaronsBoon(0, 0)
    game.player.add_item(boon)
    
    # Use the boon
    game.use_inventory_item(0)
    
    # Should apply automatically to armor, no choice needed
    assert game.game_state == 'INVENTORY'  # Should stay in inventory, no choice state
    assert len(game.player.armor.enchantments) == 1
    assert game.player.armor.enchantments[0].type == EnchantmentType.SHINY
    assert boon not in game.player.inventory  # Boon should be consumed


def test_jokers_boon_choice_system():
    """Test that Joker's Boon also works with the choice system"""
    game = Game()
    game.game_state = 'INVENTORY'
    
    # Add Joker's Boon
    boon = JokersBoon(0, 0)
    game.player.add_item(boon)
    
    # Use the boon
    game.use_inventory_item(0)
    
    # Should trigger choice state (assuming random enchantment can go on both)
    # This test might occasionally fail if random picks an enchantment that can only go on one item
    # but it should work most of the time
    if game.game_state == 'BOON_CHOICE':
        # Choice was triggered - test weapon selection
        event = tcod.event.KeyDown(sym=ord('w'), scancode=0, mod=0)
        game.handle_keydown(event)
        
        assert game.game_state == 'INVENTORY'
        assert len(game.player.weapon.enchantments) == 1
        assert boon not in game.player.inventory
    else:
        # Automatic application happened - verify one item was enchanted
        total_enchantments = len(game.player.weapon.enchantments) + len(game.player.armor.enchantments)
        assert total_enchantments == 1
        assert boon not in game.player.inventory


def test_case_insensitive_keys():
    """Test that both upper and lower case W/A work"""
    # Create a mock event class that directly tests key handling
    class MockEvent:
        def __init__(self, key):
            self.sym = key
    
    # Test uppercase W
    game = Game()
    game.game_state = 'BOON_CHOICE'
    boon = BaronsBoon(0, 0)
    game.player.add_item(boon)
    game.pending_boon_item = boon
    game.pending_boon_enchantment = EnchantmentType.SHINY
    
    # Directly test key handling logic by calling with key value
    game.handle_keydown(MockEvent(ord('W')))
    
    assert len(game.player.weapon.enchantments) == 1
    
    # Test uppercase A (reset game state)
    game = Game()
    game.game_state = 'BOON_CHOICE'
    boon = BaronsBoon(0, 0)
    game.player.add_item(boon)
    game.pending_boon_item = boon
    game.pending_boon_enchantment = EnchantmentType.SHINY
    
    game.handle_keydown(MockEvent(ord('A')))
    
    assert len(game.player.armor.enchantments) == 1


if __name__ == "__main__":
    test_boon_triggers_choice_when_both_eligible()
    test_boon_weapon_choice_works()
    test_boon_armor_choice_works()
    test_boon_choice_cancellation()
    test_boon_automatic_choice_when_only_weapon_eligible()
    test_boon_automatic_choice_when_only_armor_eligible()
    test_jokers_boon_choice_system()
    test_case_insensitive_keys()
    print("All boon choice system tests passed!")