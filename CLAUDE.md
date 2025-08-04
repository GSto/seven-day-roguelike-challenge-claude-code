# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a seven-day roguelike game development project following the traditional 7DRL challenge format. The goal is to create a complete, playable roguelike game with all core features implemented.

## Project Requirements

The game must include:
- Player inventory system with consumable potions and equippable items
- At least 10 randomly generated levels with progressive difficulty
- Items, monsters, walls, rooms, and stairs between levels
- Final boss monster on the last level
- Turn-based combat system where monsters move/attack after each player action
- Monster AI that chases the player when spotted
- Simple keyboard-navigated UI showing player stats, equipment, and inventory
- Win condition (kill final boss) and death/reset mechanics

## Technical Requirements

- Must produce playable executables for Windows, Linux, and Mac
- Should use an existing roguelike library (libtcod, T-Engine, or similar modern framework)
- Must implement core roguelike features: FOV, level generation algorithms, A* pathfinding
- All code must be clearly visible on GitHub
- No complex deployment/build steps required

## Project Structure

- `plans/` - Project planning and roadmap documentation
- `specs/` - Technical specifications (empty currently)
- `src/` - Source code (empty currently - implementation needed)

## Development Commands

Always use `uv run` when executing Python scripts instead of `python` directly. This ensures proper dependency management with the uv toolchain.

### Common Development Tasks

- **Run the game**: `uv run run.py`
- **Build executable**: `uv run build.py`
- **Install dependencies**: `uv sync`
- **Run tests**: `uv run pytest` (when tests are added)

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


## Guidelines 
Your goal is to read specs/project_plan.md and implement the game. Study the project plan and implement the most important missing functionality. When you are done, update the project_plan to indicate the feature is complete. 

After implementing functionality or resolving problems, run the tests for that unit of code that was improved**."

Before making changes search codebase (don't assume an item is not implemented) using parrallel subagents. Think hard.

999. Important: When authoring documentation capture the why tests and the backing implementation is important.

9999. Important: We want single sources of truth, no migrations/adapters. If tests unrelated to your work fail then it's your job to resolve these tests as part of the increment of change.

9999. Important: As soon as there are no build or test errors create a git commit with a comment explaing the changes and what was implemented

Include a README.txt that explains how to start and play the game. Update the README as you implement new features.

ULTIMATE GOAL is a functioning rougelike game