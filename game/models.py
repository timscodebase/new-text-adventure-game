"""Core data models for the text adventure game."""

from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass
from enum import Enum
from pydantic import BaseModel, Field
import random
from datetime import datetime, timedelta


class Direction(str, Enum):
    """Valid movement directions."""
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"
    UP = "up"
    DOWN = "down"
    NORTHEAST = "northeast"
    NORTHWEST = "northwest"
    SOUTHEAST = "southeast"
    SOUTHWEST = "southwest"


class ItemType(str, Enum):
    """Types of items in the game."""
    WEAPON = "weapon"
    ARMOR = "armor"
    TOOL = "tool"
    KEY = "key"
    TREASURE = "treasure"
    CONTAINER = "container"
    FOOD = "food"
    POTION = "potion"
    SCROLL = "scroll"
    MISC = "misc"
    MATERIAL = "material"
    CRAFTING = "crafting"


class WeatherType(str, Enum):
    """Types of weather conditions."""
    CLEAR = "clear"
    CLOUDY = "cloudy"
    RAINY = "rainy"
    STORMY = "stormy"
    FOGGY = "foggy"
    SNOWY = "snowy"


class TimeOfDay(str, Enum):
    """Times of day."""
    DAWN = "dawn"
    MORNING = "morning"
    NOON = "noon"
    AFTERNOON = "afternoon"
    DUSK = "dusk"
    NIGHT = "night"


class EnemyType(str, Enum):
    """Types of enemies."""
    GOBLIN = "goblin"
    ORC = "orc"
    TROLL = "troll"
    DRAGON = "dragon"
    SKELETON = "skeleton"
    ZOMBIE = "zombie"
    BANDIT = "bandit"
    WOLF = "wolf"


