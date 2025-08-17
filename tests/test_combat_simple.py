#!/usr/bin/env python3
"""Simple test to verify combat messages work."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_combat_messages():
    """Test that weakness/resistance messages appear correctly."""
    print("Testing combat messages for weakness/resistance...")
    
    # Import game components
    from game import Game
    from monsters import Skeleton, Zombie, Goblin
    from traits import Trait
    
    # Create a game instance
    game = Game()
    
    # Test 1: Attack a skeleton with holy weakness
    print("\n1. Creating a Skeleton (weak to HOLY)...")
    skeleton = Skeleton(game.player.x + 1, game.player.y)
    game.level.monsters.append(skeleton)
    
    # Give player a weapon with HOLY trait
    from items.weapons import ClericsStaff
    holy_weapon = ClericsStaff(0, 0)
    game.player.weapon = holy_weapon
    
    print("   Player attacks Skeleton with HOLY weapon...")
    game.ui.message_log = []
    game.player_attack_monster(skeleton)
    
    messages = [msg[0] if isinstance(msg, tuple) else msg for msg in game.ui.message_log]
    print(f"   Messages: {messages}")
    
    if "Weakness exploited!" in messages:
        print("   ✓ Weakness message appears correctly")
    else:
        print("   ✗ Expected 'Weakness exploited!' message")
    
    # Test 2: Attack with a resisted trait
    print("\n2. Creating a Zombie (resistant to SLASH)...")
    zombie = Zombie(game.player.x + 1, game.player.y)
    game.level.monsters = [zombie]  # Replace monsters list
    
    # Give player a weapon with SLASH trait
    from items.weapons import Sword
    slash_weapon = Sword(0, 0)
    game.player.weapon = slash_weapon
    
    print("   Player attacks Zombie with SLASH weapon...")
    game.ui.message_log = []
    game.player_attack_monster(zombie)
    
    messages = [msg[0] if isinstance(msg, tuple) else msg for msg in game.ui.message_log]
    print(f"   Messages: {messages}")
    
    if "Resistant!" in messages:
        print("   ✓ Resistance message appears correctly")
    else:
        print("   ✗ Expected 'Resistant!' message")
    
    # Test 3: Monster attacks player
    print("\n3. Testing monster attack on player...")
    goblin = Goblin(game.player.x + 1, game.player.y)
    
    # Give player armor with weakness
    from items.armor import LeatherArmor
    armor = LeatherArmor(0, 0)
    # Temporarily add a weakness for testing
    armor.weaknesses = [Trait.SLASH]
    game.player.armor = armor
    
    print("   Goblin attacks player (player weak to SLASH)...")
    game.ui.message_log = []
    game.monster_attack_player(goblin)
    
    messages = [msg[0] if isinstance(msg, tuple) else msg for msg in game.ui.message_log]
    print(f"   Messages: {messages}")
    
    if "Weakness exploited!" in messages:
        print("   ✓ Monster exploits weakness correctly")
    else:
        print("   ✗ Expected 'Weakness exploited!' message for monster attack")
    
    print("\n✅ Combat message test complete!")

if __name__ == "__main__":
    test_combat_messages()