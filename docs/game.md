<a id="ai_player"></a>

# ai\_player

AI player for automated game testing.

<a id="ai_player.AIStrategy"></a>

## AIStrategy Objects

```python
class AIStrategy(Enum)
```

Different AI playing strategies.

<a id="ai_player.AIStrategy.EXPLORER"></a>

#### EXPLORER

Focus on exploring all areas

<a id="ai_player.AIStrategy.COMBATANT"></a>

#### COMBATANT

Focus on combat and leveling

<a id="ai_player.AIStrategy.COLLECTOR"></a>

#### COLLECTOR

Focus on collecting items and crafting

<a id="ai_player.AIStrategy.QUESTER"></a>

#### QUESTER

Focus on completing quests

<a id="ai_player.AIStrategy.RANDOM"></a>

#### RANDOM

Random actions for chaos testing

<a id="ai_player.AIPlayer"></a>

## AIPlayer Objects

```python
class AIPlayer()
```

An AI player that can automatically play the game for testing.

<a id="ai_player.AIPlayer.__init__"></a>

#### \_\_init\_\_

```python
def __init__(strategy: AIStrategy = AIStrategy.EXPLORER,
             max_actions: int = 100)
```

Initialize the AI player.

<a id="ai_player.AIPlayer.play_game"></a>

#### play\_game

```python
def play_game(engine: GameEngine,
              delay: float = 1.0,
              verbose: bool = True) -> Dict[str, any]
```

Play the game automatically and return statistics.

<a id="ai_player.AIPlayer.save_log"></a>

#### save\_log

```python
def save_log(filename: str = "ai_player_log.txt") -> None
```

Save the game log to a file.

<a id="models"></a>

# models

Core data models for the text adventure game.

<a id="models.Direction"></a>

## Direction Objects

```python
class Direction(str, Enum)
```

Valid movement directions.

<a id="models.ItemType"></a>

## ItemType Objects

```python
class ItemType(str, Enum)
```

Types of items in the game.

<a id="models.WeatherType"></a>

## WeatherType Objects

```python
class WeatherType(str, Enum)
```

Types of weather conditions.

<a id="models.TimeOfDay"></a>

## TimeOfDay Objects

```python
class TimeOfDay(str, Enum)
```

Times of day.

<a id="models.EnemyType"></a>

## EnemyType Objects

```python
class EnemyType(str, Enum)
```

Types of enemies.

<a id="models.QuestStatus"></a>

## QuestStatus Objects

```python
class QuestStatus(str, Enum)
```

Quest status.

<a id="models.Item"></a>

## Item Objects

```python
class Item(BaseModel)
```

Represents an item in the game world.

<a id="models.Item.required_items"></a>

#### required\_items

Items needed to use this

<a id="models.Item.durability"></a>

#### durability

New: item durability

<a id="models.Item.damage"></a>

#### damage

New: weapon damage

<a id="models.Item.armor_value"></a>

#### armor\_value

New: armor protection

<a id="models.Item.healing_value"></a>

#### healing\_value

New: healing amount

<a id="models.Item.crafting_recipe"></a>

#### crafting\_recipe

New: crafting requirements

<a id="models.Item.magic_effects"></a>

#### magic\_effects

New: magical properties

<a id="models.Equipment"></a>

## Equipment Objects

```python
class Equipment(BaseModel)
```

Represents equipped items.

<a id="models.Enemy"></a>

## Enemy Objects

```python
class Enemy(BaseModel)
```

Represents an enemy in the game.

<a id="models.Enemy.aggression_level"></a>

#### aggression\_level

1-10, how likely to attack

<a id="models.Quest"></a>

## Quest Objects

```python
class Quest(BaseModel)
```

Represents a quest in the game.

<a id="models.Quest.quest_giver"></a>

#### quest\_giver

NPC ID

<a id="models.Quest.requirements"></a>

#### requirements

item_id: count

