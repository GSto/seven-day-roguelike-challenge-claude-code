"""Test that inventory display shows multipliers as percentages."""

import sys
sys.path.append('src')

import unittest
from unittest.mock import Mock, MagicMock
from ui import UI
from player import Player


class TestInventoryPercentages(unittest.TestCase):
    """Test inventory percentage display."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ui = UI()
        self.player = Player(0, 0)
        self.console = Mock()
        self.console.clear = Mock()
        self.console.print = Mock()
        
    def test_player_summary_shows_percentages(self):
        """Test that player summary shows multipliers as percentages."""
        # Give player items with multipliers
        from items.accessories import BaronsCrown, JewelersCap
        crown = BaronsCrown(0, 0)  # Has 1.25x attack multiplier
        cap = JewelersCap(0, 0)  # Has 1.1x xp multiplier
        self.player.accessories = [crown, cap, None]
        
        # Render inventory
        self.ui.render_inventory(self.console, self.player)
        
        # Check that percentages are displayed correctly
        calls = self.console.print.call_args_list
        
        # Find the player summary section
        found_attack_mult = False
        found_xp_mult = False
        found_healing = False
        
        for call in calls:
            args = call[0]
            if len(args) >= 3:
                text = str(args[2])
                # Check for percentage format (not x format)
                if "Attack Mult:" in text:
                    self.assertIn("%", text)
                    self.assertNotIn("x", text)
                    # Crown gives 1.25x = 125%
                    self.assertIn("125%", text)
                    found_attack_mult = True
                elif "XP Mult:" in text:
                    self.assertIn("%", text)
                    self.assertNotIn("x", text)
                    # Cap gives 1.1x = 110%
                    self.assertIn("110%", text)
                    found_xp_mult = True
                elif "Healing:" in text and "%" in text:
                    # Check that healing is shown as a percentage
                    self.assertIn("%", text)
                    found_healing = True
        
        self.assertTrue(found_attack_mult, "Attack multiplier not shown as percentage")
        self.assertTrue(found_xp_mult, "XP multiplier not shown as percentage")
        self.assertTrue(found_healing, "Healing aspect not shown as percentage")
    
    def test_item_description_shows_percentages(self):
        """Test that item descriptions show multipliers as percentages."""
        # Add items to inventory
        from items.accessories import BaronsCrown
        crown = BaronsCrown(0, 0)  # 1.25x attack
        self.player.inventory = [crown]
        
        # Render with item selected
        self.ui.render_inventory(self.console, self.player, selected_item_index=0)
        
        # Check item description shows percentage
        calls = self.console.print.call_args_list
        found_item_desc = False
        
        for call in calls:
            args = call[0]
            if len(args) >= 3:
                text = str(args[2])
                if "Attack Multiplier:" in text:
                    self.assertIn("125%", text)
                    self.assertNotIn("1.25x", text)
                    found_item_desc = True
        
        self.assertTrue(found_item_desc, "Item description multiplier not shown as percentage")
    
    def test_inline_stats_show_percentages(self):
        """Test that inline item stats in list show percentages."""
        # Add items with multipliers
        from items.accessories import BaronsCrown, JewelersCap
        ring = BaronsCrown(0, 0)  # 1.25x attack
        amulet = JewelersCap(0, 0)  # 1.1x xp
        self.player.inventory = [ring, amulet]
        
        # Render inventory
        self.ui.render_inventory(self.console, self.player)
        
        # Check inline stats
        calls = self.console.print.call_args_list
        found_ring_stats = False
        found_amulet_stats = False
        
        for call in calls:
            args = call[0]
            if len(args) >= 3:
                text = str(args[2])
                if "Baron's Crown" in text:
                    # Should show 125% att, not 1.25x att
                    if "125% att" in text:
                        found_ring_stats = True
                    self.assertNotIn("1.25x att", text)
                elif "Jeweler's Cap" in text:
                    # Should show 110% xp, not 1.1x xp
                    if "110% xp" in text:
                        found_amulet_stats = True
                    self.assertNotIn("1.1x xp", text)
        
        self.assertTrue(found_ring_stats, "Ring stats not shown as percentage")
        self.assertTrue(found_amulet_stats, "Amulet stats not shown as percentage")
    
    def test_healing_aspect_shows_percentage(self):
        """Test that healing aspect bonus shows as percentage."""
        # Create item with healing aspect bonus
        class HealingRing:
            def __init__(self):
                self.name = "Healing Ring"
                self.equipment_slot = "accessory"
                self.health_aspect_bonus = 0.3  # 30% healing bonus
                
            def get_health_aspect_bonus(self, player):
                return self.health_aspect_bonus
        
        healing_ring = HealingRing()
        self.player.inventory = [healing_ring]
        
        # Render with item selected
        self.ui.render_inventory(self.console, self.player, selected_item_index=0)
        
        # Check description shows percentage
        calls = self.console.print.call_args_list
        found_healing = False
        
        for call in calls:
            args = call[0]
            if len(args) >= 3:
                text = str(args[2])
                if "Healing Bonus:" in text:
                    self.assertIn("30%", text)
                    self.assertNotIn("0.3", text)
                    found_healing = True
        
        self.assertTrue(found_healing, "Healing aspect bonus not shown as percentage")


if __name__ == '__main__':
    unittest.main()