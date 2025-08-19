"""Main game engine for the text adventure game."""

import logging
import re
import readline
import os
from typing import Dict, List, Optional, Tuple, Any
from game.models import (
    GameState, Player, Room, Item, NPC, Direction, Exit, ItemType
)
from game.commands import CommandParser
from game.world_builder import WorldBuilder
from game.save_system import SaveSystem
from game.ascii_art import ASCIIArt


logger = logging.getLogger(__name__)


class CommandHistory:
    """Handles command history for the game."""
    
    def __init__(self, history_file: str = ".game_history") -> None:
        """Initialize command history."""
        self.history_file = history_file
        self._setup_readline()
        self._load_history()
    
    def _setup_readline(self) -> None:
        """Setup readline for command history."""
        try:
            # Set up readline for command history
            readline.set_history_length(1000)  # Store up to 1000 commands
            
            # Set up tab completion (basic implementation)
            readline.set_completer(self._completer)
            readline.parse_and_bind("tab: complete")
            
            # Set up history file
            if os.path.exists(self.history_file):
                readline.read_history_file(self.history_file)
                
        except Exception as e:
            logger.warning(f"Could not setup readline: {e}")
    
    def _completer(self, text: str, state: int) -> Optional[str]:
        """Basic tab completion for common commands."""
        commands = [
            'help', 'look', 'examine', 'take', 'drop', 'inventory', 'use',
            'north', 'south', 'east', 'west', 'up', 'down',
            'talk', 'attack', 'flee', 'equip', 'unequip', 'craft', 'recipes',
            'quest', 'quests', 'accept', 'progress', 'shop', 'buy', 'sell',
            'stats', 'gold', 'level', 'save', 'load', 'quit', 'exit'
        ]
        
        matches = [cmd for cmd in commands if cmd.startswith(text.lower())]
        return matches[state] if state < len(matches) else None
    
    def _load_history(self) -> None:
        """Load command history from file."""
        try:
            if os.path.exists(self.history_file):
                readline.read_history_file(self.history_file)
        except Exception as e:
            logger.warning(f"Could not load history: {e}")
    
    def save_history(self) -> None:
        """Save command history to file."""
        try:
            readline.write_history_file(self.history_file)
        except Exception as e:
            logger.warning(f"Could not save history: {e}")
    
    def add_command(self, command: str) -> None:
        """Add a command to history."""
        try:
            readline.add_history(command)
        except Exception as e:
            logger.warning(f"Could not add command to history: {e}")
    
    def get_history(self) -> List[str]:
        """Get the current command history."""
        try:
            return [readline.get_history_item(i) for i in range(1, readline.get_current_history_length() + 1)]
        except Exception as e:
            logger.warning(f"Could not get history: {e}")
            return []
    
    def clear_history(self) -> None:
        """Clear the command history."""
        try:
            readline.clear_history()
        except Exception as e:
            logger.warning(f"Could not clear history: {e}")


