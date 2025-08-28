# Item Pool System Specification

## Overview

This specification describes a generalized pool-based item generation system for weapons, armor, accessories, and consumables, based on the successful monster pool approach. The system will manage item spawning with smooth difficulty curves and specific uniqueness constraints.

## Design Goals

1. **Difficulty-Appropriate Spawning**: Items should match the difficulty and progression of each level
2. **Uniqueness Constraints**: 
   - Weapons: Only one instance of each weapon type per floor
   - Armor: Only one instance of each armor type per floor  
   - Accessories: Only one instance of each accessory type per game (globally unique)
   - Consumables: Can have multiple instances (no uniqueness constraint)
3. **Smooth Difficulty Curves**: Items should phase in and out gradually as player progresses
4. **Weighted Spawning**: Use probability weights based on rarity, level appropriateness, and target difficulty
5. **No Backwards Compatibility**: Replace the existing factory system entirely

## Core Components

### 1. ItemSpec Data Class

```python
@dataclass
class ItemSpec:
    """Specification for an item type including difficulty and spawn rules."""
    item_class: Type           # The item class to instantiate
    item_type: str             # 'weapon', 'armor', 'accessory', 'consumable'
    difficulty_rating: float   # Relative difficulty/power (1.0 = baseline)
    min_level: int            # Earliest level this item can appear
    max_level: Optional[int]  # Latest level (None = no limit)
    rarity: float            # Base spawn weight (higher = more common)
    unique_per_floor: bool   # True for weapons/armor
    unique_per_game: bool    # True for accessories
    tags: List[str] = field(default_factory=list)  # Optional tags for special handling
```

### 2. ItemPool Class

```python
class ItemPool:
    """Manages item spawning with smooth difficulty curves and uniqueness tracking."""
    
    def __init__(self):
        self.weapon_specs: List[ItemSpec]
        self.armor_specs: List[ItemSpec]
        self.accessory_specs: List[ItemSpec]
        self.consumable_specs: List[ItemSpec]
        
        # Tracking for uniqueness constraints
        self.floor_spawned_weapons: Dict[int, Set[Type]] = {}  # Per-floor tracking
        self.floor_spawned_armor: Dict[int, Set[Type]] = {}    # Per-floor tracking
        self.game_spawned_accessories: Set[Type] = set()       # Global tracking
        
        # Cache for performance
        self._level_pools: Dict[str, List[tuple]] = {}
```

### 3. Key Methods

#### 3.1 Item Creation
```python
def create_item_for_level(self, level: int, x: int, y: int, 
                         item_type: Optional[str] = None,
                         force_type: bool = False) -> Item:
    """
    Create an appropriate item for the given level.
    
    Args:
        level: Current dungeon level
        x, y: Position for the item
        item_type: Optional specific type ('weapon', 'armor', 'accessory', 'consumable')
        force_type: If True, must spawn the specified type (no fallback)
    
    Returns:
        An item instance appropriate for the level
    """
```

#### 3.2 Uniqueness Checking
```python
def is_item_available(self, item_spec: ItemSpec, level: int) -> bool:
    """
    Check if an item can spawn based on uniqueness constraints.
    
    - Weapons/Armor: Check if already spawned on current floor
    - Accessories: Check if already spawned in the game
    - Consumables: Always available
    """
```

#### 3.3 Weight Calculation
```python
def calculate_spawn_weight(self, item_spec: ItemSpec, level: int, 
                          target_difficulty: float) -> float:
    """
    Calculate spawn weight considering:
    - Base rarity
    - Difficulty matching (prefer items near target difficulty)
    - Level transition smoothing (phase in/out gradually)
    - Uniqueness availability
    """
```

#### 3.4 Floor Transition
```python
def start_new_floor(self, level: int):
    """Reset per-floor tracking for weapons and armor."""
    self.floor_spawned_weapons[level] = set()
    self.floor_spawned_armor[level] = set()
```

## Item Specifications

### Difficulty Ratings Guidelines

- **1.0 - 2.0**: Early game items (levels 1-3)
- **2.0 - 3.5**: Mid game items (levels 3-6)
- **3.5 - 5.0**: Late game items (levels 6-9)
- **5.0+**: End game items (levels 9-10)

### Rarity Weights
Create 3 new constants and use these for rarites, from most to least common: RARITY_COMMON, RARITY_UNCOMMON, RARITY_RARE. use these when creating all item specifications. 

### Example Item Specifications

