# Create Item Command Documentation

Given the description in {Argument}, create a new weapon, armor, consumable, or pickup item. Add the item to the item pool, then run grimoire.py to update the grimoire file.

## Item System Architecture

### Base Class Hierarchy

**Item** (`src/items/item.py`)
- Base class for all items
- Properties: position (x, y), name, char, color, description, market_value
- Basic render and move functionality

**Equipment** (`src/items/equipment.py`)
- Extends Item for equippable items
- Properties: attack/defense bonuses, equipment_slot, multiplier bonuses
- Event system integration (event_subscriptions, on_event method)
- Dynamic bonus methods (get_attack_bonus, get_defense_bonus, etc.)

**Consumable** (`src/items/consumable.py`)
- Extends Item for usable items
- Abstract use() method to implement consumption effects
- Categories: foods, catalysts, boons, misc

### Item Categories

#### Weapons (`src/items/weapons/`)
- **Base Class**: `Weapon` (extends Equipment)
- **Equipment Slot**: "weapon"
- **Common Properties**:
  - `attack_bonus`: Flat attack increase
  - `attack_multiplier_bonus`: Multiplicative attack bonus
  - `attack_traits`: List of elemental/special traits
  - `crit_bonus`: Critical hit chance bonus
  - `crit_multiplier_bonus`: Critical hit damage bonus

#### Armor (`src/items/armor/`)
- **Base Class**: `Armor` (extends Equipment)
- **Equipment Slot**: "armor"
- **Common Properties**:
  - `defense_bonus`: Flat defense increase
  - `defense_multiplier_bonus`: Multiplicative defense bonus
  - `resistances`: List of damage types resisted
  - `weaknesses`: List of damage types that deal extra damage

#### Accessories (`src/items/accessories/`)
- **Base Class**: `Accessory` (extends Equipment)
- **Equipment Slot**: "accessory"
- **Common Properties**:
  - Various stat bonuses (evade, crit, fov, health_aspect, xp_multiplier)
  - Event-driven effects are common
  - Often provide utility bonuses rather than direct combat stats

#### Consumables (`src/items/consumables/`)
- **Categories**:
  - **Foods**: Healing items, stat foods
  - **Catalysts**: Permanent stat increases  
  - **Boons**: Temporary powerful effects
  - **Misc**: Special use items

#### Pickups (`src/items/pickups/`)
- **Purpose**: Special items like currency, keys, tokens
- **Base Class**: Usually extends Item directly
- **Common Pattern**: Immediate effects when picked up

## Event System Integration

### Available Events (`src/event_type.py`)
```python
PLAYER_HEAL, PLAYER_CONSUME_ITEM, PLAYER_ATTACK_MONSTER, 
MONSTER_ATTACK_PLAYER, MONSTER_DEATH, LEVEL_UP, 
FLOOR_START, FLOOR_END, SUCCESSFUL_DODGE, CRITICAL_HIT, 
MISS, WEAKNESS_HIT, RESISTANCE_HIT
```

### Event-Driven Item Pattern
```python
def __init__(self, x, y):
    super().__init__(...)
    # Subscribe to events
    self.event_subscriptions.add(EventType.SUCCESSFUL_DODGE)
    self.event_subscriptions.add(EventType.CRITICAL_HIT)

def on_event(self, event_type, context):
    """Handle subscribed events."""
    if event_type == EventType.SUCCESSFUL_DODGE and isinstance(context, AttackContext):
        if context.defender == context.player:  # Only count player events
            # Implement effect
            pass
```

## Stats and Bonuses

### Available Equipment Bonuses
- **Flat Bonuses**: attack_bonus, defense_bonus, fov_bonus, evade_bonus, crit_bonus
- **Multiplier Bonuses**: attack_multiplier_bonus, defense_multiplier_bonus, xp_multiplier_bonus, crit_multiplier_bonus
- **Special Bonuses**: health_aspect_bonus (healing effectiveness)

### Dynamic Bonuses
Override `get_*_bonus(player)` methods for dynamic effects:
```python
def get_crit_bonus(self, player):
    return self.crit_bonus + (self.dodge_count * 0.01)  # +1% per dodge
```

### Traits System (`src/traits.py`)
Available traits: Fire, Ice, Lightning, Poison, Holy, Dark, Physical, Vampiric
- **attack_traits**: Damage types this item deals
- **resistances**: Damage types this armor resists
- **weaknesses**: Damage types that deal extra damage

## Item Pool Integration

### Rarity Constants
```python
RARITY_COMMON = 1.0      # Most common items
RARITY_UNCOMMON = 0.6    # Moderately rare items  
RARITY_RARE = 0.3        # Rare items
```

