"""
Enchantment types for the roguelike game.
"""

from enum import Enum


class EnchantmentType(Enum):
    """Unified enchantment types that can be applied to weapons and armor."""
    QUALITY = "Quality"
    SHINY = "Shiny" 
    GLOWING = "Glowing"
    GILDED = "Gilded"
    BLESSED = "Blessed"
    BALANCED = "Balanced"
    RENDING = "Rending"
    SHADOW = "Shadow"
    FIRE = "Fire"
    ICE = "Ice"
    HOLY = "Holy"
    DARK = "Dark"
    
    @property
    def can_enchant_weapon(self):
        """Check if this enchantment can be applied to weapons."""
        return self != EnchantmentType.SHADOW
    
    @property
    def can_enchant_armor(self):
        """Check if this enchantment can be applied to armor."""
        return self != EnchantmentType.RENDING
    
    def get_weapon_label(self):
        """Get the label for this enchantment when applied to weapons."""
        labels = {
            EnchantmentType.QUALITY: "quality",
            EnchantmentType.SHINY: "refined",
            EnchantmentType.GLOWING: "glowing",
            EnchantmentType.GILDED: "gilded",
            EnchantmentType.BLESSED: "blessed",
            EnchantmentType.BALANCED: "bolstered",
            EnchantmentType.RENDING: "rending",
            EnchantmentType.FIRE: "flaming",
            EnchantmentType.ICE: "chilling",
            EnchantmentType.HOLY: "glorious",
            EnchantmentType.DARK: "blasphemous"
        }
        return labels.get(self, self.value.lower())
    
    def get_armor_label(self):
        """Get the label for this enchantment when applied to armor."""
        labels = {
            EnchantmentType.QUALITY: "quality",
            EnchantmentType.SHINY: "refined",
            EnchantmentType.GLOWING: "glowing",
            EnchantmentType.GILDED: "gilded",
            EnchantmentType.BLESSED: "blessed",
            EnchantmentType.BALANCED: "spiked",
            EnchantmentType.SHADOW: "shadow",
            EnchantmentType.FIRE: "fireproof",
            EnchantmentType.ICE: "snuggly",
            EnchantmentType.HOLY: "hexed",
            EnchantmentType.DARK: "haloed"
        }
        return labels.get(self, self.value.lower())