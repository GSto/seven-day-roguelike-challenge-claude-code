# Shop System Specification

## Overview
Implementation specification for the shop mechanic in the seven-day roguelike, enabling players to buy and sell items using XP as currency.

## Core Requirements

### 1. Item Pricing System
- **Base Market Values**:
  - Consumables: 10 XP
  - Weapons: 25 XP  
  - Armor: 25 XP
  - Accessories: 25 XP
- **Selling Price**: 50% of market value (rounded down)
- Each item must have a `market_value` property

### 2. Shop Generation
- **Location**: One shop per floor (floors 1-9, excluding floor 10)
- **Symbol**: `$` character displayed in room center
- **Interaction**: Triggered when player moves onto shop tile

### 3. Shop Inventory
Each shop contains:
- 1 guaranteed health potion
- 2-3 level-appropriate consumables
- 2-3 level-appropriate weapons
- 2-3 level-appropriate armor pieces
- 2-3 level-appropriate accessories
- No duplicate items allowed
- Items removed from shop when purchased (replaced with 'EMPTY' slot)

## Data Structures

### Item Modifications
```python
class Item:
    def __init__(self, x, y):
        # Existing properties...
        self.market_value = self.get_default_market_value()
    
    def get_default_market_value(self):
        # Override in subclasses based on item type
        return 10  # Default for consumables
```

### Shop Class
```python
class Shop:
    def __init__(self, floor_level):
        self.floor_level = floor_level
        self.inventory = []  # List of items for sale
        self.x = None  # Position in room
        self.y = None
        
    def generate_inventory(self):
        """Generate level-appropriate items for shop"""
        pass
        
    def buy_item(self, item_index, player):
        """Handle item purchase transaction"""
        pass
        
    def sell_item(self, item, player):
        """Handle item sale transaction"""
        pass
```

### Shop Manager
```python
class ShopManager:
    def __init__(self):
        self.current_shop = None
        self.ui_mode = None  # 'buy' or 'sell'
        
    def open_shop(self, shop, player):
        """Initialize shop interface"""
        pass
        
    def handle_input(self, key):
        """Process keyboard input in shop UI"""
        pass
```

## UI/UX Specifications

### Shop Interface States
1. **Buy Mode**
   - Display shop inventory in list format
   - Show item name, type, stats, and price
   - Highlight currently selected item
   - Display player's current XP
   - Show "Press ENTER to buy, TAB to switch to sell mode, ESC to exit"

2. **Sell Mode**  
   - Display player's inventory
   - Show item name and sell price (50% of market value)
   - Highlight currently selected item
   - Display player's current XP
   - Show "Press ENTER to sell, TAB to switch to buy mode, ESC to exit"

### Visual Layout
```
================== SHOP ==================
Current XP: 250                    [BUY MODE]

Items for Sale:
> Health Potion               10 XP
  Iron Sword                  25 XP
  Leather Armor               25 XP
  Speed Ring                  25 XP
  Fire Catalyst               10 XP
  EMPTY                        --
  EMPTY                        --

[↑↓] Navigate [ENTER] Buy [TAB] Sell Mode [ESC] Exit
==========================================
```

## Implementation Steps

### Phase 1: Core Infrastructure
1. Add `market_value` property to all item classes
2. Implement `Shop` class with inventory generation
3. Create `ShopManager` for UI state management
4. Add shop symbol (`$`) to level generation

### Phase 2: Shop Generation
1. Implement level-appropriate item selection algorithm
2. Create shop placement logic in room generation
3. Ensure one shop per floor (except floor 10)
4. Add shop interaction trigger to game loop

### Phase 3: Transaction System
1. Implement XP deduction for purchases
2. Implement XP addition for sales
3. Add validation for sufficient XP
4. Handle inventory management (add/remove items)

### Phase 4: User Interface
1. Create shop UI rendering functions
2. Implement navigation controls (arrow keys)
3. Add mode switching (TAB key)
4. Implement buy/sell confirmation
5. Add visual feedback for transactions

### Phase 5: Item Pool System
1. Create level-appropriate item pools
2. Implement weighted random selection
3. Ensure no duplicate items in shop
4. Handle "EMPTY" slot display

## Events and Triggers

### New Event Types
```python
class BuyItemEvent:
    def __init__(self, item, cost, player):
        self.item = item
        self.cost = cost
        self.player = player

class SellItemEvent:
    def __init__(self, item, value, player):
        self.item = item
        self.value = value
        self.player = player
```

## Testing Requirements

### Unit Tests
1. `test_shop_generation.py`
   - Verify shop appears on floors 1-9
   - Verify no shop on floor 10
   - Verify correct inventory size
   - Verify no duplicate items

2. `test_shop_transactions.py`
   - Test buying with sufficient XP
   - Test buying with insufficient XP
   - Test selling items for correct price
   - Test inventory updates after transactions

3. `test_shop_ui.py`
   - Test navigation between items
   - Test mode switching
   - Test UI state persistence
   - Test escape/cancel functionality

### Integration Tests
1. Test shop interaction from main game loop
2. Test save/load with shop state
3. Test level transitions with shops
4. Test item pool generation for different levels

## Dependencies
- Existing item system must support `market_value` property
- XP system must allow spending/gaining XP
- Level generation must support shop placement
- UI renderer must support shop interface

## Success Criteria
1. Players can access shops on floors 1-9
2. Players can buy items using XP as currency
3. Players can sell items for 50% of market value
4. Shop interface is intuitive and responsive
5. No duplicate items appear in shops
6. Level-appropriate items are generated
7. All transactions update player XP and inventory correctly

## Future Enhancements (Out of Scope)
- Special merchant NPCs with dialogue
- Item haggling/negotiation
- Shop upgrades or reputation system
- Limited-time deals or discounts
- Buyback option for recently sold items