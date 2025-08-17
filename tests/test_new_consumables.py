"""
Test cases for all newly implemented consumables.
"""

import sys
sys.path.insert(0, 'src')
import numpy as np

from player import Player
from items.consumables import Map, Compass, Bomb, SwordsToPlowshares
from items.weapons import WoodenStick
from items.foods import HealthPotion, ShellPotion
from monster import Monster
from constants import COLOR_RED, MAP_WIDTH, MAP_HEIGHT


class MockLevel:
    """Mock level for testing consumables that need level access"""
    
    def __init__(self):
        self.explored = np.full((MAP_WIDTH, MAP_HEIGHT), False, dtype=bool)
        self.fov = np.full((MAP_WIDTH, MAP_HEIGHT), False, dtype=bool)
        self.monsters = []
        self.items = []
    
    def remove_dead_monsters(self):
        """Remove dead monsters from the list"""
        self.monsters = [monster for monster in self.monsters if monster.is_alive()]


def test_map_reveals_entire_floor():
    """Test that Map consumable reveals the entire floor"""
    player = Player(5, 5)
    mock_level = MockLevel()
    player._current_level = mock_level
    
    # Initially no tiles are explored
    assert not np.any(mock_level.explored)
    
    # Use map
    map_item = Map(0, 0)
    success, message = map_item.use(player)
    
    # Verify success
    assert success == True
    assert "The entire floor layout is revealed!" in message
    
    # Verify all tiles are now explored
    assert np.all(mock_level.explored)


def test_map_fails_without_level():
    """Test that Map fails when player has no current level"""
    player = Player(5, 5)
    # Don't set _current_level
    
    map_item = Map(0, 0)
    success, message = map_item.use(player)
    
    assert success == False
    assert "Unable to reveal map - no floor detected!" in message


def test_compass_reveals_all_items():
    """Test that Compass makes all items visible"""
    player = Player(5, 5)
    mock_level = MockLevel()
    player._current_level = mock_level
    
    # Add some items to the level
    item1 = HealthPotion(10, 10)
    item2 = WoodenStick(15, 15)
    mock_level.items = [item1, item2]
    
    # Initially items are not visible in FOV
    assert not mock_level.fov[10, 10]
    assert not mock_level.fov[15, 15]
    
    # Use compass
    compass = Compass(0, 0)
    success, message = compass.use(player)
    
    # Verify success
    assert success == True
    assert "2 items are now visible on this floor!" in message
    
    # Verify item positions are now visible in FOV
    assert mock_level.fov[10, 10]
    assert mock_level.fov[15, 15]
    
    # Verify compass has charges
    assert compass.charges == 2  # Started with 3, used 1


def test_compass_handles_no_items():
    """Test that Compass handles floors with no items"""
    player = Player(5, 5)
    mock_level = MockLevel()
    player._current_level = mock_level
    # No items on the level
    
    compass = Compass(0, 0)
    success, message = compass.use(player)
    
    assert success == True
    assert "No items detected on this floor." in message


def test_bomb_damages_nearby_enemies():
    """Test that Bomb damages enemies within radius"""
    player = Player(5, 5)
    mock_level = MockLevel()
    player._current_level = mock_level
    
    # Add monsters at various distances
    close_monster = Monster(6, 6, "Goblin", 'g', COLOR_RED, 25, 3, 1, 5)  # Distance ~1.4
    far_monster = Monster(20, 20, "Orc", 'o', COLOR_RED, 30, 4, 2, 10)   # Distance ~21
    edge_monster = Monster(8, 5, "Rat", 'r', COLOR_RED, 10, 2, 0, 2)     # Distance = 3
    
    mock_level.monsters = [close_monster, far_monster, edge_monster]
    
    # Use bomb
    bomb = Bomb(0, 0)
    success, message = bomb.use(player)
    
    # Verify success
    assert success == True
    assert "dealing 30 damage to 2 enemies!" in message
    
    # Verify damage - close and edge monsters should be damaged, far monster should not
    assert close_monster.hp == 0  # 25 - 30 = 0 (max 1 damage)
    assert far_monster.hp == 30  # Undamaged
    assert edge_monster.hp == 0  # 10 - 30 = 0
    
    # Verify dead monsters are removed
    assert len(mock_level.monsters) == 1
    assert mock_level.monsters[0] == far_monster