class GameEngine:
    """Main game engine that manages the game state and logic."""
    
    def __init__(self) -> None:
        """Initialize the game engine."""
        self.state: GameState
        self.command_parser: CommandParser
        self.world_builder: WorldBuilder
        self.save_system: SaveSystem
        self.command_history: CommandHistory
        self._initialize_game()
    
    def _initialize_game(self) -> None:
        """Initialize the game state and components."""
        self.world_builder = WorldBuilder()
        self.state = self.world_builder.create_world()
        self.command_history = CommandHistory()
        self.command_parser = CommandParser(self.state, self.command_history)
        self.save_system = SaveSystem()
        logger.info("Game engine initialized")
    
    def start_game(self) -> None:
        """Start the game and display the initial room."""
        # Display fancy title banner
        print(ASCIIArt.get_title_banner())
        print(ASCIIArt.center_text("Type 'help' for commands, 'quit' to exit"))
        print(ASCIIArt.center_text("Use ↑/↓ arrows to browse command history"))
        print(ASCIIArt.create_separator("═", 60))
        print()
        
        # Give player some starting recipes
        self.state.player.known_recipes.add("torch")
        self.state.player.known_recipes.add("health_potion")
        
        self._display_room()
        self._game_loop()
    
    def _game_loop(self) -> None:
        """Main game loop."""
        while not self.state.is_game_over and self.state.player.is_alive:
            try:
                command = input("\n> ").strip()
                if not command:
                    continue
                
                # Add command to history (before converting to lowercase)
                self.command_history.add_command(command)
                
                command_lower = command.lower()
                
                if command_lower in ['quit', 'exit', 'q']:
                    print("Thanks for playing!")
                    break
                
                self._process_command(command_lower)
                
                # Check quest progress after each command
                self._check_quest_progress()
                
            except KeyboardInterrupt:
                print("\n\nGame interrupted. Thanks for playing!")
                break
            except Exception as e:
                logger.error(f"Error in game loop: {e}")
                print("Something went wrong. Please try again.")
        
        # Save command history when game ends
        self.command_history.save_history()
    
    def _process_command(self, command: str) -> None:
        """Process a player command."""
        try:
            result = self.command_parser.parse_and_execute(command)
            if result:
                print(result)
            
            # Check for victory conditions
            self._check_victory_conditions()
            
        except Exception as e:
            logger.error(f"Error processing command '{command}': {e}")
            print("I don't understand that command.")
    
    def _display_room(self) -> None:
        """Display the current room description with ASCII art."""
        current_room = self.state.rooms[self.state.player.current_room]
        
        # Get room decoration art
        room_art = ASCIIArt.get_room_decoration(current_room.id)
        if room_art:
            print(room_art)
        else:
            # Default room header
            print(ASCIIArt.create_box("", current_room.name.upper(), 60))
        
        print()
        
        # Room description
        if current_room.is_visited:
            print(current_room.description)
        else:
            print(current_room.long_description or current_room.description)
            current_room.is_visited = True
        
        print()
        
        # Display exits
        if current_room.exits:
            exit_dirs = [exit_obj.direction.value for exit_obj in current_room.exits.values() if exit_obj.is_open]
            if exit_dirs:
                print(f"🚪 Exits: {', '.join(exit_dirs)}")
        
        # Display items in room
        room_items = [self.state.items[item_id] for item_id in current_room.items 
                     if item_id in self.state.items and self.state.items[item_id].is_visible]
        if room_items:
            print(f"📦 You see: {', '.join(item.name for item in room_items)}")
        
        # Display NPCs in room
        room_npcs = [self.state.npcs[npc_id] for npc_id in current_room.npcs 
                    if npc_id in self.state.npcs and self.state.npcs[npc_id].is_alive]
        if room_npcs:
            print(f"👥 Present: {', '.join(npc.name for npc in room_npcs)}")
        
        # Display enemies in room
        room_enemies = [self.state.enemies[enemy_id] for enemy_id in current_room.enemies 
                       if enemy_id in self.state.enemies and self.state.enemies[enemy_id].is_alive]
        if room_enemies:
            print(f"👹 Enemies: {', '.join(enemy.name for enemy in room_enemies)}")
        
        print()
        print(ASCIIArt.create_separator("─", 60))
    
    def _check_victory_conditions(self) -> None:
        """Check if victory conditions have been met."""
        # Example victory condition: player has a specific item
        if "treasure_chest" in self.state.player.inventory:
            print()
            print(ASCIIArt.get_victory_banner())
            print()
            self.state.is_game_over = True
    
    def _check_quest_progress(self) -> None:
        """Check and update quest progress after each command."""
        from game.quests import QuestSystem
        quest_system = QuestSystem(self.state)
        quest_system.check_quest_progress()
    
    def get_player_status(self) -> str:
        """Get a formatted status display for the player."""
        player = self.state.player
        
        # Create a fancy status box
        status_lines = [
            f"👤 {player.name} (Level {player.level})",
            f"❤️  Health: {ASCIIArt.create_health_bar(player.health, player.max_health)}",
            f"⭐ Experience: {ASCIIArt.create_experience_bar(player.experience, player.experience_to_next)}",
            f"💰 Gold: {player.gold}",
            f"🎒 Items: {len(player.inventory)}/{player.max_inventory}",
            f"🚶 Moves: {player.moves}",
            f"📍 Location: {self.state.rooms[player.current_room].name}"
        ]
        
        return ASCIIArt.create_box("Player Status", "\n".join(status_lines), 50)
    
    # Save/Load methods that delegate to SaveSystem
    def save_game(self, save_name: str) -> bool:
        """Save the current game state."""
        return self.save_system.save_game(self.state, save_name)
    
    def load_game(self, save_name: str) -> bool:
        """Load a game state."""
        loaded_state = self.save_system.load_game(save_name)
        if loaded_state:
            self.state = loaded_state
            # Reinitialize command parser with new state
            self.command_parser = CommandParser(self.state, self.command_history)
            return True
        return False
    
    def list_saves(self) -> List[str]:
        """List available save files."""
        return self.save_system.list_saves()
    
    def delete_save(self, save_name: str) -> bool:
        """Delete a save file."""
        return self.save_system.delete_save(save_name)
    
    def create_backup(self, save_name: str) -> bool:
        """Create a backup of a save file."""
        return self.save_system.create_backup(save_name)
    
    def get_save_info(self, save_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a save file."""
        return self.save_system.get_save_info(save_name)