class QuestStatus(str, Enum):
    """Quest status."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Item(BaseModel):
    """Represents an item in the game world."""
    name: str
    description: str
    item_type: ItemType
    weight: float = 0.0
    value: int = 0
    is_takeable: bool = True
    is_visible: bool = True
    keywords: List[str] = Field(default_factory=list)
    use_description: Optional[str] = None
    required_items: List[str] = Field(default_factory=list)  # Items needed to use this
    durability: int = 100  # New: item durability
    max_durability: int = 100
    damage: int = 0  # New: weapon damage
    armor_value: int = 0  # New: armor protection
    healing_value: int = 0  # New: healing amount
    crafting_recipe: Optional[Dict[str, int]] = None  # New: crafting requirements
    magic_effects: Dict[str, Any] = Field(default_factory=dict)  # New: magical properties


class Equipment(BaseModel):
    """Represents equipped items."""
    weapon: Optional[str] = None
    armor: Optional[str] = None
    helmet: Optional[str] = None
    boots: Optional[str] = None
    gloves: Optional[str] = None
    ring: Optional[str] = None
    amulet: Optional[str] = None


class Enemy(BaseModel):
    """Represents an enemy in the game."""
    id: str
    name: str
    enemy_type: EnemyType
    description: str
    health: int
    max_health: int
    damage: int
    armor: int
    experience_reward: int
    gold_reward: int
    current_room: str
    is_alive: bool = True
    aggression_level: int = 5  # 1-10, how likely to attack
    inventory: List[str] = Field(default_factory=list)
    special_abilities: List[str] = Field(default_factory=list)


class Quest(BaseModel):
    """Represents a quest in the game."""
    id: str
    name: str
    description: str
    quest_giver: str  # NPC ID
    status: QuestStatus = QuestStatus.NOT_STARTED
    requirements: Dict[str, int] = Field(default_factory=dict)  # item_id: count
    rewards: Dict[str, int] = Field(default_factory=dict)  # item_id: count
    experience_reward: int = 0
    gold_reward: int = 0
    is_repeatable: bool = False
    time_limit: Optional[int] = None  # in game hours


class Exit(BaseModel):
    """Represents an exit from one room to another."""
    direction: Direction
    destination: str
    description: Optional[str] = None
    is_locked: bool = False
    required_key: Optional[str] = None
    is_hidden: bool = False
    is_open: bool = True
    required_level: int = 1  # New: level requirement
    required_items: List[str] = Field(default_factory=list)  # New: items needed to pass


class Room(BaseModel):
    """Represents a room in the game world."""
    id: str
    name: str
    description: str
    long_description: Optional[str] = None
    exits: Dict[Direction, Exit] = Field(default_factory=dict)
    items: List[str] = Field(default_factory=list)  # Item IDs
    npcs: List[str] = Field(default_factory=list)  # NPC IDs
    enemies: List[str] = Field(default_factory=list)  # Enemy IDs
    is_visited: bool = False
    is_dark: bool = False
    ambient_sounds: Optional[str] = None
    weather_effects: List[str] = Field(default_factory=list)  # New: weather-specific effects
    is_safe_zone: bool = False  # New: no combat allowed
    respawn_rate: int = 0  # New: enemy respawn rate in minutes


class Player(BaseModel):
    """Represents the player character."""
    name: str
    health: int = 100
    max_health: int = 100
    inventory: List[str] = Field(default_factory=list)  # Item IDs
    equipment: Equipment = Field(default_factory=Equipment)
    current_room: str
    score: int = 0
    moves: int = 0
    is_alive: bool = True
    # New combat stats
    level: int = 1
    experience: int = 0
    experience_to_next: int = 100
    gold: int = 0
    # New attributes
    strength: int = 10
    dexterity: int = 10
    intelligence: int = 10
    constitution: int = 10
    # New status effects
    status_effects: Dict[str, int] = Field(default_factory=dict)  # effect: duration
    # New crafting
    known_recipes: Set[str] = Field(default_factory=set)
    # New quests
    active_quests: List[str] = Field(default_factory=list)  # Quest IDs
    completed_quests: Set[str] = Field(default_factory=set)


class NPC(BaseModel):
    """Represents a non-player character."""
    id: str
    name: str
    description: str
    dialogue: Dict[str, str] = Field(default_factory=dict)
    current_room: str
    is_friendly: bool = True
    inventory: List[str] = Field(default_factory=list)
    health: int = 100
    is_alive: bool = True
    # New NPC features
    schedule: Dict[str, str] = Field(default_factory=dict)  # time: room_id
    quests_offered: List[str] = Field(default_factory=list)  # Quest IDs
    shop_items: List[str] = Field(default_factory=list)  # Items for sale
    shop_prices: Dict[str, int] = Field(default_factory=dict)  # item_id: price
    reputation: int = 0  # Player's reputation with this NPC


class Weather(BaseModel):
    """Represents current weather conditions."""
    current_weather: WeatherType = WeatherType.CLEAR
    temperature: int = 20  # Celsius
    wind_speed: int = 0
    visibility: int = 100  # Percentage
    effects: List[str] = Field(default_factory=list)


class TimeSystem(BaseModel):
    """Represents the game's time system."""
    current_time: datetime = Field(default_factory=datetime.now)
    time_of_day: TimeOfDay = TimeOfDay.MORNING
    day: int = 1
    hour: int = 8
    minute: int = 0
    time_scale: int = 1  # Minutes per real second


class CraftingRecipe(BaseModel):
    """Represents a crafting recipe."""
    id: str
    name: str
    description: str
    materials: Dict[str, int]  # item_id: quantity
    result_item: str
    result_quantity: int = 1
    required_level: int = 1
    required_tools: List[str] = Field(default_factory=list)
    crafting_time: int = 1  # in minutes


class GameState(BaseModel):
    """Represents the current state of the game."""
    player: Player
    rooms: Dict[str, Room] = Field(default_factory=dict)
    items: Dict[str, Item] = Field(default_factory=dict)
    npcs: Dict[str, NPC] = Field(default_factory=dict)
    enemies: Dict[str, Enemy] = Field(default_factory=dict)
    quests: Dict[str, Quest] = Field(default_factory=dict)
    crafting_recipes: Dict[str, CraftingRecipe] = Field(default_factory=dict)
    game_messages: List[str] = Field(default_factory=list)
    is_game_over: bool = False
    victory_conditions: List[str] = Field(default_factory=list)
    completed_quests: Set[str] = Field(default_factory=set)
    # New systems
    weather: Weather = Field(default_factory=Weather)
    time_system: TimeSystem = Field(default_factory=TimeSystem)
    combat_log: List[str] = Field(default_factory=list)
    # New game mechanics
    random_events: List[str] = Field(default_factory=list)
    world_events: Dict[str, Any] = Field(default_factory=dict)
    difficulty_level: int = 1
