#!/usr/bin/env python3
"""
Test inventory use and examine functionality.
"""
import sys
sys.path.append('src')

from game import Game
from items.armor import LeatherArmor
from items.consumables import HealthPotion

def test_inventory_actions():
    """Test use and examine functionality."""
    
    # Create a game instance
    game = Game()
    
    # Add leather armor to inventory
    leather_armor = LeatherArmor(0, 0)
    game.player.add_item(leather_armor)
    
    print(f"Leather armor description: '{leather_armor.description}'")
    print(f"Leather armor defense bonus: {leather_armor.defense_bonus}")
    
    # Test examine functionality
    game.game_state = 'INVENTORY'
    game.selected_item_index = 0
    game.show_item_description = False
    
    print(f"Before examine: show_item_description = {game.show_item_description}")
    
    # Simulate 'E' key press
    game.show_item_description = not game.show_item_description
    
    print(f"After examine: show_item_description = {game.show_item_description}")
    
    # Test use/equip functionality
    print(f"Before equip - player armor: {game.player.armor}")
    print(f"Inventory size: {len(game.player.inventory)}")
    
    # Simulate 'U' key press (use/equip)
    if game.selected_item_index is not None:
        game.use_inventory_item(game.selected_item_index)
    
    print(f"After equip - player armor: {game.player.armor}")
    print(f"Inventory size: {len(game.player.inventory)}")
    print(f"Game state: {game.game_state}")
    
    # Check if armor was equipped
    if game.player.armor and game.player.armor.name == "Leather Armor":
        print("✓ Leather armor was successfully equipped!")
    else:
        print("✗ Leather armor was not equipped properly")
    
    # Check if we're still in inventory
    if game.game_state == 'INVENTORY':
        print("✓ Still in inventory after equipping!")
    else:
        print("✗ Left inventory after equipping")
    
    return True

if __name__ == "__main__":
    test_inventory_actions()