<a id="models.Quest.rewards"></a>

#### rewards

item_id: count

<a id="models.Quest.time_limit"></a>

#### time\_limit

in game hours

<a id="models.Exit"></a>

## Exit Objects

```python
class Exit(BaseModel)
```

Represents an exit from one room to another.

<a id="models.Exit.required_level"></a>

#### required\_level

New: level requirement

<a id="models.Exit.required_items"></a>

#### required\_items

New: items needed to pass

<a id="models.Room"></a>

## Room Objects

```python
class Room(BaseModel)
```

Represents a room in the game world.

<a id="models.Room.items"></a>

#### items

Item IDs

<a id="models.Room.npcs"></a>

#### npcs

NPC IDs

<a id="models.Room.enemies"></a>

#### enemies

Enemy IDs

<a id="models.Room.weather_effects"></a>

#### weather\_effects

New: weather-specific effects

<a id="models.Room.is_safe_zone"></a>

#### is\_safe\_zone

New: no combat allowed

<a id="models.Room.respawn_rate"></a>

#### respawn\_rate

New: enemy respawn rate in minutes

<a id="models.Player"></a>

## Player Objects

```python
class Player(BaseModel)
```

Represents the player character.

<a id="models.Player.inventory"></a>

#### inventory

Item IDs

<a id="models.Player.status_effects"></a>

#### status\_effects

effect: duration

<a id="models.Player.active_quests"></a>

#### active\_quests

Quest IDs

<a id="models.NPC"></a>

## NPC Objects

```python
class NPC(BaseModel)
```

Represents a non-player character.

<a id="models.NPC.schedule"></a>

#### schedule

time: room_id

<a id="models.NPC.quests_offered"></a>

#### quests\_offered

Quest IDs

<a id="models.NPC.shop_items"></a>

#### shop\_items

Items for sale

<a id="models.NPC.shop_prices"></a>

#### shop\_prices

item_id: price

<a id="models.NPC.reputation"></a>

#### reputation

Player's reputation with this NPC

<a id="models.Weather"></a>

## Weather Objects

```python
class Weather(BaseModel)
```

Represents current weather conditions.

<a id="models.Weather.temperature"></a>

#### temperature

Celsius

<a id="models.Weather.visibility"></a>

#### visibility

Percentage

<a id="models.TimeSystem"></a>

## TimeSystem Objects

```python
class TimeSystem(BaseModel)
```

Represents the game's time system.

<a id="models.TimeSystem.time_scale"></a>

#### time\_scale

Minutes per real second

<a id="models.CraftingRecipe"></a>

## CraftingRecipe Objects

```python
class CraftingRecipe(BaseModel)
```

Represents a crafting recipe.

<a id="models.CraftingRecipe.materials"></a>

#### materials

item_id: quantity

<a id="models.CraftingRecipe.crafting_time"></a>

#### crafting\_time

in minutes

<a id="models.GameState"></a>

## GameState Objects

```python
class GameState(BaseModel)
```

Represents the current state of the game.

<a id="combat"></a>

# combat

Combat system for the text adventure game.

<a id="combat.CombatSystem"></a>

## CombatSystem Objects

```python
class CombatSystem()
```

Handles combat between player and enemies.

<a id="combat.CombatSystem.__init__"></a>

#### \_\_init\_\_

```python
def __init__(game_state: GameState) -> None
```

Initialize the combat system.

<a id="combat.CombatSystem.start_combat"></a>

#### start\_combat

```python
def start_combat(enemy_id: str) -> str
```

Start combat with an enemy.

<a id="combat.CombatSystem.attack"></a>

#### attack

```python
def attack(target_name: str = "") -> str
```

Player attacks an enemy.

<a id="combat.CombatSystem.flee"></a>

#### flee

```python
def flee() -> str
```

Attempt to flee from combat.

<a id="combat.CombatSystem.use_item"></a>

#### use\_item

