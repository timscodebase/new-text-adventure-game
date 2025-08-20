"""Command parsing and execution for the text adventure game."""

import logging
import re
from typing import Dict, List, Optional, Tuple, Any, Callable
from game.models import (
    GameState, Player, Room, Item, NPC, Direction, Exit, ItemType
)
from game.combat import CombatSystem
from game.crafting import CraftingSystem
from game.quests import QuestSystem
from game.visuals import Visuals


logger = logging.getLogger(__name__)


class CommandParser:
    """Parses and executes player commands."""
    
    def __init__(self, game_state: GameState, command_history=None, console=None) -> None:
        """Initialize the command parser with the game state."""
        self.state = game_state
        self.combat_system = CombatSystem(game_state)
        self.crafting_system = CraftingSystem(game_state)
        self.quest_system = QuestSystem(game_state)
        self.command_history = command_history
        self.console = console
        self._setup_commands()
    
    def _setup_commands(self) -> None:
        """Setup the command handlers."""
        self.commands: Dict[str, Callable[[List[str]], str]] = {
            'help': self._cmd_help,
            'look': self._cmd_look,
            'l': self._cmd_look, # Add a shortcut for look
            'examine': self._cmd_examine,
            'take': self._cmd_take,
            'drop': self._cmd_drop,
            'inventory': self._cmd_inventory,
            'use': self._cmd_use,
            'talk': self._cmd_talk,
            'status': self._cmd_status,
            'score': self._cmd_score,
            'save': self._cmd_save,
            'load': self._cmd_load,
            # New combat commands
            'attack': self._cmd_attack,
            'flee': self._cmd_flee,
            'combat': self._cmd_combat_status,
            # New equipment commands
            'equip': self._cmd_equip,
            'unequip': self._cmd_unequip,
            'equipment': self._cmd_equipment,
            # New crafting commands
            'craft': self._cmd_craft,
            'recipes': self._cmd_recipes,
            'recipe': self._cmd_recipe_info,
            'learn': self._cmd_learn_recipe,
            # New quest commands
            'quest': self._cmd_quest,
            'quests': self._cmd_quests,
            'accept': self._cmd_accept_quest,
            'progress': self._cmd_quest_progress,
            # New system commands
            'stats': self._cmd_stats,
            'gold': self._cmd_gold,
            'level': self._cmd_level,
            'shop': self._cmd_shop,
            'buy': self._cmd_buy,
            'sell': self._cmd_sell,
            # Command history
            'history': self._cmd_history,
        }
        
        # Movement commands
        for direction in Direction:
            self.commands[direction.value] = self._cmd_move
    
    def parse_and_execute(self, command: str) -> Optional[str]:
        """Parse a command string and execute the appropriate action."""
        parts = command.split()
        if not parts:
            return None
        
        verb = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        # Handle movement commands
        if verb in [d.value for d in Direction]:
            return self._cmd_move(verb, args)
        
        # Handle other commands
        if verb in self.commands:
            return self.commands[verb](args)
        
        # Try to handle unknown commands
        return self._handle_unknown_command(verb, args)
    
    def _cmd_help(self, args: List[str]) -> str:
        """Display help information."""
        help_text = """
╔══════════════════════════════════════════════════════════════╗
║                    🎮 GAME COMMANDS 🎮                      ║
╚══════════════════════════════════════════════════════════════╝

🚶 Movement: north, south, east, west, up, down, northeast, northwest, southeast, southwest
🎯 Actions: look, examine <item>, take <item>, drop <item>, use <item>
📊 Information: inventory, status, score, help, stats, gold, level

⚔️ Combat: attack <enemy>, flee, combat
🛡️ Equipment: equip <item>, unequip <slot>, equipment
🔨 Crafting: craft <recipe>, recipes, recipe <name>, learn <recipe>
📜 Quests: quest <name>, quests, accept <quest>, progress
💰 Trading: shop, buy <item>, sell <item>

💾 System: save, load, history, quit
        """
        return help_text.strip()
    
    def _cmd_look(self, args: List[str]) -> str:
        """Look around the current room."""
        current_room = self.state.rooms[self.state.player.current_room]
        room_npcs = [self.state.npcs[npc_id] for npc_id in current_room.npcs
                     if npc_id in self.state.npcs and self.state.npcs[npc_id].is_alive]
        room_enemies = [self.state.enemies[enemy_id] for enemy_id in current_room.enemies
                        if enemy_id in self.state.enemies and self.state.enemies[enemy_id].is_alive]

        output = [f"{current_room.name.upper()}"]
        output.append(Visuals.create_separator("─", len(current_room.name) + 4))
        output.append(current_room.description)

        # Add room visual
        output.append(Visuals.get_room_visual(current_room, room_npcs, room_enemies))

        # Show exits
        if current_room.exits:
            exit_dirs = [exit_obj.direction.value for exit_obj in current_room.exits.values() if exit_obj.is_open]
            if exit_dirs:
                output.append(f"\nExits: {', '.join(exit_dirs)}")

        # Show items
        room_items = [self.state.items[item_id] for item_id in current_room.items
                     if item_id in self.state.items and self.state.items[item_id].is_visible]
        if room_items:
            output.append(f"\nYou see: {', '.join(item.name for item in room_items)}")

        # Show NPCs
        if room_npcs:
            output.append(f"\nPresent: {', '.join(npc.name for npc in room_npcs)}")

        # Show enemies
        if room_enemies:
            output.append(f"\nEnemies: {', '.join(enemy.name for enemy in room_enemies)}")

        return "\n".join(output)
    
    def _cmd_examine(self, args: List[str]) -> str:
        """Examine an item or NPC."""
        if not args:
            return "Examine what?"
        
        target_name = " ".join(args).lower()
        
        # Check inventory
        for item_id in self.state.player.inventory:
            item = self.state.items[item_id]
            if target_name in [item.name.lower()] + item.keywords:
                item_art = Visuals.get_item_art(item.name)
                if item_art:
                    return f"{item_art}\n{item.name}: {item.description}"
                return f"{item.name}: {item.description}"
        
        # Check room items
        current_room = self.state.rooms[self.state.player.current_room]
        for item_id in current_room.items:
            if item_id in self.state.items:
                item = self.state.items[item_id]
                if target_name in [item.name.lower()] + item.keywords:
                    item_art = Visuals.get_item_art(item.name)
                    if item_art:
                        return f"{item_art}\n{item.name}: {item.description}"
                    return f"{item.name}: {item.description}"
        
        # Check NPCs
        for npc_id in current_room.npcs:
            if npc_id in self.state.npcs:
                npc = self.state.npcs[npc_id]
                if target_name in npc.name.lower():
                    npc_art = Visuals.get_npc_art(npc.name)
                    if npc_art:
                        return f"{npc_art}\n{npc.name}: {npc.description}"
                    return f"{npc.name}: {npc.description}"
        
        # Check enemies
        for enemy_id in current_room.enemies:
            if enemy_id in self.state.enemies:
                enemy = self.state.enemies[enemy_id]
                if target_name in enemy.name.lower():
                    enemy_art = Visuals.get_enemy_art(enemy.enemy_type.value)
                    if enemy_art:
                        return f"{enemy_art}\n{enemy.name}: {enemy.description}"
                    return f"{enemy.name}: {enemy.description}"
        
        return f"You don't see a '{target_name}' here."
    
    def _cmd_take(self, args: List[str]) -> str:
        """Take an item from the room."""
        if not args:
            return "Take what?"
        
        target_name = " ".join(args).lower()
        current_room = self.state.rooms[self.state.player.current_room]
        
        for item_id in current_room.items[:]:  # Copy list to avoid modification during iteration
            if item_id in self.state.items:
                item = self.state.items[item_id]
                if target_name in [item.name.lower()] + item.keywords:
                    if not item.is_takeable:
                        return f"You can't take the {item.name}."
                    
                    if not item.is_visible:
                        return f"You don't see a {item.name} here."
                    
                    # Move item from room to inventory
                    current_room.items.remove(item_id)
                    self.state.player.inventory.append(item_id)
                    self.state.player.score += item.value
                    
                    return f"You take the {item.name}."
        
        return f"You don't see a '{target_name}' here."
    
    def _cmd_drop(self, args: List[str]) -> str:
        """Drop an item from inventory."""
        if not args:
            return "Drop what?"
        
        target_name = " ".join(args).lower()
        current_room = self.state.rooms[self.state.player.current_room]
        
        for item_id in self.state.player.inventory[:]:
            item = self.state.items[item_id]
            if target_name in [item.name.lower()] + item.keywords:
                # Move item from inventory to room
                self.state.player.inventory.remove(item_id)
                current_room.items.append(item_id)
                return f"You drop the {item.name}."
        
        return f"You don't have a '{target_name}'."
    
    def _cmd_inventory(self, args: List[str]) -> str:
        """Show player inventory."""
        if not self.state.player.inventory:
            if self.console:
                self.console.print("You are carrying nothing.", style="info")
                return ""
            return "You are carrying nothing."
        items = []
        equipped_ids = set()
        for slot, item_id in self.state.player.equipment.model_dump().items():
            if item_id:
                equipped_ids.add(item_id)
        for item_id in self.state.player.inventory:
            item = self.state.items[item_id]
            if item_id in equipped_ids:
                items.append(f"[info]{item.name}[/info] (equipped)")
            else:
                items.append(f"[item]{item.name}[/item]")
        if self.console:
            self.console.print(f"You are carrying: {', '.join(items)}")
            return ""
        return f"You are carrying: {', '.join(items)}"
    
    def _cmd_use(self, args: List[str]) -> str:
        """Use an item."""
        if not args:
            return "Use what?"
        
        target_name = " ".join(args).lower()
        
        # Check inventory first
        for item_id in self.state.player.inventory:
            item = self.state.items[item_id]
            if target_name in [item.name.lower()] + item.keywords:
                if item.use_description:
                    return f"{item.use_description}"
                else:
                    return f"You use the {item.name}, but nothing happens."
        
        return f"You don't have a '{target_name}'."
    
    def _cmd_talk(self, args: List[str]) -> str:
        """Talk to an NPC."""
        if not args:
            return "Talk to whom?"
        
        target_name = " ".join(args).lower()
        current_room = self.state.rooms[self.state.player.current_room]
        
        for npc_id in current_room.npcs:
            if npc_id in self.state.npcs:
                npc = self.state.npcs[npc_id]
                if target_name in npc.name.lower():
                    if npc.dialogue:
                        npc_art = Visuals.get_npc_art(npc.name)
                        default_message = f"{npc.name} doesn't seem interested in talking."
                        dialogue = npc.dialogue.get('greeting', default_message)
                        if npc_art:
                            return f"{npc_art}\n{npc.name}: {dialogue}"
                        return f"{npc.name}: {dialogue}"
                    else:
                        return f"{npc.name} doesn't respond."
        
        return f"You don't see '{target_name}' here."
    
    def _cmd_status(self, args: List[str]) -> str:
        """Show player status."""
        player = self.state.player
        health_str = f"[error]{player.health}[/error]" if player.health < player.max_health * 0.3 else f"[info]{player.health}[/info]"
        gold_str = f"[info]{player.gold}[/info]" if player.gold > 0 else f"[error]{player.gold}[/error]"
        exp_str = f"[info]{player.experience}[/info]"
        status = (
            f"Health: {health_str}/{player.max_health} | "
            f"Level: [info]{player.level}[/info] | "
            f"Experience: {exp_str}/[info]{player.experience_to_next}[/info] | "
            f"Gold: {gold_str} | "
            f"Score: [info]{player.score}[/info] | Moves: [info]{player.moves}[/info]"
        )
        if self.console:
            self.console.print(status)
            if player.status_effects:
                self.console.print("Status Effects:", style="error")
                for effect, duration in player.status_effects.items():
                    self.console.print(f"  [error]{effect}[/error]: {duration} turns")
            return ""
        return status
    
    def _cmd_score(self, args: List[str]) -> str:
        """Show player score."""
        return f"Your score is {self.state.player.score} points."
    
    def _cmd_save(self, args: List[str]) -> str:
        """Save the game."""
        filename = args[0] if args else "savegame.dat"
        # In a real implementation, you'd actually save the game state
        return f"Game saved to {filename}"
    
    def _cmd_load(self, args: List[str]) -> str:
        """Load a game."""
        filename = args[0] if args else "savegame.dat"
        # In a real implementation, you'd actually load the game state
        return f"Game loaded from {filename}"
    
    # Combat commands
    def _cmd_attack(self, args: List[str]) -> str:
        """Attack an enemy."""
        target_name = " ".join(args) if args else ""
        result = self.combat_system.attack(target_name)
        
        # Add combat art if it's an attack
        if self.console:
            if "miss" in result.lower() or "fail" in result.lower():
                self.console.print(result, style="error")
            elif "critical" in result.lower() or "level up" in result.lower():
                self.console.print(result, style="info")
            elif "heal" in result.lower():
                self.console.print(result, style="info")
            elif "defeat" in result.lower() or "killed" in result.lower():
                self.console.print(result, style="enemy")
            else:
                self.console.print(result, style="enemy")
            combat_art = Visuals.get_combat_art("attack")
            if combat_art:
                self.console.print(combat_art, style="enemy")
            return ""
        else:
            combat_art = Visuals.get_combat_art("attack")
            if combat_art:
                return f"{combat_art}\n{result}"
            return result
    
    def _cmd_flee(self, args: List[str]) -> str:
        """Flee from combat."""
        result = self.combat_system.flee()
        if self.console:
            if "success" in result.lower():
                self.console.print(result, style="info")
            else:
                self.console.print(result, style="error")
            return ""
        return result
    
    def _cmd_combat_status(self, args: List[str]) -> str:
        """Show combat status."""
        return self.combat_system.get_combat_status()
    
    # Equipment commands
    def _cmd_equip(self, args: List[str]) -> str:
        """Equip an item."""
        if not args:
            return "Equip what?"
        
        target_name = " ".join(args).lower()
        
        # Find item in inventory
        item_id = None
        for inv_item_id in self.state.player.inventory:
            item = self.state.items[inv_item_id]
            if target_name in [item.name.lower()] + item.keywords:
                item_id = inv_item_id
                break
        
        if not item_id:
            return f"You don't have a {target_name}."
        
        item = self.state.items[item_id]
        
        # Determine equipment slot
        if item.item_type == ItemType.WEAPON:
            slot = "weapon"
        elif item.item_type == ItemType.ARMOR:
            slot = "armor"
        else:
            return f"You can't equip {item.name}."
        
        # Unequip current item if any
        current_item_id = getattr(self.state.player.equipment, slot)
        if current_item_id:
            self.state.player.inventory.append(current_item_id)
        
        # Equip new item
        setattr(self.state.player.equipment, slot, item_id)
        self.state.player.inventory.remove(item_id)
        
        return f"You equip {item.name}."
    
    def _cmd_unequip(self, args: List[str]) -> str:
        """Unequip an item."""
        if not args:
            return "Unequip what?"
        
        slot_name = args[0].lower()
        valid_slots = ["weapon", "armor", "helmet", "boots", "gloves", "ring", "amulet"]
        
        if slot_name not in valid_slots:
            return f"Invalid slot. Valid slots: {', '.join(valid_slots)}"
        
        current_item_id = getattr(self.state.player.equipment, slot_name)
        if not current_item_id:
            return f"You don't have anything equipped in {slot_name}."
        
        # Unequip item
        item = self.state.items[current_item_id]
        self.state.player.inventory.append(current_item_id)
        setattr(self.state.player.equipment, slot_name, None)
        
        return f"You unequip {item.name}."
    
    def _cmd_equipment(self, args: List[str]) -> str:
        """Show equipped items."""
        equipment = self.state.player.equipment
        equipped_items = []
        for slot, item_id in equipment.model_dump().items():
            if item_id:
                item = self.state.items[item_id]
                style = "info" if slot in ("weapon", "armor") else "item"
                equipped_items.append(f"[bold]{slot.title()}[/bold]: [{style}]{item.name}[/{style}]")
            else:
                equipped_items.append(f"[bold]{slot.title()}[/bold]: [error]Nothing[/error]")
        if self.console:
            self.console.print("Equipped Items:")
            for line in equipped_items:
                self.console.print(line)
            return ""
        return "Equipped Items:\n" + "\n".join(equipped_items)
    
    # Crafting commands
    def _cmd_craft(self, args: List[str]) -> str:
        """Craft an item."""
        if not args:
            return "Craft what?"
        
        recipe_name = " ".join(args)
        result = self.crafting_system.craft_item(recipe_name)
        
        if "successfully" in result.lower():
            return f"{result}"
        else:
            return f"{result}"
    
    def _cmd_recipes(self, args: List[str]) -> str:
        """List known recipes."""
        return self.crafting_system.list_recipes()
    
    def _cmd_recipe_info(self, args: List[str]) -> str:
        """Get recipe information."""
        if not args:
            return "Recipe info for what?"
        
        recipe_name = " ".join(args)
        return self.crafting_system.get_recipe_info(recipe_name)
    
    def _cmd_learn_recipe(self, args: List[str]) -> str:
        """Learn a recipe."""
        if not args:
            return "Learn what recipe?"
        
        recipe_id = args[0]
        result = self.crafting_system.learn_recipe(recipe_id)
        
        if "learn" in result.lower():
            return f"{result}"
        else:
            return f"{result}"
    
    # Quest commands
    def _cmd_quest(self, args: List[str]) -> str:
        """Get quest information."""
        if not args:
            return "Quest info for what?"
        
        quest_name = " ".join(args)
        return self.quest_system.get_quest_details(quest_name)
    
    def _cmd_quests(self, args: List[str]) -> str:
        """List all quests."""
        return self.quest_system.list_quests()
    
    def _cmd_accept_quest(self, args: List[str]) -> str:
        """Accept a quest."""
        if not args:
            return "Accept what quest?"
        
        quest_name = " ".join(args)
        result = self.quest_system.accept_quest(quest_name)
        
        if self.console:
            if "accept" in result.lower():
                self.console.print(f"{result}", style="info")
            else:
                self.console.print(f"{result}", style="error")
            return ""
        if "accept" in result.lower():
            return f"{result}"
        else:
            return f"{result}"
    
    def _cmd_quest_progress(self, args: List[str]) -> str:
        """Check quest progress."""
        result = self.quest_system.check_quest_progress()
        if self.console:
            if "complete" in result.lower():
                self.console.print(result, style="info")
            else:
                self.console.print(result)
            return ""
        return result
    
    # System commands
    def _cmd_stats(self, args: List[str]) -> str:
        """Show detailed player stats."""
        player = self.state.player
        stats = [
            f"👤 Name: {player.name}",
            f"⭐ Level: {player.level}",
            f"📊 Experience: {player.experience}/{player.experience_to_next}",
            f"❤️  Health: {player.health}/{player.max_health}",
            f"💰 Gold: {player.gold}",
            f"🏆 Score: {player.score}",
            f"👣 Moves: {player.moves}",
            "",
            "📈 Attributes:",
            f"  💪 Strength: {player.strength}",
            f"  🏃 Dexterity: {player.dexterity}",
            f"  🧠 Intelligence: {player.intelligence}",
            f"  ❤️  Constitution: {player.constitution}"
        ]
        
        if player.status_effects:
            stats.append("")
            stats.append("⚠️  Status Effects:")
            for effect, duration in player.status_effects.items():
                stats.append(f"  {effect}: {duration} turns")
        
        return "\n".join(stats)
    
    def _cmd_gold(self, args: List[str]) -> str:
        """Show player gold."""
        return f"💰 You have {self.state.player.gold} gold pieces."
    
    def _cmd_level(self, args: List[str]) -> str:
        """Show player level information."""
        player = self.state.player
        return (f"⭐ Level: {player.level} | "
                f"📊 Experience: {player.experience}/{player.experience_to_next} | "
                f"📈 Next level in: {player.experience_to_next - player.experience} XP")
    
    # Trading commands
    def _cmd_shop(self, args: List[str]) -> str:
        """Show shop inventory."""
        current_room = self.state.rooms[self.state.player.current_room]
        
        # Find merchant in room
        merchant = None
        for npc_id in current_room.npcs:
            if npc_id in self.state.npcs:
                npc = self.state.npcs[npc_id]
                if "merchant" in npc.name.lower():
                    merchant = npc
                    break
        
        if not merchant:
            return "There's no merchant here."
        
        if not merchant.shop_items:
            return f"{merchant.name} has nothing for sale."
        
        shop_list = [f"{merchant.name}'s Shop:"]
        for item_id in merchant.shop_items:
            if item_id in self.state.items:
                item = self.state.items[item_id]
                price = merchant.shop_prices.get(item_id, item.value)
                shop_list.append(f"  {item.name}: {price} gold")
        
        return "\n".join(shop_list)
    
    def _cmd_buy(self, args: List[str]) -> str:
        """Buy an item from a merchant."""
        if not args:
            return "Buy what?"
        
        target_name = " ".join(args).lower()
        current_room = self.state.rooms[self.state.player.current_room]
        
        # Find merchant in room
        merchant = None
        for npc_id in current_room.npcs:
            if npc_id in self.state.npcs:
                npc = self.state.npcs[npc_id]
                if "merchant" in npc.name.lower():
                    merchant = npc
                    break
        
        if not merchant:
            return "There's no merchant here."
        
        # Find item in shop
        item_id = None
        for shop_item_id in merchant.shop_items:
            item = self.state.items[shop_item_id]
            if target_name in [item.name.lower()] + item.keywords:
                item_id = shop_item_id
                break
        
        if not item_id:
            return f"{merchant.name} doesn't sell {target_name}."
        
        item = self.state.items[item_id]
        price = merchant.shop_prices.get(item_id, item.value)
        
        if self.state.player.gold < price:
            return f"You don't have enough gold. {item.name} costs {price} gold."
        
        # Complete transaction
        self.state.player.gold -= price
        self.state.player.inventory.append(item_id)
        
        return f"You buy {item.name} for {price} gold."
    
    def _cmd_sell(self, args: List[str]) -> str:
        """Sell an item to a merchant."""
        if not args:
            return "Sell what?"
        
        target_name = " ".join(args).lower()
        current_room = self.state.rooms[self.state.player.current_room]
        
        # Find merchant in room
        merchant = None
        for npc_id in current_room.npcs:
            if npc_id in self.state.npcs:
                npc = self.state.npcs[npc_id]
                if "merchant" in npc.name.lower():
                    merchant = npc
                    break
        
        if not merchant:
            return "There's no merchant here."
        
        # Find item in inventory
        item_id = None
        for inv_item_id in self.state.player.inventory:
            item = self.state.items[inv_item_id]
            if target_name in [item.name.lower()] + item.keywords:
                item_id = inv_item_id
                break
        
        if not item_id:
            return f"You don't have {target_name}."
        
        item = self.state.items[item_id]
        sell_price = item.value // 2  # Sell for half value
        
        # Complete transaction
        self.state.player.gold += sell_price
        self.state.player.inventory.remove(item_id)
        
        return f"You sell {item.name} for {sell_price} gold."
    
    def _cmd_move(self, direction: str, args: List[str]) -> str:
        """Move in a specified direction."""
        try:
            direction_enum = Direction(direction)
        except ValueError:
            return f"'{direction}' is not a valid direction."
        
        current_room = self.state.rooms[self.state.player.current_room]
        
        if direction_enum not in current_room.exits:
            return f"You can't go {direction} from here."
        
        exit_obj = current_room.exits[direction_enum]
        
        if not exit_obj.is_open:
            return f"The exit to the {direction} is closed."
        
        if exit_obj.is_locked:
            if exit_obj.required_key:
                if exit_obj.required_key not in self.state.player.inventory:
                    return f"The exit to the {direction} is locked. You need a key."
            else:
                return f"The exit to the {direction} is locked."
        
        # Check level requirement
        if self.state.player.level < exit_obj.required_level:
            return f"You need to be level {exit_obj.required_level} to go {direction}."
        
        # Check required items
        for required_item in exit_obj.required_items:
            if not any(required_item in self.state.items[item_id].name.lower() 
                      for item_id in self.state.player.inventory):
                return f"You need {required_item} to go {direction}."
        
        # Move to the new room
        self.state.player.current_room = exit_obj.destination
        self.state.player.moves += 1
        
        # Display the new room
        new_room = self.state.rooms[self.state.player.current_room]
        
        output = [f"\nMoving {direction}..."]
        
        # Get room decoration art
        room_art = Visuals.get_room_decoration(new_room.id)
        if room_art:
            output.append(room_art)
        else:
            # Default room header
            output.append(Visuals.create_box("", new_room.name.upper(), 60))
        
        output.append("")
        
        if new_room.is_visited:
            output.append(new_room.description)
        else:
            output.append(new_room.long_description or new_room.description)
            new_room.is_visited = True
        
        output.append("")
        
        # Show exits
        if new_room.exits:
            exit_dirs = [exit_obj.direction.value for exit_obj in new_room.exits.values() if exit_obj.is_open]
            if exit_dirs:
                output.append(f"Exits: {', '.join(exit_dirs)}")
        
        # Show items
        room_items = [self.state.items[item_id] for item_id in new_room.items 
                     if item_id in self.state.items and self.state.items[item_id].is_visible]
        if room_items:
            output.append(f"You see: {', '.join(item.name for item in room_items)}")
        
        # Show NPCs
        room_npcs = [self.state.npcs[npc_id] for npc_id in new_room.npcs 
                    if npc_id in self.state.npcs and self.state.npcs[npc_id].is_alive]
        if room_npcs:
            output.append(f"Present: {', '.join(npc.name for npc in room_npcs)}")
        
        # Show enemies
        room_enemies = [self.state.enemies[enemy_id] for enemy_id in new_room.enemies 
                       if enemy_id in self.state.enemies and self.state.enemies[enemy_id].is_alive]
        if room_enemies:
            output.append(f"Enemies: {', '.join(enemy.name for enemy in room_enemies)}")
        
        output.append("")
        output.append(Visuals.create_separator("─", 60))
        
        return "\n".join(output)
    
    def _cmd_history(self, args: List[str]) -> str:
        """Display command history."""
        if not self.command_history:
            return "Command history is not available."
        
        history = self.command_history.get_history()
        if not history:
            return "No command history yet."
        
        # Show last 10 commands by default, or specified number
        try:
            count = int(args[0]) if args else 10
            count = min(count, len(history))  # Don't exceed available history
        except (ValueError, IndexError):
            count = 10
        
        output = [f"Last {count} commands:"]
        output.append(Visuals.create_separator("─", 30))
        
        # Show most recent commands first
        recent_commands = history[-count:]
        for i, cmd in enumerate(recent_commands, 1):
            output.append(f"{i:2d}. {cmd}")
        
        return "\n".join(output)
    
    def _handle_unknown_command(self, verb: str, args: List[str]) -> str:
        """Handle unknown commands."""
        return f"I don't understand '{verb}'. Type 'help' for available commands."
