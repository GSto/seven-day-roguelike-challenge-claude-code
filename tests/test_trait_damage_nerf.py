#!/usr/bin/env python3

import unittest
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from entity import Entity
from traits import Trait
from stats import Stats


class TestTraitDamageNerf(unittest.TestCase):
    """Test the nerfed trait-based damage system."""
    
    def setUp(self):
        """Set up test fixtures."""
        stats = Stats(
            max_hp=100, hp=100, attack=10, defense=0, evade=0.0, 
            crit=0.0, crit_multiplier=1.0, attack_multiplier=1.0, 
            defense_multiplier=1.0, xp_multiplier=1.0, xp=0
        )
        self.entity = Entity(
            x=5, y=5, character='E', color=(255, 255, 255), stats=stats,
            attack_traits=[],
            weaknesses=[Trait.FIRE, Trait.ICE],  # Multiple weaknesses
            resistances=[Trait.STRIKE, Trait.SLASH]  # Multiple resistances
        )
    
    def test_single_weakness_applies_1_5x_damage(self):
        """Test that a single weakness applies 1.5x damage (nerfed from 2.0x)."""
        base_hp = self.entity.hp
        damage = 20
        
        # Attack with fire trait (entity is weak to fire)
        actual_damage = self.entity.take_damage_with_traits(damage, [Trait.FIRE])
        
        # Should deal 1.5x damage: 20 * 1.5 = 30
        expected_damage = int(damage * 1.5)
        self.assertEqual(actual_damage, expected_damage)
        self.assertEqual(self.entity.hp, base_hp - expected_damage)
    
    def test_multiple_weaknesses_only_apply_once(self):
        """Test that multiple weaknesses only apply one modifier."""
        base_hp = self.entity.hp
        damage = 20
        
        # Attack with both fire and ice traits (entity is weak to both)
        actual_damage = self.entity.take_damage_with_traits(damage, [Trait.FIRE, Trait.ICE])
        
        # Should only apply ONE weakness modifier: 20 * 1.5 = 30 (not 20 * 1.5 * 1.5 = 45)
        expected_damage = int(damage * 1.5)
        self.assertEqual(actual_damage, expected_damage)
        self.assertEqual(self.entity.hp, base_hp - expected_damage)
    
    def test_single_resistance_applies_0_5x_damage(self):
        """Test that a single resistance applies 0.5x damage."""
        base_hp = self.entity.hp
        damage = 20
        
        # Attack with strike trait (entity resists strike)
        actual_damage = self.entity.take_damage_with_traits(damage, [Trait.STRIKE])
        
        # Should deal 0.5x damage: 20 * 0.5 = 10
        expected_damage = int(damage * 0.5)
        self.assertEqual(actual_damage, expected_damage)
        self.assertEqual(self.entity.hp, base_hp - expected_damage)
    
    def test_multiple_resistances_only_apply_once(self):
        """Test that multiple resistances only apply one modifier."""
        base_hp = self.entity.hp
        damage = 20
        
        # Attack with both strike and slash traits (entity resists both)
        actual_damage = self.entity.take_damage_with_traits(damage, [Trait.STRIKE, Trait.SLASH])
        
        # Should only apply ONE resistance modifier: 20 * 0.5 = 10 (not 20 * 0.5 * 0.5 = 5)
        expected_damage = int(damage * 0.5)
        self.assertEqual(actual_damage, expected_damage)
        self.assertEqual(self.entity.hp, base_hp - expected_damage)
    
    def test_resistance_takes_priority_over_weakness(self):
        """Test that if both resistance and weakness apply, only one is used."""
        # Create entity with overlapping resistance and weakness
        stats = Stats(
            max_hp=100, hp=100, attack=10, defense=0, evade=0.0, 
            crit=0.0, crit_multiplier=1.0, attack_multiplier=1.0, 
            defense_multiplier=1.0, xp_multiplier=1.0, xp=0
        )
        entity = Entity(
            x=5, y=5, character='E', color=(255, 255, 255), stats=stats,
            attack_traits=[],
            weaknesses=[Trait.FIRE],
            resistances=[Trait.FIRE]  # Same trait in both
        )
        
        base_hp = entity.hp
        damage = 20
        
        # Attack with fire trait (entity both resists and is weak to fire)
        actual_damage = entity.take_damage_with_traits(damage, [Trait.FIRE])
        
        # Should apply resistance first (as it's checked first): 20 * 0.5 = 10
        expected_damage = int(damage * 0.5)
        self.assertEqual(actual_damage, expected_damage)
        self.assertEqual(entity.hp, base_hp - expected_damage)
    
    def test_no_trait_match_applies_normal_damage(self):
        """Test that attacks with no matching traits deal normal damage."""
        base_hp = self.entity.hp
        damage = 20
        
        # Attack with poison trait (entity has no interaction with poison)
        actual_damage = self.entity.take_damage_with_traits(damage, [Trait.POISON])
        
        # Should deal normal damage (no modifier)
        self.assertEqual(actual_damage, damage)
        self.assertEqual(self.entity.hp, base_hp - damage)
    
    def test_minimum_damage_still_applies(self):
        """Test that minimum damage of 1 is still enforced."""
        # Create entity with high defense
        stats = Stats(
            max_hp=100, hp=100, attack=10, defense=50, evade=0.0, 
            crit=0.0, crit_multiplier=1.0, attack_multiplier=1.0, 
            defense_multiplier=1.0, xp_multiplier=1.0, xp=0
        )
        entity = Entity(
            x=5, y=5, character='E', color=(255, 255, 255), stats=stats,
            attack_traits=[],
            weaknesses=[],
            resistances=[Trait.STRIKE]
        )
        
        base_hp = entity.hp
        damage = 2  # Low damage that will be reduced further
        
        # Attack with strike trait (resisted) with low base damage
        actual_damage = entity.take_damage_with_traits(damage, [Trait.STRIKE])
        
        # Should deal minimum 1 damage even after resistance and defense
        # damage = 2 * 0.5 = 1, then 1 - 50 defense = min(1, -49) = 1
        self.assertEqual(actual_damage, 1)
        self.assertEqual(entity.hp, base_hp - 1)


if __name__ == '__main__':
    unittest.main()