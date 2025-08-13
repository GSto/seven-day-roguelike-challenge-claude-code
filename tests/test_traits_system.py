"""
Tests for the traits system.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from traits import Trait
from player import Player
from monster import Orc, Goblin, Troll, Devil
from items.weapons import Sword, Axe, DemonSlayer
from items.armor import ChainMail
from items.enchantments import Enchantment, EnchantmentType, ArmorEnchantment, ArmorEnchantmentType
from game import Game


class TestAspectEnum:
    """Test the Aspect enum."""
    
    def test_aspect_enum_values(self):
        """Test that all aspects exist."""
        assert Trait.FIRE
        assert Trait.ICE
        assert Trait.HOLY
        assert Trait.DARK
        assert Trait.STRIKE
        assert Trait.SLASH
        assert Trait.DEMONSLAYER


class TestPlayerTraits:
    """Test player trait functionality."""
    
    def test_player_default_traits(self):
        """Test that player starts with empty traits."""
        player = Player(5, 5)
        assert player.attack_traits == []
        assert player.weaknesses == []
        assert player.resistances == []
        
    def test_player_total_traits_empty_equipment(self):
        """Test trait aggregation with no equipment."""
        player = Player(5, 5)
        assert player.get_total_attack_traits() == []
        assert player.get_total_weaknesses() == []
        assert player.get_total_resistances() == []
    
    def test_player_weapon_traits(self):
        """Test that weapon traits are included in player totals."""
        player = Player(5, 5)
        sword = Sword(0, 0)
        player.weapon = sword
        
        # Sword should have slash trait
        assert Trait.SLASH in player.get_total_attack_traits()


class TestMonsterTraits:
    """Test monster trait functionality."""
    
    def test_orc_traits(self):
        """Test Orc trait configuration."""
        orc = Orc(5, 5)
        assert Trait.STRIKE in orc.weaknesses
        
    def test_goblin_traits(self):
        """Test Goblin trait configuration."""
        goblin = Goblin(5, 5)
        assert Trait.SLASH in goblin.attack_traits
        assert Trait.ICE in goblin.weaknesses
        assert Trait.HOLY in goblin.weaknesses
        assert Trait.FIRE in goblin.resistances
        
    def test_troll_traits(self):
        """Test Troll trait configuration."""
        troll = Troll(5, 5)
        assert Trait.STRIKE in troll.attack_traits
        assert Trait.FIRE in troll.weaknesses
        assert Trait.SLASH in troll.weaknesses
        
    def test_devil_traits(self):
        """Test Devil trait configuration."""
        devil = Devil(5, 5)
        assert Trait.DARK in devil.attack_traits
        assert Trait.FIRE in devil.attack_traits
        assert Trait.DEMONSLAYER in devil.weaknesses


class TestWeaponTraits:
    """Test weapon trait functionality."""
    
    def test_sword_traits(self):
        """Test that sword has slash trait."""
        sword = Sword(0, 0)
        assert Trait.SLASH in sword.attack_traits
        
    def test_axe_traits(self):
        """Test that axe has strike trait."""
        axe = Axe(0, 0)
        assert Trait.STRIKE in axe.attack_traits
        
    def test_demon_slayer_traits(self):
        """Test that DemonSlayer has correct traits."""
        demon_slayer = DemonSlayer(0, 0)
        assert Trait.DEMONSLAYER in demon_slayer.attack_traits
        assert Trait.SLASH in demon_slayer.attack_traits


class TestEnchantments:
    """Test enchantment trait functionality."""
    
    def test_flaming_enchantment(self):
        """Test flaming enchantment provides fire trait."""
        enchantment = Enchantment(EnchantmentType.FLAMING)
        assert Trait.FIRE in enchantment.attack_traits
        
    def test_chilling_enchantment(self):
        """Test chilling enchantment provides ice trait."""
        enchantment = Enchantment(EnchantmentType.CHILLING)
        assert Trait.ICE in enchantment.attack_traits
        
    def test_weapon_with_enchantment_traits(self):
        """Test weapon with enchantment includes enchantment traits."""
        sword = Sword(0, 0)
        flaming_enchantment = Enchantment(EnchantmentType.FLAMING)
        sword.add_enchantment(flaming_enchantment)
        
        total_traits = sword.get_total_attack_traits()
        assert Trait.SLASH in total_traits  # From sword
        assert Trait.FIRE in total_traits   # From enchantment


class TestArmorEnchantments:
    """Test armor enchantment functionality."""
    
    def test_fireproof_enchantment(self):
        """Test fireproof enchantment provides fire resistance."""
        enchantment = ArmorEnchantment(ArmorEnchantmentType.FIREPROOF)
        assert Trait.FIRE in enchantment.resistances
        
    def test_armor_with_enchantment_resistances(self):
        """Test armor with enchantment includes enchantment resistances."""
        armor = ChainMail(0, 0)
        fireproof_enchantment = ArmorEnchantment(ArmorEnchantmentType.FIREPROOF)
        armor.add_enchantment(fireproof_enchantment)
        
        total_resistances = armor.get_total_resistances()
        assert Trait.FIRE in total_resistances


class TestCombatAspectCalculations:
    """Test aspect damage calculations in combat."""
    
    def test_aspect_damage_multiplier_weakness(self):
        """Test damage multiplier for weakness."""
        game = Game()
        
        # Attack with fire trait against fire weakness should be 1.5x
        attack_traits = [Trait.FIRE]
        target_weaknesses = [Trait.FIRE]
        target_resistances = []
        
        multiplier = game.calculate_aspect_damage_multiplier(
            attack_traits, target_weaknesses, target_resistances
        )
        
        assert multiplier == 1.5
        
    def test_aspect_damage_multiplier_resistance(self):
        """Test damage multiplier for resistance."""
        game = Game()
        
        # Attack with fire trait against fire resistance should be 0.5x
        attack_traits = [Trait.FIRE]
        target_weaknesses = []
        target_resistances = [Trait.FIRE]
        
        multiplier = game.calculate_aspect_damage_multiplier(
            attack_traits, target_weaknesses, target_resistances
        )
        
        assert multiplier == 0.5
        
    def test_aspect_damage_multiplier_multiple_traits(self):
        """Test damage multiplier with multiple traits."""
        game = Game()
        
        # Attack with fire and ice traits, target weak to fire, resistant to ice
        # Should be 1.5 * 0.5 = 0.75
        attack_traits = [Trait.FIRE, Trait.ICE]
        target_weaknesses = [Trait.FIRE]
        target_resistances = [Trait.ICE]
        
        multiplier = game.calculate_aspect_damage_multiplier(
            attack_traits, target_weaknesses, target_resistances
        )
        
        assert multiplier == 0.75
        
    def test_aspect_damage_multiplier_no_interaction(self):
        """Test damage multiplier with no trait interactions."""
        game = Game()
        
        # Attack with fire trait, target has no fire weakness/resistance
        attack_traits = [Trait.FIRE]
        target_weaknesses = [Trait.ICE]
        target_resistances = [Trait.HOLY]
        
        multiplier = game.calculate_aspect_damage_multiplier(
            attack_traits, target_weaknesses, target_resistances
        )
        
        assert multiplier == 1.0


class TestDemonSlayerSpecialLogic:
    """Test DemonSlayer weapon special functionality."""
    
    def test_demon_slayer_vs_devil(self):
        """Test DemonSlayer weapon against Devil."""
        game = Game()
        
        # DemonSlayer has DEMONSLAYER trait, Devil is weak to DEMONSLAYER
        attack_traits = [Trait.DEMONSLAYER, Trait.SLASH]
        devil_weaknesses = [Trait.DEMONSLAYER]
        devil_resistances = []
        
        multiplier = game.calculate_aspect_damage_multiplier(
            attack_traits, devil_weaknesses, devil_resistances
        )
        
        # Should get 1.5x bonus for DEMONSLAYER trait
        assert multiplier == 1.5


def run_all_tests():
    """Run all test functions."""
    
    # Test Aspect enum
    test = TestAspectEnum()
    test.test_aspect_enum_values()
    print("✓ Aspect enum tests passed")
    
    # Test Player traits
    test = TestPlayerTraits()
    test.test_player_default_traits()
    test.test_player_total_traits_empty_equipment()
    test.test_player_weapon_traits()
    print("✓ Player traits tests passed")
    
    # Test Monster traits  
    test = TestMonsterTraits()
    test.test_orc_traits()
    test.test_goblin_traits()
    test.test_troll_traits()
    test.test_devil_traits()
    print("✓ Monster traits tests passed")
    
    # Test Weapon traits
    test = TestWeaponTraits()
    test.test_sword_traits()
    test.test_axe_traits()
    test.test_demon_slayer_traits()
    print("✓ Weapon traits tests passed")
    
    # Test Enchantments
    test = TestEnchantments()
    test.test_flaming_enchantment()
    test.test_chilling_enchantment()
    test.test_weapon_with_enchantment_traits()
    print("✓ Enchantment tests passed")
    
    # Test Armor enchantments
    test = TestArmorEnchantments()
    test.test_fireproof_enchantment()
    test.test_armor_with_enchantment_resistances()
    print("✓ Armor enchantment tests passed")
    
    # Test Combat calculations
    test = TestCombatAspectCalculations()
    test.test_aspect_damage_multiplier_weakness()
    test.test_aspect_damage_multiplier_resistance()
    test.test_aspect_damage_multiplier_multiple_traits()
    test.test_aspect_damage_multiplier_no_interaction()
    print("✓ Combat aspect calculation tests passed")
    
    # Test DemonSlayer
    test = TestDemonSlayerSpecialLogic()
    test.test_demon_slayer_vs_devil()
    print("✓ DemonSlayer special logic tests passed")
    
    print("\n🎉 All traits system tests passed!")


if __name__ == "__main__":
    run_all_tests()