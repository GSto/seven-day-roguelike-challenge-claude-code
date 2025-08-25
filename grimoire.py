#!/usr/bin/env python3
"""
Grimoire utility - generates documentation for all items in the game.
"""

import os
import sys
import importlib
import inspect
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from items.consumable import Consumable
from items.weapons.base import Weapon
from items.armor.base import Armor
from items.accessories.accessory import Accessory


def get_all_classes_from_module(module_path, base_class):
    """Get all classes from a module that inherit from base_class."""
    classes = []
    
    # Convert module path to import path
    import_path = module_path.replace('/', '.').replace('\\', '.')
    if import_path.startswith('src.'):
        import_path = import_path[4:]  # Remove 'src.' prefix
    
    try:
        module = importlib.import_module(import_path)
        for name, obj in inspect.getmembers(module):
            if (inspect.isclass(obj) and 
                issubclass(obj, base_class) and 
                obj != base_class and
                not name.startswith('_')):
                classes.append(obj)
    except ImportError as e:
        pass
    
    return classes


def get_all_items_of_type(base_path, base_class):
    """Get all items of a specific type from the file system."""
    items = []
    
    # Find all Python files in the directory
    for root, dirs, files in os.walk(base_path):
        # Skip __pycache__ directories
        if '__pycache__' in root:
            continue
            
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                # Build the module path
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, Path(__file__).parent)
                module_path = rel_path[:-3]  # Remove .py extension
                
                # Get classes from this module
                classes = get_all_classes_from_module(module_path, base_class)
                
                for cls in classes:
                    # Try to instantiate to get properties
                    try:
                        # Create temporary instance at 0,0 to extract properties
                        instance = cls(0, 0)
                        items.append({
                            'name': instance.name,
                            'description': instance.description,
                            'class': cls,
                            'instance': instance
                        })
                    except Exception as e:
                        # Some classes might need special parameters
                        # Try with minimal parameters
                        try:
                            if base_class == Weapon:
                                instance = cls(0, 0)
                            elif base_class == Armor:
                                instance = cls(0, 0)
                            elif base_class == Consumable:
                                instance = cls(0, 0)
                            elif base_class == Accessory:
                                instance = cls(0, 0)
                            else:
                                continue
                                
                            items.append({
                                'name': instance.name,
                                'description': instance.description,
                                'class': cls,
                                'instance': instance
                            })
                        except:
                            pass
    
    # Sort items alphabetically by name
    items.sort(key=lambda x: x['name'].lower())
    return items


def format_consumable(item_data):
    """Format a consumable item for the grimoire."""
    instance = item_data['instance']
    lines = []
    lines.append(f"{instance.name}")
    
    # Build description with effects
    desc_parts = []
    if instance.description:
        desc_parts.append(instance.description)
    
    # Add effect information
    effects = []
    if hasattr(instance, 'effect_value') and instance.effect_value != 0:
        if 'potion' in instance.name.lower() or 'elixir' in instance.name.lower():
            effects.append(f"Heals {instance.effect_value} HP")
    
    if hasattr(instance, 'attack_multiplier_effect') and instance.attack_multiplier_effect != 0:
        effects.append(f"Attack multiplier +{instance.attack_multiplier_effect:.1f}")
    
    if hasattr(instance, 'defense_multiplier_effect') and instance.defense_multiplier_effect != 0:
        effects.append(f"Defense multiplier +{instance.defense_multiplier_effect:.1f}")
    
    if hasattr(instance, 'xp_multiplier_effect') and instance.xp_multiplier_effect != 0:
        effects.append(f"XP multiplier +{instance.xp_multiplier_effect:.1f}")
    
    if hasattr(instance, 'resistances') and instance.resistances:
        for res in instance.resistances:
            effects.append(f"Adds {res.name} resistance")
    
    if hasattr(instance, 'weaknesses') and instance.weaknesses:
        for weak in instance.weaknesses:
            effects.append(f"Adds {weak.name} weakness")
    
    if hasattr(instance, 'attack_traits') and instance.attack_traits:
        for trait in instance.attack_traits:
            effects.append(f"Adds {trait.name} attack trait")
    
    # Special handling for boons and catalysts
    if 'boon' in instance.__class__.__name__.lower():
        if hasattr(instance, 'enchantment_type') and instance.enchantment_type:
            effects.append(f"Applies {instance.enchantment_type.name} enchantment to equipped item")
    
    if 'catalyst' in instance.__class__.__name__.lower() and not effects:
        # Look for permanent effects in description
        if 'permanently' in instance.description.lower():
            effects.append(instance.description)
    
    # Combine description and effects
    if effects:
        if desc_parts and effects:
            lines.append(desc_parts[0] if desc_parts[0] != effects[0] else effects[0])
        else:
            lines.append('; '.join(effects))
    elif desc_parts:
        lines.append(desc_parts[0])
    
    return '\n'.join(lines)


