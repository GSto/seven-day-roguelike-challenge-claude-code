"""
Tests for Item Pack 2 features including new items and mechanics.
"""

import unittest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from player import Player
from items.consumables import MayhemsBoon, Compass, Map, Bomb, SwordsToPlowshares, Transmutation
from items.armor import CoatedPlate, AntiAngelTechnology, SpikedCuirass, UtilityBelt, SOSArmor
from items.weapons import AcidDagger, ClairObscur, FeuGlace, BigStick
from items.accessories import ElementalMayhem, GodsEye, SavingThrow, Anaglyph, MallNinja, RighteousFury, SongOfIceAndFire
from traits import Trait
from items.base import Consumable


class TestChargesMechanic(unittest.TestCase):
    """Test the new charges mechanic for consumables."""
    
    def test_consumable_with_charges(self):
        """Test that consumables with charges work correctly."""
        compass = Compass(0, 0)
        self.assertEqual(compass.charges, 3)
        self.assertEqual(compass.max_charges, 3)
        
        # Test display name includes charges
        display_name = compass.get_display_name()
        self.assertIn("(3/3)", display_name)
        
        # Test using charges
        should_destroy = compass.use_charge()
        self.assertFalse(should_destroy)
        self.assertEqual(compass.charges, 2)
        
        # Use remaining charges
        compass.use_charge()
        should_destroy = compass.use_charge()
        self.assertTrue(should_destroy)
        self.assertEqual(compass.charges, 0)
    
    def test_consumable_without_charges(self):
        """Test that regular consumables still work as before."""
        bomb = Bomb(0, 0)
        self.assertIsNone(bomb.charges)
        self.assertIsNone(bomb.max_charges)
        
        # Test display name doesn't include charges
        display_name = bomb.get_display_name()
        self.assertNotIn("(", display_name)
        
        # Test destruction after use
        should_destroy = bomb.use_charge()
        self.assertTrue(should_destroy)


class TestCleanupMechanic(unittest.TestCase):
    """Test the new cleanup step mechanism for accessories."""
    
    def test_accessory_cleanup_flag(self):
        """Test that accessories can be marked for cleanup."""
        anaglyph = Anaglyph(0, 0)
        self.assertTrue(anaglyph.is_cleanup)
        
        regular_accessory = GodsEye(0, 0)
        self.assertFalse(regular_accessory.is_cleanup)


class TestNewConsumables(unittest.TestCase):
    """Test the new consumables from Item Pack 2."""
    
    def setUp(self):
        self.player = Player(5, 5)
    
    def test_mayhems_boon(self):
        """Test Mayhem's Boon functionality."""
        boon = MayhemsBoon(0, 0)
        self.assertEqual(boon.name, "Mayhem's Boon")
        self.assertEqual(boon.char, '*')
        
        # Test use with basic equipment - should succeed
        result = boon.use(self.player)
        if isinstance(result, tuple) and len(result) == 3:
            success, message, should_destroy = result
            self.assertTrue(success)
            self.assertTrue(should_destroy)
        else:
            # Handle different return format
            success, message = result
            self.assertTrue(success)
    
    def test_compass_with_charges(self):
        """Test Compass with charges mechanism."""
        compass = Compass(0, 0)
        self.assertEqual(compass.charges, 3)
        
        result = compass.use(self.player)
        if isinstance(result, tuple) and len(result) == 3:
            success, message, should_destroy = result
            self.assertTrue(success)
            self.assertFalse(should_destroy)
        else:
            success, message = result
            self.assertTrue(success)
        self.assertEqual(compass.charges, 2)
    
    def test_other_consumables(self):
        """Test other new consumables can be created."""
        items = [
            Map(0, 0),
            Bomb(0, 0),
            SwordsToPlowshares(0, 0),
            Transmutation(0, 0)
        ]
        
        for item in items:
            self.assertIsInstance(item, Consumable)
            self.assertIsNotNone(item.name)


class TestNewArmor(unittest.TestCase):
    """Test the new armor pieces from Item Pack 2."""
    
    def setUp(self):
        self.player = Player(5, 5)
    
    def test_coated_plate(self):
        """Test Coated Plate armor."""
        armor = CoatedPlate(0, 0)
        self.assertEqual(armor.name, "Coated Plate")
        self.assertEqual(armor.defense_bonus, 4)
        
        # Test status effect blocking
        self.assertTrue(armor.blocks_status_effect('poison'))
        self.assertTrue(armor.blocks_status_effect('burn'))
        self.assertTrue(armor.blocks_status_effect('stun'))
        self.assertFalse(armor.blocks_status_effect('freeze'))
    
    def test_anti_angel_technology(self):
        """Test Anti-Angel Technology armor."""
        armor = AntiAngelTechnology(0, 0)
        self.assertEqual(armor.defense_bonus, 4)
        self.assertIn(Trait.HOLY, armor.resistances)
        self.assertTrue(armor.blocks_status_effect('blindness'))
    
    def test_spiked_cuirass(self):
        """Test Spiked Cuirass armor."""
        armor = SpikedCuirass(0, 0)
        self.assertEqual(armor.defense_bonus, 4)
        self.assertEqual(armor.attack_bonus, 2)
    
    def test_utility_belt(self):
        """Test Utility Belt armor."""
        armor = UtilityBelt(0, 0)
        self.assertEqual(armor.defense_bonus, 3)
        self.assertEqual(armor.fov_bonus, 3)
        self.assertEqual(armor.health_aspect_bonus, 0.1)
        self.assertEqual(armor.xp_multiplier_bonus, 1.1)
    
    def test_sos_armor(self):
        """Test SOS Armor conditional defense."""
        armor = SOSArmor(0, 0)
        
        # Test normal defense at full HP
        self.player.hp = self.player.max_hp
        defense = armor.get_defense_bonus(self.player)
        self.assertEqual(defense, 2)
        
        # Test bonus defense at low HP (20% or less)
        self.player.hp = int(self.player.max_hp * 0.15)  # 15% HP
        defense = armor.get_defense_bonus(self.player)
        self.assertEqual(defense, 8)  # 2 base + 6 bonus


