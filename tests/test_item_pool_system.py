"""
Comprehensive tests for the item pool system.
"""

import unittest
from collections import defaultdict
from src.items.pool import ItemPool, ItemSpec, RARITY_COMMON, RARITY_UNCOMMON, RARITY_RARE
from src.items.weapons.dagger import Dagger
from src.items.weapons.sword import Sword
from src.items.weapons.demon_slayer import DemonSlayer
from src.items.armor.leather_armor import LeatherArmor
from src.items.armor.plate_armor import PlateArmor
from src.items.accessories.power_ring import PowerRing
from src.items.accessories.greater_power_ring import GreaterPowerRing
from src.items.consumables.health_potion import HealthPotion
from src.items.consumables.elixir import Elixir


class TestItemPoolSystem(unittest.TestCase):
    """Test the item pool system functionality."""
    
    def setUp(self):
        """Set up test cases."""
        self.pool = ItemPool()
    
    def test_item_spec_creation(self):
        """Test that ItemSpec dataclass works correctly."""
        spec = ItemSpec(
            item_class=Dagger,
            item_type='weapon',
            difficulty_rating=1.0,
            min_level=1,
            max_level=4,
            rarity=RARITY_COMMON,
            unique_per_floor=True,
            unique_per_game=False,
            tags=['test']
        )
        
        self.assertEqual(spec.item_class, Dagger)
        self.assertEqual(spec.item_type, 'weapon')
        self.assertEqual(spec.difficulty_rating, 1.0)
        self.assertEqual(spec.min_level, 1)
        self.assertEqual(spec.max_level, 4)
        self.assertEqual(spec.rarity, RARITY_COMMON)
        self.assertTrue(spec.unique_per_floor)
        self.assertFalse(spec.unique_per_game)
        self.assertIn('test', spec.tags)
    
    def test_floor_uniqueness_weapons(self):
        """Test that weapons are unique per floor."""
        # Start a new floor
        self.pool.start_new_floor(1)
        
        # Create first weapon
        item1 = self.pool.create_item_for_level(1, 0, 0, item_type='weapon')
        
        # Try to create multiple weapons - should not get duplicates on same floor
        weapons_created = set()
        weapons_created.add(type(item1).__name__)
        
        # Count actual weapons available at level 1
        available_weapons = 0
        for spec in self.pool.weapon_specs:
            if spec.min_level <= 1 and (spec.max_level is None or spec.max_level >= 1):
                available_weapons += 1
        
        # Try to create weapons up to the available limit
        for i in range(min(available_weapons - 1, 10)):  # -1 because we already created one
            item = self.pool.create_item_for_level(1, 0, 0, item_type='weapon')
            weapon_type = type(item).__name__
            
            # Check if it's actually a weapon (not a fallback consumable)
            is_weapon = any(spec.item_class.__name__ == weapon_type 
                          for spec in self.pool.weapon_specs)
            
            if is_weapon:
                # Should not create duplicate weapon types on same floor
                self.assertNotIn(weapon_type, weapons_created, 
                               f"Duplicate weapon {weapon_type} created on same floor")
                weapons_created.add(weapon_type)
        
        # New floor should reset uniqueness
        self.pool.start_new_floor(2)
        item_floor2 = self.pool.create_item_for_level(2, 0, 0, item_type='weapon')
        # Should be able to spawn same weapon type on different floor
        self.assertIsNotNone(item_floor2)
    
    def test_floor_uniqueness_armor(self):
        """Test that armor is unique per floor."""
        # Start a new floor
        self.pool.start_new_floor(1)
        
        # Create armor and track types
        armor_created = set()
        
        # Count actual armor available at level 1
        available_armor = 0
        for spec in self.pool.armor_specs:
            if spec.min_level <= 1 and (spec.max_level is None or spec.max_level >= 1):
                available_armor += 1
        
        for i in range(min(available_armor, 10)):  # Only try up to available armor count
            item = self.pool.create_item_for_level(1, 0, 0, item_type='armor')
            armor_type = type(item).__name__
            
            # Check if it's actually armor (not a fallback consumable)
            is_armor = any(spec.item_class.__name__ == armor_type 
                          for spec in self.pool.armor_specs)
            
            if is_armor:
                # Should not create duplicate armor types on same floor
                self.assertNotIn(armor_type, armor_created,
                               f"Duplicate armor {armor_type} created on same floor")
                armor_created.add(armor_type)
    
    def test_game_uniqueness_accessories(self):
        """Test that accessories are unique per game."""
        # Start multiple floors
        self.pool.start_new_floor(3)
        
        # Create first accessory
        item1 = self.pool.create_item_for_level(3, 0, 0, item_type='accessory')
        accessory_type1 = type(item1).__name__
        
        # Try on different floors - should not get same accessory
        accessories_found = {accessory_type1}
        
        for level in [4, 5, 6, 7]:
            self.pool.start_new_floor(level)
            for _ in range(5):  # Try multiple times per floor
                item = self.pool.create_item_for_level(level, 0, 0, item_type='accessory')
                if item:
                    accessory_type = type(item).__name__
                    self.assertNotIn(accessory_type, accessories_found,
                                   f"Duplicate accessory {accessory_type} spawned in game")
                    accessories_found.add(accessory_type)
    
    def test_consumables_no_uniqueness(self):
        """Test that consumables can spawn multiple times."""
        self.pool.start_new_floor(1)
        
        # Create multiple consumables
        consumables = []
        for _ in range(10):
            item = self.pool.create_item_for_level(1, 0, 0, item_type='consumable')
            consumables.append(type(item).__name__)
        
        # Should be able to have duplicates
        # Count occurrences
        counts = defaultdict(int)
        for c in consumables:
            counts[c] += 1
        
        # At least one consumable type should appear multiple times (likely HealthPotion)
        has_duplicate = any(count > 1 for count in counts.values())
        self.assertTrue(has_duplicate, "Consumables should be able to spawn multiple times")
    
    def test_level_appropriate_items(self):
        """Test that items spawn appropriate to their level ranges."""
        # Level 1 - should get early game items
        self.pool.start_new_floor(1)
        early_items = []
        for _ in range(20):
            item = self.pool.create_item_for_level(1, 0, 0)
            early_items.append(item)
        
        # Check that we don't get high-level items
        for item in early_items:
            item_name = type(item).__name__
            # Should not get end-game items like DemonSlayer, Elixir at level 1
            self.assertNotEqual(item_name, 'DemonSlayer', "DemonSlayer should not spawn at level 1")
            self.assertNotEqual(item_name, 'Elixir', "Elixir should not spawn at level 1")
        
        # Level 10 - should have chance for DemonSlayer
        self.pool.start_new_floor(10)
        found_demon_slayer = False
        for _ in range(50):  # Try many times
            item = self.pool.create_item_for_level(10, 0, 0, item_type='weapon')
            if type(item).__name__ == 'DemonSlayer':
                found_demon_slayer = True
                break
        
        self.assertTrue(found_demon_slayer, "DemonSlayer should be available at level 10")
    
    def test_difficulty_scaling(self):
        """Test that item difficulty scales with level."""
        difficulties_by_level = {}
        
        for level in [1, 3, 5, 7, 9]:
            self.pool.start_new_floor(level)
            difficulties = []
            
            # Sample items and track their difficulties
            for _ in range(20):
                item = self.pool.create_item_for_level(level, 0, 0)
                # Find the spec for this item
                for spec_list in [self.pool.weapon_specs, self.pool.armor_specs, 
                                self.pool.accessory_specs, self.pool.consumable_specs]:
                    for spec in spec_list:
                        if spec.item_class == type(item):
                            difficulties.append(spec.difficulty_rating)
                            break
            
            if difficulties:
                avg_difficulty = sum(difficulties) / len(difficulties)
                difficulties_by_level[level] = avg_difficulty
        
        # Difficulty should generally increase with level
        prev_difficulty = 0
        for level in sorted(difficulties_by_level.keys()):
            current_difficulty = difficulties_by_level[level]
            # Allow some variance but trend should be upward
            if level > 1:
                self.assertGreaterEqual(current_difficulty, prev_difficulty * 0.8,
                                      f"Difficulty should generally increase (level {level})")
            prev_difficulty = current_difficulty
    
    def test_weight_calculation(self):
        """Test spawn weight calculation."""
        spec = ItemSpec(
            item_class=Dagger,
            item_type='weapon',
            difficulty_rating=1.0,
            min_level=1,
            max_level=4,
            rarity=RARITY_COMMON,
            unique_per_floor=True,
            unique_per_game=False
        )
        
        # Weight should be 0 before min_level
        weight = self.pool.calculate_spawn_weight(spec, 0, 1.0)
        self.assertEqual(weight, 0.0, "Weight should be 0 before min_level")
        
        # Weight should be 0 after max_level
        weight = self.pool.calculate_spawn_weight(spec, 5, 1.0)
        self.assertEqual(weight, 0.0, "Weight should be 0 after max_level")
        
        # Weight should be positive within range
        weight = self.pool.calculate_spawn_weight(spec, 2, 1.0)
        self.assertGreater(weight, 0, "Weight should be positive within level range")
        
        # Weight should be higher when difficulty matches target
        weight_matched = self.pool.calculate_spawn_weight(spec, 2, 1.0)  # Matches difficulty
        weight_unmatched = self.pool.calculate_spawn_weight(spec, 2, 3.0)  # Far from difficulty
        self.assertGreater(weight_matched, weight_unmatched,
                         "Weight should be higher when difficulty matches target")
    
    def test_item_type_distribution(self):
        """Test that item type distribution changes with level."""
        type_counts = {}
        
        for level in [1, 5, 9]:
            self.pool.start_new_floor(level)
            counts = defaultdict(int)
            
            # Generate many items
            for _ in range(100):
                item = self.pool.create_item_for_level(level, 0, 0)
                # Determine item type
                item_type = 'unknown'
                for spec in self.pool.weapon_specs:
                    if spec.item_class == type(item):
                        item_type = 'weapon'
                        break
                if item_type == 'unknown':
                    for spec in self.pool.armor_specs:
                        if spec.item_class == type(item):
                            item_type = 'armor'
                            break
                if item_type == 'unknown':
                    for spec in self.pool.accessory_specs:
                        if spec.item_class == type(item):
                            item_type = 'accessory'
                            break
                if item_type == 'unknown':
                    for spec in self.pool.consumable_specs:
                        if spec.item_class == type(item):
                            item_type = 'consumable'
                            break
                
                counts[item_type] += 1
            
            type_counts[level] = dict(counts)
        
        # Level 1 should have no accessories
        self.assertEqual(type_counts.get(1, {}).get('accessory', 0), 0,
                        "Level 1 should not spawn accessories")
        
        # Higher levels should have accessories
        self.assertGreater(type_counts.get(5, {}).get('accessory', 0), 0,
                         "Level 5 should spawn some accessories")
    
    def test_boss_weapon_level_10(self):
        """Test that DemonSlayer has very high spawn chance on level 10."""
        self.pool.start_new_floor(10)
        
        # Check weight calculation for DemonSlayer at level 10
        demon_slayer_spec = None
        for spec in self.pool.weapon_specs:
            if spec.item_class.__name__ == 'DemonSlayer':
                demon_slayer_spec = spec
                break
        
        self.assertIsNotNone(demon_slayer_spec, "DemonSlayer spec should exist")
        
        # Weight should be extremely high on level 10
        weight = self.pool.calculate_spawn_weight(
            demon_slayer_spec, 10, self.pool.get_target_difficulty_for_level(10)
        )
        self.assertEqual(weight, 100.0, "DemonSlayer should have weight 100 on level 10")
    
    def test_save_and_load_state(self):
        """Test saving and loading pool state."""
        # Set up some state
        self.pool.start_new_floor(1)
        self.pool.floor_spawned_weapons[1].add(Dagger)
        self.pool.floor_spawned_armor[1].add(LeatherArmor)
        
        self.pool.start_new_floor(2)
        self.pool.floor_spawned_weapons[2].add(Sword)
        
        self.pool.game_spawned_accessories.add(PowerRing)
        self.pool.game_spawned_accessories.add(GreaterPowerRing)
        
        # Save state
        save_data = self.pool.get_save_data()
        
        # Create new pool and load state
        new_pool = ItemPool()
        new_pool.load_save_data(save_data)
        
        # Verify state was restored
        self.assertIn(Dagger, new_pool.floor_spawned_weapons.get(1, set()))
        self.assertIn(LeatherArmor, new_pool.floor_spawned_armor.get(1, set()))
        self.assertIn(Sword, new_pool.floor_spawned_weapons.get(2, set()))
        self.assertIn(PowerRing, new_pool.game_spawned_accessories)
        self.assertIn(GreaterPowerRing, new_pool.game_spawned_accessories)
    
    def test_enchantment_chance(self):
        """Test that enchantment chance increases with level."""
        # This is a statistical test, so we need many samples
        enchanted_counts = {}
        
        for level in [1, 5, 10]:
            self.pool.start_new_floor(level)
            enchanted = 0
            total = 0
            
            for _ in range(50):
                item = self.pool.create_item_for_level(level, 0, 0, item_type='weapon')
                if hasattr(item, 'enchantments') and len(item.enchantments) > 0:
                    enchanted += 1
                total += 1
            
            enchanted_counts[level] = enchanted / total if total > 0 else 0
        
        # Enchantment chance should increase with level
        self.assertLess(enchanted_counts.get(1, 0), enchanted_counts.get(10, 0),
                       "Enchantment chance should increase with level")


if __name__ == '__main__':
    unittest.main()