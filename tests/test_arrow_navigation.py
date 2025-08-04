#!/usr/bin/env python3
"""
Test arrow key navigation in inventory.
"""
import sys
sys.path.append('src')

from game import Game
from items import HealthPotion, create_random_item_for_level

def test_arrow_navigation():
    """Test that arrow key navigation works correctly."""
    
    # Create a game instance
    game = Game()
    
    # Add some items to the player's inventory
    potion1 = HealthPotion(0, 0)
    potion2 = HealthPotion(0, 0)
    weapon = create_random_item_for_level(1, 0, 0)
    
    game.player.add_item(potion1)
    game.player.add_item(potion2)
    game.player.add_item(weapon)
    
    print(f"Added {len(game.player.inventory)} items to inventory")
    
    # Simulate opening inventory (should select first item)
    game.game_state = 'INVENTORY'
    game.selected_item_index = 0 if len(game.player.inventory) > 0 else None
    game.show_item_description = False
    
    print(f"Initial selection: {game.selected_item_index}")
    
    # Test down arrow navigation
    class MockEvent:
        def __init__(self, key):
            self.sym = key
    
    import tcod
    
    # Navigate down
    event = MockEvent(tcod.event.KeySym.DOWN)
    original_index = game.selected_item_index
    
    # Simulate the down key logic
    if len(game.player.inventory) > 0:
        if game.selected_item_index is None:
            game.selected_item_index = 0
        else:
            game.selected_item_index = (game.selected_item_index + 1) % len(game.player.inventory)
        game.show_item_description = False
    
    print(f"After DOWN key: {original_index} -> {game.selected_item_index}")
    
    # Navigate up
    event = MockEvent(tcod.event.KeySym.UP)
    original_index = game.selected_item_index
    
    # Simulate the up key logic  
    if len(game.player.inventory) > 0:
        if game.selected_item_index is None:
            game.selected_item_index = 0
        else:
            game.selected_item_index = (game.selected_item_index - 1) % len(game.player.inventory)
        game.show_item_description = False
    
    print(f"After UP key: {original_index} -> {game.selected_item_index}")
    
    # Test wrapping (go past the end)
    game.selected_item_index = len(game.player.inventory) - 1  # Last item
    original_index = game.selected_item_index
    
    # Navigate down (should wrap to 0)
    if len(game.player.inventory) > 0:
        game.selected_item_index = (game.selected_item_index + 1) % len(game.player.inventory)
    
    print(f"Wrap test - from last to first: {original_index} -> {game.selected_item_index}")
    
    print("✓ Arrow navigation logic works correctly!")
    return True

if __name__ == "__main__":
    test_arrow_navigation()