```python
# Weapons
ItemSpec(Dagger, 'weapon', 1.0, 1, 4, 1.0, unique_per_floor=True, unique_per_game=False),
ItemSpec(Sword, 'weapon', 1.5, 1, 5, 0.9, unique_per_floor=True, unique_per_game=False),
ItemSpec(WarHammer, 'weapon', 4.0, 7, None, 0.5, unique_per_floor=True, unique_per_game=False),
ItemSpec(DemonSlayer, 'weapon', 10.0, 10, 10, 1.0, unique_per_floor=True, unique_per_game=False, tags=['boss_weapon']),

# Armor
ItemSpec(LeatherArmor, 'armor', 1.0, 1, 4, 1.0, unique_per_floor=True, unique_per_game=False),
ItemSpec(PlateArmor, 'armor', 4.0, 6, None, 0.6, unique_per_floor=True, unique_per_game=False),

# Accessories (unique per game)
ItemSpec(PowerRing, 'accessory', 2.0, 3, 7, 0.8, unique_per_floor=False, unique_per_game=True),
ItemSpec(GreaterPowerRing, 'accessory', 4.0, 6, None, 0.5, unique_per_floor=False, unique_per_game=True),
ItemSpec(GodsEye, 'accessory', 5.0, 8, None, 0.3, unique_per_floor=False, unique_per_game=True, tags=['legendary']),

# Consumables (no uniqueness)
ItemSpec(HealthPotion, 'consumable', 1.0, 1, None, 1.5, unique_per_floor=False, unique_per_game=False),
ItemSpec(Elixir, 'consumable', 5.0, 9, None, 0.4, unique_per_floor=False, unique_per_game=False),
```

## Special Handling

### 1. Level 10 Boss Items
- DemonSlayer weapon should have extremely high spawn weight on level 10
- Special boss-tier items can be tagged with 'boss_weapon', 'boss_armor', etc.

### 2. Enchantments
- Enchantment chance increases with level difficulty
- Enchantment system remains separate but can be integrated:
```python
def apply_enchantment_chance(self, item: Item, level: int):
    """Apply enchantment based on level-appropriate chance."""
    if hasattr(item, 'add_enchantment'):
        chance = min(0.5, 0.1 + (level * 0.05))  # 10% at level 1, up to 50%
        if random.random() < chance:
            # Apply appropriate enchantment
```

### 3. Item Distribution Control
```python
def get_item_type_weights(self, level: int) -> Dict[str, float]:
    """
    Return weights for item type selection based on level.
    
    Example:
    - Level 1-2: {'consumable': 0.6, 'weapon': 0.25, 'armor': 0.15, 'accessory': 0.0}
    - Level 3-5: {'consumable': 0.5, 'weapon': 0.2, 'armor': 0.15, 'accessory': 0.15}
    - Level 6-9: {'consumable': 0.4, 'weapon': 0.2, 'armor': 0.2, 'accessory': 0.2}
    """
```

## Implementation Plan

### Phase 1: Core System
1. Create `src/items/pool.py` with ItemSpec and ItemPool classes
2. Implement uniqueness tracking mechanisms
3. Implement weight calculation and item selection logic

### Phase 2: Item Specifications
1. Convert all existing items to ItemSpec format
2. Assign appropriate difficulty ratings and level ranges
3. Set uniqueness constraints per item type

### Phase 3: Integration
1. Replace `create_random_item_for_level` in factory.py with pool system
2. Update level generation to call `start_new_floor` when generating new levels
3. Update save/load system to persist uniqueness tracking

### Phase 4: Testing
1. Create comprehensive tests for uniqueness constraints
2. Test difficulty curves and spawn distributions
3. Verify special cases (level 10 boss items, etc.)

## Benefits Over Current System

1. **Better Difficulty Scaling**: Items naturally match level difficulty rather than hard-coded tiers
2. **Uniqueness Guarantees**: No duplicate weapons/armor on same floor, truly unique accessories
3. **Smoother Transitions**: Items phase in/out gradually rather than sudden tier changes
4. **More Flexible**: Easy to add new items with appropriate specifications
5. **Performance**: Cached pools for better performance
6. **Maintainable**: Single source of truth for item spawning logic

## Migration Notes

### Files to Modify
- `src/items/factory.py` - Replace with pool system interface
- `src/level/level.py` - Update to use new pool system and track floor transitions
- `src/game.py` - Update save/load for uniqueness tracking
- All test files using item factory

### Data to Preserve
- Game state must track spawned accessories globally
- Save files need to store uniqueness tracking data

## Testing Requirements

1. **Unit Tests**
   - Test uniqueness constraints enforcement
   - Test weight calculations
   - Test difficulty curve progression
   - Test floor transition resets

2. **Integration Tests**
   - Verify items spawn appropriately per level
   - Verify no duplicate weapons/armor on same floor
   - Verify accessories only spawn once per game
   - Verify level 10 boss item spawning

3. **Statistical Tests**
   - Analyze spawn distributions across many iterations
   - Verify difficulty curves match expectations
   - Check rarity distributions