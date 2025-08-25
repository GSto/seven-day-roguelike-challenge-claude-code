#!/usr/bin/env python3
"""
Beastiary utility - generates documentation for all monsters in the game.
"""

import os
import sys
import importlib
import inspect
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from monsters.base import Monster


def get_all_monster_classes():
    """Get all monster classes from the monsters directory."""
    monsters = []
    
    # Path to monsters directory
    monsters_path = Path(__file__).parent / 'src' / 'monsters'
    
    # Find all Python files in the monsters directory
    for file_path in monsters_path.glob('*.py'):
        if file_path.name.startswith('__') or file_path.name == 'base.py' or file_path.name == 'factory.py':
            continue
            
        # Build the module path
        module_name = f"monsters.{file_path.stem}"
        
        try:
            # Import the module
            module = importlib.import_module(module_name)
            
            # Find all Monster subclasses in the module
            for name, obj in inspect.getmembers(module):
                if (inspect.isclass(obj) and 
                    issubclass(obj, Monster) and 
                    obj != Monster and
                    not name.startswith('_')):
                    
                    # Try to instantiate to get properties
                    try:
                        # Create temporary instance at 0,0 to extract properties
                        instance = obj(0, 0)
                        
                        # Get the class docstring for description
                        description = ""
                        if obj.__doc__:
                            # Clean up the docstring
                            description = obj.__doc__.strip()
                            # Remove any leading/trailing quotes
                            description = description.replace('"""', '').strip()
                        
                        # If no docstring, try to get from module docstring
                        if not description and module.__doc__:
                            mod_doc = module.__doc__.strip()
                            # Extract first line after module declaration
                            lines = mod_doc.split('\n')
                            for line in lines:
                                if line and not line.startswith('"""'):
                                    description = line.strip()
                                    if description.endswith('.'):
                                        description = description[:-1]
                                    break
                        
                        monsters.append({
                            'name': instance.name,
                            'description': description,
                            'instance': instance,
                            'class': obj
                        })
                    except Exception as e:
                        print(f"Warning: Could not instantiate {name}: {e}")
                        
        except ImportError as e:
            print(f"Warning: Could not import {module_name}: {e}")
    
    # Sort monsters alphabetically by name
    monsters.sort(key=lambda x: x['name'].lower())
    return monsters


def format_monster(monster_data):
    """Format a monster for the beastiary."""
    instance = monster_data['instance']
    description = monster_data['description']
    
    lines = []
    
    # Monster name
    lines.append(f"### {instance.name}")
    
    # Description (if available)
    if description:
        lines.append(f"*{description}*")
    
    lines.append("")
    
    # Core stats
    stats_parts = []
    stats_parts.append(f"**HP:** {instance.stats.max_hp}")
    stats_parts.append(f"**Attack:** {instance.stats.attack}")
    stats_parts.append(f"**Defense:** {instance.stats.defense}")
    stats_parts.append(f"**XP Value:** {instance.xp_value}")
    
    lines.append(" | ".join(stats_parts))
    
    # Advanced stats if they differ from defaults
    advanced_stats = []
    
    if instance.stats.evade != 0.05:  # Default evade is 5%
        advanced_stats.append(f"**Evade:** {instance.stats.evade:.0%}")
    
    if instance.stats.crit != 0.05:  # Default crit is 5%
        advanced_stats.append(f"**Crit:** {instance.stats.crit:.0%}")
    
    if instance.stats.crit_multiplier != 2.0:  # Default crit multiplier is 2x
        advanced_stats.append(f"**Crit Multiplier:** {instance.stats.crit_multiplier}x")
    
    if advanced_stats:
        lines.append(" | ".join(advanced_stats))
    
    # Traits, weaknesses, and resistances
    combat_traits = []
    
    if instance.attack_traits:
        trait_names = [trait.name for trait in instance.attack_traits]
        combat_traits.append(f"**Attacks:** {', '.join(trait_names)}")
    
    if instance.resistances:
        resist_names = [resist.name for resist in instance.resistances]
        combat_traits.append(f"**Resists:** {', '.join(resist_names)}")
    
    if instance.weaknesses:
        weak_names = [weak.name for weak in instance.weaknesses]
        combat_traits.append(f"**Weak to:** {', '.join(weak_names)}")
    
    if combat_traits:
        lines.append("")
        for trait in combat_traits:
            lines.append(trait)
    
    # Visual representation
    lines.append("")
    lines.append(f"**Appearance:** `{instance.character}` (in game)")
    
    return '\n'.join(lines)


def generate_beastiary():
    """Generate the beastiary documentation."""
    output = []
    
    # Header
    output.append("# BEASTIARY")
    output.append("Complete catalog of all monsters in the game")
    output.append("")
    output.append("---")
    output.append("")
    
    # Get all monsters
    monsters = get_all_monster_classes()
    
    if not monsters:
        output.append("No monsters found!")
    else:
        # Add table of contents
        output.append("## Table of Contents")
        output.append("")
        for monster in monsters:
            output.append(f"- [{monster['name']}](#{monster['name'].lower().replace(' ', '-')})")
        output.append("")
        output.append("---")
        output.append("")
        
        # Add monster entries
        output.append("## Monsters")
        output.append("")
        
        for i, monster in enumerate(monsters):
            output.append(format_monster(monster))
            
            # Add separator between monsters (except for last one)
            if i < len(monsters) - 1:
                output.append("")
                output.append("---")
                output.append("")
    
    # Statistics section
    output.append("")
    output.append("---")
    output.append("")
    output.append("## Statistics")
    output.append("")
    output.append(f"**Total Monsters:** {len(monsters)}")
    
    if monsters:
        # Calculate some interesting stats
        avg_hp = sum(m['instance'].stats.max_hp for m in monsters) / len(monsters)
        avg_attack = sum(m['instance'].stats.attack for m in monsters) / len(monsters)
        avg_defense = sum(m['instance'].stats.defense for m in monsters) / len(monsters)
        avg_xp = sum(m['instance'].xp_value for m in monsters) / len(monsters)
        
        weakest = min(monsters, key=lambda m: m['instance'].stats.max_hp)
        strongest = max(monsters, key=lambda m: m['instance'].stats.max_hp)
        most_valuable = max(monsters, key=lambda m: m['instance'].xp_value)
        
        output.append(f"**Average HP:** {avg_hp:.1f}")
        output.append(f"**Average Attack:** {avg_attack:.1f}")
        output.append(f"**Average Defense:** {avg_defense:.1f}")
        output.append(f"**Average XP Value:** {avg_xp:.1f}")
        output.append("")
        output.append(f"**Weakest Monster:** {weakest['name']} ({weakest['instance'].stats.max_hp} HP)")
        output.append(f"**Strongest Monster:** {strongest['name']} ({strongest['instance'].stats.max_hp} HP)")
        output.append(f"**Most Valuable:** {most_valuable['name']} ({most_valuable['instance'].xp_value} XP)")
    
    # Write to file
    docs_path = Path(__file__).parent / 'docs'
    docs_path.mkdir(exist_ok=True)
    
    beastiary_path = docs_path / 'beastiary.md'
    with open(beastiary_path, 'w') as f:
        f.write('\n'.join(output))
    
    print(f"Beastiary generated successfully at: {beastiary_path}")
    print(f"Found {len(monsters)} monsters")
    return beastiary_path


if __name__ == "__main__":
    generate_beastiary()