def format_weapon(item_data):
    """Format a weapon item for the grimoire."""
    instance = item_data['instance']
    lines = []
    
    # Build stat bonuses
    stats = []
    if hasattr(instance, 'attack_bonus') and instance.attack_bonus != 0:
        stats.append(f"+{instance.attack_bonus} att")
    if hasattr(instance, 'defense_bonus') and instance.defense_bonus != 0:
        stats.append(f"+{instance.defense_bonus} def")
    if hasattr(instance, 'fov_bonus') and instance.fov_bonus != 0:
        stats.append(f"+{instance.fov_bonus} FOV")
    if hasattr(instance, 'health_aspect_bonus') and instance.health_aspect_bonus != 0:
        stats.append(f"+{instance.health_aspect_bonus:.1f} health aspect")
    if hasattr(instance, 'evade_bonus') and instance.evade_bonus != 0:
        stats.append(f"+{instance.evade_bonus:.0%} evade")
    if hasattr(instance, 'crit_bonus') and instance.crit_bonus != 0:
        stats.append(f"+{instance.crit_bonus:.0%} crit")
    if hasattr(instance, 'crit_multiplier_bonus') and instance.crit_multiplier_bonus != 0:
        stats.append(f"+{instance.crit_multiplier_bonus:.1f}x crit damage")
    
    # Multipliers
    if hasattr(instance, 'attack_multiplier_bonus') and instance.attack_multiplier_bonus != 1.0:
        stats.append(f"{instance.attack_multiplier_bonus:.1f}x attack")
    if hasattr(instance, 'defense_multiplier_bonus') and instance.defense_multiplier_bonus != 1.0:
        stats.append(f"{instance.defense_multiplier_bonus:.1f}x defense")
    if hasattr(instance, 'xp_multiplier_bonus') and instance.xp_multiplier_bonus != 1.0:
        stats.append(f"{instance.xp_multiplier_bonus:.1f}x XP")
    
    # Format name with stats
    if stats:
        lines.append(f"{instance.name} ({', '.join(stats)})")
    else:
        lines.append(instance.name)
    
    # Add description
    if instance.description:
        lines.append(instance.description)
    
    # Add traits/resistances/weaknesses if any
    special = []
    if hasattr(instance, 'attack_traits') and instance.attack_traits:
        for trait in instance.attack_traits:
            special.append(f"Attack: {trait.name}")
    if hasattr(instance, 'resistances') and instance.resistances:
        for res in instance.resistances:
            special.append(f"Resist: {res.name}")
    if hasattr(instance, 'weaknesses') and instance.weaknesses:
        for weak in instance.weaknesses:
            special.append(f"Weak to: {weak.name}")
    
    if special:
        lines.append(f"[{', '.join(special)}]")
    
    return '\n'.join(lines)


def format_armor(item_data):
    """Format an armor item for the grimoire."""
    instance = item_data['instance']
    lines = []
    
    # Build stat bonuses
    stats = []
    if hasattr(instance, 'defense_bonus') and instance.defense_bonus != 0:
        stats.append(f"+{instance.defense_bonus} def")
    if hasattr(instance, 'attack_bonus') and instance.attack_bonus != 0:
        stats.append(f"+{instance.attack_bonus} att")
    if hasattr(instance, 'fov_bonus') and instance.fov_bonus != 0:
        stats.append(f"+{instance.fov_bonus} FOV")
    if hasattr(instance, 'health_aspect_bonus') and instance.health_aspect_bonus != 0:
        stats.append(f"+{instance.health_aspect_bonus:.1f} health aspect")
    if hasattr(instance, 'evade_bonus') and instance.evade_bonus != 0:
        stats.append(f"+{instance.evade_bonus:.0%} evade")
    if hasattr(instance, 'crit_bonus') and instance.crit_bonus != 0:
        stats.append(f"+{instance.crit_bonus:.0%} crit")
    
    # Multipliers
    if hasattr(instance, 'attack_multiplier_bonus') and instance.attack_multiplier_bonus != 1.0:
        stats.append(f"{instance.attack_multiplier_bonus:.1f}x attack")
    if hasattr(instance, 'defense_multiplier_bonus') and instance.defense_multiplier_bonus != 1.0:
        stats.append(f"{instance.defense_multiplier_bonus:.1f}x defense")
    if hasattr(instance, 'xp_multiplier_bonus') and instance.xp_multiplier_bonus != 1.0:
        stats.append(f"{instance.xp_multiplier_bonus:.1f}x XP")
    
    # Format name with stats
    if stats:
        lines.append(f"{instance.name} ({', '.join(stats)})")
    else:
        lines.append(instance.name)
    
    # Add description
    if instance.description:
        lines.append(instance.description)
    
    # Add traits/resistances/weaknesses if any
    special = []
    if hasattr(instance, 'attack_traits') and instance.attack_traits:
        for trait in instance.attack_traits:
            special.append(f"Attack: {trait.name}")
    if hasattr(instance, 'resistances') and instance.resistances:
        for res in instance.resistances:
            special.append(f"Resist: {res.name}")
    if hasattr(instance, 'weaknesses') and instance.weaknesses:
        for weak in instance.weaknesses:
            special.append(f"Weak to: {weak.name}")
    
    if special:
        lines.append(f"[{', '.join(special)}]")
    
    return '\n'.join(lines)


