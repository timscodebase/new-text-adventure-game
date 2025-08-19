"""Tests for the game models."""

import pytest
from game.models import (
    Direction, ItemType, Item, Exit, Room, Player, NPC, GameState
)


class TestDirection:
    """Test the Direction enum."""
    
    def test_direction_values(self) -> None:
        """Test that all direction values are valid."""
        assert Direction.NORTH == "north"
        assert Direction.SOUTH == "south"
        assert Direction.EAST == "east"
        assert Direction.WEST == "west"
        assert Direction.UP == "up"
        assert Direction.DOWN == "down"


class TestItem:
    """Test the Item model."""
    
    def test_item_creation(self) -> None:
        """Test creating a basic item."""
        item = Item(
            name="test sword",
            description="A test sword",
            item_type=ItemType.WEAPON,
            value=50
        )
        
        assert item.name == "test sword"
        assert item.description == "A test sword"
        assert item.item_type == ItemType.WEAPON
        assert item.value == 50
        assert item.is_takeable is True
        assert item.is_visible is True
    
    def test_item_with_keywords(self) -> None:
        """Test item with keywords."""
        item = Item(
            name="rusty key",
            description="A rusty key",
            item_type=ItemType.KEY,
            keywords=["key", "rusty", "old"]
        )
        
        assert "key" in item.keywords
        assert "rusty" in item.keywords
        assert "old" in item.keywords


class TestRoom:
    """Test the Room model."""
    
    def test_room_creation(self) -> None:
        """Test creating a basic room."""
        room = Room(
            id="test_room",
            name="Test Room",
            description="A test room"
        )
        
        assert room.id == "test_room"
        assert room.name == "Test Room"
        assert room.description == "A test room"
        assert room.is_visited is False
        assert room.is_dark is False
    
    def test_room_with_exits(self) -> None:
        """Test room with exits."""
        exit_north = Exit(
            direction=Direction.NORTH,
            destination="north_room"
        )
        
        room = Room(
            id="test_room",
            name="Test Room",
            description="A test room",
            exits={Direction.NORTH: exit_north}
        )
        
        assert Direction.NORTH in room.exits
        assert room.exits[Direction.NORTH].destination == "north_room"


class TestPlayer:
    """Test the Player model."""
    
    def test_player_creation(self) -> None:
        """Test creating a player."""
        player = Player(
            name="Test Player",
            current_room="entrance"
        )
        
        assert player.name == "Test Player"
        assert player.current_room == "entrance"
        assert player.health == 100
        assert player.max_health == 100
        assert player.score == 0
        assert player.moves == 0
        assert player.is_alive is True


class TestGameState:
    """Test the GameState model."""
    
    def test_game_state_creation(self) -> None:
        """Test creating a game state."""
        player = Player(name="Test Player", current_room="entrance")
        rooms = {"entrance": Room(id="entrance", name="Entrance", description="An entrance")}
        items = {"sword": Item(name="sword", description="A sword", item_type=ItemType.WEAPON)}
        
        game_state = GameState(
            player=player,
            rooms=rooms,
            items=items
        )
        
        assert game_state.player.name == "Test Player"
        assert "entrance" in game_state.rooms
        assert "sword" in game_state.items
        assert game_state.is_game_over is False
