# One Class Per File Refactoring Specification

## Overview
Refactor the entire codebase to enforce a strict one-class-per-file rule to improve maintainability, readability, and follow Python best practices. This refactoring involves reorganizing the existing code structure without changing functionality.

## 1. Directory Structure Reorganization

### Todo List:
1. **Create new directory structure**
   - [x] Create `src/items/weapons/` directory for weapon classes
   - [x] Create `src/items/armor/` directory for armor classes  
   - [x] Create `src/items/accessories/` directory for accessory classes
   - [x] Create `src/items/consumables/` directory for consumable classes
   - [x] Create `src/enchantments/` directory for enchantment classes
   - [x] Create `src/enchantments/utils.py` for enchantment utility functions
   - [x] Create `src/level/` directory for level-related classes
   - [x] Create `src/level/room.py` for Room class
   - [x] Create `src/level/level.py` for Level class

## 2. Items Refactoring

### Weapons (25 classes to separate)
2. **Split weapons.py into individual files in items/weapons/**
   - [x] Create `items/weapons/base.py` with Weapon base class
   - [x] Create `items/weapons/wooden_stick.py` with WoodenStick class
   - [x] Create `items/weapons/dagger.py` with Dagger class
   - [x] Create `items/weapons/shield.py` with Shield class
   - [x] Create `items/weapons/tower_shield.py` with TowerShield class
   - [x] Create `items/weapons/sword.py` with Sword class
   - [x] Create `items/weapons/longsword.py` with Longsword class
   - [x] Create `items/weapons/war_scythe.py` with WarScythe class
   - [x] Create `items/weapons/axe.py` with Axe class
   - [x] Create `items/weapons/morning_star.py` with MorningStar class
   - [x] Create `items/weapons/war_hammer.py` with WarHammer class
   - [x] Create `items/weapons/katana.py` with Katana class
   - [x] Create `items/weapons/uchigatana.py` with Uchigatana class
   - [x] Create `items/weapons/rivers_of_blood.py` with RiversOfBlood class
   - [x] Create `items/weapons/clerics_staff.py` with ClericsStaff class
   - [x] Create `items/weapons/materia_staff.py` with MateriaStaff class
   - [x] Create `items/weapons/pickaxe.py` with Pickaxe class
   - [x] Create `items/weapons/gauntlets.py` with Gauntlets class
   - [x] Create `items/weapons/demon_slayer.py` with DemonSlayer class
   - [x] Create `items/weapons/snakes_fang.py` with SnakesFang class
   - [x] Create `items/weapons/rapier.py` with Rapier class
   - [x] Create `items/weapons/acid_dagger.py` with AcidDagger class
   - [x] Create `items/weapons/clair_obscur.py` with ClairObscur class
   - [x] Create `items/weapons/feu_glace.py` with FeuGlace class
   - [x] Create `items/weapons/big_stick.py` with BigStick class
   - [x] Update `items/weapons/__init__.py` to export all weapon classes

### Armor (19 classes to separate)
3. **Split armor.py into individual files in items/armor/**
   - [x] Create `items/armor/base.py` with Armor base class
   - [x] Create `items/armor/white_tshirt.py` with WhiteTShirt class
   - [x] Create `items/armor/leather_armor.py` with LeatherArmor class
   - [x] Create `items/armor/safety_vest.py` with SafetyVest class
   - [x] Create `items/armor/cloak.py` with Cloak class
   - [x] Create `items/armor/night_cloak.py` with NightCloak class
   - [x] Create `items/armor/shadow_cloak.py` with ShadowCloak class
   - [x] Create `items/armor/gamblers_vest.py` with GamblersVest class
   - [x] Create `items/armor/skin_suit.py` with SkinSuit class
   - [x] Create `items/armor/minimal_suit.py` with MinimalSuit class
   - [x] Create `items/armor/chain_mail.py` with ChainMail class
   - [x] Create `items/armor/plate_armor.py` with PlateArmor class
   - [x] Create `items/armor/dragon_scale.py` with DragonScale class
   - [x] Create `items/armor/spiked_armor.py` with SpikedArmor class
   - [x] Create `items/armor/coated_plate.py` with CoatedPlate class
   - [x] Create `items/armor/anti_angel_technology.py` with AntiAngelTechnology class
   - [x] Create `items/armor/spiked_cuirass.py` with SpikedCuirass class
   - [x] Create `items/armor/utility_belt.py` with UtilityBelt class
   - [x] Create `items/armor/sos_armor.py` with SOSArmor class
   - [x] Update `items/armor/__init__.py` to export all armor classes

### Accessories (37 classes to separate)
4. **Split accessories.py into individual files in items/accessories/**
   - [x] Create `items/accessories/base.py` with Accessory base class
   - [x] Create `items/accessories/ring.py` with Ring base class
   - [x] Create `items/accessories/necklace.py` with Necklace base class
   - [x] Create individual files for each of the remaining 34 accessory classes
   - [x] Update `items/accessories/__init__.py` to export all accessory classes

### Consumables (multiple files with many classes)
5. **Reorganize consumable items into items/consumables/**
   - [x] Move each consumable class from `foods.py` to individual files (10 classes)
   - [x] Move each consumable class from `catalysts.py` to individual files (12 classes)
   - [x] Move each consumable class from `boons.py` to individual files (11 classes)
   - [x] Move each consumable class from `consumables.py` to individual files (7 classes)
   - [x] Update `items/consumables/__init__.py` to export all consumable classes

## 3. Enchantments Refactoring

6. **Split enchantments.py into separate class files**
   - [x] Create `enchantments/enchantment.py` with Enchantment class
   - [x] Create `enchantments/enchantment_type.py` with EnchantmentType enum
   - [x] Create `enchantments/utils.py` with all utility functions:
     - get_random_weapon_enchantment()
     - get_random_armor_enchantment()
     - get_weapon_enchantment_by_type()
     - get_armor_enchantment_by_type()
     - get_random_enchantment()
     - get_enchantment_by_type()
     - should_spawn_with_enchantment()
     - should_armor_spawn_with_enchantment()
   - [x] Update imports across the codebase

## 4. Level System Refactoring

7. **Split level.py into separate files**
   - [x] Create `level/room.py` with Room class
   - [x] Create `level/level.py` with Level class
   - [x] Create `level/__init__.py` to export both classes
   - [x] Update all imports from `level` to use new structure

## 5. Import Updates and Testing

8. **Update all imports throughout the codebase**
   - [x] Update all imports in game.py
   - [x] Update all imports in player.py
   - [x] Update all imports in ui.py
   - [x] Update all imports in factory files
   - [x] Update all test file imports
   - [x] Update all __init__.py files to properly export classes

9. **Verify refactoring with tests**
   - [x] Run all existing unit tests to ensure no functionality broken
   - [x] Fix any import errors or circular dependencies
   - [x] Test game manually to ensure everything works
   - [x] Create git commit after each major refactoring step

## 6. Documentation

10. **Create project structure documentation**
    - [x] Create `.claude/project-structure.md` documenting the new file organization
    - [x] Update CLAUDE.md to import the project structure documentation
    - [x] Document any utility functions and their locations
    - [x] Update README if needed to reflect new structure

## Refactoring Principles

1. **One Class Per File**: Each Python file should contain exactly one class
2. **Descriptive Filenames**: Use snake_case filenames that match the class name
3. **Logical Organization**: Group related classes in appropriate subdirectories
4. **Utility Functions**: Extract standalone functions into `utils.py` files
5. **Clean Imports**: Use `__init__.py` files to provide clean import interfaces
6. **No Functionality Changes**: This refactoring should not change any game behavior

## Expected Benefits

- **Improved Maintainability**: Easier to find and modify specific classes
- **Better Code Navigation**: IDEs can better navigate one-class-per-file structures
- **Reduced Merge Conflicts**: Smaller files reduce likelihood of conflicts
- **Clearer Dependencies**: Import statements clearly show dependencies
- **Follows Python Best Practices**: Aligns with PEP 8 and community standards

## Implementation Order

1. Start with items refactoring (largest impact)
2. Then enchantments (utility functions extraction)
3. Then level system (simple two-class split)
4. Update imports incrementally
5. Test after each major step
6. Document the final structure

## Current File Analysis

### Files with Multiple Classes (Priority Targets)
- `items/weapons.py`: 25 classes
- `items/armor.py`: 19 classes  
- `items/accessories.py`: 37 classes
- `items/foods.py`: 10 classes
- `items/catalysts.py`: 12 classes
- `items/boons.py`: 11 classes
- `items/consumables.py`: 7 classes
- `items/enchantments.py`: 2 classes + 8 functions
- `level.py`: 2 classes

### Total Refactoring Scope
- **~143 total classes** to be separated into individual files
- **8 utility functions** to be extracted into utils.py
- **9 main directories** to be created or reorganized

## Success Criteria

- [x] All Python files contain exactly one class (except __init__.py and utils.py)
- [x] All tests pass without modification
- [x] Game functionality remains unchanged
- [x] Imports are clean and organized
- [x] Documentation is updated to reflect new structure
- [x] Code can be easily navigated by filename