def test_bomb_handles_no_enemies():
    """Test that Bomb handles case with no enemies in range"""
    player = Player(5, 5)
    mock_level = MockLevel()
    player._current_level = mock_level
    # No monsters on the level
    
    bomb = Bomb(0, 0)
    success, message = bomb.use(player)
    
    assert success == True
    assert "BOOM! The bomb explodes, but no enemies were in range." in message


def test_swords_to_plowshares_converts_weapons():
    """Test that SwordsToPlowshares converts unequipped weapons"""
    player = Player(5, 5)
    
    # Add some weapons to inventory (not equipped)
    sword1 = WoodenStick(0, 0)
    sword2 = WoodenStick(0, 0)
    player.add_item(sword1)
    player.add_item(sword2)
    
    # Verify initial state
    assert len(player.inventory) == 2
    assert sword1 in player.inventory
    assert sword2 in player.inventory
    
    # Use swords to plowshares
    converter = SwordsToPlowshares(0, 0)
    success, message = converter.use(player)
    
    # Verify success
    assert success == True
    assert "2 weapons transform into healing potions!" in message
    
    # Verify weapons are removed and health potions are added
    assert sword1 not in player.inventory
    assert sword2 not in player.inventory
    assert len(player.inventory) == 2  # Same count, but now potions
    
    # Check that all items are health potions
    health_potions = [item for item in player.inventory if isinstance(item, HealthPotion)]
    assert len(health_potions) == 2


def test_swords_to_plowshares_ignores_equipped_weapon():
    """Test that SwordsToPlowshares does not convert equipped weapon"""
    player = Player(5, 5)
    
    # Add weapon to inventory
    extra_sword = WoodenStick(0, 0)
    player.add_item(extra_sword)
    
    # Current equipped weapon should not be converted
    equipped_weapon = player.weapon
    
    # Use swords to plowshares
    converter = SwordsToPlowshares(0, 0)
    success, message = converter.use(player)
    
    # Verify success
    assert success == True
    assert f"Your {extra_sword.name} transforms into a healing potion!" in message
    
    # Verify equipped weapon is still equipped
    assert player.weapon == equipped_weapon
    
    # Verify unequipped weapon is converted
    assert extra_sword not in player.inventory
    health_potions = [item for item in player.inventory if isinstance(item, HealthPotion)]
    assert len(health_potions) == 1


def test_swords_to_plowshares_no_weapons():
    """Test that SwordsToPlowshares fails when no unequipped weapons available"""
    player = Player(5, 5)
    
    # Don't add any weapons to inventory (only equipped weapon exists)
    
    converter = SwordsToPlowshares(0, 0)
    success, message = converter.use(player)
    
    # Verify failure
    assert success == False
    assert "You have no unequipped weapons to convert!" in message
    
    # Verify inventory is unchanged
    assert len(player.inventory) == 0


def test_compass_charges_system():
    """Test that Compass properly uses its charge system"""
    player = Player(5, 5)
    mock_level = MockLevel()
    player._current_level = mock_level
    
    compass = Compass(0, 0)
    assert compass.charges == 3
    
    # Use compass three times
    for i in range(3):
        success, message = compass.use(player)
        assert success == True
        assert compass.charges == 2 - i
    
    # Compass should be destroyed after 3 uses (charges = 0)
    assert compass.charges == 0


if __name__ == "__main__":
    test_map_reveals_entire_floor()
    test_map_fails_without_level()
    test_compass_reveals_all_items()
    test_compass_handles_no_items()
    test_bomb_damages_nearby_enemies()
    test_bomb_handles_no_enemies()
    test_swords_to_plowshares_converts_weapons()
    test_swords_to_plowshares_ignores_equipped_weapon()
    test_swords_to_plowshares_no_weapons()
    test_compass_charges_system()
    print("All new consumable tests passed!")