```python
def use_item(item_name: str) -> str
```

Use an item during combat.

<a id="combat.CombatSystem.get_combat_status"></a>

#### get\_combat\_status

```python
def get_combat_status() -> str
```

Get current combat status.

<a id="quests"></a>

# quests

Quest system for the text adventure game.

<a id="quests.QuestSystem"></a>

## QuestSystem Objects

```python
class QuestSystem()
```

Handles quest management and progression.

<a id="quests.QuestSystem.__init__"></a>

#### \_\_init\_\_

```python
def __init__(game_state: GameState) -> None
```

Initialize the quest system.

<a id="quests.QuestSystem.get_available_quests"></a>

#### get\_available\_quests

```python
def get_available_quests() -> List[Quest]
```

Get quests available to the player.

<a id="quests.QuestSystem.accept_quest"></a>

#### accept\_quest

```python
def accept_quest(quest_name: str) -> str
```

Accept a quest from an NPC.

<a id="quests.QuestSystem.check_quest_progress"></a>

#### check\_quest\_progress

```python
def check_quest_progress() -> str
```

Check progress on all active quests.

<a id="quests.QuestSystem.list_quests"></a>

#### list\_quests

```python
def list_quests() -> str
```

List all quests and their status.

<a id="quests.QuestSystem.get_quest_details"></a>

#### get\_quest\_details

```python
def get_quest_details(quest_name: str) -> str
```

Get detailed information about a quest.

<a id="world_builder"></a>

# world\_builder

World builder for creating the game world.

<a id="world_builder.WorldBuilder"></a>

## WorldBuilder Objects

```python
class WorldBuilder()
```

Builds the game world with rooms, items, and NPCs.

<a id="world_builder.WorldBuilder.create_world"></a>

#### create\_world

```python
def create_world() -> GameState
```

Create a complete game world.

<a id="save_system"></a>

# save\_system

Save and load system for the text adventure game.

<a id="save_system.SaveSystem"></a>

## SaveSystem Objects

```python
class SaveSystem()
```

Handles saving and loading game states.

<a id="save_system.SaveSystem.__init__"></a>

#### \_\_init\_\_

```python
def __init__(save_directory: str = "saves") -> None
```

Initialize the save system.

<a id="save_system.SaveSystem.save_game"></a>

#### save\_game

```python
def save_game(game_state: GameState, save_name: str = "autosave") -> bool
```

Save the current game state to a file.

<a id="save_system.SaveSystem.load_game"></a>

#### load\_game

```python
def load_game(save_name: str) -> Optional[GameState]
```

Load a game state from a file.

<a id="save_system.SaveSystem.list_saves"></a>

#### list\_saves

```python
def list_saves() -> List[Dict[str, Any]]
```

List all available save files.

<a id="save_system.SaveSystem.delete_save"></a>

#### delete\_save

```python
def delete_save(save_name: str) -> bool
```

Delete a save file.

<a id="save_system.SaveSystem.create_backup"></a>

#### create\_backup

```python
def create_backup(game_state: GameState) -> bool
```

Create a backup save.

<a id="save_system.SaveSystem.get_save_info"></a>

#### get\_save\_info

```python
def get_save_info(save_name: str) -> Optional[Dict[str, Any]]
```

Get detailed information about a save file.

<a id="save_system.SaveSystem.export_save"></a>

#### export\_save

```python
def export_save(save_name: str, export_path: str) -> bool
```

Export a save file to a different location.

<a id="save_system.SaveSystem.import_save"></a>

#### import\_save

```python
def import_save(import_path: str, save_name: str = None) -> bool
```

Import a save file from a different location.

<a id="crafting"></a>

# crafting

Crafting system for the text adventure game.

<a id="crafting.CraftingSystem"></a>

## CraftingSystem Objects

```python
class CraftingSystem()
```

Handles item crafting and recipe management.

<a id="crafting.CraftingSystem.__init__"></a>

