# Architecture Documentation

## Overview

This is a complete roguelike game built in Python using the tcod library, following traditional 7DRL challenge conventions. The architecture follows object-oriented design principles with a strong emphasis on modularity, maintainability, and the **one-class-per-file** rule.

## Core Architecture Principles

1. **Object-Oriented Design**: Heavy use of inheritance and composition
2. **Event-Driven System**: Equipment and items respond to game events
3. **Component-Based Entities**: Entities (players/monsters) use stats, traits, and status effects
4. **Data-Driven Content**: Items, monsters, and levels are defined through structured data
5. **Separation of Concerns**: Clear boundaries between game logic, UI, and data

## Directory Structure

```
seven-day-roguelike/
├── src/                    # Main source code
│   ├── enchantments/       # Enchantments that can be applied to weapons and armor
│   ├── items/              # Complete item system
│   │   ├── weapons/        # weapon classes (swords, axes, staves, etc.)
│   │   ├── armor/          # armor classes (robes, leather, chain, plate)
│   │   ├── accessories/    # accessory classes (rings, amulets, belts)
│   │   ├── consumables/    # consumable items (foods, catalysts, boons)
│   │   └── pickups/        # Special pickup items (gold, keys, etc.)
│   ├── level/              # Level generation and management
│   └── monsters/           # Monster definitions and AI
├── tests/                  # Comprehensive unit tests
├── specs/                  # Technical specifications
├── plans/                  # Development roadmaps
└── docs/                   # Additional documentation
```

## Key Components

### Entry Points

#### `run.py` & `build.py`
- **Purpose**: Application launchers and build scripts
- **Responsibility**: Initialize Python environment and start the game

#### `src/main.py`
- **Purpose**: Primary game entry point
- **Responsibility**: Creates Game instance and starts main loop

### Core Game Loop

#### `src/game.py` (The Heart)
- **Purpose**: Central game controller and state manager
- **Key Responsibilities**:
  - Main game loop (handle events → update → render)
  - State management (MENU, PLAYING, INVENTORY, SHOP, DEAD, VICTORY)
  - Input handling and event dispatching
  - Turn management (player/monster turns)
  - Level transitions
  - Integration point for all major systems
- **Key Relationships**:
  - Owns: Player, UI, LevelManager, ShopManager
  - Updates: FOV, monster AI, status effects

### Entity System

#### `src/entity.py`
- **Purpose**: Base class for all living entities
- **Key Features**:
  - Position tracking (x, y)
  - Stats system integration
  - Trait-based combat (resistances/weaknesses)
  - Status effects
  - Damage calculation with modifiers

#### `src/player.py`
- **Purpose**: Player character implementation
- **Extends**: Entity
- **Key Features**:
  - Inventory management (60 slots)
  - Equipment system (weapon, armor, 3 accessories)
  - XP and leveling system
  - Stat growth on level up
  - FOV calculation
  - Event emission for reactive equipment

#### `src/stats.py`
- **Purpose**: Unified stat management
- **Key Stats**:
  - Core: HP, MaxHP, Attack, Defense
  - Modifiers: Evade, Crit, Multipliers
  - Player-specific: XP, XP Multiplier, Health Aspect

### Item System

#### `src/items/item.py`
- **Purpose**: Base class for all items
- **Features**: Position, rendering, market value

#### `src/items/equipment.py`
- **Purpose**: Base for equippable items
- **Extends**: Item
- **Key Features**:
  - Stat bonuses (attack, defense, etc.)
  - Slot system (weapon, armor, accessory)
  - Trait modifiers
  - Event handling capability
  - Cleanup phase for dynamic bonuses

#### `src/items/consumable.py`
- **Purpose**: Base for usable items
- **Categories**: Foods, Catalysts, Boons, Misc

