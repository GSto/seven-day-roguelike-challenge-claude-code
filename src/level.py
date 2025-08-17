"""
Level generation and management.

This file maintains backward compatibility by re-exporting classes from the level module.
"""

# Import from the new modular structure
from level import Room, Level

# Re-export for backward compatibility
__all__ = ['Room', 'Level']