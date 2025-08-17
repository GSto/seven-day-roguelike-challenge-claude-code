# Project Structure

## Overview
This document describes the organization and structure of the Seven-Day Roguelike codebase after the one-class-per-file refactoring.

## Directory Structure

```
seven-day-roguelike/
├── .claude/                    # Claude AI configuration and documentation
│   └── project-structure.md    # This file
├── plans/                      # Project planning documents
├── specs/                      # Technical specifications
│   └── project_plan.md        # Main project plan with phases
├── src/                        # Source code root
│   ├── main.py                # Entry point
│   ├── game.py                # Game class and main game loop
│   ├── player.py              # Player class
│   ├── ui.py                  # UI class
│   ├── constants.py           # Game constants
│   ├── traits.py              # Trait enum
│   ├── status_effects.py      # StatusEffectType enum
│   │
│   ├── level/                 # Level generation system
│   │   ├── __init__.py        # Exports Level and Room
│   │   ├── level.py           # Level class
│   │   └── room.py            # Room class
│   │
│   ├── monsters/              # Monster system (already one-class-per-file)
│   │   ├── __init__.py        # Monster exports
│   │   ├── base.py            # Monster base class
│   │   ├── factory.py         # Monster generation
│   │   ├── angel.py           # Angel class
│   │   ├── devil.py           # Devil class
│   │   ├── goblin.py          # Goblin class
│   │   ├── horror.py          # Horror class
│   │   ├── orc.py             # Orc class
│   │   ├── phantom.py         # Phantom class
│   │   ├── skeleton.py        # Skeleton class
│   │   ├── troll.py           # Troll class
│   │   └── zombie.py          # Zombie class
│   │
│   ├── enchantments/          # Enchantment system
│   │   ├── __init__.py        # Enchantment exports
│   │   ├── enchantment.py     # Enchantment class
│   │   ├── enchantment_type.py # EnchantmentType enum
│   │   └── utils.py           # Enchantment utility functions
│   │
│   └── items/                 # Item system
│       ├── __init__.py        # Main item exports
│       ├── item.py            # Base Item class
│       ├── consumable.py      # Base Consumable class
│       ├── equipment.py       # Base Equipment class
│       ├── factory.py         # Item generation
│       │
│       ├── weapons/           # Weapon items
│       │   ├── __init__.py    # Weapon exports
│       │   ├── base.py        # Weapon base class
│       │   ├── acid_dagger.py
│       │   ├── axe.py
│       │   ├── big_stick.py
│       │   ├── clair_obscur.py
│       │   ├── clerics_staff.py
│       │   ├── dagger.py
│       │   ├── demon_slayer.py
│       │   ├── feu_glace.py
│       │   ├── gauntlets.py
│       │   ├── katana.py
│       │   ├── longsword.py
│       │   ├── materia_staff.py
│       │   ├── morning_star.py
│       │   ├── pickaxe.py
│       │   ├── rapier.py
│       │   ├── rivers_of_blood.py
│       │   ├── shield.py
│       │   ├── snakes_fang.py
│       │   ├── sword.py
│       │   ├── tower_shield.py
│       │   ├── uchigatana.py
│       │   ├── war_hammer.py
│       │   ├── war_scythe.py
│       │   └── wooden_stick.py
│       │
│       ├── armor/             # Armor items
│       │   ├── __init__.py    # Armor exports
│       │   ├── base.py        # Armor base class
│       │   ├── anti_angel_technology.py
│       │   ├── chain_mail.py
│       │   ├── cloak.py
│       │   ├── coated_plate.py
│       │   ├── dragon_scale.py
│       │   ├── gamblers_vest.py
│       │   ├── leather_armor.py
│       │   ├── minimal_suit.py
│       │   ├── night_cloak.py
│       │   ├── plate_armor.py
│       │   ├── safety_vest.py
│       │   ├── shadow_cloak.py
│       │   ├── skin_suit.py
│       │   ├── sos_armor.py
│       │   ├── spiked_armor.py
│       │   ├── spiked_cuirass.py
│       │   ├── utility_belt.py
│       │   └── white_tshirt.py
│       │
│       ├── accessories/       # Accessory items
│       │   ├── __init__.py    # Accessory exports
│       │   ├── base.py        # Accessory base class
│       │   ├── ring.py        # Ring base class
│       │   ├── necklace.py    # Necklace base class
│       │   └── [34 individual accessory files]
│       │
│       └── consumables/       # Consumable items
│           ├── __init__.py    # Consumable exports
│           ├── foods/         # Food items (10 classes)
│           ├── catalysts/     # Catalyst items (12 classes)
│           ├── boons/         # Boon items (11 classes)
│           └── misc/          # Miscellaneous consumables (7 classes)
│
└── tests/                     # Unit tests
    └── [test files]
```

## File Naming Conventions

1. **Classes**: PascalCase (e.g., `WoodenStick`, `LeatherArmor`)
2. **Files**: snake_case matching the class (e.g., `wooden_stick.py`, `leather_armor.py`)
3. **Directories**: lowercase with underscores for multi-word (e.g., `items/`, `status_effects/`)
4. **Utility files**: Named `utils.py` when containing helper functions

## Import Organization

### Base Classes
- `from items.item import Item`
- `from items.consumable import Consumable`
- `from items.equipment import Equipment`

### Specific Items
- `from items.weapons.sword import Sword`
- `from items.armor.leather_armor import LeatherArmor`
- `from items.accessories.power_ring import PowerRing`
- `from items.consumables.health_potion import HealthPotion`

### Convenience Imports via __init__.py
- `from items import Sword, LeatherArmor, PowerRing`  # Exported through __init__.py

## Utility Functions Location

### Enchantment Utilities (`enchantments/utils.py`)
- `get_random_weapon_enchantment()`
- `get_random_armor_enchantment()`
- `get_weapon_enchantment_by_type(enchantment_type)`
- `get_armor_enchantment_by_type(enchantment_type)`
- `get_random_enchantment()`
- `get_enchantment_by_type(enchantment_type)`
- `should_spawn_with_enchantment()`
- `should_armor_spawn_with_enchantment()`

### Item Factory (`items/factory.py`)
- `create_random_item_for_level(level_num, x, y)`

### Monster Factory (`monsters/factory.py`)
- `create_random_monster(level_num, x, y)`
- `create_boss_monster(x, y)`

## Key Design Principles

1. **One Class Per File**: Every class has its own file for maximum clarity
2. **Logical Grouping**: Related classes are grouped in subdirectories
3. **Base Classes**: Abstract base classes are in `base.py` files
4. **Utility Functions**: Helper functions are in `utils.py` files
5. **Clean Exports**: `__init__.py` files provide clean import interfaces
6. **No Circular Dependencies**: Import structure prevents circular dependencies

## Benefits of This Structure

1. **Easy Navigation**: Find any class by its name in the filesystem
2. **Clear Dependencies**: Import statements show exact dependencies
3. **Parallel Development**: Multiple developers can work on different items without conflicts
4. **Maintainability**: Changes to one class don't affect unrelated classes
5. **Testing**: Each class can be tested in isolation
6. **Documentation**: Each file can have its own focused documentation

## Migration Notes

When refactoring from the old structure to this new structure:

1. Start with leaf nodes (items) that have no dependencies
2. Work up to base classes
3. Update imports incrementally
4. Run tests after each major change
5. Commit frequently to allow rollback if needed

## Future Considerations

1. Consider adding type hints to all function signatures
2. Consider using dataclasses for items with many attributes
3. Consider adding abstract base classes with formal interfaces
4. Consider adding a `common/` directory for shared utilities