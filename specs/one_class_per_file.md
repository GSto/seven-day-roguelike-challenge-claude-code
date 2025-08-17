# One Class Per File Refactoring Specification

## Overview
Refactor the entire codebase to enforce a strict one-class-per-file rule to improve maintainability, readability, and follow Python best practices. This refactoring involves reorganizing the existing code structure without changing functionality.

## 1. Directory Structure Reorganization

### Todo List:
1. **Create new directory structure**
   - [ ] Create `src/items/weapons/` directory for weapon classes
   - [ ] Create `src/items/armor/` directory for armor classes  
   - [ ] Create `src/items/accessories/` directory for accessory classes
   - [ ] Create `src/items/consumables/` directory for consumable classes
   - [ ] Create `src/enchantments/` directory for enchantment classes
   - [ ] Create `src/enchantments/utils.py` for enchantment utility functions
   - [ ] Create `src/level/` directory for level-related classes
   - [ ] Create `src/level/room.py` for Room class
   - [ ] Create `src/level/level.py` for Level class

## 2. Items Refactoring

### Weapons (25 classes to separate)
2. **Split weapons.py into individual files in items/weapons/**
   - [ ] Create `items/weapons/base.py` with Weapon base class
   - [ ] Create `items/weapons/wooden_stick.py` with WoodenStick class
   - [ ] Create `items/weapons/dagger.py` with Dagger class
   - [ ] Create `items/weapons/shield.py` with Shield class
   - [ ] Create `items/weapons/tower_shield.py` with TowerShield class
   - [ ] Create `items/weapons/sword.py` with Sword class
   - [ ] Create `items/weapons/longsword.py` with Longsword class
   - [ ] Create `items/weapons/war_scythe.py` with WarScythe class
   - [ ] Create `items/weapons/axe.py` with Axe class
   - [ ] Create `items/weapons/morning_star.py` with MorningStar class
   - [ ] Create `items/weapons/war_hammer.py` with WarHammer class
   - [ ] Create `items/weapons/katana.py` with Katana class
   - [ ] Create `items/weapons/uchigatana.py` with Uchigatana class
   - [ ] Create `items/weapons/rivers_of_blood.py` with RiversOfBlood class
   - [ ] Create `items/weapons/clerics_staff.py` with ClericsStaff class
   - [ ] Create `items/weapons/materia_staff.py` with MateriaStaff class
   - [ ] Create `items/weapons/pickaxe.py` with Pickaxe class
   - [ ] Create `items/weapons/gauntlets.py` with Gauntlets class
   - [ ] Create `items/weapons/demon_slayer.py` with DemonSlayer class
   - [ ] Create `items/weapons/snakes_fang.py` with SnakesFang class
   - [ ] Create `items/weapons/rapier.py` with Rapier class
   - [ ] Create `items/weapons/acid_dagger.py` with AcidDagger class
   - [ ] Create `items/weapons/clair_obscur.py` with ClairObscur class
   - [ ] Create `items/weapons/feu_glace.py` with FeuGlace class
   - [ ] Create `items/weapons/big_stick.py` with BigStick class
   - [ ] Update `items/weapons/__init__.py` to export all weapon classes

### Armor (19 classes to separate)
3. **Split armor.py into individual files in items/armor/**
   - [ ] Create `items/armor/base.py` with Armor base class
   - [ ] Create `items/armor/white_tshirt.py` with WhiteTShirt class
   - [ ] Create `items/armor/leather_armor.py` with LeatherArmor class
   - [ ] Create `items/armor/safety_vest.py` with SafetyVest class
   - [ ] Create `items/armor/cloak.py` with Cloak class
   - [ ] Create `items/armor/night_cloak.py` with NightCloak class
   - [ ] Create `items/armor/shadow_cloak.py` with ShadowCloak class
   - [ ] Create `items/armor/gamblers_vest.py` with GamblersVest class
   - [ ] Create `items/armor/skin_suit.py` with SkinSuit class
   - [ ] Create `items/armor/minimal_suit.py` with MinimalSuit class
   - [ ] Create `items/armor/chain_mail.py` with ChainMail class
   - [ ] Create `items/armor/plate_armor.py` with PlateArmor class
   - [ ] Create `items/armor/dragon_scale.py` with DragonScale class
   - [ ] Create `items/armor/spiked_armor.py` with SpikedArmor class
   - [ ] Create `items/armor/coated_plate.py` with CoatedPlate class
   - [ ] Create `items/armor/anti_angel_technology.py` with AntiAngelTechnology class
   - [ ] Create `items/armor/spiked_cuirass.py` with SpikedCuirass class
   - [ ] Create `items/armor/utility_belt.py` with UtilityBelt class
   - [ ] Create `items/armor/sos_armor.py` with SOSArmor class
   - [ ] Update `items/armor/__init__.py` to export all armor classes

### Accessories (37 classes to separate)
4. **Split accessories.py into individual files in items/accessories/**
   - [ ] Create `items/accessories/base.py` with Accessory base class
   - [ ] Create `items/accessories/ring.py` with Ring base class
   - [ ] Create `items/accessories/necklace.py` with Necklace base class
   - [ ] Create individual files for each of the remaining 34 accessory classes
   - [ ] Update `items/accessories/__init__.py` to export all accessory classes

### Consumables (multiple files with many classes)
5. **Reorganize consumable items into items/consumables/**
   - [ ] Move each consumable class from `foods.py` to individual files (10 classes)
   - [ ] Move each consumable class from `catalysts.py` to individual files (12 classes)
   - [ ] Move each consumable class from `boons.py` to individual files (11 classes)
   - [ ] Move each consumable class from `consumables.py` to individual files (7 classes)
   - [ ] Update `items/consumables/__init__.py` to export all consumable classes

## 3. Enchantments Refactoring

6. **Split enchantments.py into separate class files**
   - [ ] Create `enchantments/enchantment.py` with Enchantment class
   - [ ] Create `enchantments/enchantment_type.py` with EnchantmentType enum
   - [ ] Create `enchantments/utils.py` with all utility functions:
     - get_random_weapon_enchantment()
     - get_random_armor_enchantment()
     - get_weapon_enchantment_by_type()
     - get_armor_enchantment_by_type()
     - get_random_enchantment()
     - get_enchantment_by_type()
     - should_spawn_with_enchantment()
     - should_armor_spawn_with_enchantment()
   - [ ] Update imports across the codebase

## 4. Level System Refactoring

7. **Split level.py into separate files**
   - [ ] Create `level/room.py` with Room class
   - [ ] Create `level/level.py` with Level class
   - [ ] Create `level/__init__.py` to export both classes
   - [ ] Update all imports from `level` to use new structure

## 5. Import Updates and Testing

8. **Update all imports throughout the codebase**
   - [ ] Update all imports in game.py
   - [ ] Update all imports in player.py
   - [ ] Update all imports in ui.py
   - [ ] Update all imports in factory files
   - [ ] Update all test file imports
   - [ ] Update all __init__.py files to properly export classes

9. **Verify refactoring with tests**
   - [ ] Run all existing unit tests to ensure no functionality broken
   - [ ] Fix any import errors or circular dependencies
   - [ ] Test game manually to ensure everything works
   - [ ] Create git commit after each major refactoring step

## 6. Documentation

10. **Create project structure documentation**
    - [ ] Create `.claude/project-structure.md` documenting the new file organization
    - [ ] Update CLAUDE.md to import the project structure documentation
    - [ ] Document any utility functions and their locations
    - [ ] Update README if needed to reflect new structure

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

- [ ] All Python files contain exactly one class (except __init__.py and utils.py)
- [ ] All tests pass without modification
- [ ] Game functionality remains unchanged
- [ ] Imports are clean and organized
- [ ] Documentation is updated to reflect new structure
- [ ] Code can be easily navigated by filename