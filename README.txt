Seven Day Roguelike Game
========================

A complete roguelike game built in 7 days using Python and the tcod library.

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
- Arrow keys OR hjkl (vi-style) for movement
- yubn for diagonal movement

Other Controls:
- ESC or q: Quit game
- >: Descend stairs (when standing on >)
- <: Ascend stairs (when standing on <)

GAMEPLAY
--------

Goal: Descend through 10 levels of the dungeon and defeat the boss on the final level.

Features:
- Turn-based gameplay
- Field of view and exploration
- Randomly generated levels
- Player stats and progression
- Inventory system (coming soon)
- Combat with monsters (coming soon)
- Equipment system (coming soon)

CURRENT STATUS
--------------

Phase 1 Complete:
✓ Basic game loop and rendering
✓ Player movement and controls  
✓ Level generation with rooms and corridors
✓ Field of view system
✓ Stairs between levels
✓ Basic UI with player stats

Coming Next:
- Monster system and AI
- Combat mechanics
- Item and inventory system
- Equipment and progression

BUILD FROM SOURCE
-----------------

Requirements:
- Python 3.8+
- tcod library
- numpy

To build executable:
uv run build.py

This will create a standalone executable in the dist/ folder.

DEVELOPMENT
-----------

Project structure:
- src/main.py - Entry point
- src/game.py - Main game loop
- src/player.py - Player character
- src/level.py - Level generation
- src/ui.py - User interface
- src/constants.py - Game constants

The game follows a modular design for easy expansion and modification.