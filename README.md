# Enhanced Text Adventure Game

A comprehensive Zork-style text adventure game built in Python with modern architecture, advanced game systems, and best practices.

## 🚀 **Major Features**

### **Core Systems**
- **Modular Design**: Clean, maintainable code structure with separate modules for different game components
- **Rich Game World**: Multiple interconnected rooms with items, NPCs, enemies, and puzzles
- **Interactive Commands**: Natural language command parsing with helpful feedback
- **Type Safety**: Full type hints and Pydantic models for data validation
- **Comprehensive Logging**: Detailed logging for debugging and monitoring
- **Extensible Architecture**: Easy to add new rooms, items, NPCs, and game mechanics

### **Combat System** ⚔️
- **Turn-based Combat**: Strategic battles with enemies
- **Weapon & Armor System**: Equipment affects damage and defense
- **Experience & Leveling**: Gain XP and level up with stat increases
- **Special Abilities**: Enemies have unique abilities (poison, stun, heal)
- **Flee Mechanics**: Attempt to escape from dangerous situations
- **Combat Status**: Real-time health and status tracking

### **Crafting System** 🔨
- **Recipe System**: Learn and craft items from materials
- **Material Collection**: Gather resources throughout the world
- **Tool Requirements**: Some recipes require specific tools
- **Level Requirements**: Advanced recipes require higher levels
- **Item Durability**: Equipment wears out over time
- **Crafting Time**: Realistic crafting durations

### **Quest System** 📜
- **Multiple Quest Types**: Collection, exploration, crafting, and combat quests
- **NPC Quest Givers**: Different characters offer unique quests
- **Quest Progress Tracking**: Real-time progress monitoring
- **Rewards System**: Experience, gold, and item rewards
- **Repeatable Quests**: Some quests can be completed multiple times
- **Quest Requirements**: Level and item requirements

### **Equipment System** 🛡️
- **Multiple Equipment Slots**: Weapon, armor, helmet, boots, gloves, rings, amulets
- **Equipment Effects**: Items provide damage, armor, and special bonuses
- **Equipment Management**: Easy equip/unequip commands
- **Equipment Display**: Clear view of all equipped items

### **Trading System** 💰
- **NPC Merchants**: Buy and sell items with merchants
- **Dynamic Pricing**: Items have different buy/sell prices
- **Shop Inventories**: Merchants have specific items for sale
- **Gold Economy**: Earn and spend gold throughout the game

### **Save/Load System** 💾
- **Multiple Save Slots**: Save your progress in different slots
- **JSON Serialization**: Human-readable save files
- **Save Metadata**: Track save dates, player info, and game stats
- **Backup System**: Automatic backup creation
- **Import/Export**: Share save files between installations

## 🎮 **Game World**

The enhanced game features:

- **9 interconnected rooms** including an entrance, guard room, market, library, treasure chamber, and underground caves
- **20+ unique items** including weapons, armor, tools, materials, and magical items
- **3 NPCs** with dialogue, quests, and trading capabilities
- **3 enemies** with unique abilities and loot drops
- **Multiple crafting recipes** for creating powerful equipment
- **5 quests** with different objectives and rewards
- **Safe zones** where combat is not allowed
- **Dark areas** requiring light sources

## 🎯 **Commands**

### **Movement**
- `north`, `south`, `east`, `west`, `up`, `down`
- `northeast`, `northwest`, `southeast`, `southwest`

### **Actions**
- `look` - Look around the current room
- `examine <item>` - Examine an item, NPC, or enemy
- `take <item>` - Pick up an item
- `drop <item>` - Drop an item from inventory
- `use <item>` - Use an item

### **Combat** ⚔️
- `attack <enemy>` - Attack an enemy
- `flee` - Attempt to flee from combat
- `combat` - Show combat status

### **Equipment** 🛡️
- `equip <item>` - Equip a weapon or armor
- `unequip <slot>` - Unequip an item from a slot
- `equipment` - Show all equipped items

### **Crafting** 🔨
- `craft <recipe>` - Craft an item using a recipe
- `recipes` - List all known recipes
- `recipe <name>` - Get detailed recipe information
- `learn <recipe>` - Learn a new crafting recipe

### **Quests** 📜
- `quest <name>` - Get quest information
- `quests` - List all quests and their status
- `accept <quest>` - Accept a quest from an NPC
- `progress` - Check progress on active quests

### **Trading** 💰
- `shop` - Show merchant's inventory
- `buy <item>` - Buy an item from a merchant
- `sell <item>` - Sell an item to a merchant

### **Information**
- `inventory` - Show what you're carrying
- `status` - Show health, level, gold, and basic stats
- `stats` - Show detailed character statistics
- `gold` - Show your gold amount
- `level` - Show level and experience information
- `score` - Show your current score
- `help` - Show available commands

### **System**
- `save` - Save the game
- `load` - Load a saved game
- `quit` - Exit the game

