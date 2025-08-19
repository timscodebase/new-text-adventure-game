"""Crafting system for the text adventure game."""

import logging
from typing import Dict, List, Optional, Tuple, Any
from game.models import (
    Player, Item, CraftingRecipe, GameState, ItemType
)


logger = logging.getLogger(__name__)


class CraftingSystem:
    """Handles item crafting and recipe management."""
    
    def __init__(self, game_state: GameState) -> None:
        """Initialize the crafting system."""
        self.state = game_state
        self._setup_default_recipes()
    
    def _setup_default_recipes(self) -> None:
        """Setup default crafting recipes."""
        recipes = {
            "health_potion": CraftingRecipe(
                id="health_potion",
                name="Health Potion",
                description="A potion that restores health",
                materials={"herb": 2, "water": 1},
                result_item="health_potion",
                required_level=1,
                crafting_time=2
            ),
            "iron_sword": CraftingRecipe(
                id="iron_sword",
                name="Iron Sword",
                description="A sturdy iron sword",
                materials={"iron_ore": 3, "wood": 1},
                result_item="iron_sword",
                required_level=3,
                required_tools=["hammer"],
                crafting_time=10
            ),
            "leather_armor": CraftingRecipe(
                id="leather_armor",
                name="Leather Armor",
                description="Light leather armor",
                materials={"leather": 4, "thread": 2},
                result_item="leather_armor",
                required_level=2,
                required_tools=["needle"],
                crafting_time=8
            ),
            "torch": CraftingRecipe(
                id="torch",
                name="Torch",
                description="A wooden torch for light",
                materials={"wood": 1, "cloth": 1},
                result_item="torch",
                required_level=1,
                crafting_time=1
            ),
            "lockpick": CraftingRecipe(
                id="lockpick",
                name="Lockpick",
                description="A tool for picking locks",
                materials={"iron_ore": 1},
                result_item="lockpick",
                required_level=2,
                required_tools=["hammer"],
                crafting_time=3
            ),
            "magic_scroll": CraftingRecipe(
                id="magic_scroll",
                name="Magic Scroll",
                description="A scroll with magical properties",
                materials={"parchment": 1, "magic_essence": 1},
                result_item="magic_scroll",
                required_level=5,
                crafting_time=5
            )
        }
        
        self.state.crafting_recipes.update(recipes)
    
    def get_available_recipes(self) -> List[CraftingRecipe]:
        """Get recipes the player can craft."""
        available = []
        
        for recipe in self.state.crafting_recipes.values():
            if self._can_craft_recipe(recipe):
                available.append(recipe)
        
        return available
    
    def _can_craft_recipe(self, recipe: CraftingRecipe) -> bool:
        """Check if player can craft a recipe."""
        # Check level requirement
        if self.state.player.level < recipe.required_level:
            return False
        
        # Check if player knows the recipe
        if recipe.id not in self.state.player.known_recipes:
            return False
        
        # Check if player has required tools
        for tool in recipe.required_tools:
            if not self._player_has_item(tool):
                return False
        
        # Check if player has required materials
        for material, quantity in recipe.materials.items():
            if not self._player_has_material(material, quantity):
                return False
        
        return True
    
    def _player_has_item(self, item_name: str) -> bool:
        """Check if player has an item by name."""
        for item_id in self.state.player.inventory:
            item = self.state.items.get(item_id)
            if item and item_name.lower() in item.name.lower():
                return True
        return False
    
    def _player_has_material(self, material_name: str, quantity: int) -> int:
        """Check how much of a material the player has."""
        count = 0
        for item_id in self.state.player.inventory:
            item = self.state.items.get(item_id)
            if item and material_name.lower() in item.name.lower():
                count += 1
        return count
    
    def craft_item(self, recipe_name: str) -> str:
        """Craft an item using a recipe."""
        # Find the recipe
        recipe = None
        for r in self.state.crafting_recipes.values():
            if recipe_name.lower() in r.name.lower():
                recipe = r
                break
        
        if not recipe:
            return f"Recipe '{recipe_name}' not found."
        
        # Check if player can craft it
        if not self._can_craft_recipe(recipe):
            if recipe.id not in self.state.player.known_recipes:
                return f"You don't know how to craft {recipe.name}."
            elif self.state.player.level < recipe.required_level:
                return f"You need level {recipe.required_level} to craft {recipe.name}."
            else:
                return f"You don't have the required materials to craft {recipe.name}."
        
        # Consume materials
        for material, quantity in recipe.materials.items():
            self._consume_material(material, quantity)
        
        # Create the crafted item
        crafted_item = self._create_crafted_item(recipe)
        if crafted_item:
            self.state.player.inventory.append(crafted_item.id)
            return f"You successfully craft {recipe.name}!"
        else:
            return f"Failed to create {recipe.name}."
    
    def _consume_material(self, material_name: str, quantity: int) -> None:
        """Consume materials from player inventory."""
        consumed = 0
        items_to_remove = []
        
        for item_id in self.state.player.inventory:
            if consumed >= quantity:
                break
            
            item = self.state.items.get(item_id)
            if item and material_name.lower() in item.name.lower():
                items_to_remove.append(item_id)
                consumed += 1
        
        # Remove consumed items
        for item_id in items_to_remove:
            self.state.player.inventory.remove(item_id)
    
    def _create_crafted_item(self, recipe: CraftingRecipe) -> Optional[Item]:
        """Create a crafted item based on the recipe."""
        # Check if the result item already exists in the game
        if recipe.result_item in self.state.items:
            return self.state.items[recipe.result_item]
        
        # Create new item based on recipe
        item_id = recipe.result_item
        item = Item(
            name=recipe.name,
            description=recipe.description,
            item_type=self._get_item_type_from_recipe(recipe),
            value=self._calculate_item_value(recipe),
            keywords=[recipe.name.lower().replace(" ", "_")]
        )
        
        # Add special properties based on recipe
        if "potion" in recipe.name.lower():
            item.item_type = ItemType.POTION
            item.healing_value = 25
        elif "sword" in recipe.name.lower():
            item.item_type = ItemType.WEAPON
            item.damage = 15
        elif "armor" in recipe.name.lower():
            item.item_type = ItemType.ARMOR
            item.armor_value = 10
        elif "torch" in recipe.name.lower():
            item.item_type = ItemType.TOOL
            item.use_description = "The torch provides light in dark areas."
        
        # Add to game state
        self.state.items[item_id] = item
        return item
    
    def _get_item_type_from_recipe(self, recipe: CraftingRecipe) -> ItemType:
        """Determine item type from recipe name."""
        name = recipe.name.lower()
        
        if "potion" in name:
            return ItemType.POTION
        elif "sword" in name or "weapon" in name:
            return ItemType.WEAPON
        elif "armor" in name:
            return ItemType.ARMOR
        elif "scroll" in name:
            return ItemType.SCROLL
        elif "key" in name or "lockpick" in name:
            return ItemType.TOOL
        else:
            return ItemType.MISC
    
    def _calculate_item_value(self, recipe: CraftingRecipe) -> int:
        """Calculate the value of a crafted item."""
        base_value = 10
        
        # Add value based on materials
        for material, quantity in recipe.materials.items():
            base_value += quantity * 5
        
        # Add value based on level requirement
        base_value += recipe.required_level * 10
        
        # Add value based on crafting time
        base_value += recipe.crafting_time * 2
        
        return base_value
    
    def learn_recipe(self, recipe_id: str) -> str:
        """Learn a new crafting recipe."""
        if recipe_id not in self.state.crafting_recipes:
            return f"Recipe '{recipe_id}' not found."
        
        if recipe_id in self.state.player.known_recipes:
            return f"You already know the {self.state.crafting_recipes[recipe_id].name} recipe."
        
        self.state.player.known_recipes.add(recipe_id)
        recipe_name = self.state.crafting_recipes[recipe_id].name
        return f"You learn how to craft {recipe_name}!"
    
    def get_recipe_info(self, recipe_name: str) -> str:
        """Get detailed information about a recipe."""
        recipe = None
        for r in self.state.crafting_recipes.values():
            if recipe_name.lower() in r.name.lower():
                recipe = r
                break
        
        if not recipe:
            return f"Recipe '{recipe_name}' not found."
        
        info = [f"Recipe: {recipe.name}"]
        info.append(f"Description: {recipe.description}")
        info.append(f"Required Level: {recipe.required_level}")
        info.append(f"Crafting Time: {recipe.crafting_time} minutes")
        
        if recipe.required_tools:
            info.append(f"Required Tools: {', '.join(recipe.required_tools)}")
        
        info.append("Materials:")
        for material, quantity in recipe.materials.items():
            player_has = self._player_has_material(material, quantity)
            status = "✓" if player_has >= quantity else "✗"
            info.append(f"  {status} {material}: {player_has}/{quantity}")
        
        # Check if player can craft it
        can_craft = self._can_craft_recipe(recipe)
        info.append(f"\nCan Craft: {'Yes' if can_craft else 'No'}")
        
        if not can_craft:
            if recipe.id not in self.state.player.known_recipes:
                info.append("Reason: You don't know this recipe.")
            elif self.state.player.level < recipe.required_level:
                info.append(f"Reason: You need level {recipe.required_level}.")
            else:
                info.append("Reason: Missing required materials or tools.")
        
        return "\n".join(info)
    
    def list_recipes(self) -> str:
        """List all known recipes."""
        if not self.state.player.known_recipes:
            return "You don't know any crafting recipes."
        
        recipes = []
        for recipe_id in self.state.player.known_recipes:
            if recipe_id in self.state.crafting_recipes:
                recipe = self.state.crafting_recipes[recipe_id]
                can_craft = "✓" if self._can_craft_recipe(recipe) else "✗"
                recipes.append(f"{can_craft} {recipe.name} (Level {recipe.required_level})")
        
        return "Known Recipes:\n" + "\n".join(recipes)
