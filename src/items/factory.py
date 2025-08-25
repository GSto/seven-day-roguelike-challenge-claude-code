"""
Factory functions for creating random items using the pool system.
"""

from .pool import item_pool

def create_random_item_for_level(level_number, x, y):
    """Create a random item appropriate for the given dungeon level using the pool system."""
    return item_pool.create_item_for_level(level_number, x, y)