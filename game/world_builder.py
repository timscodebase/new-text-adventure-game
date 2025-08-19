"""World builder for creating the game world."""

import logging
from typing import Dict, List
from game.models import (
    GameState, Player, Room, Item, NPC, Enemy, Direction, Exit, ItemType, EnemyType
)


logger = logging.getLogger(__name__)


class WorldBuilder:
    """Builds the game world with rooms, items, and NPCs."""
    
    def create_world(self) -> GameState:
        """Create a complete game world."""
        # Create items
        items = self._create_items()
        
        # Create NPCs
        npcs = self._create_npcs()
        
        # Create enemies
        enemies = self._create_enemies()
        
        # Create rooms
        rooms = self._create_rooms()
        
        # Create player
        player = Player(
            name="Adventurer",
            current_room="entrance"
        )
        
        # Create game state
        game_state = GameState(
            player=player,
            rooms=rooms,
            items=items,
            npcs=npcs,
            enemies=enemies,
            victory_conditions=["Find the treasure chest"]
        )
        
        logger.info("Game world created successfully")
        return game_state
    
    def _create_items(self) -> Dict[str, Item]:
        """Create all items in the game world."""
        items = {
            # Original items
            "rusty_key": Item(
                name="rusty key",
                description="An old, rusty key that might unlock something.",
                item_type=ItemType.KEY,
                value=5,
                keywords=["key", "rusty"]
            ),
            "torch": Item(
                name="torch",
                description="A wooden torch that provides light in dark places.",
                item_type=ItemType.TOOL,
                value=10,
                keywords=["light", "fire"]
            ),
            "sword": Item(
                name="sword",
                description="A sharp steel sword with a leather-wrapped hilt.",
                item_type=ItemType.WEAPON,
                damage=12,
                value=50,
                keywords=["weapon", "blade"]
            ),
            "gold_coin": Item(
                name="gold coin",
                description="A shiny gold coin worth 10 points.",
                item_type=ItemType.TREASURE,
                value=10,
                keywords=["coin", "gold", "money"]
            ),
            "treasure_chest": Item(
                name="treasure chest",
                description="A magnificent chest filled with untold riches!",
                item_type=ItemType.TREASURE,
                value=1000,
                keywords=["chest", "treasure", "riches"]
            ),
            "potion": Item(
                name="health potion",
                description="A red potion that restores health when consumed.",
                item_type=ItemType.POTION,
                healing_value=25,
                value=25,
                keywords=["potion", "health", "red"],
                use_description="You drink the potion and feel your strength returning!"
            ),
            "map": Item(
                name="old map",
                description="A weathered map showing the layout of the dungeon.",
                item_type=ItemType.TOOL,
                value=15,
                keywords=["map", "paper"]
            ),
            "gem": Item(
                name="ruby gem",
                description="A beautiful red ruby that sparkles in the light.",
                item_type=ItemType.TREASURE,
                value=100,
                keywords=["gem", "ruby", "red"]
            ),
            
            # New crafting materials
            "herb": Item(
                name="herb",
                description="A common herb used in potion making.",
                item_type=ItemType.MATERIAL,
                value=2,
                keywords=["herb", "plant", "material"]
            ),
            "iron_ore": Item(
                name="iron ore",
                description="Raw iron ore that can be smelted into metal.",
                item_type=ItemType.MATERIAL,
                value=5,
                keywords=["ore", "iron", "metal", "material"]
            ),
            "wood": Item(
                name="wood",
                description="A piece of wood suitable for crafting.",
                item_type=ItemType.MATERIAL,
                value=1,
                keywords=["wood", "material"]
            ),
            "leather": Item(
                name="leather",
                description="Treated animal hide used for armor.",
                item_type=ItemType.MATERIAL,
                value=3,
                keywords=["leather", "hide", "material"]
            ),
            "thread": Item(
                name="thread",
                description="Strong thread for sewing and crafting.",
                item_type=ItemType.MATERIAL,
                value=1,
                keywords=["thread", "string", "material"]
            ),
            "cloth": Item(
                name="cloth",
                description="A piece of fabric for various uses.",
                item_type=ItemType.MATERIAL,
                value=1,
                keywords=["cloth", "fabric", "material"]
            ),
            "parchment": Item(
                name="parchment",
                description="Fine parchment for writing and scrolls.",
                item_type=ItemType.MATERIAL,
                value=2,
                keywords=["parchment", "paper", "material"]
            ),
            "magic_essence": Item(
                name="magic essence",
                description="A glowing essence of pure magic.",
                item_type=ItemType.MATERIAL,
                value=20,
                keywords=["essence", "magic", "material"]
            ),
            "water": Item(
                name="water",
                description="Clear water in a small vial.",
                item_type=ItemType.MATERIAL,
                value=1,
                keywords=["water", "liquid", "material"]
            ),
            
            # New equipment
            "iron_sword": Item(
                name="iron sword",
                description="A sturdy iron sword with excellent balance.",
                item_type=ItemType.WEAPON,
                damage=18,
                value=75,
                keywords=["sword", "iron", "weapon"]
            ),
            "leather_armor": Item(
                name="leather armor",
                description="Light leather armor that provides good protection.",
                item_type=ItemType.ARMOR,
                armor_value=8,
                value=40,
                keywords=["armor", "leather", "protection"]
            ),
            "lockpick": Item(
                name="lockpick",
                description="A delicate tool for picking locks.",
                item_type=ItemType.TOOL,
                value=15,
                keywords=["lockpick", "tool", "lock"]
            ),
            "magic_scroll": Item(
                name="magic scroll",
                description="A scroll inscribed with ancient magical runes.",
                item_type=ItemType.SCROLL,
                value=50,
                keywords=["scroll", "magic", "rune"]
            ),
            
            # Tools
            "hammer": Item(
                name="hammer",
                description="A sturdy hammer for crafting and repairs.",
                item_type=ItemType.TOOL,
                value=8,
                keywords=["hammer", "tool", "craft"]
            ),
            "needle": Item(
                name="needle",
                description="A fine needle for sewing and leatherwork.",
                item_type=ItemType.TOOL,
                value=3,
                keywords=["needle", "tool", "sew"]
            )
        }
        
        return items
    
    def _create_enemies(self) -> Dict[str, Enemy]:
        """Create all enemies in the game world."""
        enemies = {
            "goblin": Enemy(
                id="goblin",
                name="goblin",
                enemy_type=EnemyType.GOBLIN,
                description="A small, green-skinned goblin with sharp teeth and malicious eyes.",
                health=30,
                max_health=30,
                damage=8,
                armor=2,
                experience_reward=25,
                gold_reward=10,
                current_room="corridor",
                aggression_level=7,
                inventory=["herb"],
                special_abilities=["poison"]
            ),
            "skeleton": Enemy(
                id="skeleton",
                name="skeleton",
                enemy_type=EnemyType.SKELETON,
                description="An animated skeleton with glowing red eyes.",
                health=40,
                max_health=40,
                damage=10,
                armor=3,
                experience_reward=35,
                gold_reward=15,
                current_room="secret_passage",
                aggression_level=8,
                inventory=["iron_ore"],
                special_abilities=["stun"]
            ),
            "bandit": Enemy(
                id="bandit",
                name="bandit",
                enemy_type=EnemyType.BANDIT,
                description="A rough-looking bandit with a scarred face and leather armor.",
                health=50,
                max_health=50,
                damage=12,
                armor=5,
                experience_reward=45,
                gold_reward=25,
                current_room="cave",
                aggression_level=6,
                inventory=["gold_coin", "leather"],
                special_abilities=["heal"]
            )
        }
        
        return enemies
    
    def _create_npcs(self) -> Dict[str, NPC]:
        """Create all NPCs in the game world."""
        npcs = {
            "guard": NPC(
                id="guard",
                name="guard",
                description="A stern-looking guard in chainmail armor.",
                current_room="guard_room",
                dialogue={
                    "greeting": "Halt! Who goes there? Oh, just an adventurer. Be careful in the dungeon ahead.",
                    "help": "The dungeon is dangerous. You'll need a torch to see in the dark areas.",
                    "quest": "There's a goblin causing trouble in the corridor. If you can defeat it, I'll reward you.",
                    "crafting": "I've seen some adventurers crafting their own gear. You might want to learn some recipes."
                },
                quests_offered=["defeat_goblin", "explore_caves"]
            ),
            "merchant": NPC(
                id="merchant",
                name="merchant",
                description="A friendly merchant with a backpack full of goods.",
                current_room="market",
                dialogue={
                    "greeting": "Welcome, traveler! I have many fine items for sale... if you have the coin.",
                    "trade": "I'm always looking for rare items. Bring me something valuable and I'll make you a deal.",
                    "quest": "I need herbs for my potion making. If you can collect some for me, I'll pay you well.",
                    "crafting": "Crafting is a valuable skill. I can teach you some basic recipes if you're interested."
                },
                quests_offered=["collect_herbs", "craft_sword"],
                shop_items=["torch", "potion", "map"],
                shop_prices={"torch": 15, "potion": 30, "map": 20}
            ),
            "wizard": NPC(
                id="wizard",
                name="wizard",
                description="An elderly wizard in flowing robes covered in mystical symbols.",
                current_room="library",
                dialogue={
                    "greeting": "Ah, a visitor! I sense great potential in you, young adventurer.",
                    "quest": "I've lost my precious ruby gem somewhere in the dungeon. If you find it, I'll reward you handsomely.",
                    "magic": "Magic is everywhere, young one. You just need to know where to look.",
                    "crafting": "The most powerful items are those crafted with your own hands and magic."
                },
                quests_offered=["find_gem"]
            )
        }
        
        return npcs
    
    def _create_rooms(self) -> Dict[str, Room]:
        """Create all rooms in the game world."""
        rooms = {
            "entrance": Room(
                id="entrance",
                name="Dungeon Entrance",
                description="You stand at the entrance to an ancient dungeon. Stone walls rise around you, and the air is thick with mystery.",
                long_description="You find yourself at the entrance to an ancient dungeon. The stone walls are covered in moss and strange runes. A cool breeze whispers through the corridors, carrying the scent of old stone and adventure. Torches flicker on the walls, casting dancing shadows.",
                exits={
                    Direction.NORTH: Exit(direction=Direction.NORTH, destination="guard_room"),
                    Direction.EAST: Exit(direction=Direction.EAST, destination="market")
                },
                items=["torch", "map", "herb"],
                is_safe_zone=True
            ),
            
            "guard_room": Room(
                id="guard_room",
                name="Guard Room",
                description="A small room with a guard stationed at a wooden table. Weapons and armor line the walls.",
                exits={
                    Direction.SOUTH: Exit(direction=Direction.SOUTH, destination="entrance"),
                    Direction.EAST: Exit(direction=Direction.EAST, destination="corridor")
                },
                npcs=["guard"],
                items=["hammer"],
                is_safe_zone=True
            ),
            
            "market": Room(
                id="market",
                name="Market Square",
                description="A bustling market square with stalls and merchants. The air is filled with the sounds of haggling and the smell of spices.",
                exits={
                    Direction.WEST: Exit(direction=Direction.WEST, destination="entrance"),
                    Direction.NORTH: Exit(direction=Direction.NORTH, destination="library")
                },
                npcs=["merchant"],
                items=["gold_coin", "thread", "cloth"],
                is_safe_zone=True
            ),
            
            "library": Room(
                id="library",
                name="Ancient Library",
                description="Rows of dusty bookshelves line the walls. The air is thick with the smell of old parchment and magic.",
                exits={
                    Direction.SOUTH: Exit(direction=Direction.SOUTH, destination="market"),
                    Direction.WEST: Exit(direction=Direction.WEST, destination="corridor")
                },
                npcs=["wizard"],
                items=["parchment", "magic_essence"],
                is_safe_zone=True
            ),
            
            "corridor": Room(
                id="corridor",
                name="Dark Corridor",
                description="A long, dark corridor with stone walls. The only light comes from occasional torches.",
                exits={
                    Direction.WEST: Exit(direction=Direction.WEST, destination="guard_room"),
                    Direction.EAST: Exit(direction=Direction.EAST, destination="library"),
                    Direction.NORTH: Exit(direction=Direction.NORTH, destination="treasure_room")
                },
                enemies=["goblin"],
                items=["iron_ore"],
                is_dark=True
            ),
            
            "treasure_room": Room(
                id="treasure_room",
                name="Treasure Chamber",
                description="A magnificent chamber filled with gold and jewels. The walls sparkle with embedded gems.",
                exits={
                    Direction.SOUTH: Exit(direction=Direction.SOUTH, destination="corridor"),
                    Direction.EAST: Exit(direction=Direction.EAST, destination="secret_passage")
                },
                items=["treasure_chest", "gem"],
                is_safe_zone=True
            ),
            
            "secret_passage": Room(
                id="secret_passage",
                name="Secret Passage",
                description="A hidden passage behind a loose stone. The air is stale and the walls are rough.",
                exits={
                    Direction.WEST: Exit(direction=Direction.WEST, destination="treasure_room"),
                    Direction.NORTH: Exit(direction=Direction.NORTH, destination="cave")
                },
                enemies=["skeleton"],
                items=["rusty_key", "wood"],
                is_dark=True
            ),
            
            "cave": Room(
                id="cave",
                name="Underground Cave",
                description="A natural cave with stalactites hanging from the ceiling. Water drips somewhere in the darkness.",
                exits={
                    Direction.SOUTH: Exit(direction=Direction.SOUTH, destination="secret_passage"),
                    Direction.DOWN: Exit(direction=Direction.DOWN, destination="deep_cavern")
                },
                enemies=["bandit"],
                items=["leather", "water"],
                is_dark=True,
                ambient_sounds="The sound of dripping water echoes through the cave."
            ),
            
            "deep_cavern": Room(
                id="deep_cavern",
                name="Deep Cavern",
                description="A vast cavern deep underground. Strange crystals glow with an otherworldly light.",
                exits={
                    Direction.UP: Exit(direction=Direction.UP, destination="cave")
                },
                items=["sword", "potion", "needle"],
                ambient_sounds="The crystals hum with a mysterious energy."
            )
        }
        
        return rooms
