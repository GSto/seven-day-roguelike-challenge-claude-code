Seven Day Roguelike Game
========================

A complete roguelike game built in 7 days using Python and the tcod library.
Explore a 10-level dungeon, fight monsters, collect items, and defeat the Ancient Dragon!

QUICK START
-----------

For Development:
1. Install Python 3.8 or later and uv (https://docs.astral.sh/uv/)
2. Install dependencies: uv sync
3. Run the game: uv run run.py

For Playing (Executable):
1. Download the executable for your platform from the releases
2. Run seven-day-roguelike.exe (Windows) or ./seven-day-roguelike (Linux/Mac)

GAME CONTROLS
-------------

Movement:
- Arrow keys OR hjkl (vi-style) for cardinal movement
- yubn for diagonal movement
- Walk into monsters to attack them

Actions:
- g: Pick up items from the ground
- i: Open/close inventory
- x: Level up (when you have enough XP)
- ESC: Close menus or quit game
- q: Quit game

Inventory:
- a-z: Select/use items by letter
- Enter: Use selected item (consumables) or equip (equipment)
- d: Drop selected item
- Arrow keys/jk: Navigate inventory
- ESC: Close inventory

Stairs:
- >: Descend stairs (automatic when walking on them)
- <: Ascend stairs (automatic when walking on them)

GAMEPLAY
--------

Goal: Descend through all 10 levels of the dungeon and defeat the Ancient Dragon!

Core Mechanics:
- Turn-based gameplay - monsters move after you do
- Field of view - you can only see areas within your sight range
- Experience system - gain XP by defeating monsters, press 'x' to level up manually
- Health system - avoid death by managing your HP with potions and equipment
- Inventory management - collect items, potions, and equipment (20-item limit)

Character Progression:
- Gain XP by defeating monsters
- Level up manually by pressing 'x' when you have enough XP
- Each level increases HP (+20), Attack (+3), and Defense (+1)
- Equip better weapons, armor, and accessories for stat bonuses

Monster Types:
- Goblins (weak, fast) - Early levels
- Orcs (medium strength) - Mid levels  
- Trolls (strong, high defense) - Late levels
- Ancient Dragon (final boss) - Level 10 only

Item Types:
- Health Potions: Restore HP based on your health aspect stat
- Equipment: Weapons, armor, and accessories with stat bonuses
- Special Consumables: Catalysts and random effect items
- Progressive quality: Better items found on deeper levels

CURRENT STATUS
--------------

✅ COMPLETE FEATURES:
✓ Full roguelike gameplay with 10 levels
✓ Complete combat system with 4 monster types
✓ Field of view and exploration system
✓ Full inventory and equipment system
✓ Manual leveling system (press 'x' to level up)
✓ Item generation and monster drops
✓ Progressive difficulty scaling
✓ Final boss and victory condition
✓ Death and restart mechanics
✓ Complete UI with menus and help system

The game is feature-complete and ready to play!

BUILD FROM SOURCE
-----------------

Requirements:
- Python 3.8+
- uv package manager

Setup:
1. Clone the repository
2. Run: uv sync
3. Run game: uv run run.py
4. Build executable: uv run build.py

This will create a standalone executable in the dist/ folder for your platform.

DEVELOPMENT
-----------

Project structure:
- src/main.py - Entry point
- src/game.py - Main game loop and state management
- src/player.py - Player character and stats
- src/level.py - Level generation and map management
- src/monster.py - Monster AI and behavior
- src/items/ - Item system (weapons, armor, consumables, accessories)
- src/ui.py - User interface rendering
- src/constants.py - Game constants and configuration

The game follows a modular design with comprehensive test coverage.

TIPS FOR NEW PLAYERS
--------------------

1. Start by learning the movement keys (hjkl or arrow keys)
2. Press 'g' to pick up items, especially health potions
3. Open inventory with 'i' and learn to use potions for healing
4. Walk into monsters to attack them - combat is automatic
5. Watch your HP and XP - level up with 'x' when available
6. Equip better weapons and armor as you find them
7. The UI shows "Next Lvl: X (Press X)" when you can level up
8. Each level gets progressively harder - use strategy!
9. Save health potions for tough fights
10. The final boss is on level 10 - prepare well before descending!

Have fun exploring the Seven-Day Dungeon!