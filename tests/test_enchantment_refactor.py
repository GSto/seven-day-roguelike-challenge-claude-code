"""
Test for enchantment refactor.
Verifies that enchantments don't modify base stats but are applied dynamically.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from player import Player
from items.weapons import Sword, MateriaStaff, Katana, ClericsStaff
from items.enchantments import EnchantmentType, Enchantment


def test_enchantments_dont_modify_base_stats():
    """Test that adding enchantments doesn't modify the weapon's base stats."""
    player = Player(10, 10)
    sword = Sword(0, 0)
    
    # Store base values
    base_attack = sword.attack_bonus
    base_defense = sword.defense_bonus
    base_fov = sword.fov_bonus
    
    # Add an enchantment
    quality_enchant = Enchantment(EnchantmentType.QUALITY)
    sword.add_enchantment(quality_enchant)
    
    # Base stats should remain unchanged
    assert sword.attack_bonus == base_attack
    assert sword.defense_bonus == base_defense
    assert sword.fov_bonus == base_fov


def test_enchantments_apply_dynamically():
    """Test that enchantments are applied dynamically through getter methods."""
    player = Player(10, 10)
    sword = Sword(0, 0)
    
    # Get base attack bonus
    base_bonus = sword.get_attack_bonus(player)
    assert base_bonus == 5  # Sword has +5 attack
    
    # Add Quality enchantment (+3 attack)
    quality_enchant = Enchantment(EnchantmentType.QUALITY)
    sword.add_enchantment(quality_enchant)
    
    # Attack bonus should increase dynamically
    new_bonus = sword.get_attack_bonus(player)
    assert new_bonus == 8  # 5 base + 3 from enchantment


def test_multiple_enchantments_stack():
    """Test that multiple enchantments stack correctly."""
    player = Player(10, 10)
    sword = Sword(0, 0)
    
    # Get base bonuses
    base_attack = sword.get_attack_bonus(player)
    base_defense = sword.get_defense_bonus(player)
    
    # Add Quality enchantment (+3 attack)
    quality_enchant = Enchantment(EnchantmentType.QUALITY)
    sword.add_enchantment(quality_enchant)
    
    # Add Bolstered enchantment (+1 defense)
    bolstered_enchant = Enchantment(EnchantmentType.BOLSTERED)
    sword.add_enchantment(bolstered_enchant)
    
    # Both enchantments should apply
    assert sword.get_attack_bonus(player) == base_attack + 3
    assert sword.get_defense_bonus(player) == base_defense + 1


def test_enchantment_multipliers():
    """Test that multiplier enchantments work correctly."""
    player = Player(10, 10)
    sword = Sword(0, 0)
    
    # Get base multiplier
    base_multiplier = sword.get_attack_multiplier_bonus(player)
    
    # Add Shiny enchantment (+0.25 attack multiplier)
    shiny_enchant = Enchantment(EnchantmentType.SHINY)
    sword.add_enchantment(shiny_enchant)
    
    # Multiplier should increase
    new_multiplier = sword.get_attack_multiplier_bonus(player)
    assert new_multiplier == base_multiplier + 0.25


def test_fov_enchantment():
    """Test that FOV enchantments work correctly."""
    player = Player(10, 10)
    sword = Sword(0, 0)
    
    # Get base FOV bonus
    base_fov = sword.get_fov_bonus(player)
    
    # Add Glowing enchantment (+2 FOV)
    glowing_enchant = Enchantment(EnchantmentType.GLOWING)
    sword.add_enchantment(glowing_enchant)
    
    # FOV should increase
    new_fov = sword.get_fov_bonus(player)
    assert new_fov == base_fov + 2


def test_crit_enchantment():
    """Test that crit enchantments work correctly."""
    player = Player(10, 10)
    katana = Katana(0, 0)
    
    # Get base crit bonus (Katana has 0.25 base)
    base_crit = katana.get_crit_bonus(player)
    assert base_crit == 0.25
    
    # Add Rending enchantment (+0.10 crit)
    rending_enchant = Enchantment(EnchantmentType.RENDING)
    katana.add_enchantment(rending_enchant)
    
    # Crit should increase
    new_crit = katana.get_crit_bonus(player)
    assert new_crit == 0.35  # 0.25 base + 0.10 from enchantment


def test_health_aspect_enchantment():
    """Test that health aspect enchantments work correctly."""
    player = Player(10, 10)
    staff = ClericsStaff(0, 0)
    
    # Get base health aspect bonus (ClericsStaff has 0.2 base)
    base_health = staff.get_health_aspect_bonus(player)
    assert base_health == 0.2
    
    # Add Blessed enchantment (+0.05 health aspect)
    blessed_enchant = Enchantment(EnchantmentType.BLESSED)
    staff.add_enchantment(blessed_enchant)
    
    # Health aspect should increase
    new_health = staff.get_health_aspect_bonus(player)
    assert new_health == 0.25  # 0.2 base + 0.05 from enchantment


def test_materia_staff_with_enchantments():
    """Test that MateriaStaff correctly stacks enchantments with its special ability."""
    player = Player(10, 10)
    staff = MateriaStaff(0, 0)
    
    # Base attack for MateriaStaff is 2
    base_attack = staff.get_attack_bonus(player)
    assert base_attack == 2
    
    # Add one enchantment - MateriaStaff gets +6 bonus
    quality_enchant = Enchantment(EnchantmentType.QUALITY)
    staff.add_enchantment(quality_enchant)
    
    # Should be: 2 base + 6 (special) + 3 (enchantment) = 11
    one_enchant_attack = staff.get_attack_bonus(player)
    assert one_enchant_attack == 11
    
    # Add second enchantment - MateriaStaff gets +12 bonus
    bolstered_enchant = Enchantment(EnchantmentType.BOLSTERED)
    staff.add_enchantment(bolstered_enchant)
    
    # Should be: 2 base + 12 (special) + 3 (quality) + 0 (bolstered is defense) = 17
    two_enchant_attack = staff.get_attack_bonus(player)
    assert two_enchant_attack == 17


def test_weapon_name_updates_with_enchantments():
    """Test that weapon names update correctly with enchantments."""
    player = Player(10, 10)
    sword = Sword(0, 0)
    
    # Initial name
    assert sword.name == "Sword"
    
    # Add Quality enchantment
    quality_enchant = Enchantment(EnchantmentType.QUALITY)
    sword.add_enchantment(quality_enchant)
    assert sword.name == "Quality Sword"
    
    # Add Shiny enchantment
    shiny_enchant = Enchantment(EnchantmentType.SHINY)
    sword.add_enchantment(shiny_enchant)
    assert sword.name == "Quality Shiny Sword"


def test_max_two_enchantments():
    """Test that weapons can only have max 2 enchantments."""
    player = Player(10, 10)
    sword = Sword(0, 0)
    
    # Add first enchantment
    quality_enchant = Enchantment(EnchantmentType.QUALITY)
    assert sword.add_enchantment(quality_enchant) == True
    
    # Add second enchantment
    shiny_enchant = Enchantment(EnchantmentType.SHINY)
    assert sword.add_enchantment(shiny_enchant) == True
    
    # Try to add third enchantment - should fail
    glowing_enchant = Enchantment(EnchantmentType.GLOWING)
    assert sword.add_enchantment(glowing_enchant) == False
    
    # Should still have only 2 enchantments
    assert len(sword.enchantments) == 2


def test_no_duplicate_enchantment_types():
    """Test that duplicate enchantment types cannot be added."""
    player = Player(10, 10)
    sword = Sword(0, 0)
    
    # Add Quality enchantment
    quality1 = Enchantment(EnchantmentType.QUALITY)
    assert sword.add_enchantment(quality1) == True
    
    # Try to add another Quality enchantment - should fail
    quality2 = Enchantment(EnchantmentType.QUALITY)
    assert sword.add_enchantment(quality2) == False
    
    # Should still have only 1 enchantment
    assert len(sword.enchantments) == 1


if __name__ == "__main__":
    test_enchantments_dont_modify_base_stats()
    test_enchantments_apply_dynamically()
    test_multiple_enchantments_stack()
    test_enchantment_multipliers()
    test_fov_enchantment()
    test_crit_enchantment()
    test_health_aspect_enchantment()
    test_materia_staff_with_enchantments()
    test_weapon_name_updates_with_enchantments()
    test_max_two_enchantments()
    test_no_duplicate_enchantment_types()
    print("All enchantment refactor tests passed!")