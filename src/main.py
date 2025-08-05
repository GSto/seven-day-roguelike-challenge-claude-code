#!/usr/bin/env python3
"""
Devil's Den Roguelike - Main Entry Point
A complete roguelike game built in 7 days using Python and tcod.
"""

import tcod

from game import Game


def main():
    """Main entry point for the game."""
    # Initialize the game
    game = Game()
    
    # Run the main game loop
    game.run()


if __name__ == "__main__":
    main()