#### Item Subdirectories
- **weapons/**: 30+ weapon classes (swords, axes, staves)
- **armor/**: 24+ armor classes (light, heavy, magical)
- **accessories/**: 42+ accessory classes (rings, amulets, belts)
- **consumables/**: 39+ consumable classes organized by type

#### `src/items/pool.py`
- **Purpose**: Item generation and rarity system
- **Features**:
  - Tier-based item pools (Common, Rare, Epic, Legendary)
  - Floor-appropriate item generation
  - Weighted random selection

### Monster System

#### `src/monsters/base.py`
- **Purpose**: Base monster class
- **Key Features**:
  - AI behavior (aggressive, passive, ranged)
  - Pathfinding
  - Combat actions
  - XP value calculation


#### `src/monsters/pool.py`
- **Purpose**: Monster spawning and difficulty scaling
- **Features**:
  - Floor-based monster pools
  - Weighted spawning
  - Boss placement

### Level System

#### `src/level/level.py`
- **Purpose**: Dungeon floor representation
- **Key Features**:
  - Procedural room generation
  - BSP (Binary Space Partitioning) algorithm
  - Corridor creation
  - FOV calculation using tcod
  - Item and monster placement
  - Stairs (up/down) management

#### `src/level/base.py`
- **Purpose**: Special level types
- **Types**: Tutorial base, regular base levels

#### `src/level_manager.py`
- **Purpose**: Multi-floor dungeon management
- **Features**:
  - Floor transitions
  - Progress tracking
  - Area generation

### UI System

#### `src/ui.py`
- **Purpose**: All user interface rendering
- **Key Responsibilities**:
  - Main game view
  - Inventory screen
  - Shop interface
  - Status displays
  - Message log
  - Menu screens
  - Victory/death screens

### Event System

#### `src/event_emitter.py`
- **Purpose**: Central event bus
- **Pattern**: Observer/Publisher-Subscriber
- **Usage**: Equipment reacts to game events

#### `src/event_type.py` & `src/event_context.py`
- **Purpose**: Event definitions and data structures
- **Events**: Combat, healing, consumption, level changes

### Shop System

#### `src/shop.py` & `src/shop_manager.py`
- **Purpose**: In-game economy
- **Features**:
  - Dynamic shop generation
  - Gold-based transactions
  - Item valuation
  - Stock management

### Mechanics

#### `src/enchantments/`
- **Purpose**: Item modifier system
- **Features**: enchantments with stat modifications to weapons and armor

#### `src/traits.py`
- **Purpose**: Elemental/damage type system
- **Types**: Fire, Ice, Lightning, Poison, Holy, Dark, Physical, Vampiric

#### `src/status_effects.py`
- **Purpose**: Temporary entity modifiers
- **Types**: Poison, Burn, Freeze, Stun, Blessed, Cursed

#### `src/constants.py`
- **Purpose**: Game-wide configuration
- **Contains**: Screen dimensions, colors, tiles, game parameters

### Available Events (`src/event_type.py`)
```python
PLAYER_HEAL, PLAYER_CONSUME_ITEM, PLAYER_ATTACK_MONSTER, 
MONSTER_ATTACK_PLAYER, MONSTER_DEATH, LEVEL_UP, 
FLOOR_START, FLOOR_END, SUCCESSFUL_DODGE, CRITICAL_HIT, 
MISS, WEAKNESS_HIT

## Data Files

#### `grimoire.py`
- **Purpose**: Spell and magical item definitions
- **Content**: Detailed spell descriptions and effects

#### `beastiary.py`
- **Purpose**: Monster lore and descriptions
- **Content**: Flavor text and background for all monsters

## Testing Architecture

#### `tests/`
- **Coverage**: 90+ test files
- **Approach**: Unit tests for all major systems
- **Key Areas**:
  - Combat mechanics
  - Item interactions
  - XP/leveling
  - UI layouts
  - Bug regression tests

## Build System

#### `pyproject.toml`
- **Purpose**: Project dependencies and metadata
- **Tool**: Uses `uv` for dependency management
- **Key Dependencies**:
  - tcod (rendering, FOV, pathfinding)
  - numpy (array operations)
  - pytest (testing)

## Game Flow

1. **Initialization**: main.py → Game.__init__()
2. **Menu**: Display main menu, await player choice
3. **Game Start**: Generate Floor 1, place player at base
4. **Game Loop**:
   - Handle input
   - Update player state
   - Process monster turns
   - Update status effects
   - Render current view
5. **Level Transitions**: Via stairs up/down
6. **Victory Conditions**: Defeat Devil on Floor 10
7. **Death**: Return to menu with option to restart
