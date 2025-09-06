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
from items.pickups.pickup import Pickup


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


def format_pickup(item_data):
    """Format a pickup item for the grimoire."""
    instance = item_data['instance']
    lines = []
    
    lines.append(f"{instance.name}")
    
    # Add description
    if instance.description:
        lines.append(instance.description)
    
    # Try to determine the pickup effect from common attributes
    effects = []
    if hasattr(instance, 'heal_amount') and instance.heal_amount > 0:
        effects.append(f"Instantly heals {instance.heal_amount} HP")
    
    if hasattr(instance, 'xp_amount') and instance.xp_amount > 0:
        effects.append(f"Instantly grants {instance.xp_amount} XP")
    
    # For shell tokens or other special effects, try to parse from description or class name
    if 'token' in instance.name.lower():
        effects.append("Special pickup effect")
    
    if effects:
        lines.append(f"Effect: {'; '.join(effects)}")
    
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
    
    # Generate pickups section
    output.append("")
    output.append("## PICKUPS")
    output.append("-" * 50)
    output.append("")
    
    pickups = get_all_items_of_type(src_path / 'items' / 'pickups', Pickup)
    for item in pickups:
        output.append(format_pickup(item))
        output.append("")
    
    # Generate statistics section
    output.append("")
    output.append("---")
    output.append("")
    output.append("## STATISTICS")
    output.append("")
    
    # Item counts
    output.append("### Item Counts")
    output.append(f"**Total Items:** {len(consumables) + len(weapons) + len(armor) + len(accessories) + len(pickups)}")
    output.append(f"- **Consumables:** {len(consumables)}")
    output.append(f"- **Weapons:** {len(weapons)}")
    output.append(f"- **Armor:** {len(armor)}")
    output.append(f"- **Accessories:** {len(accessories)}")
    output.append(f"- **Pickups:** {len(pickups)}")
    output.append("")
    
    # Analyze consumable types
    catalysts = [c for c in consumables if 'catalyst' in c['name'].lower()]
    boons = [c for c in consumables if 'boon' in c['name'].lower()]
    potions = [c for c in consumables if 'potion' in c['name'].lower() or 'elixir' in c['name'].lower()]
    foods = [c for c in consumables if any(food in c['name'].lower() for food in ['beef', 'chicken', 'carrot', 'salmon', 'mushroom'])]
    
    output.append("### Consumable Breakdown")
    output.append(f"- **Catalysts (Permanent):** {len(catalysts)}")
    output.append(f"- **Boons (Enchantments):** {len(boons)}")
    output.append(f"- **Potions/Elixirs:** {len(potions)}")
    output.append(f"- **Food Items:** {len(foods)}")
    output.append("")
    
    # Analyze weapon traits
    weapon_traits = {}
    for weapon in weapons:
        if hasattr(weapon['instance'], 'attack_traits') and weapon['instance'].attack_traits:
            for trait in weapon['instance'].attack_traits:
                trait_name = trait.name
                if trait_name not in weapon_traits:
                    weapon_traits[trait_name] = []
                weapon_traits[trait_name].append(weapon['name'])
    
    output.append("### Weapon Attack Traits")
    if weapon_traits:
        # Sort by frequency
        sorted_traits = sorted(weapon_traits.items(), key=lambda x: len(x[1]), reverse=True)
        for trait_name, weapon_names in sorted_traits:
            output.append(f"- **{trait_name}:** {len(weapon_names)} weapons")
            if len(weapon_names) <= 5:  # Show weapon names if not too many
                output.append(f"  - {', '.join(weapon_names)}")
    else:
        output.append("No weapon traits found")
    output.append("")
    
    # Analyze armor traits
    armor_resistances = {}
    armor_weaknesses = {}
    
    for armor_item in armor:
        if hasattr(armor_item['instance'], 'resistances') and armor_item['instance'].resistances:
            for res in armor_item['instance'].resistances:
                res_name = res.name
                if res_name not in armor_resistances:
                    armor_resistances[res_name] = []
                armor_resistances[res_name].append(armor_item['name'])
        
        if hasattr(armor_item['instance'], 'weaknesses') and armor_item['instance'].weaknesses:
            for weak in armor_item['instance'].weaknesses:
                weak_name = weak.name
                if weak_name not in armor_weaknesses:
                    armor_weaknesses[weak_name] = []
                armor_weaknesses[weak_name].append(armor_item['name'])
    
    output.append("### Armor Resistances")
    if armor_resistances:
        sorted_res = sorted(armor_resistances.items(), key=lambda x: len(x[1]), reverse=True)
        for res_name, armor_names in sorted_res:
            output.append(f"- **{res_name}:** {len(armor_names)} armors")
            if len(armor_names) <= 3:
                output.append(f"  - {', '.join(armor_names)}")
    else:
        output.append("No armor resistances found")
    output.append("")
    
    if armor_weaknesses:
        output.append("### Armor Weaknesses")
        sorted_weak = sorted(armor_weaknesses.items(), key=lambda x: len(x[1]), reverse=True)
        for weak_name, armor_names in sorted_weak:
            output.append(f"- **{weak_name}:** {len(armor_names)} armors")
            if len(armor_names) <= 3:
                output.append(f"  - {', '.join(armor_names)}")
        output.append("")
    
    # Analyze accessory traits
    accessory_traits = {}
    accessory_resistances = {}
    
    for acc in accessories:
        if hasattr(acc['instance'], 'attack_traits') and acc['instance'].attack_traits:
            for trait in acc['instance'].attack_traits:
                trait_name = trait.name
                if trait_name not in accessory_traits:
                    accessory_traits[trait_name] = []
                accessory_traits[trait_name].append(acc['name'])
        
        if hasattr(acc['instance'], 'resistances') and acc['instance'].resistances:
            for res in acc['instance'].resistances:
                res_name = res.name
                if res_name not in accessory_resistances:
                    accessory_resistances[res_name] = []
                accessory_resistances[res_name].append(acc['name'])
    
    if accessory_traits or accessory_resistances:
        output.append("### Accessory Traits")
        if accessory_traits:
            sorted_traits = sorted(accessory_traits.items(), key=lambda x: len(x[1]), reverse=True)
            for trait_name, acc_names in sorted_traits:
                output.append(f"- **{trait_name} (Attack):** {len(acc_names)} accessories")
                if len(acc_names) <= 3:
                    output.append(f"  - {', '.join(acc_names)}")
        
        if accessory_resistances:
            sorted_res = sorted(accessory_resistances.items(), key=lambda x: len(x[1]), reverse=True)
            for res_name, acc_names in sorted_res:
                output.append(f"- **{res_name} (Resist):** {len(acc_names)} accessories")
                if len(acc_names) <= 3:
                    output.append(f"  - {', '.join(acc_names)}")
        output.append("")
    
    # Highest stat items
    output.append("### Notable Items")
    
    # Highest attack weapon
    if weapons:
        highest_attack = max(weapons, key=lambda w: w['instance'].attack_bonus if hasattr(w['instance'], 'attack_bonus') else 0)
        output.append(f"**Highest Attack Weapon:** {highest_attack['name']} (+{highest_attack['instance'].attack_bonus} attack)")
    
    # Highest defense armor
    if armor:
        highest_defense = max(armor, key=lambda a: a['instance'].defense_bonus if hasattr(a['instance'], 'defense_bonus') else 0)
        output.append(f"**Highest Defense Armor:** {highest_defense['name']} (+{highest_defense['instance'].defense_bonus} defense)")
    
    # Most valuable accessory (by total stat bonuses)
    if accessories:
        def acc_value(acc):
            inst = acc['instance']
            value = 0
            if hasattr(inst, 'attack_bonus'): value += inst.attack_bonus
            if hasattr(inst, 'defense_bonus'): value += inst.defense_bonus
            if hasattr(inst, 'fov_bonus'): value += inst.fov_bonus
            if hasattr(inst, 'health_aspect_bonus'): value += inst.health_aspect_bonus * 10
            if hasattr(inst, 'evade_bonus'): value += inst.evade_bonus * 100
            if hasattr(inst, 'crit_bonus'): value += inst.crit_bonus * 100
            if hasattr(inst, 'crit_multiplier_bonus'): value += inst.crit_multiplier_bonus * 10
            return value
        
        best_acc = max(accessories, key=acc_value)
        output.append(f"**Most Powerful Accessory:** {best_acc['name']}")
    
    # Write to file
    docs_path = Path(__file__).parent / 'docs'
    docs_path.mkdir(exist_ok=True)
    
    grimoire_path = docs_path / 'grimoire.md'
    with open(grimoire_path, 'w') as f:
        f.write('\n'.join(output))
    
    print(f"Grimoire generated successfully at: {grimoire_path}")
    print(f"Total items: {len(consumables) + len(weapons) + len(armor) + len(accessories) + len(pickups)}")
    return grimoire_path


if __name__ == "__main__":
    generate_grimoire()