class TestNewWeapons(unittest.TestCase):
    """Test the new weapons from Item Pack 2."""
    
    def test_acid_dagger(self):
        """Test Acid Dagger weapon."""
        weapon = AcidDagger(0, 0)
        self.assertEqual(weapon.attack_bonus, 6)
        self.assertIn(Trait.SLASH, weapon.attack_traits)
        self.assertIn(Trait.FIRE, weapon.attack_traits)
        self.assertIn(Trait.POISON, weapon.attack_traits)
    
    def test_clair_obscur(self):
        """Test Clair Obscur weapon."""
        weapon = ClairObscur(0, 0)
        self.assertEqual(weapon.attack_bonus, 10)
        self.assertIn(Trait.HOLY, weapon.attack_traits)
        self.assertIn(Trait.DARK, weapon.attack_traits)
        self.assertIn(Trait.MYSTIC, weapon.attack_traits)
    
    def test_feu_glace(self):
        """Test Feu-Glace weapon."""
        weapon = FeuGlace(0, 0)
        self.assertEqual(weapon.attack_bonus, 10)
        self.assertIn(Trait.FIRE, weapon.attack_traits)
        self.assertIn(Trait.ICE, weapon.attack_traits)
        self.assertIn(Trait.MYSTIC, weapon.attack_traits)
    
    def test_big_stick(self):
        """Test Big Stick weapon."""
        weapon = BigStick(0, 0)
        self.assertEqual(weapon.attack_bonus, 5)
        self.assertIn(Trait.STRIKE, weapon.attack_traits)


class TestNewAccessories(unittest.TestCase):
    """Test the new accessories from Item Pack 2."""
    
    def setUp(self):
        self.player = Player(5, 5)
        # Mock some player methods that accessories might use
        self.player.get_total_attack_traits = lambda: []
        self.player.get_total_resistances = lambda: []
        self.player.inventory = []
        self.player.current_floor = 3
    
    def test_elemental_mayhem(self):
        """Test Elemental Mayhem accessory."""
        accessory = ElementalMayhem(0, 0)
        
        # Mock player with elemental traits
        self.player.get_total_attack_traits = lambda: [Trait.FIRE, Trait.ICE]
        self.player.get_total_resistances = lambda: [Trait.HOLY]
        
        attack_bonus = accessory.get_attack_bonus(self.player)
        # Should be 3 unique elemental traits * 3 = 9 bonus
        self.assertEqual(attack_bonus, 9)
    
    def test_gods_eye(self):
        """Test God's Eye accessory."""
        accessory = GodsEye(0, 0)
        self.assertEqual(accessory.fov_bonus, 20)
        self.assertIn(Trait.HOLY, accessory.attack_traits)
    
    def test_saving_throw(self):
        """Test Saving Throw accessory."""
        accessory = SavingThrow(0, 0)
        
        # Should prevent death if starting HP > 1
        self.assertTrue(accessory.prevents_death(self.player, 10))
        self.assertFalse(accessory.prevents_death(self.player, 1))
    
    def test_anaglyph_cleanup(self):
        """Test Anaglyph cleanup mechanism."""
        accessory = Anaglyph(0, 0)
        self.assertTrue(accessory.is_cleanup)
        
        # Test stat balancing
        new_attack, new_defense = accessory.apply_cleanup_effect(self.player, 10, 6)
        self.assertEqual(new_attack, 8)  # (10+6)//2
        self.assertEqual(new_defense, 8)
    
    def test_mall_ninja(self):
        """Test Mall Ninja accessory."""
        accessory = MallNinja(0, 0)
        
        # Mock weapons in inventory
        from items.weapons import Sword, Dagger
        self.player.inventory = [Sword(0, 0), Dagger(0, 0)]
        
        attack_bonus = accessory.get_attack_bonus(self.player)
        self.assertEqual(attack_bonus, 2)  # 2 weapons
    
    def test_song_of_ice_and_fire(self):
        """Test Song of Ice and Fire accessory."""
        accessory = SongOfIceAndFire(0, 0)
        
        # Test on floor 5 or lower with fire trait
        self.player.current_floor = 3
        self.player.get_total_attack_traits = lambda: [Trait.FIRE]
        
        attack_bonus = accessory.get_attack_bonus(self.player)
        self.assertEqual(attack_bonus, 6)
        
        # Test on higher floor - should not get bonus
        self.player.current_floor = 7
        attack_bonus = accessory.get_attack_bonus(self.player)
        self.assertEqual(attack_bonus, 0)


if __name__ == '__main__':
    unittest.main()