### ItemSpec Structure
```python
ItemSpec(
    item_class,           # The item class (e.g., BlackBelt)
    item_type,           # 'weapon', 'armor', 'accessory', 'consumable'
    min_floor,           # Minimum floor to spawn (1-10)
    max_floor,           # Maximum floor to spawn (None = no limit)
    rarity_weight,       # RARITY_COMMON/UNCOMMON/RARE
    unique_per_floor,    # Can only spawn once per floor
    unique_per_game,     # Can only spawn once per game
    tags                 # Optional special tags
)
```

## Implementation Checklist

### 1. Create Item Class File
- Place in appropriate subdirectory (`weapons/`, `armor/`, `accessories/`, `consumables/`)
- Import base class and required modules
- Implement `__init__` with proper parameters
- Set market_value based on rarity and power level

### 2. Implement Special Behaviors
- **Event-driven**: Subscribe to events, implement `on_event`
- **Dynamic bonuses**: Override `get_*_bonus` methods
- **Consumables**: Implement `use(player)` method
- **Traits**: Set attack_traits, resistances, or weaknesses

### 3. Update Module Imports
- Add import to category's `__init__.py`
- Add to `__all__` export list
- Import in `src/items/pool.py`

### 4. Add to Item Pool
- Add ItemSpec to appropriate category list in `pool.py`
- Consider level restrictions and uniqueness
- Set appropriate rarity weight

### 5. Run Grimoire Update
```bash
uv run grimoire.py
```

### 6. Write Comprehensive Tests
- Create `tests/test_[item_name].py`
- Use unittest framework with proper setup/tearDown
- Test creation, bonuses, special behaviors, edge cases
- Run with `uv run tests/test_[item_name].py`

## Common Implementation Patterns

### Event-Driven Accessory
```python
class EventAccessory(Accessory):
    def __init__(self, x, y):
        super().__init__(x, y, name="Event Item", char="○")
        self.event_subscriptions.add(EventType.SUCCESSFUL_DODGE)
        self.counter = 0
    
    def on_event(self, event_type, context):
        if event_type == EventType.SUCCESSFUL_DODGE and isinstance(context, AttackContext):
            if context.defender == context.player:
                self.counter += 1
    
    def get_crit_bonus(self, player):
        return self.crit_bonus + (self.counter * 0.01)
```

### Conditional Bonus Item
```python
def get_attack_bonus(self, player):
    base_bonus = self.attack_bonus
    if player.current_floor >= 5:  # Bonus at deeper floors
        base_bonus += 2
    return base_bonus
```

### Trait-Based Weapon
```python
def __init__(self, x, y):
    super().__init__(
        x, y, name="Fire Sword", char="/",
        attack_bonus=5,
        attack_traits=[Trait.FIRE]  # Deals fire damage
    )
```

### Healing Consumable
```python
def use(self, player):
    heal_amount = int(player.max_hp * 0.25)  # 25% max health
    player.heal(heal_amount)
    return f"Healed for {heal_amount} HP!"
```

### Cleanup Phase Item
```python
def __init__(self, x, y):
    super().__init__(x, y, name="Late Calculator", char="=", is_cleanup=True)
    
def get_attack_bonus(self, player):
    # Calculated after all other equipment bonuses
    total_other_attack = sum(item.attack_bonus for item in player.equipped_items if item != self)
    return int(total_other_attack * 0.1)  # 10% of other equipment
```

## Testing Patterns

### Basic Item Test Structure
```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import unittest
from player import Player
from event_type import EventType
from event_context import AttackContext
from items.accessories.my_item import MyItem

class TestMyItem(unittest.TestCase):
    def setUp(self):
        EventEmitter._instance = None
        self.emitter = EventEmitter()
    
    def tearDown(self):
        self.emitter.clear_all_listeners()
    
    def test_creation(self):
        item = MyItem(0, 0)
        self.assertEqual(item.name, "Expected Name")
        # Test all properties
    
    def test_special_behavior(self):
        # Test unique functionality
        pass

if __name__ == '__main__':
    unittest.main()
```

## Market Value Guidelines
- **Common**: 15-35 gold
- **Uncommon**: 35-60 gold  
- **Rare**: 60-100+ gold
- **Special/Legendary**: 100+ gold

Consider power level, utility, and rarity when setting market_value.

## Final Notes
- Always follow the **one-class-per-file** principle
- Use descriptive names and clear descriptions
- Consider game balance when setting bonuses
- Test thoroughly, especially event interactions
- Update grimoire.md via grimoire.py after implementation