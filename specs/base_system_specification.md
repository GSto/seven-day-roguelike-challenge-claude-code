# Base System Specification

## Overview
Implementation specification for the Base system - safe hub areas between dungeon floors that provide respite and shopping opportunities for players progressing through the game.

## Core Concept
Bases are non-randomized safe zones that appear between every dungeon floor, creating a progression pattern of Floor → Base → Floor → Base throughout the game. They serve as strategic checkpoints where players can shop for upcoming challenges without enemy threats.

## Game Progression Structure

### New Level Progression
```
Floor 1 → Base 1 → Floor 2 → Base 2 → Floor 3 → Base 3 → ... → Floor 9 → Base 9 → Floor 10 (Boss)
```

### Key Changes
- **Total Levels**: 19 (10 floors + 9 bases)
- **Shop Relocation**: Shops ONLY spawn in Bases, NOT on regular floors
- **Safe Zones**: Bases have no enemies or random items

## Base Level Design

### Layout Specifications
```
┌────────────────────────────┐
│ SHOP($)          EXIT(>)   │
│                             │
│                             │
│         MEDIUM ROOM         │
│                             │
│                             │
│           ENTRY(<)          │
└────────────────────────────┘
```

### Room Dimensions
- **Shape**: Rectangle (not square)
- **Size**: Medium (approximately 15x10 to 20x12 tiles)
- **Walls**: Fixed perimeter, no corridors or additional rooms

### Fixed Element Positions
1. **Entry Stairs (<)**
   - Position: Bottom center
   - Offset: 1-2 tiles from bottom wall (not touching)
   - Symbol: '<' (stairs up from previous floor)

2. **Exit Stairs (>)**
   - Position: Top center  
   - Offset: 1-2 tiles from top wall (not touching)
   - Symbol: '>' (stairs down to next floor)
   - Alignment: Parallel to entry stairs

3. **Shop ($)**
   - Position: Top-right corner
   - Offset: 2-3 tiles from walls
   - Symbol: '$' (shop interaction point)
   - Inventory: Items appropriate for NEXT floor

## Shop System Modifications

### Shop Location Changes
- **Remove**: Shop generation from regular floors (1-9)
- **Add**: Shop generation in all Bases (1-9)
- **No Shop**: Base 10 does not exist (Floor 10 is final boss level)

### Shop Inventory Scaling
```python
# Base N shop contains items for Floor N+1
base_1_shop → floor_2_items
base_2_shop → floor_3_items
base_3_shop → floor_4_items
...
base_9_shop → floor_10_items (boss-tier items)
```

### Shop Generation Logic
- Use existing shop generation system
- Adjust item level to `base_number + 1`
- Maintain existing price structure (XP currency)
- Keep buy/sell mechanics unchanged

## Event System Changes

### Event Renaming
- **OLD**: `FLOOR_CHANGE` event
- **NEW**: `FLOOR_START` event

### New Event Types
```python
class EventType(Enum):
    FLOOR_START = "floor_start"  # Entering a dungeon floor
    FLOOR_END = "floor_end"      # Entering a base (leaving floor)
```

### Event Triggers
- **FLOOR_START**: Fired when entering any dungeon floor (1-10)
- **FLOOR_END**: Fired when entering any base (1-9)
- **No Event**: Moving between stairs within a base

## Implementation Requirements

### Base Class Structure
```python
class Base:
    def __init__(self, base_number):
        self.base_number = base_number
        self.width = 18  # Fixed dimensions
        self.height = 11
        self.tiles = self.generate_base_layout()
        self.shop = self.create_base_shop()
        self.entry_pos = self.calculate_entry_position()
        self.exit_pos = self.calculate_exit_position()
        
    def generate_base_layout(self):
        """Create fixed rectangular room with walls"""
        
    def create_base_shop(self):
        """Generate shop with next floor's items"""
        
    def is_safe_zone(self):
        """Always returns True - no combat allowed"""
```

### Level Manager Changes
```python
class LevelManager:
    def get_current_area(self):
        """Return either Floor or Base instance"""
        
    def transition_to_base(self, base_number):
        """Handle floor → base transition"""
        
    def transition_to_floor(self, floor_number):
        """Handle base → floor transition"""
```

## UI/UX Specifications

### Display Changes
- **Floor Display**: "Floor 1", "Base 1", "Floor 2", etc.
- **Safe Zone Indicator**: Show "SAFE ZONE" or similar in Bases
- **No Combat Messages**: Disable attack actions in Bases

### Player Feedback
- Entry message: "You enter a safe base. No enemies here."
- Shop proximity: "A shop is nearby. Press $ to browse."
- Exit available: "Stairs down lead to Floor {N+1}."

## Testing Requirements

### Unit Tests
1. `test_base_generation.py`
   - Verify fixed layout generation
   - Confirm shop placement
   - Validate stairs positioning
   - Ensure no random elements

2. `test_base_progression.py`
   - Test floor → base transitions
   - Test base → floor transitions
   - Verify correct numbering sequence
   - Confirm event firing

3. `test_base_shop.py`
   - Verify shop spawns in bases only
   - Confirm no shops on regular floors
   - Test inventory level scaling
   - Validate XP transactions

4. `test_base_safety.py`
   - Confirm no monster spawning
   - Verify no random items
   - Test combat disabled
   - Ensure safe zone status

## Migration Steps

### Phase 1: Core Base Implementation ✅ COMPLETED
1. ✅ Create `Base` class with fixed layout generation
2. ✅ Implement base room structure (walls, floor)
3. ✅ Add stairs positioning logic
4. ✅ Create base number tracking

### Phase 2: Shop Migration ✅ COMPLETED
1. ✅ Remove shop generation from regular floors
2. ✅ Add shop to base generation
3. ✅ Adjust shop inventory scaling
4. ✅ Update shop UI for base context

### Phase 3: Event System Update ✅ COMPLETED
1. ✅ Rename FLOOR_CHANGE to FLOOR_START
2. ✅ Add FLOOR_END event type
3. ✅ Update event triggers for transitions
4. ✅ Modify listeners for new events

### Phase 4: Level Progression ✅ COMPLETED
1. ✅ Implement alternating floor/base progression
2. ✅ Update level manager for dual area types
3. ✅ Adjust save/load for bases
4. ✅ Update UI to show current area type

### Phase 5: Polish & Testing ✅ COMPLETED
1. ✅ Add base-specific messages
2. ✅ Implement safe zone mechanics
3. ✅ Complete test coverage
4. ✅ Balance gameplay pacing

## Success Criteria ✅ ALL COMPLETED
1. ✅ Players alternate between floors and bases throughout game
2. ✅ All shops appear only in bases (none on floors)
3. ✅ Bases provide safe respite with no combat
4. ✅ Shop inventory scales appropriately for upcoming floor
5. ✅ Events fire correctly for floor/base transitions
6. ✅ Fixed base layout is consistent and predictable
7. ✅ Clear UI distinction between floors and bases

## Future Enhancements (Out of Scope)
- Base customization or upgrades
- NPCs or dialogue in bases
- Storage/stash system in bases
- Base-specific achievements
- Multiple shop types in bases
- Crafting stations in bases