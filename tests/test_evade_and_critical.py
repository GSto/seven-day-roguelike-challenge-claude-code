"""
Test the evade and critical hit mechanics.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from player import Player
from monsters import Skeleton, Goblin, Horror, Devil
from items.consumables.reapers_catalyst import ReapersCatalyst
from items.consumables.shadows_catalyst import ShadowsCatalyst
from items.consumables.reapers_boon import ReapersBoon
from enchantments import EnchantmentType, get_enchantment_by_type
from items.weapons.sword import Sword


def test_player_has_evade_crit_stats():
    """Test that player has evade, crit, and crit_multiplier stats."""
    player = Player(0, 0)
    
    # Check default values
    assert hasattr(player, 'evade')
    assert hasattr(player, 'crit')
    assert hasattr(player, 'crit_multiplier')
    
    assert player.evade == 0.05  # 5% default
    assert player.crit == 0.05  # 5% default
    assert player.crit_multiplier == 2.0  # 2x default
    
    # Check that methods exist
    assert hasattr(player, 'get_total_evade')
    assert hasattr(player, 'get_total_crit')
    assert hasattr(player, 'get_total_crit_multiplier')
    
    # Check method returns
    assert player.get_total_evade() == 0.05
    assert player.get_total_crit() == 0.05
    assert player.get_total_crit_multiplier() == 2.0
    
    print("✓ Player has evade, crit, and crit_multiplier stats")


def test_monsters_have_evade_crit_stats():
    """Test that monsters have evade, crit, and crit_multiplier stats."""
    skeleton = Skeleton(0, 0)
    goblin = Goblin(0, 0)
    horror = Horror(0, 0)
    devil = Devil(0, 0)
    
    # Check Skeleton (higher evade)
    assert skeleton.evade == 0.15  # 15% evade
    assert skeleton.crit == 0.05
    assert skeleton.crit_multiplier == 2.0
    
    # Check Goblin (higher crit)
    assert goblin.evade == 0.1
    assert goblin.crit == 0.15  # 15% crit
    assert goblin.crit_multiplier == 2.0
    
    # Check Horror (higher crit multiplier)
    assert horror.evade == 0.02
    assert horror.crit == 0.1
    assert horror.crit_multiplier == 2.5  # 2.5x crit damage
    
    # Check Devil (boss stats)
    assert devil.evade == 0.1
    assert devil.crit == 0.2  # 20% crit
    assert devil.crit_multiplier == 3.0  # 3x crit damage
    
    print("✓ Monsters have appropriate evade and crit stats")


def test_reapers_catalyst():
    """Test that Reaper's Catalyst increases crit chance."""
    player = Player(0, 0)
    catalyst = ReapersCatalyst(0, 0)
    
    # Check initial crit
    initial_crit = player.crit
    assert initial_crit == 0.05
    
    # Use catalyst
    success, message = catalyst.use(player)
    assert success
    assert "crit chance" in message.lower()
    
    # Check crit increased
    assert player.crit == initial_crit + 0.05
    assert player.crit == 0.10  # Should be 10% now
    
    print("✓ Reaper's Catalyst increases crit chance by 5%")


def test_shadows_catalyst():
    """Test that Shadow's Catalyst increases evade chance."""
    player = Player(0, 0)
    catalyst = ShadowsCatalyst(0, 0)
    
    # Check initial evade
    initial_evade = player.evade
    assert initial_evade == 0.05
    
    # Use catalyst
    success, message = catalyst.use(player)
    assert success
    assert "evade chance" in message.lower()
    
    # Check evade increased
    assert player.evade == initial_evade + 0.05
    assert player.evade == 0.10  # Should be 10% now
    
    print("✓ Shadow's Catalyst increases evade chance by 5%")


def test_reapers_boon():
    """Test that Reaper's Boon applies Rending enchantment."""
    player = Player(0, 0)
    boon = ReapersBoon(0, 0)
    
    # Player starts with a WoodenStick, so remove it first
    player.weapon = None
    
    # Need a weapon equipped first
    success, message = boon.use(player)
    assert not success  # Should fail without weapon
    
    # Equip a weapon
    sword = Sword(0, 0)
    player.weapon = sword
    
    # Apply the boon
    success, message = boon.use(player)
    assert success
    assert "Rending" in message
    assert "10% crit" in message.lower()
    
    # Check that weapon has the enchantment
    assert len(player.weapon.enchantments) == 1
    assert player.weapon.enchantments[0].type == EnchantmentType.RENDING
    
    # Check that weapon's crit bonus increased
    assert player.weapon.crit_bonus == 0.10
    
    print("✓ Reaper's Boon applies Rending enchantment correctly")


def test_rending_enchantment():
    """Test that Rending enchantment provides crit bonus."""
    enchantment = get_enchantment_by_type(EnchantmentType.RENDING)
    
    assert enchantment.type == EnchantmentType.RENDING
    assert enchantment.get_crit_bonus() == 0.10  # 10% crit bonus
    assert enchantment.get_attack_bonus() == 0  # No attack bonus
    assert enchantment.get_defense_bonus() == 0  # No defense bonus
    
    print("✓ Rending enchantment provides 10% crit bonus")


def test_equipment_with_evade_crit():
    """Test that equipment can have evade and crit bonuses."""
    player = Player(0, 0)
    
    # Create a custom weapon with crit bonus
    sword = Sword(0, 0)
    sword.crit_bonus = 0.05  # 5% crit bonus
    player.weapon = sword
    
    # Check total crit includes weapon bonus
    assert player.get_total_crit() == 0.10  # 5% base + 5% weapon
    
    print("✓ Equipment crit bonuses work correctly")


def test_evade_cap():
    """Test that evade is capped at 75%."""
    player = Player(0, 0)
    
    # Set ridiculous evade
    player.evade = 0.90  # 90% evade
    
    # Should be capped at 75%
    assert player.get_total_evade() == 0.75
    
    print("✓ Evade is capped at 75%")


def test_crit_cap():
    """Test that crit is capped at 75%."""
    player = Player(0, 0)
    
    # Set ridiculous crit
    player.crit = 0.90  # 90% crit
    
    # Should be capped at 75%
    assert player.get_total_crit() == 0.75
    
    print("✓ Crit is capped at 75%")


if __name__ == "__main__":
    print("Testing evade and critical hit mechanics...")
    print()
    
    test_player_has_evade_crit_stats()
    test_monsters_have_evade_crit_stats()
    test_reapers_catalyst()
    test_shadows_catalyst()
    test_reapers_boon()
    test_rending_enchantment()
    test_equipment_with_evade_crit()
    test_evade_cap()
    test_crit_cap()
    
    print()
    print("✅ All evade and critical tests passed!")