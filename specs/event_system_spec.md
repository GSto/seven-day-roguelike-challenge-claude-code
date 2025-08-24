# Event System Specification

## Overview
The Event System enables reactive and dynamic gameplay by allowing equipment and items to respond to game events. This system will make weapons, armor, and accessories more interesting by triggering special effects when certain events occur.

## Architecture

### Core Components

#### EventEmitter
- Central event bus that manages all game events
- Singleton pattern to ensure single source of truth
- Methods:
  - `emit(event_type: EventType, context: EventContext)` - Trigger an event
  - `subscribe(event_type: EventType, callback: Callable)` - Register listener
  - `unsubscribe(event_type: EventType, callback: Callable)` - Remove listener

#### EventType (Enum)
- PLAYER_HEAL
- PLAYER_CONSUME_ITEM
- PLAYER_ATTACK_MONSTER
- MONSTER_ATTACK_PLAYER
- MONSTER_DEATH
- LEVEL_UP
- FLOOR_CHANGE
- SUCCESSFUL_DODGE
- CRITICAL_HIT
- MISS
- WEAKNESS_HIT
- RESISTANCE_HIT

#### EventContext
Base class with common fields:
- `player: Player` - The player involved
- `timestamp: float` - When the event occurred

Specialized contexts:
- `HealContext`: amount_healed
- `ConsumeContext`: item_type, item
- `AttackContext`: attacker, defender, damage, is_critical, is_miss, trait_interaction
- `DeathContext`: monster, experience_gained
- `LevelUpContext`: new_level, stat_increases
- `FloorContext`: floor_number, previous_floor

### Integration Points

#### Equipment Base Classes
All equipment types need event handling capability:
- `Weapon.on_event(event_type: EventType, context: EventContext)`
- `Armor.on_event(event_type: EventType, context: EventContext)`
- `Accessory.on_event(event_type: EventType, context: EventContext)`

#### Event Registration
Equipment automatically registers/unregisters when equipped/unequipped:
- Equipment tracks its subscribed events
- Player manages registration lifecycle
- Cleanup on unequip to prevent memory leaks

## Implementation Plan

### Phase 1: Core Event System

TODO:
- [ ] Create EventType enum with all event types
- [ ] Create EventContext base class and specialized contexts
- [ ] Implement EventEmitter singleton class
- [ ] Add event emission points in existing code:
  - [ ] Player.heal() - emit PLAYER_HEAL
  - [ ] Player.consume_item() - emit PLAYER_CONSUME_ITEM
  - [ ] Combat system - emit attack events
  - [ ] Monster.die() - emit MONSTER_DEATH
  - [ ] Player.level_up() - emit LEVEL_UP
  - [ ] Floor transition - emit FLOOR_CHANGE
- [ ] Write unit tests for EventEmitter

### Phase 2: Equipment Integration

TODO:
- [ ] Add on_event method to Equipment base class
- [ ] Add event_subscriptions property to Equipment
- [ ] Modify Player.equip_item() to register events
- [ ] Modify Player.unequip_item() to unregister events
- [ ] Create TriggeredEffect base class for reusable effects
- [ ] Write unit tests for equipment event handling

### Phase 3: New Accessories Implementation

TODO:
- [ ] Implement Healing Dodge accessory
  - Trigger: SUCCESSFUL_DODGE
  - Effect: Heal 5% max health
- [ ] Implement Vampire's Pendant accessory
  - Trigger: MONSTER_DEATH
  - Effect: Heal 5% max health
- [ ] Implement Warden's Tome accessory
  - Trigger: LEVEL_UP
  - Effect: +1 permanent DEF
- [ ] Implement Turtle's Blessing accessory
  - Trigger: FLOOR_CHANGE
  - Effect: Gain 1 shield
- [ ] Implement Protective Level accessory
  - Trigger: LEVEL_UP
  - Effect: Gain 1 shield
- [ ] Add all new accessories to default pool
- [ ] Write unit tests for each accessory

### Phase 4: New Weapons Implementation

TODO:
- [ ] Implement Defender weapon
  - Base: +7 ATK
  - Trigger: MONSTER_DEATH
  - Effect: -1 ATK, +1 DEF (min 1 ATK)
- [ ] Implement Holy Avenger weapon
  - Base: +8 ATK, Holy trait
  - Trigger: MONSTER_ATTACK_PLAYER
  - Effect: 10% chance counter attack
- [ ] Implement Backhand Blade weapon
  - Base: +3 ATK, +5% EVD, Dark trait
  - Trigger: SUCCESSFUL_DODGE
  - Effect: Counter attack
- [ ] Add all new weapons to default pool
- [ ] Write unit tests for each weapon

### Phase 5: Updated Weapons

TODO:
- [ ] Update Psychic's Turban
  - Add internal counter property
  - Trigger: PLAYER_CONSUME_ITEM
  - Effect: Increment counter, update stats
- [ ] Update SkinSuit
  - Add internal counter property
  - Trigger: MONSTER_DEATH
  - Effect: Increment counter, update stats
- [ ] Write unit tests for updated weapons

### Phase 6: Testing & Polish

TODO:
- [ ] Integration tests for complex event chains
- [ ] Performance testing with multiple listeners
- [ ] Memory leak testing (proper cleanup)
- [ ] Balance testing for new items
- [ ] Documentation updates

## Technical Considerations

### Performance
- Use weak references for callbacks to prevent memory leaks
- Consider event batching for multiple simultaneous events
- Profile event emission overhead

### Thread Safety
- Ensure EventEmitter is thread-safe if game becomes multi-threaded
- Use locks for subscription management

### Debugging
- Add debug mode to log all events
- Event history for replay/analysis
- Performance metrics for event processing

### Extensibility
- Plugin system for custom events
- Event filtering/middleware support
- Priority system for event handlers

## Testing Strategy

### Unit Tests
- EventEmitter functionality
- Each event type emission
- Each new item's trigger behavior
- Event context data accuracy

### Integration Tests
- Equipment equip/unequip event lifecycle
- Multiple items responding to same event
- Event cascades (one event triggering another)
- Save/load with event system

### Balance Tests
- New item power levels
- Synergy between triggered items
- Edge cases (e.g., multiple counter attacks)

## Success Criteria
- All listed events are implemented and firing correctly
- All new items are functional with their triggers
- No performance degradation from event system
- No memory leaks from event subscriptions
- Comprehensive test coverage (>90%)
- Items feel impactful and interesting to use