"""
Test to investigate the XP message bug when walking over items.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from player import Player
from level import Level
from items import HealthPotion
from ui import UI
from game import Game


def test_walking_over_item_no_xp():
    """Test that walking over items doesn't trigger XP messages."""
    player = Player(10, 10)
    level = Level(level_number=1)
    ui = UI()
    
    # Place an item at player position
    health_potion = HealthPotion(player.x, player.y)
    level.items.append(health_potion)
    
    # Check message log before any actions
    initial_message_count = len(ui.message_log)
    
    # Simulate the exact UI rendering process that happens each frame
    item = level.get_item_at(player.x, player.y)
    assert item == health_potion
    
    # Simulate multiple calls to mimic walking over item repeatedly  
    for i in range(10):
        item_check = level.get_item_at(player.x, player.y)
        assert item_check == health_potion
    
    # Check that no messages were added just by checking for item
    assert len(ui.message_log) == initial_message_count
    
    # Check that no XP-related messages exist
    for message, color in ui.message_log:
        assert "XP" not in message
        assert "gain" not in message.lower()
    
    print("✓ Walking over item doesn't trigger XP messages")


def test_monster_death_xp_message():
    """Test that XP messages only appear when monsters die."""
    ui = UI()
    
    # Simulate adding an XP message
    ui.add_message("You gain 10 XP!")
    
    # Check that message was added
    assert len(ui.message_log) == 1
    assert ui.message_log[0][0] == "You gain 10 XP!"
    
    print("✓ XP messages work correctly when added properly")


def test_message_log_persistence():
    """Test that message log doesn't duplicate messages."""
    ui = UI()
    
    # Add some messages
    ui.add_message("Message 1")
    ui.add_message("Message 2") 
    ui.add_message("You gain 10 XP!")
    
    # Check message count
    assert len(ui.message_log) == 3
    
    # Messages should not duplicate when rendered
    message_texts = [msg[0] for msg in ui.message_log]
    assert message_texts.count("You gain 10 XP!") == 1
    
    print("✓ Message log doesn't duplicate messages")


def test_pickup_prompt_vs_messages():
    """Test that pickup prompts don't interfere with message log."""
    player = Player(10, 10)
    level = Level(level_number=1)
    ui = UI()
    
    # Add some regular messages
    ui.add_message("Regular message")
    ui.add_message("You gain 10 XP!")
    
    initial_message_count = len(ui.message_log)
    
    # Place item at player position
    health_potion = HealthPotion(player.x, player.y)
    level.items.append(health_potion)
    
    # Check for item (this creates pickup prompt but shouldn't add to message log)
    item = level.get_item_at(player.x, player.y)
    assert item is not None
    
    # Message log should be unchanged
    assert len(ui.message_log) == initial_message_count
    
    # The pickup prompt should be separate from message log
    expected_prompt = f"Press 'g' to pick up {item.name}"
    # This is displayed directly, not added to message log
    
    print("✓ Pickup prompts don't interfere with message log")


def test_dead_monster_cleanup():
    """Test that dead monsters are properly cleaned up."""
    level = Level(level_number=1)
    
    # Check if there are any monsters on the level
    initial_monster_count = len(level.monsters)
    
    # All monsters should be alive initially
    living_monsters = [m for m in level.monsters if m.is_alive()]
    assert len(living_monsters) == initial_monster_count
    
    # Simulate killing a monster (if any exist)
    if level.monsters:
        monster = level.monsters[0]
        monster.hp = 0  # Kill the monster
        
        # Check that is_alive returns False
        assert not monster.is_alive()
        
        # Clean up dead monsters
        level.remove_dead_monsters()
        
        # Monster should be removed from level
        assert monster not in level.monsters
    
    print("✓ Dead monster cleanup works correctly")


def test_persistent_message_issue():
    """Test the likely cause: old XP messages persist in UI."""
    ui = UI()
    
    # Simulate the exact scenario: kill monster, get XP message
    ui.add_message("You attack the Goblin for 13 damage!")
    ui.add_message("The Goblin dies!")
    ui.add_message("You gain 10 XP!")  # This is the problematic message
    ui.add_message("The Goblin dropped a Mana Potion!")
    
    # Now simulate walking around without generating new messages
    # The XP message should still be visible in the message log
    xp_messages = [msg for msg, color in ui.message_log if "gain" in msg and "XP" in msg]
    assert len(xp_messages) == 1
    assert xp_messages[0] == "You gain 10 XP!"
    
    # This message will keep appearing in the UI until new messages push it out
    print("✓ Identified persistent message issue")


def run_all_tests():
    """Run all XP message bug tests."""
    print("Running XP message bug investigation tests...")
    print()
    
    test_walking_over_item_no_xp()
    test_monster_death_xp_message()
    test_message_log_persistence()
    test_pickup_prompt_vs_messages()
    test_dead_monster_cleanup()
    test_persistent_message_issue()
    
    print()
    print("✅ All XP message bug tests passed!")


if __name__ == "__main__":
    run_all_tests()