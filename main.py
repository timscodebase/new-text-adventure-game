#!/usr/bin/env python3
"""Main entry point for the text adventure game."""

import logging
import sys
from pathlib import Path
import argparse

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from game.engine import GameEngine


def setup_logging() -> None:
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('game.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main() -> None:
    """Main function to start the game."""
    parser = argparse.ArgumentParser(description="Text Adventure Game")
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')
    args = parser.parse_args()

    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting text adventure game")
        engine = GameEngine(no_color=args.no_color)
        engine.start_game()
        logger.info("Game ended")
        
    except KeyboardInterrupt:
        logger.info("Game interrupted by user")
        print("\n\nGame interrupted. Thanks for playing!")
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
