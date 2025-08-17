# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.


## Project Overview

This is a seven-day roguelike game development project following the traditional 7DRL challenge format. It is a complete, playable roguelike.


## Project Structure
Read this project structure when making changes, to help you understand where items should be placed. 

Overview
- `plans/` - Project planning and roadmap documentation
- `specs/` - Technical specifications (empty currently)
- `src/` - Source code 
- `tests/` - Where we store unit tests. 

### Logic
- `game.py` - runs the game, handles events, player movement, combat, turns, item usage
- `level.py` - level generation 
- `main.py` - entry point, no logic here. 
- `monster.py` - collection of monsters and logic for generating them
- `player.py` - player related logic
- `ui.py` - handles rendering elements on screen.

### Game Pieces 
Users have three kinds of equipment: Weapon, Armor, and Accessories
- `src/items/accessories.py` - all of the accesories users can equip. 
- `src/items/weapons.py` - all weapons
- `src/items/armor.py` - all armor

#### Consumables 
- `src/items/consumables.py` There are all consumable items, which are things the user can use once. Includes, potions, boons, catalysts.

#### Logic & Utilities
- `src/items/enchantments.py` -enchantments that can be applied to users 
- `src/items/base.py` - base item classes
- `src/items/factory.py` - generates items for levels



## Development Commands

Always use `uv run` when executing Python scripts instead of `python` directly. This ensures proper dependency management with the uv toolchain.

### Common Development Tasks

- **Run the game**: `uv run run.py`
- **Build executable**: `uv run build.py`
- **Install dependencies**: `uv sync`
- **Run all tests**: `uv run pytest tests/` (run all tests in tests directory)
- **Run specific test**: `uv run tests/test_filename.py` (run individual test file)

### Game Testing Safety Protocol

**CRITICAL: When testing the game, always use timeouts to prevent getting stuck.**

- **Test game execution**: `timeout 30s uv run src/main.py` (auto-terminate after 30 seconds)
- **Manual testing**: Use `Ctrl+C` to force quit if game becomes unresponsive
- **Automated testing**: Always include timeout parameter when using Bash tool
- **Never run the game indefinitely** - this can cause the session to hang

If the game needs to be tested interactively:
1. Use a short timeout (10-30 seconds) to verify it starts
2. Test specific functionality through unit tests instead of manual gameplay
3. If manual testing is required, warn the user first and ask them to test locally

### Project Dependencies

Dependencies are managed in `pyproject.toml`. The main dependencies are:
- `tcod>=13.8.0` - Roguelike library for rendering, FOV, pathfinding
- `numpy>=1.21.0` - For efficient array operations in level generation

## Development Status

Phase 1 (Foundation Setup) - COMPLETED:
✓ Technology stack: Python + tcod library
✓ Project structure with pyproject.toml
✓ Core game loop and rendering system
✓ Player movement and controls
✓ Level generation with rooms and corridors
✓ Field of view system
✓ Stairs between levels
✓ Basic UI with player stats

Next Phase (Core Mechanics):
- Monster system and AI
- Combat mechanics
- Item and inventory system


## Development Guidelines

### Testing Requirements
**MANDATORY: Always write and run unit tests when implementing features or fixing bugs.**

When implementing new features or fixing bugs, you MUST:
1. **Write unit tests** for the new functionality in `tests/test_[feature_name].py`
2. **Run the tests** to ensure they pass: `uv run tests/test_[feature_name].py`
3. **Update existing tests** if changes affect existing functionality
4. **Verify all tests pass** before committing code
5. **Include test results** in commit messages to show validation

**IMPORTANT: All test files must be placed in the `tests/` directory. Do not create test files in the root directory or elsewhere.**

Test files should:
- Be placed in the `tests/` folder with descriptive names
- Cover core functionality and edge cases
- Use descriptive test names (e.g., `test_player_gains_xp_when_monster_dies`)
- Include both positive and negative test cases
- Test integration between components when relevant

### Implementation Process
Your goal is to read specs/project_plan.md and implement the game. Study the project plan and implement the most important missing functionality. When you are done, update the project_plan to indicate the feature is complete.

After implementing functionality or resolving problems, run the tests for that unit of code that was improved.

999. Important: When authoring documentation capture the why tests and the backing implementation is important.

9999. Important

9999. Important: We want single sources of truth, no migrations/adapters. If tests unrelated to your work fail then it's your job to resolve these tests as part of the increment of change.

9999. Important: As soon as there are no build or test errors create a git commit with a comment explaing the changes and what was implemented

9999999999999999999999999999. DO NOT IMPLEMENT PLACEHOLDER OR SIMPLE IMPLEMENTATIONS. WE WANT FULL IMPLEMENTATIONS. DO IT OR I WILL YELL AT YOU

Include a README.txt that explains how to start and play the game. Update the README as you implement new features.

ULTIMATE GOAL is a functioning rougelike game