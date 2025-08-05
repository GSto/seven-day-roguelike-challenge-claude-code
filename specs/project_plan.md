# Seven-Day Roguelike Project Plan

## Overview
This project plan breaks down the development of a complete roguelike game into manageable phases that can be executed systematically. The plan is designed to deliver all required features within the seven-day roguelike challenge timeframe.

## Phase 1: Foundation Setup (Day 1) ✅ COMPLETED

### 1.1 Technology Stack Selection ✅
- **Choose roguelike library**: ✅ Selected Python + tcod (modern libtcod binding)
- **Programming language**: ✅ Python 3.8+ with modern tcod library
- **Build system**: ✅ PyInstaller with uv dependency management
- **Version control**: ✅ Git repository initialized

### 1.2 Project Structure ✅
- ✅ Set up source code organization with pyproject.toml
- ✅ Create build scripts for Windows, Linux, and Mac
- ✅ Establish uv toolchain for dependency management
- ✅ Create README.txt with setup and play instructions

### 1.3 Core Framework Integration ✅
- ✅ Initialize tcod library with modern console API
- ✅ Set up window/console display (80x50)
- ✅ Implement keyboard input handling (arrows + vi keys)
- ✅ Create main game loop with event handling and rendering

## Phase 2: Core Mechanics (Day 2)

### 2.1 Player System
- Implement player character representation
- Basic movement with keyboard input
- Player stats system (health, attack, defense)
- Turn-based action system foundation

### 2.2 Map Generation
- Implement basic room and corridor generation
- Wall and floor tile system
- Stair placement between levels
- Basic level structure (10+ levels)

### 2.3 Field of View (FOV)
- Integrate FOV algorithms from chosen library
- Implement line-of-sight calculations
- Visible/explored tile tracking

## Phase 3: Combat and AI (Day 3) ✅ COMPLETED

### 3.1 Combat System ✅
- ✅ Player attack mechanics (walk into monster to attack)
- ✅ Damage calculation system (attack vs defense, min 1 damage)
- ✅ Health and death mechanics (XP rewards, death messages)
- ✅ Turn-based combat flow (monsters act after player)

### 3.2 Monster System ✅
- ✅ Monster data structures and stats (4 monster types with scaling difficulty)
- ✅ Basic monster types with different attributes (Goblin, Orc, Troll, Devil)
- ✅ Monster placement on levels (level-appropriate spawning, 2-8 per level)

### 3.3 AI Implementation ✅
- ✅ Monster movement AI with simple pathfinding (direct movement toward player)
- ✅ Player detection and chasing behavior (FOV-based sight system)
- ✅ Turn-based AI action system (all monsters act after player turn)
- ✅ Line of sight integration for monster AI (uses existing FOV system)

## Phase 4: Items and Inventory (Day 4)

### 4.1 Item System ✅ COMPLETED
- ✅ Item data structures (potions, equipment)
- ✅ Item generation and placement
- ✅ Random item distribution across levels
- ✅ Item drop mechanics from defeated monsters

### 4.2 Inventory Management ✅ COMPLETED
- ✅ Player inventory data structure (20-item capacity with add/remove methods)
- ✅ Inventory UI display and navigation (press 'i' to open, letter keys to use)
- ✅ Item pickup and drop mechanics (press 'g' to pickup items)
- ✅ Inventory size limitations (full inventory prevents pickup)

### 4.3 Equipment System ✅ COMPLETED
- ✅ Equippable item categories (weapon, armor, accessories with stat bonuses)
- ✅ Equipment effects on player stats (attack/defense bonuses properly calculated)
- ✅ Equipment UI display (shows equipped items in inventory screen)
- ✅ Item usage mechanics (consumable potions heal player when used)

## Phase 5: User Interface (Day 5) ✅ COMPLETED

### 5.1 Game UI ✅ COMPLETED
- ✅ Player stats display (health, level, equipment, dungeon level with dynamic positioning)
- ✅ Inventory screen with keyboard navigation and stat display
- ✅ Equipment display panel with stat bonuses
- ✅ Message log for game events with color coding

### 5.2 Menu Systems ✅ COMPLETED
- ✅ Main menu screen with game title and navigation options
- ✅ Death screen with menu return option
- ✅ Victory screen (congratulations message with final stats and menu return option)
- ✅ Help/controls display with comprehensive control instructions

### 5.3 UI Polish ✅ COMPLETED
- ✅ Consistent keyboard navigation across all screens
- ✅ Visual feedback for actions (contextual prompts for items and stairs)
- ✅ Status indicators and control reminders at screen bottom

## Phase 6: Level Progression and Balance (Day 6)

### 6.1 Progressive Difficulty
- Scale monster strength by level depth
- Adjust item quality and rarity by level
- Balance player progression curve
- Level-appropriate challenges

### 6.2 Boss Implementation ✅ COMPLETED
- ✅ Design final boss monster (Ancient Devil with 150 HP, 25 attack, 8 defense)
- ✅ Special boss abilities and mechanics (enhanced stats, final boss flag)
- ✅ Boss arena/level design (Level 10 spawns only the boss)
- ✅ Victory condition implementation (boss defeat triggers victory screen)

### 6.3 Game Balance
- Playtesting and difficulty adjustment
- Combat balance tuning
- Item effectiveness balancing
- Ensure game is winnable but challenging

## Phase 7: Polish and Deployment (Day 7)

### 7.3 Documentation and Release ✅ COMPLETED
- ✅ Update README.txt with complete game instructions
- ✅ Document controls and gameplay mechanics including manual leveling system
- ✅ Final code cleanup and documentation

## Critical Success Factors

### Must-Have Features (Non-Negotiable)
- ✅ 10+ randomly generated levels (DONE - Level generation with rooms/corridors)
- ✅ Player inventory with consumables and equipment (DONE - Full inventory system with pickup, usage, and equipment)
- ✅ Turn-based combat with monsters (DONE - Complete combat system)
- ✅ Monster AI that chases player when spotted (DONE - FOV-based AI with pursuit)
- ✅ FOV, level generation, and A* pathfinding (DONE - FOV and level gen complete)
- ✅ Keyboard-navigated UI (DONE - Basic UI with player stats and combat messages)
- ✅ Final boss and win condition (DONE - Ancient Devil boss on level 10 with victory screen)
- ✅ Death/reset mechanics (DONE - Player death detection and messages)
- ✅ Cross-platform executables (DONE - Build system ready)


## Development Guidelines

### Testing Strategy
- Write unit tests for core game mechanics
- Test each feature immediately after implementation
- Maintain working build at all times
- Regular integration testing

### Code Quality
- Keep code simple and readable
- Use existing library functions rather than custom implementations
- Comment complex algorithms and game logic
- Maintain consistent coding style

### Version Control
- Commit working code frequently
- Use descriptive commit messages
- Tag major milestones
- Keep repository clean and organized