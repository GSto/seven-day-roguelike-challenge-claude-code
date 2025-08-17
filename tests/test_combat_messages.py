#!/usr/bin/env python3
"""Test combat messages for weakness/resistance logging."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from game import Game
from monsters import Monster
from traits import Trait

def test_weakness_resistance_messages():
    """Test that weakness/resistance messages appear correctly."""
    game = Game()
    
    # Create a test monster with specific weaknesses and resistances
    test_monster = Monster(
        x=game.player.x + 1,
        y=game.player.y,
        name="Test Goblin",
        char='g',
        color=(255, 0, 0),
        hp=10,
        attack=5,
        defense=0,
        xp_value=10,
        weaknesses=[Trait.FIRE],
        resistances=[Trait.ICE],
        attack_traits=[Trait.SLASH]
    )
    game.level.monsters.append(test_monster)
    
    # Test 1: Player attacks with weakness trait (FIRE)
    game.player.weapon = type('obj', (object,), {
        'attack': 10,
        'attack_traits': [Trait.FIRE],
        'crit': 0,
        'crit_multiplier': 2.0
    })()
    
    print("Test 1: Player attacks with FIRE (monster weak to FIRE)")
    game.ui.message_log = []  # Clear messages
    game.player_attack_monster(test_monster)
    
    # Check that "Weakness exploited!" appears in messages
    messages = [msg[0] if isinstance(msg, tuple) else msg for msg in game.ui.message_log]
    assert "Weakness exploited!" in messages, f"Expected 'Weakness exploited!' in messages, got: {messages}"
    print("✓ Weakness message appears correctly")
    
    # Test 2: Player attacks with resistance trait (ICE)
    test_monster.hp = 10  # Reset HP
    game.player.weapon.attack_traits = [Trait.ICE]
    
    print("\nTest 2: Player attacks with ICE (monster resistant to ICE)")
    game.ui.message_log = []  # Clear messages
    game.player_attack_monster(test_monster)
    
    messages = [msg[0] if isinstance(msg, tuple) else msg for msg in game.ui.message_log]
    assert "Resistant!" in messages, f"Expected 'Resistant!' in messages, got: {messages}"
    print("✓ Resistance message appears correctly")
    
    # Test 3: Monster attacks player with weakness
    game.player.armor = type('obj', (object,), {
        'defense': 5,
        'weaknesses': [Trait.SLASH],
        'resistances': []
    })()
    
    print("\nTest 3: Monster attacks with SLASH (player weak to SLASH)")
    game.ui.message_log = []  # Clear messages
    game.monster_attack_player(test_monster)
    
    messages = [msg[0] if isinstance(msg, tuple) else msg for msg in game.ui.message_log]
    assert "Weakness exploited!" in messages, f"Expected 'Weakness exploited!' in messages for monster attack, got: {messages}"
    print("✓ Monster exploits player weakness correctly")
    
    # Test 4: Monster attacks player with resistance
    game.player.armor.weaknesses = []
    game.player.armor.resistances = [Trait.SLASH]
    
    print("\nTest 4: Monster attacks with SLASH (player resistant to SLASH)")
    game.ui.message_log = []  # Clear messages
    game.monster_attack_player(test_monster)
    
    messages = [msg[0] if isinstance(msg, tuple) else msg for msg in game.ui.message_log]
    assert "Resistant!" in messages, f"Expected 'Resistant!' in messages for monster attack, got: {messages}"
    print("✓ Player resists monster attack correctly")
    
    # Test 5: Both weakness and resistance (no special message)
    game.player.weapon.attack_traits = [Trait.FIRE, Trait.ICE]
    test_monster.hp = 10  # Reset HP
    
    print("\nTest 5: Player attacks with FIRE and ICE (both weakness and resistance)")
    game.ui.message_log = []  # Clear messages
    game.player_attack_monster(test_monster)
    
    messages = [msg[0] if isinstance(msg, tuple) else msg for msg in game.ui.message_log]
    assert "Weakness exploited!" not in messages, f"Should not show weakness message when both apply, got: {messages}"
    assert "Resistant!" not in messages, f"Should not show resistance message when both apply, got: {messages}"
    print("✓ No special message when both weakness and resistance apply")
    
    print("\n✅ All tests passed!")

if __name__ == "__main__":
    test_weakness_resistance_messages()