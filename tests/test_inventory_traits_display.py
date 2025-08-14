"""Test that inventory UI displays trait information correctly."""

import unittest
from unittest.mock import MagicMock, patch
from src.ui import UI
from src.player import Player
from src.items.weapons import Sword
from src.items.armor import LeatherArmor
from src.items.enchantments import EnchantmentType, ArmorEnchantmentType, Enchantment, ArmorEnchantment
from src.traits import Trait


class TestInventoryTraitsDisplay(unittest.TestCase):
    """Test the inventory UI trait display functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.ui = UI()
        self.player = Player(5, 5)
        # Create mock console
        self.console = MagicMock()
        self.console.clear = MagicMock()
        self.console.print = MagicMock()
        
    def test_player_traits_display(self):
        """Test that player traits are displayed correctly in inventory."""
        # Equip a weapon with fire enchantment
        weapon = Sword(0, 0)
        fire_enchant = Enchantment(EnchantmentType.FLAMING)
        weapon.enchantments = [fire_enchant]
        self.player.weapon = weapon
        
        # Equip armor with fire resistance
        armor = LeatherArmor(0, 0)
        fire_resist = ArmorEnchantment(ArmorEnchantmentType.FIREPROOF)
        armor.enchantments = [fire_resist]
        self.player.armor = armor
        
        # Render inventory
        self.ui.render_inventory(self.console, self.player)
        
        # Check that damage types were displayed
        calls = self.console.print.call_args_list
        damage_type_displayed = False
        resistance_displayed = False
        
        for call in calls:
            args = call[0]
            if len(args) >= 3:
                text = str(args[2])
                if "Damage Types:" in text and "Fire" in text:
                    damage_type_displayed = True
                if "Resistant to:" in text and "Fire" in text:
                    resistance_displayed = True
        
        self.assertTrue(damage_type_displayed, "Damage types should be displayed")
        self.assertTrue(resistance_displayed, "Resistances should be displayed")
    
    def test_enchantment_effects_display(self):
        """Test that enchantments show their effects, not just names."""
        # Create a weapon with a fire enchantment
        weapon = Sword(0, 0)
        fire_enchant = Enchantment(EnchantmentType.FLAMING)
        weapon.enchantments = [fire_enchant]
        # Add item to inventory
        self.player.inventory.append(weapon)
        
        # Render inventory with this item selected
        self.ui.render_inventory(self.console, self.player, selected_item_index=0)
        
        # Check that enchantment effects were displayed
        calls = self.console.print.call_args_list
        enchant_effect_displayed = False
        
        for call in calls:
            args = call[0]
            if len(args) >= 3:
                text = str(args[2])
                # Should show effect like "Flaming (+Fire damage)" not just "Flaming"
                if "Flaming" in text and ("Fire" in text or "damage" in text):
                    enchant_effect_displayed = True
        
        self.assertTrue(enchant_effect_displayed, "Enchantment effects should be displayed, not just names")
    
    def test_multiple_traits_no_duplicates(self):
        """Test that duplicate traits are not shown multiple times."""
        # Equip weapon with two fire enchantments
        weapon = Sword(0, 0)
        fire_enchant1 = Enchantment(EnchantmentType.FLAMING)
        fire_enchant2 = Enchantment(EnchantmentType.FLAMING)
        weapon.enchantments = [fire_enchant1, fire_enchant2]
        self.player.weapon = weapon
        
        # Render inventory
        self.ui.render_inventory(self.console, self.player)
        
        # Check that Fire appears only once in damage types
        calls = self.console.print.call_args_list
        for call in calls:
            args = call[0]
            if len(args) >= 3:
                text = str(args[2])
                if "Damage Types:" in text:
                    # Count occurrences of "Fire" - should be 1
                    fire_count = text.count("Fire")
                    self.assertEqual(fire_count, 1, "Fire should appear only once in damage types")
    
    def test_weakness_display(self):
        """Test that weaknesses are displayed correctly."""
        # Create a mock weapon with ice weakness
        weapon = MagicMock()
        weapon.name = "Test Weapon"
        weapon.get_attack_bonus = MagicMock(return_value=5)
        weapon.get_defense_bonus = MagicMock(return_value=0)
        weapon.get_attack_traits = MagicMock(return_value=[])
        weapon.get_resistances = MagicMock(return_value=[])
        weapon.get_weaknesses = MagicMock(return_value=[Trait.ICE, Trait.DARK])
        weapon.get_attack_multiplier_bonus = MagicMock(return_value=1.0)
        weapon.get_defense_multiplier_bonus = MagicMock(return_value=1.0)
        weapon.get_xp_multiplier_bonus = MagicMock(return_value=1.0)
        weapon.crit_bonus = 0
        weapon.evade_bonus = 0
        
        self.player.weapon = weapon
        
        # Render inventory
        self.ui.render_inventory(self.console, self.player)
        
        # Check that weaknesses were displayed
        calls = self.console.print.call_args_list
        weakness_displayed = False
        
        for call in calls:
            args = call[0]
            if len(args) >= 3:
                text = str(args[2])
                if "Weak against:" in text and "Ice" in text and "Dark" in text:
                    weakness_displayed = True
        
        self.assertTrue(weakness_displayed, "Weaknesses should be displayed")


if __name__ == '__main__':
    unittest.main()