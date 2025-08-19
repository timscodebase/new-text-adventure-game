"""AI player for automated game testing."""

import logging
import random
import time
from typing import List, Dict, Optional, Set, Tuple
from enum import Enum

from game.models import GameState, Direction
from game.engine import GameEngine


logger = logging.getLogger(__name__)


class AIStrategy(Enum):
    """Different AI playing strategies."""
    EXPLORER = "explorer"  # Focus on exploring all areas
    COMBATANT = "combatant"  # Focus on combat and leveling
    COLLECTOR = "collector"  # Focus on collecting items and crafting
    QUESTER = "quester"  # Focus on completing quests
    RANDOM = "random"  # Random actions for chaos testing


class AIPlayer:
    """An AI player that can automatically play the game for testing."""
    
    def __init__(self, strategy: AIStrategy = AIStrategy.EXPLORER, max_actions: int = 100):
        """Initialize the AI player."""
        self.strategy = strategy
        self.max_actions = max_actions
        self.actions_taken = 0
        self.visited_rooms: Set[str] = set()
        self.known_items: Set[str] = set()
        self.known_npcs: Set[str] = set()
        self.known_enemies: Set[str] = set()
        self.failed_commands: List[str] = []
        self.successful_commands: List[str] = []
        self.game_log: List[str] = []
        
        # Strategy-specific state
        self.exploration_targets: List[Direction] = []
        self.combat_preference = 0.3  # 30% chance to engage in combat
        self.crafting_materials: Dict[str, int] = {}
        self.active_quests: List[str] = []
        
        logger.info(f"AI Player initialized with strategy: {strategy.value}")
    
    def play_game(self, engine: GameEngine, delay: float = 1.0, verbose: bool = True) -> Dict[str, any]:
        """Play the game automatically and return statistics."""
        logger.info("AI Player starting game session")
        self.game_log.append(f"=== AI Player Session Started (Strategy: {self.strategy.value}) ===")
        
        start_time = time.time()
        
        while (self.actions_taken < self.max_actions and 
               not engine.state.is_game_over and 
               engine.state.player.is_alive):
            
            # Get current game state info
            self._analyze_current_state(engine.state)
            
            # Choose next action based on strategy
            command = self._choose_action(engine.state)
            
            if not command:
                logger.warning("AI Player couldn't choose an action, ending session")
                break
            
            # Execute the command
            self._execute_command(engine, command, verbose)
            
            # Add delay for readability
            if delay > 0:
                time.sleep(delay)
            
            self.actions_taken += 1
        
        end_time = time.time()
        session_duration = end_time - start_time
        
        # Generate session statistics
        stats = self._generate_statistics(engine.state, session_duration)
        
        if verbose:
            self._print_session_summary(stats)
        
        return stats
    
    def _analyze_current_state(self, state: GameState) -> None:
        """Analyze the current game state and update AI knowledge."""
        current_room = state.rooms[state.player.current_room]
        
        # Track visited rooms
        self.visited_rooms.add(current_room.id)
        
        # Track known items in current room
        for item_id in current_room.items:
            if item_id in state.items:
                self.known_items.add(state.items[item_id].name)
        
        # Track known NPCs
        for npc_id in current_room.npcs:
            if npc_id in state.npcs:
                self.known_npcs.add(state.npcs[npc_id].name)
        
        # Track known enemies
        for enemy_id in current_room.enemies:
            if enemy_id in state.enemies and state.enemies[enemy_id].is_alive:
                self.known_enemies.add(state.enemies[enemy_id].name)
    
    def _choose_action(self, state: GameState) -> Optional[str]:
        """Choose the next action based on the AI strategy."""
        current_room = state.rooms[state.player.current_room]
        
        if self.strategy == AIStrategy.EXPLORER:
            return self._choose_explorer_action(state, current_room)
        elif self.strategy == AIStrategy.COMBATANT:
            return self._choose_combatant_action(state, current_room)
        elif self.strategy == AIStrategy.COLLECTOR:
            return self._choose_collector_action(state, current_room)
        elif self.strategy == AIStrategy.QUESTER:
            return self._choose_quester_action(state, current_room)
        elif self.strategy == AIStrategy.RANDOM:
            return self._choose_random_action(state, current_room)
        
        return None
    
    def _choose_explorer_action(self, state: GameState, current_room) -> Optional[str]:
        """Choose actions focused on exploration."""
        # Priority 1: Move to unexplored areas
        unvisited_exits = []
        for direction, exit_obj in current_room.exits.items():
            if exit_obj.is_open and exit_obj.destination not in self.visited_rooms:
                unvisited_exits.append(direction.value)
        
        if unvisited_exits:
            return random.choice(unvisited_exits)
        
        # Priority 2: Take items for potential use
        room_items = [state.items[item_id].name for item_id in current_room.items 
                     if item_id in state.items and state.items[item_id].is_visible]
        if room_items and len(state.player.inventory) < 20:  # Reasonable inventory limit
            return f"take {random.choice(room_items)}"
        
        # Priority 3: Talk to NPCs for information
        room_npcs = [state.npcs[npc_id].name for npc_id in current_room.npcs 
                    if npc_id in state.npcs and state.npcs[npc_id].is_alive]
        if room_npcs:
            return f"talk {random.choice(room_npcs)}"
        
        # Priority 4: Move to any available exit
        available_exits = [exit_obj.direction.value for exit_obj in current_room.exits.values() 
                          if exit_obj.is_open]
        if available_exits:
            return random.choice(available_exits)
        
        # Priority 5: Look around or check status
        return random.choice(["look", "inventory", "status"])
    
    def _choose_combatant_action(self, state: GameState, current_room) -> Optional[str]:
        """Choose actions focused on combat and leveling."""
        # Priority 1: Engage in combat if enemies present
        room_enemies = [state.enemies[enemy_id].name for enemy_id in current_room.enemies 
                       if enemy_id in state.enemies and state.enemies[enemy_id].is_alive]
        if room_enemies and random.random() < self.combat_preference:
            return f"attack {random.choice(room_enemies)}"
        
        # Priority 2: Equip better weapons/armor
        for item_id in state.player.inventory:
            item = state.items[item_id]
            if item.item_type.value in ["weapon", "armor"] and not item.is_equipped:
                return f"equip {item.name}"
        
        # Priority 3: Use healing items if health is low
        if state.player.health < state.player.max_health * 0.5:
            healing_items = [state.items[item_id].name for item_id in state.player.inventory
                           if state.items[item_id].healing_value > 0]
            if healing_items:
                return f"use {random.choice(healing_items)}"
        
        # Priority 4: Explore for more combat opportunities
        return self._choose_explorer_action(state, current_room)
    
    def _choose_collector_action(self, state: GameState, current_room) -> Optional[str]:
        """Choose actions focused on collecting and crafting."""
        # Priority 1: Take all available items
        room_items = [state.items[item_id].name for item_id in current_room.items 
                     if item_id in state.items and state.items[item_id].is_visible]
        if room_items and len(state.player.inventory) < 20:  # Reasonable inventory limit
            return f"take {random.choice(room_items)}"
        
        # Priority 2: Try crafting if we have recipes
        if state.player.known_recipes and random.random() < 0.4:
            recipe = random.choice(list(state.player.known_recipes))
            return f"craft {recipe}"
        
        # Priority 3: Talk to merchants for trading
        room_npcs = [state.npcs[npc_id].name for npc_id in current_room.npcs 
                    if npc_id in state.npcs and state.npcs[npc_id].is_alive]
        if room_npcs and "merchant" in str(room_npcs).lower():
            return "shop"
        
        # Priority 4: Explore for more items
        return self._choose_explorer_action(state, current_room)
    
    def _choose_quester_action(self, state: GameState, current_room) -> Optional[str]:
        """Choose actions focused on completing quests."""
        # Priority 1: Accept available quests
        room_npcs = [npc_id for npc_id in current_room.npcs 
                    if npc_id in state.npcs and state.npcs[npc_id].is_alive]
        if room_npcs and random.random() < 0.6:
            return "quests"
        
        # Priority 2: Check quest progress
        if state.player.active_quests and random.random() < 0.3:
            return "progress"
        
        # Priority 3: Collect quest items
        room_items = [state.items[item_id].name for item_id in current_room.items 
                     if item_id in state.items and state.items[item_id].is_visible]
        if room_items and len(state.player.inventory) < 20:  # Reasonable inventory limit
            return f"take {random.choice(room_items)}"
        
        # Priority 4: Explore for quest objectives
        return self._choose_explorer_action(state, current_room)
    
    def _choose_random_action(self, state: GameState, current_room) -> Optional[str]:
        """Choose completely random actions for chaos testing."""
        all_commands = [
            "look", "inventory", "status", "help", "stats", "gold", "level",
            "north", "south", "east", "west", "up", "down",
            "recipes", "quests", "progress", "equipment", "history"
        ]
        
        # Add contextual commands
        room_items = [state.items[item_id].name for item_id in current_room.items 
                     if item_id in state.items and state.items[item_id].is_visible]
        if room_items:
            all_commands.extend([f"take {item}" for item in room_items[:3]])
            all_commands.extend([f"examine {item}" for item in room_items[:3]])
        
        room_npcs = [state.npcs[npc_id].name for npc_id in current_room.npcs 
                    if npc_id in state.npcs and state.npcs[npc_id].is_alive]
        if room_npcs:
            all_commands.extend([f"talk {npc}" for npc in room_npcs])
        
        room_enemies = [state.enemies[enemy_id].name for enemy_id in current_room.enemies 
                       if enemy_id in state.enemies and state.enemies[enemy_id].is_alive]
        if room_enemies:
            all_commands.extend([f"attack {enemy}" for enemy in room_enemies])
        
        return random.choice(all_commands)
    
    def _execute_command(self, engine: GameEngine, command: str, verbose: bool) -> None:
        """Execute a command and track the result."""
        if verbose:
            print(f"\n🤖 AI: {command}")
        
        self.game_log.append(f"Action {self.actions_taken + 1}: {command}")
        
        try:
            # Capture the current state before command
            old_room = engine.state.player.current_room
            old_health = engine.state.player.health
            old_level = engine.state.player.level
            old_gold = engine.state.player.gold
            
            # Execute the command
            result = engine.command_parser.parse_and_execute(command)
            
            if result:
                if verbose:
                    print(result)
                self.game_log.append(f"Result: {result[:100]}...")  # Truncate long results
                
                # Check for significant changes
                if engine.state.player.current_room != old_room:
                    self.game_log.append(f"  -> Moved to: {engine.state.rooms[engine.state.player.current_room].name}")
                if engine.state.player.health != old_health:
                    self.game_log.append(f"  -> Health changed: {old_health} -> {engine.state.player.health}")
                if engine.state.player.level != old_level:
                    self.game_log.append(f"  -> Level up! {old_level} -> {engine.state.player.level}")
                if engine.state.player.gold != old_gold:
                    self.game_log.append(f"  -> Gold changed: {old_gold} -> {engine.state.player.gold}")
                
                self.successful_commands.append(command)
            else:
                self.failed_commands.append(command)
                if verbose:
                    print("❌ Command failed or returned no result")
        
        except Exception as e:
            logger.error(f"Error executing command '{command}': {e}")
            self.failed_commands.append(command)
            self.game_log.append(f"ERROR: {str(e)}")
            if verbose:
                print(f"❌ Error: {e}")
    
    def _generate_statistics(self, state: GameState, duration: float) -> Dict[str, any]:
        """Generate comprehensive statistics from the AI session."""
        return {
            "strategy": self.strategy.value,
            "actions_taken": self.actions_taken,
            "session_duration": round(duration, 2),
            "actions_per_second": round(self.actions_taken / duration, 2) if duration > 0 else 0,
            "successful_commands": len(self.successful_commands),
            "failed_commands": len(self.failed_commands),
            "success_rate": round(len(self.successful_commands) / max(self.actions_taken, 1) * 100, 1),
            "rooms_visited": len(self.visited_rooms),
            "items_discovered": len(self.known_items),
            "npcs_encountered": len(self.known_npcs),
            "enemies_encountered": len(self.known_enemies),
            "final_level": state.player.level,
            "final_health": state.player.health,
            "final_gold": state.player.gold,
            "inventory_size": len(state.player.inventory),
            "quests_active": len(state.player.active_quests),
            "quests_completed": len(state.player.completed_quests),
            "recipes_known": len(state.player.known_recipes),
            "game_completed": state.is_game_over,
            "player_alive": state.player.is_alive,
            "most_common_successful_commands": self._get_most_common(self.successful_commands),
            "most_common_failed_commands": self._get_most_common(self.failed_commands)
        }
    
    def _get_most_common(self, commands: List[str], top_n: int = 5) -> List[Tuple[str, int]]:
        """Get the most common commands from a list."""
        from collections import Counter
        counter = Counter(commands)
        return counter.most_common(top_n)
    
    def _print_session_summary(self, stats: Dict[str, any]) -> None:
        """Print a summary of the AI session."""
        print("\n" + "="*60)
        print("🤖 AI PLAYER SESSION SUMMARY")
        print("="*60)
        print(f"Strategy: {stats['strategy'].upper()}")
        print(f"Duration: {stats['session_duration']}s ({stats['actions_taken']} actions)")
        print(f"Success Rate: {stats['success_rate']}% ({stats['successful_commands']}/{stats['actions_taken']})")
        print(f"Exploration: {stats['rooms_visited']} rooms, {stats['items_discovered']} items, {stats['npcs_encountered']} NPCs")
        print(f"Player Status: Level {stats['final_level']}, {stats['final_health']} HP, {stats['final_gold']} gold")
        print(f"Progress: {stats['quests_completed']} quests completed, {stats['recipes_known']} recipes known")
        print(f"Game Status: {'COMPLETED' if stats['game_completed'] else 'IN PROGRESS'}, Player {'ALIVE' if stats['player_alive'] else 'DEAD'}")
        
        if stats['most_common_successful_commands']:
            print("\nMost Successful Commands:")
            for cmd, count in stats['most_common_successful_commands']:
                print(f"  {cmd}: {count} times")
        
        if stats['most_common_failed_commands']:
            print("\nMost Failed Commands:")
            for cmd, count in stats['most_common_failed_commands']:
                print(f"  {cmd}: {count} times")
        
        print("="*60)
    
    def save_log(self, filename: str = "ai_player_log.txt") -> None:
        """Save the game log to a file."""
        with open(filename, 'w') as f:
            f.write("\n".join(self.game_log))
        logger.info(f"AI Player log saved to {filename}")