#### \_\_init\_\_

```python
def __init__(game_state: GameState) -> None
```

Initialize the crafting system.

<a id="crafting.CraftingSystem.get_available_recipes"></a>

#### get\_available\_recipes

```python
def get_available_recipes() -> List[CraftingRecipe]
```

Get recipes the player can craft.

<a id="crafting.CraftingSystem.craft_item"></a>

#### craft\_item

```python
def craft_item(recipe_name: str) -> str
```

Craft an item using a recipe.

<a id="crafting.CraftingSystem.learn_recipe"></a>

#### learn\_recipe

```python
def learn_recipe(recipe_id: str) -> str
```

Learn a new crafting recipe.

<a id="crafting.CraftingSystem.get_recipe_info"></a>

#### get\_recipe\_info

```python
def get_recipe_info(recipe_name: str) -> str
```

Get detailed information about a recipe.

<a id="crafting.CraftingSystem.list_recipes"></a>

#### list\_recipes

```python
def list_recipes() -> str
```

List all known recipes.

<a id="engine"></a>

# engine

Main game engine for the text adventure game.

<a id="engine.CommandHistory"></a>

## CommandHistory Objects

```python
class CommandHistory()
```

Handles command history for the game.

<a id="engine.CommandHistory.__init__"></a>

#### \_\_init\_\_

```python
def __init__(history_file: str = ".game_history") -> None
```

Initialize command history.

<a id="engine.CommandHistory.save_history"></a>

#### save\_history

```python
def save_history() -> None
```

Save command history to file.

<a id="engine.CommandHistory.add_command"></a>

#### add\_command

```python
def add_command(command: str) -> None
```

Add a command to history.

<a id="engine.CommandHistory.get_history"></a>

#### get\_history

```python
def get_history() -> List[str]
```

Get the current command history.

<a id="engine.CommandHistory.clear_history"></a>

#### clear\_history

```python
def clear_history() -> None
```

Clear the command history.

<a id="engine.GameEngine"></a>

## GameEngine Objects

```python
class GameEngine()
```

Main game engine that manages the game state and logic.

<a id="engine.GameEngine.__init__"></a>

#### \_\_init\_\_

```python
def __init__(no_color: bool = False) -> None
```

Initialize the game engine.

<a id="engine.GameEngine.start_game"></a>

#### start\_game

```python
def start_game() -> None
```

Start the game and display the initial room.

<a id="engine.GameEngine.get_player_status"></a>

#### get\_player\_status

```python
def get_player_status() -> str
```

Get a formatted status display for the player.

<a id="engine.GameEngine.save_game"></a>

#### save\_game

```python
def save_game(save_name: str) -> bool
```

Save the current game state.

<a id="engine.GameEngine.load_game"></a>

#### load\_game

```python
def load_game(save_name: str) -> bool
```

Load a game state.

<a id="engine.GameEngine.list_saves"></a>

#### list\_saves

```python
def list_saves() -> List[str]
```

List available save files.

<a id="engine.GameEngine.delete_save"></a>

#### delete\_save

```python
def delete_save(save_name: str) -> bool
```

Delete a save file.

<a id="engine.GameEngine.create_backup"></a>

#### create\_backup

```python
def create_backup(save_name: str) -> bool
```

Create a backup of a save file.

<a id="engine.GameEngine.get_save_info"></a>

#### get\_save\_info

```python
def get_save_info(save_name: str) -> Optional[Dict[str, Any]]
```

Get information about a save file.

<a id="visuals"></a>

# visuals

Visuals for the text adventure game.

<a id="visuals.Visuals"></a>

## Visuals Objects

```python
class Visuals()
```

Handles all visuals for the game.

<a id="visuals.Visuals.get_room_visual"></a>

#### get\_room\_visual

```python
@classmethod
def get_room_visual(cls, room, npcs, enemies) -> str
```

Get the visual representation of a room.