def format_accessory(item_data):
    """Format an accessory item for the grimoire."""
    instance = item_data['instance']
    lines = []
    
    # Build stat bonuses
    stats = []
    if hasattr(instance, 'attack_bonus') and instance.attack_bonus != 0:
        stats.append(f"+{instance.attack_bonus} att")
    if hasattr(instance, 'defense_bonus') and instance.defense_bonus != 0:
        stats.append(f"+{instance.defense_bonus} def")
    if hasattr(instance, 'fov_bonus') and instance.fov_bonus != 0:
        stats.append(f"+{instance.fov_bonus} FOV")
    if hasattr(instance, 'health_aspect_bonus') and instance.health_aspect_bonus != 0:
        stats.append(f"+{instance.health_aspect_bonus:.1f} health aspect")
    if hasattr(instance, 'evade_bonus') and instance.evade_bonus != 0:
        stats.append(f"+{instance.evade_bonus:.0%} evade")
    if hasattr(instance, 'crit_bonus') and instance.crit_bonus != 0:
        stats.append(f"+{instance.crit_bonus:.0%} crit")
    if hasattr(instance, 'crit_multiplier_bonus') and instance.crit_multiplier_bonus != 0:
        stats.append(f"+{instance.crit_multiplier_bonus:.1f}x crit damage")
    
    # Multipliers
    if hasattr(instance, 'attack_multiplier_bonus') and instance.attack_multiplier_bonus != 1.0:
        stats.append(f"{instance.attack_multiplier_bonus:.1f}x attack")
    if hasattr(instance, 'defense_multiplier_bonus') and instance.defense_multiplier_bonus != 1.0:
        stats.append(f"{instance.defense_multiplier_bonus:.1f}x defense")
    if hasattr(instance, 'xp_multiplier_bonus') and instance.xp_multiplier_bonus != 1.0:
        stats.append(f"{instance.xp_multiplier_bonus:.1f}x XP")
    
    # Format name with stats
    if stats:
        lines.append(f"{instance.name} ({', '.join(stats)})")
    else:
        lines.append(instance.name)
    
    # Add description
    if instance.description:
        lines.append(instance.description)
    
    # Add traits/resistances/weaknesses if any
    special = []
    if hasattr(instance, 'attack_traits') and instance.attack_traits:
        for trait in instance.attack_traits:
            special.append(f"Attack: {trait.name}")
    if hasattr(instance, 'resistances') and instance.resistances:
        for res in instance.resistances:
            special.append(f"Resist: {res.name}")
    if hasattr(instance, 'weaknesses') and instance.weaknesses:
        for weak in instance.weaknesses:
            special.append(f"Weak to: {weak.name}")
    
    if special:
        lines.append(f"[{', '.join(special)}]")
    
    return '\n'.join(lines)


def generate_grimoire():
    """Generate the grimoire documentation."""
    output = []
    
    # Get source path
    src_path = Path(__file__).parent / 'src'
    
    # Generate consumables section
    output.append("# GRIMOIRE")
    output.append("Complete catalog of all items in the game")
    output.append("")
    output.append("## CONSUMABLES")
    output.append("-" * 50)
    output.append("")
    
    consumables = get_all_items_of_type(src_path / 'items' / 'consumables', Consumable)
    for item in consumables:
        output.append(format_consumable(item))
        output.append("")
    
    # Generate weapons section
    output.append("")
    output.append("## WEAPONS")
    output.append("-" * 50)
    output.append("")
    
    weapons = get_all_items_of_type(src_path / 'items' / 'weapons', Weapon)
    for item in weapons:
        output.append(format_weapon(item))
        output.append("")
    
    # Generate armor section
    output.append("")
    output.append("## ARMOR")
    output.append("-" * 50)
    output.append("")
    
    armor = get_all_items_of_type(src_path / 'items' / 'armor', Armor)
    for item in armor:
        output.append(format_armor(item))
        output.append("")
    
    # Generate accessories section
    output.append("")
    output.append("## ACCESSORIES")
    output.append("-" * 50)
    output.append("")
    
    accessories = get_all_items_of_type(src_path / 'items' / 'accessories', Accessory)
    for item in accessories:
        output.append(format_accessory(item))
        output.append("")
    
    # Write to file
    docs_path = Path(__file__).parent / 'docs'
    docs_path.mkdir(exist_ok=True)
    
    grimoire_path = docs_path / 'grimoire.md'
    with open(grimoire_path, 'w') as f:
        f.write('\n'.join(output))
    
    print(f"Grimoire generated successfully at: {grimoire_path}")
    return grimoire_path


if __name__ == "__main__":
    generate_grimoire()