## 🛠️ **Installation**

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd new-text-adventure-game
   ```

2. **Install dependencies**:
   ```bash
   pip install -e .
   ```

3. **Run the game**:
   ```bash
   python main.py
   ```

## 🏗️ **Development**

### **Project Structure**

```
new-text-adventure-game/
├── game/
│   ├── __init__.py          # Package initialization
│   ├── models.py            # Data models (Pydantic)
│   ├── engine.py            # Main game engine
│   ├── commands.py          # Command parsing and execution
│   ├── world_builder.py     # World creation and setup
│   ├── combat.py            # Combat system
│   ├── crafting.py          # Crafting system
│   ├── quests.py            # Quest system
│   └── save_system.py       # Save/load system
├── tests/
│   ├── __init__.py          # Test package
│   └── test_models.py       # Model tests
├── saves/                   # Save files directory
├── main.py                  # Entry point
├── pyproject.toml          # Project configuration
└── README.md               # This file
```

### **Code Quality**

The project follows Python best practices:

- **Type Hints**: All functions and variables are properly typed
- **Pydantic Models**: Data validation and serialization
- **Logging**: Comprehensive logging with proper levels
- **Error Handling**: Robust exception handling
- **Documentation**: Google-style docstrings for all public APIs
- **Modularity**: Clean separation of concerns

### **Testing**

Run tests with pytest:
```bash
pytest
```

### **Linting and Formatting**

The project uses Ruff for both linting and formatting:
```bash
ruff check .          # Lint the code
ruff format .         # Format the code
```

## 🎮 **Game Mechanics**

### **Victory Conditions**
- Find the treasure chest in the Treasure Chamber
- Complete all available quests
- Reach maximum level
- The game tracks your score based on items collected and quests completed

### **Combat Mechanics**
- **Turn-based**: Player and enemy take turns attacking
- **Damage Calculation**: Based on weapon damage, strength, and enemy armor
- **Experience Rewards**: Defeating enemies grants XP and gold
- **Level Progression**: Gain levels to increase stats and unlock new content
- **Special Abilities**: Enemies can poison, stun, or heal themselves

### **Crafting Mechanics**
- **Material Requirements**: Each recipe needs specific materials
- **Tool Requirements**: Some recipes require tools like hammers or needles
- **Level Requirements**: Advanced recipes need higher player levels
- **Crafting Time**: More complex items take longer to craft
- **Item Quality**: Crafted items have better stats than basic items

### **Quest Mechanics**
- **Quest Types**: Collection, exploration, crafting, and combat quests
- **Progress Tracking**: Real-time updates on quest objectives
- **Rewards**: Experience points, gold, and unique items
- **Requirements**: Some quests need specific levels or items
- **Repeatable**: Certain quests can be completed multiple times

### **Items**
- **Weapons**: Swords, axes, and magical weapons for combat
- **Armor**: Leather, chain, and plate armor for protection
- **Tools**: Hammers, needles, and other crafting tools
- **Materials**: Herbs, ore, wood, leather, and magical essences
- **Potions**: Health potions and magical elixirs
- **Treasure**: Gold coins, gems, and valuable artifacts

### **NPCs**
- **Guard**: Provides warnings and combat quests
- **Merchant**: Offers trading and crafting quests
- **Wizard**: Gives magical quests and advice

### **Enemies**
- **Goblin**: Weak but aggressive, can poison
- **Skeleton**: Undead warrior with stun abilities
- **Bandit**: Tough opponent with healing abilities

## 🔧 **Extending the Game**

### **Adding New Combat Features**
1. Add new enemy types to `EnemyType` enum
2. Create enemy data in `WorldBuilder._create_enemies()`
3. Add special abilities to `CombatSystem._use_enemy_special_ability()`

### **Adding New Crafting Recipes**
1. Add recipe to `CraftingSystem._setup_default_recipes()`
2. Define materials, tools, and level requirements
3. Add crafting logic if needed

### **Adding New Quests**
1. Create quest in `QuestSystem._setup_default_quests()`
2. Define requirements, rewards, and quest giver
3. Add quest completion logic

### **Adding New Items**
1. Create item in `WorldBuilder._create_items()`
2. Define properties like type, value, and keywords
3. Add to room inventories or NPC inventories

### **Adding New Commands**
1. Add command handler to `CommandParser._setup_commands()`
2. Implement the command method
3. Update help text

## 📈 **Future Enhancements**

### **Planned Features**
- **Weather System**: Dynamic weather affecting gameplay
- **Day/Night Cycles**: Different NPC behaviors and events
- **Multiple Game Worlds**: Different areas to explore
- **Advanced AI**: Smarter enemy behavior and NPC interactions
- **Sound Effects**: Audio feedback for actions
- **Character Classes**: Different starting abilities and progression
- **Multiplayer Support**: Cooperative and competitive play
- **Mod Support**: User-created content and modifications

### **Technical Improvements**
- **Database Integration**: Persistent world state
- **Web Interface**: Browser-based game client
- **Mobile Support**: Touch-friendly interface
- **Cloud Saves**: Cross-device save synchronization
- **Performance Optimization**: Faster loading and processing

## 📄 **License**

This project is open source. Feel free to modify and extend it for your own adventures!

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 🎉 **Version History**

### **v2.0.0** - Enhanced Edition
- Added comprehensive combat system
- Implemented crafting and material collection
- Added quest system with multiple quest types
- Enhanced equipment system with multiple slots
- Added trading system with merchants
- Implemented save/load system with multiple slots
- Added enemies with special abilities
- Enhanced world with more items and interactions

### **v1.0.0** - Basic Edition
- Core text adventure functionality
- Basic movement and interaction
- Simple inventory system
- Basic world with rooms and items