<a id="visuals.Visuals.get_title_banner"></a>

#### get\_title\_banner

```python
@classmethod
def get_title_banner(cls) -> str
```

Get the game title banner.

<a id="visuals.Visuals.get_victory_banner"></a>

#### get\_victory\_banner

```python
@classmethod
def get_victory_banner(cls) -> str
```

Get the victory banner.

<a id="visuals.Visuals.get_game_over_banner"></a>

#### get\_game\_over\_banner

```python
@classmethod
def get_game_over_banner(cls) -> str
```

Get the game over banner.

<a id="visuals.Visuals.get_room_decoration"></a>

#### get\_room\_decoration

```python
@classmethod
def get_room_decoration(cls, room_id: str) -> Optional[str]
```

Get room decoration art.

<a id="visuals.Visuals.get_enemy_art"></a>

#### get\_enemy\_art

```python
@classmethod
def get_enemy_art(cls, enemy_type: str) -> Optional[str]
```

Get enemy art.

<a id="visuals.Visuals.get_item_art"></a>

#### get\_item\_art

```python
@classmethod
def get_item_art(cls, item_name: str) -> Optional[str]
```

Get item art.

<a id="visuals.Visuals.get_npc_art"></a>

#### get\_npc\_art

```python
@classmethod
def get_npc_art(cls, npc_name: str) -> Optional[str]
```

Get NPC art.

<a id="visuals.Visuals.get_combat_art"></a>

#### get\_combat\_art

```python
@classmethod
def get_combat_art(cls, action: str) -> Optional[str]
```

Get combat action art.

<a id="visuals.Visuals.get_status_art"></a>

#### get\_status\_art

```python
@classmethod
def get_status_art(cls, status: str) -> Optional[str]
```

Get status effect art.

<a id="visuals.Visuals.create_box"></a>

#### create\_box

```python
@classmethod
def create_box(cls, title: str, content: str, width: int = 60) -> str
```

Create a fancy box around content.

<a id="visuals.Visuals.create_separator"></a>

#### create\_separator

```python
@classmethod
def create_separator(cls, char: str = "-", width: int = 60) -> str
```

Create a separator line.

<a id="visuals.Visuals.center_text"></a>

#### center\_text

```python
@classmethod
def center_text(cls, text: str, width: int = 60) -> str
```

Center text within a given width.

<a id="visuals.Visuals.create_progress_bar"></a>

#### create\_progress\_bar

```python
@classmethod
def create_progress_bar(cls,
                        current: int,
                        maximum: int,
                        width: int = 20,
                        filled_char: str = "#",
                        empty_char: str = " ") -> str
```

Create a visual progress bar.

<a id="visuals.Visuals.create_health_bar"></a>

#### create\_health\_bar

```python
@classmethod
def create_health_bar(cls, current: int, maximum: int) -> str
```

Create a health bar.

<a id="visuals.Visuals.create_experience_bar"></a>

#### create\_experience\_bar

```python
@classmethod
def create_experience_bar(cls, current: int, maximum: int) -> str
```

Create an experience bar.

<a id="visuals.Visuals.create_centered_box"></a>

#### create\_centered\_box

```python
@classmethod
def create_centered_box(cls, title: str, content: str, width: int = 60) -> str
```

Create a centered box with title and content.

<a id="commands"></a>

# commands

Command parsing and execution for the text adventure game.

<a id="commands.CommandParser"></a>

## CommandParser Objects

```python
class CommandParser()
```

Parses and executes player commands.

<a id="commands.CommandParser.__init__"></a>

#### \_\_init\_\_

```python
def __init__(game_state: GameState,
             command_history=None,
             console=None) -> None
```

Initialize the command parser with the game state.

<a id="commands.CommandParser.parse_and_execute"></a>

#### parse\_and\_execute

```python
def parse_and_execute(command: str) -> Optional[str]
```

Parse a command string and execute the appropriate action.

