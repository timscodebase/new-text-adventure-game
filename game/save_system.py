"""Save and load system for the text adventure game."""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from game.models import GameState


logger = logging.getLogger(__name__)


class SaveSystem:
    """Handles saving and loading game states."""
    
    def __init__(self, save_directory: str = "saves") -> None:
        """Initialize the save system."""
        self.save_directory = Path(save_directory)
        self.save_directory.mkdir(exist_ok=True)
    
    def save_game(self, game_state: GameState, save_name: str = "autosave") -> bool:
        """Save the current game state to a file."""
        try:
            # Create save data
            save_data = self._serialize_game_state(game_state)
            
            # Add metadata
            save_data["metadata"] = {
                "save_name": save_name,
                "save_date": datetime.now().isoformat(),
                "game_version": "1.0.0",
                "player_name": game_state.player.name,
                "player_level": game_state.player.level,
                "current_room": game_state.player.current_room,
                "play_time": game_state.player.moves,  # Rough estimate
                "score": game_state.player.score
            }
            
            # Save to file
            save_file = self.save_directory / f"{save_name}.json"
            with open(save_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Game saved to {save_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving game: {e}")
            return False
    
    def load_game(self, save_name: str) -> Optional[GameState]:
        """Load a game state from a file."""
        try:
            save_file = self.save_directory / f"{save_name}.json"
            
            if not save_file.exists():
                logger.error(f"Save file {save_file} not found")
                return None
            
            with open(save_file, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            # Validate save data
            if not self._validate_save_data(save_data):
                logger.error("Invalid save data")
                return None
            
            # Deserialize game state
            game_state = self._deserialize_game_state(save_data)
            
            logger.info(f"Game loaded from {save_file}")
            return game_state
            
        except Exception as e:
            logger.error(f"Error loading game: {e}")
            return None
    
    def list_saves(self) -> List[Dict[str, Any]]:
        """List all available save files."""
        saves = []
        
        for save_file in self.save_directory.glob("*.json"):
            try:
                with open(save_file, 'r', encoding='utf-8') as f:
                    save_data = json.load(f)
                
                metadata = save_data.get("metadata", {})
                saves.append({
                    "name": save_file.stem,
                    "date": metadata.get("save_date", "Unknown"),
                    "player_name": metadata.get("player_name", "Unknown"),
                    "level": metadata.get("player_level", 1),
                    "room": metadata.get("current_room", "Unknown"),
                    "score": metadata.get("score", 0),
                    "play_time": metadata.get("play_time", 0)
                })
                
            except Exception as e:
                logger.error(f"Error reading save file {save_file}: {e}")
                continue
        
        # Sort by date (newest first)
        saves.sort(key=lambda x: x["date"], reverse=True)
        return saves
    
    def delete_save(self, save_name: str) -> bool:
        """Delete a save file."""
        try:
            save_file = self.save_directory / f"{save_name}.json"
            
            if not save_file.exists():
                logger.error(f"Save file {save_file} not found")
                return False
            
            save_file.unlink()
            logger.info(f"Save file {save_file} deleted")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting save file: {e}")
            return False
    
    def _serialize_game_state(self, game_state: GameState) -> Dict[str, Any]:
        """Serialize the game state to a dictionary."""
        # Convert GameState to dict, handling complex objects
        state_dict = game_state.model_dump()
        
        # Handle datetime objects
        if "time_system" in state_dict:
            time_system = state_dict["time_system"]
            if "current_time" in time_system:
                time_system["current_time"] = time_system["current_time"].isoformat()
        
        return state_dict
    
    def _deserialize_game_state(self, save_data: Dict[str, Any]) -> GameState:
        """Deserialize a dictionary back to GameState."""
        # Handle datetime objects
        if "time_system" in save_data:
            time_system = save_data["time_system"]
            if "current_time" in time_system:
                time_system["current_time"] = datetime.fromisoformat(time_system["current_time"])
        
        # Create GameState from dict
        return GameState(**save_data)
    
    def _validate_save_data(self, save_data: Dict[str, Any]) -> bool:
        """Validate that save data has required fields."""
        required_fields = ["player", "rooms", "items", "npcs", "enemies", "quests"]
        
        for field in required_fields:
            if field not in save_data:
                logger.error(f"Missing required field: {field}")
                return False
        
        return True
    
    def create_backup(self, game_state: GameState) -> bool:
        """Create a backup save."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}"
        return self.save_game(game_state, backup_name)
    
    def get_save_info(self, save_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a save file."""
        try:
            save_file = self.save_directory / f"{save_name}.json"
            
            if not save_file.exists():
                return None
            
            with open(save_file, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            metadata = save_data.get("metadata", {})
            
            # Calculate file size
            file_size = save_file.stat().st_size
            
            return {
                "name": save_name,
                "file_size": file_size,
                "metadata": metadata,
                "has_player": "player" in save_data,
                "has_rooms": "rooms" in save_data,
                "room_count": len(save_data.get("rooms", {})),
                "item_count": len(save_data.get("items", {})),
                "npc_count": len(save_data.get("npcs", {})),
                "enemy_count": len(save_data.get("enemies", {})),
                "quest_count": len(save_data.get("quests", {}))
            }
            
        except Exception as e:
            logger.error(f"Error getting save info: {e}")
            return None
    
    def export_save(self, save_name: str, export_path: str) -> bool:
        """Export a save file to a different location."""
        try:
            save_file = self.save_directory / f"{save_name}.json"
            export_file = Path(export_path)
            
            if not save_file.exists():
                logger.error(f"Save file {save_file} not found")
                return False
            
            # Copy the file
            import shutil
            shutil.copy2(save_file, export_file)
            
            logger.info(f"Save exported to {export_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting save: {e}")
            return False
    
    def import_save(self, import_path: str, save_name: str = None) -> bool:
        """Import a save file from a different location."""
        try:
            import_file = Path(import_path)
            
            if not import_file.exists():
                logger.error(f"Import file {import_file} not found")
                return False
            
            # Validate the import file
            with open(import_file, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            if not self._validate_save_data(save_data):
                logger.error("Invalid import file")
                return False
            
            # Determine save name
            if save_name is None:
                save_name = import_file.stem
            
            # Copy to save directory
            save_file = self.save_directory / f"{save_name}.json"
            import shutil
            shutil.copy2(import_file, save_file)
            
            logger.info(f"Save imported as {save_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error importing save: {e}")
            return False
