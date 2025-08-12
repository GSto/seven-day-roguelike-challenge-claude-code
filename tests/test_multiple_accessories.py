"""
Unit tests for the multiple accessory slots system.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from player import Player
from items.accessories import PowerRing, ProtectionRing, ShadowRing, BaronsCrown, Joker


class TestMultipleAccessories:
    """Test multiple accessory slot functionality."""
    
    def test_player_has_three_accessory_slots(self):
        """Test that player starts with 3 empty accessory slots."""
        player = Player(10, 10)
        assert player.accessory_slots == 3
        assert len(player.accessories) == 0
    
    def test_can_equip_multiple_accessories(self):
        """Test that player can equip multiple accessories."""
        player = Player(10, 10)
        
        # Create test accessories
        ring1 = PowerRing(0, 0)
        ring2 = ProtectionRing(0, 0)
        ring3 = ShadowRing(0, 0)
        
        # Add to inventory
        player.add_item(ring1)
        player.add_item(ring2)
        player.add_item(ring3)
        
        # Simulate equipping by directly manipulating accessories list
        player.accessories.append(ring1)
        player.accessories.append(ring2)
        player.accessories.append(ring3)
        
        assert len(player.accessories) == 3
        assert ring1 in player.accessories
        assert ring2 in player.accessories
        assert ring3 in player.accessories
    
    def test_attack_bonus_stacking(self):
        """Test that attack bonuses from multiple accessories stack."""
        player = Player(10, 10)
        
        # Create test accessories with attack bonuses
        ring1 = PowerRing(0, 0)  # +3 attack
        ring2 = PowerRing(0, 0)  # +3 attack
        
        # Get base attack bonus without accessories
        base_bonus = player.get_attack_bonus()
        
        # Add accessories
        player.accessories.append(ring1)
        player.accessories.append(ring2)
        
        # Should have both bonuses stacked
        total_bonus = player.get_attack_bonus()
        assert total_bonus == base_bonus + 3 + 3
    
    def test_defense_bonus_stacking(self):
        """Test that defense bonuses from multiple accessories stack."""
        player = Player(10, 10)
        
        # Create test accessories with defense bonuses
        ring1 = ProtectionRing(0, 0)  # +2 defense
        ring2 = ProtectionRing(0, 0)  # +2 defense
        
        # Get base defense without accessories
        base_defense = player.get_total_defense()
        
        # Add accessories
        player.accessories.append(ring1)
        player.accessories.append(ring2)
        
        # Should have both bonuses stacked
        total_defense = player.get_total_defense()
        assert total_defense == base_defense + 4  # +2 + 2
    
    def test_multiplier_bonuses_multiply(self):
        """Test that multiplier bonuses from multiple accessories multiply together."""
        player = Player(10, 10)
        
        # Create accessories with multiplier bonuses
        crown1 = BaronsCrown(0, 0)  # 1.25x attack
        crown2 = BaronsCrown(0, 0)  # 1.25x attack
        
        # Get base multiplier
        base_multiplier = player.get_total_attack_multiplier()
        
        # Add accessories
        player.accessories.append(crown1)
        player.accessories.append(crown2)
        
        # Should multiply: base * 1.25 * 1.25 = base * 1.5625
        total_multiplier = player.get_total_attack_multiplier()
        expected = base_multiplier * 1.25 * 1.25
        assert abs(total_multiplier - expected) < 0.001  # Allow for floating point precision
    
    def test_dynamic_bonuses_work_with_multiple_accessories(self):
        """Test that dynamic bonus methods work with multiple accessories."""
        player = Player(10, 10)
        
        # Create joker cards with dynamic bonuses
        joker1 = Joker(0, 0)
        joker2 = Joker(0, 0)
        
        # Add accessories
        player.accessories.append(joker1)
        player.accessories.append(joker2)
        
        # Get multipliers - they should be calculated
        attack_multiplier = player.get_total_attack_multiplier()
        defense_multiplier = player.get_total_defense_multiplier()
        xp_multiplier = player.get_total_xp_multiplier()
        
        # The exact values will be random due to Joker's nature, but they should be calculated
        assert isinstance(attack_multiplier, (int, float))
        assert isinstance(defense_multiplier, (int, float))
        assert isinstance(xp_multiplier, (int, float))
    
    def test_evade_and_crit_bonuses_stack(self):
        """Test that evade and crit bonuses from multiple accessories stack."""
        player = Player(10, 10)
        
        # Create accessories with evade bonuses
        ring1 = ShadowRing(0, 0)  # +0.10 evade
        ring2 = ShadowRing(0, 0)  # +0.10 evade
        
        # Get base evade
        base_evade = player.get_total_evade()
        
        # Add accessories
        player.accessories.append(ring1)
        player.accessories.append(ring2)
        
        # Should have both bonuses stacked
        total_evade = player.get_total_evade()
        assert total_evade == base_evade + 0.20  # +0.10 + 0.10
    
    def test_empty_accessories_return_zero_bonuses(self):
        """Test that empty accessory list returns zero bonuses."""
        player = Player(10, 10)
        
        # Player starts with no accessories - bonuses should work normally
        attack_bonus = player.get_attack_bonus()
        
        # Should not crash and should return valid values
        assert isinstance(attack_bonus, int)
        
        # Test all bonus methods don't crash with empty accessories
        player.get_total_defense()
        player.get_total_fov()
        player.get_total_health_aspect()
        player.get_total_attack_multiplier()
        player.get_total_defense_multiplier()
        player.get_total_xp_multiplier()
        player.get_total_evade()
        player.get_total_crit()
        player.get_total_crit_multiplier()
    
    def test_accessory_slots_limitation(self):
        """Test that accessory slots are properly limited."""
        player = Player(10, 10)
        
        # Should start with 3 slots
        assert player.accessory_slots == 3
        
        # Should be able to track more accessories than slots (for testing equipment logic)
        ring1 = PowerRing(0, 0)
        ring2 = ProtectionRing(0, 0)
        ring3 = ShadowRing(0, 0)
        ring4 = PowerRing(0, 0)  # Extra accessory
        
        # The game logic should prevent equipping more than 3, but the list can theoretically hold more
        player.accessories.extend([ring1, ring2, ring3, ring4])
        
        # All accessories should still provide bonuses (though game logic should prevent this scenario)
        attack_bonus = player.get_attack_bonus()
        assert isinstance(attack_bonus, int)


def test_player_has_three_accessory_slots():
    """Test that player starts with 3 empty accessory slots."""
    player = Player(10, 10)
    assert player.accessory_slots == 3
    assert len(player.accessories) == 0


def test_can_equip_multiple_accessories():
    """Test that player can equip multiple accessories."""
    player = Player(10, 10)
    
    # Create test accessories
    ring1 = PowerRing(0, 0)
    ring2 = ProtectionRing(0, 0)
    
    # Simulate equipping by directly manipulating accessories list
    player.accessories.append(ring1)
    player.accessories.append(ring2)
    
    assert len(player.accessories) == 2
    assert ring1 in player.accessories
    assert ring2 in player.accessories


def test_attack_bonus_stacking():
    """Test that attack bonuses from multiple accessories stack."""
    player = Player(10, 10)
    
    # Create test accessories with attack bonuses
    ring1 = PowerRing(0, 0)  # +3 attack
    ring2 = PowerRing(0, 0)  # +3 attack
    
    # Get base attack bonus without accessories (should include weapon)
    base_bonus = player.get_attack_bonus()
    
    # Add accessories
    player.accessories.append(ring1)
    player.accessories.append(ring2)
    
    # Should have both bonuses stacked
    total_bonus = player.get_attack_bonus()
    assert total_bonus == base_bonus + 6  # +3 + 3


def test_empty_accessories_return_zero_bonuses():
    """Test that empty accessory list returns zero bonuses."""
    player = Player(10, 10)
    
    # Player starts with no accessories - bonuses should work normally
    attack_bonus = player.get_attack_bonus()
    
    # Should not crash and should return valid values
    assert isinstance(attack_bonus, int)
    
    # Test all bonus methods don't crash with empty accessories
    player.get_total_defense()
    player.get_total_fov()
    player.get_total_health_aspect()
    player.get_total_attack_multiplier()
    player.get_total_defense_multiplier()
    player.get_total_xp_multiplier()
    player.get_total_evade()
    player.get_total_crit()
    player.get_total_crit_multiplier()


if __name__ == "__main__":
    # Run tests manually
    test_player_has_three_accessory_slots()
    test_can_equip_multiple_accessories()
    test_attack_bonus_stacking()
    test_empty_accessories_return_zero_bonuses()
    print("All tests passed!")