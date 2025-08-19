"""Quest system for the text adventure game."""

import logging
from typing import Dict, List, Optional, Tuple, Any
from game.models import (
    Player, Quest, QuestStatus, NPC, GameState
)


logger = logging.getLogger(__name__)


class QuestSystem:
    """Handles quest management and progression."""
    
    def __init__(self, game_state: GameState) -> None:
        """Initialize the quest system."""
        self.state = game_state
        self._setup_default_quests()
    
    def _setup_default_quests(self) -> None:
        """Setup default quests in the game."""
        quests = {
            "find_gem": Quest(
                id="find_gem",
                name="The Lost Ruby",
                description="Find the wizard's lost ruby gem somewhere in the dungeon.",
                quest_giver="wizard",
                requirements={"gem": 1},
                rewards={"gold_coin": 2},
                experience_reward=50,
                gold_reward=25
            ),
            "defeat_goblin": Quest(
                id="defeat_goblin",
                name="Goblin Hunter",
                description="Defeat the goblin that has been terrorizing the area.",
                quest_giver="guard",
                requirements={"goblin_defeated": 1},
                rewards={"sword": 1},
                experience_reward=100,
                gold_reward=50
            ),
            "collect_herbs": Quest(
                id="collect_herbs",
                name="Herb Collection",
                description="Collect herbs for the merchant's potion making.",
                quest_giver="merchant",
                requirements={"herb": 5},
                rewards={"health_potion": 2},
                experience_reward=30,
                gold_reward=15,
                is_repeatable=True
            ),
            "explore_caves": Quest(
                id="explore_caves",
                name="Cave Explorer",
                description="Explore the deep caverns and report back what you find.",
                quest_giver="guard",
                requirements={"cave_explored": 1},
                rewards={"torch": 1},
                experience_reward=75,
                gold_reward=30
            ),
            "craft_sword": Quest(
                id="craft_sword",
                name="Master Craftsman",
                description="Craft an iron sword to prove your crafting skills.",
                quest_giver="merchant",
                requirements={"iron_sword": 1},
                rewards={"gold_coin": 3},
                experience_reward=80,
                gold_reward=40
            )
        }
        
        self.state.quests.update(quests)
    
    def get_available_quests(self) -> List[Quest]:
        """Get quests available to the player."""
        available = []
        
        for quest in self.state.quests.values():
            if self._can_accept_quest(quest):
                available.append(quest)
        
        return available
    
    def _can_accept_quest(self, quest: Quest) -> bool:
        """Check if player can accept a quest."""
        # Check if quest is already active or completed
        if quest.id in self.state.player.active_quests:
            return False
        
        if quest.id in self.state.player.completed_quests:
            if not quest.is_repeatable:
                return False
        
        # Check if quest giver is in the same room
        quest_giver = self.state.npcs.get(quest.quest_giver)
        if not quest_giver or quest_giver.current_room != self.state.player.current_room:
            return False
        
        return True
    
    def accept_quest(self, quest_name: str) -> str:
        """Accept a quest from an NPC."""
        # Find the quest
        quest = None
        for q in self.state.quests.values():
            if quest_name.lower() in q.name.lower():
                quest = q
                break
        
        if not quest:
            return f"Quest '{quest_name}' not found."
        
        # Check if player can accept it
        if not self._can_accept_quest(quest):
            if quest.id in self.state.player.active_quests:
                return f"You have already accepted the {quest.name} quest."
            elif quest.id in self.state.player.completed_quests and not quest.is_repeatable:
                return f"You have already completed the {quest.name} quest."
            else:
                return f"You cannot accept the {quest.name} quest right now."
        
        # Add to active quests
        self.state.player.active_quests.append(quest.id)
        quest.status = QuestStatus.IN_PROGRESS
        
        return f"You accept the quest: {quest.name}\n{quest.description}"
    
    def check_quest_progress(self) -> str:
        """Check progress on all active quests."""
        if not self.state.player.active_quests:
            return "You have no active quests."
        
        progress = []
        completed_quests = []
        
        for quest_id in self.state.player.active_quests:
            quest = self.state.quests.get(quest_id)
            if not quest:
                continue
            
            if self._is_quest_complete(quest):
                completed_quests.append(quest)
            else:
                progress.append(self._get_quest_progress(quest))
        
        # Complete finished quests
        for quest in completed_quests:
            self._complete_quest(quest)
        
        if progress:
            return "\n\n".join(progress)
        else:
            return "All active quests are complete!"
    
    def _is_quest_complete(self, quest: Quest) -> bool:
        """Check if a quest is complete."""
        for requirement, count in quest.requirements.items():
            if not self._check_requirement(requirement, count):
                return False
        return True
    
    def _check_requirement(self, requirement: str, count: int) -> bool:
        """Check if a quest requirement is met."""
        if requirement == "goblin_defeated":
            # Check if goblin is defeated
            for enemy in self.state.enemies.values():
                if enemy.enemy_type.value == "goblin" and not enemy.is_alive:
                    return True
            return False
        
        elif requirement == "cave_explored":
            # Check if deep cavern has been visited
            deep_cavern = self.state.rooms.get("deep_cavern")
            return deep_cavern and deep_cavern.is_visited
        
        else:
            # Check inventory for items
            player_count = 0
            for item_id in self.state.player.inventory:
                item = self.state.items.get(item_id)
                if item and requirement.lower() in item.name.lower():
                    player_count += 1
            
            return player_count >= count
    
    def _get_quest_progress(self, quest: Quest) -> str:
        """Get progress description for a quest."""
        progress = [f"Quest: {quest.name}"]
        
        for requirement, count in quest.requirements.items():
            current = self._get_requirement_progress(requirement)
            progress.append(f"  {requirement}: {current}/{count}")
        
        return "\n".join(progress)
    
    def _get_requirement_progress(self, requirement: str) -> int:
        """Get current progress for a requirement."""
        if requirement == "goblin_defeated":
            for enemy in self.state.enemies.values():
                if enemy.enemy_type.value == "goblin" and not enemy.is_alive:
                    return 1
            return 0
        
        elif requirement == "cave_explored":
            deep_cavern = self.state.rooms.get("deep_cavern")
            return 1 if deep_cavern and deep_cavern.is_visited else 0
        
        else:
            count = 0
            for item_id in self.state.player.inventory:
                item = self.state.items.get(item_id)
                if item and requirement.lower() in item.name.lower():
                    count += 1
            return count
    
    def _complete_quest(self, quest: Quest) -> None:
        """Complete a quest and give rewards."""
        # Remove from active quests
        self.state.player.active_quests.remove(quest.id)
        quest.status = QuestStatus.COMPLETED
        
        # Add to completed quests
        self.state.player.completed_quests.add(quest.id)
        
        # Give rewards
        self.state.player.experience += quest.experience_reward
        self.state.player.gold += quest.gold_reward
        
        # Give item rewards
        for item_id, count in quest.rewards.items():
            for _ in range(count):
                if item_id in self.state.items:
                    self.state.player.inventory.append(item_id)
        
        # Consume required items
        for requirement, count in quest.requirements.items():
            if requirement not in ["goblin_defeated", "cave_explored"]:
                self._consume_quest_items(requirement, count)
    
    def _consume_quest_items(self, item_name: str, count: int) -> None:
        """Consume items required for quest completion."""
        consumed = 0
        items_to_remove = []
        
        for item_id in self.state.player.inventory:
            if consumed >= count:
                break
            
            item = self.state.items.get(item_id)
            if item and item_name.lower() in item.name.lower():
                items_to_remove.append(item_id)
                consumed += 1
        
        # Remove consumed items
        for item_id in items_to_remove:
            self.state.player.inventory.remove(item_id)
    
    def list_quests(self) -> str:
        """List all quests and their status."""
        if not self.state.quests:
            return "No quests available."
        
        quest_list = []
        
        # Active quests
        active_quests = []
        for quest_id in self.state.player.active_quests:
            quest = self.state.quests.get(quest_id)
            if quest:
                active_quests.append(f"ACTIVE: {quest.name}")
        
        if active_quests:
            quest_list.append("Active Quests:")
            quest_list.extend(active_quests)
            quest_list.append("")
        
        # Available quests
        available_quests = []
        for quest in self.state.quests.values():
            if self._can_accept_quest(quest):
                available_quests.append(f"AVAILABLE: {quest.name} (from {self.state.npcs[quest.quest_giver].name})")
        
        if available_quests:
            quest_list.append("Available Quests:")
            quest_list.extend(available_quests)
            quest_list.append("")
        
        # Completed quests
        completed_quests = []
        for quest_id in self.state.player.completed_quests:
            quest = self.state.quests.get(quest_id)
            if quest:
                completed_quests.append(f"COMPLETED: {quest.name}")
        
        if completed_quests:
            quest_list.append("Completed Quests:")
            quest_list.extend(completed_quests)
        
        return "\n".join(quest_list) if quest_list else "No quests available."
    
    def get_quest_details(self, quest_name: str) -> str:
        """Get detailed information about a quest."""
        quest = None
        for q in self.state.quests.values():
            if quest_name.lower() in q.name.lower():
                quest = q
                break
        
        if not quest:
            return f"Quest '{quest_name}' not found."
        
        details = [f"Quest: {quest.name}"]
        details.append(f"Description: {quest.description}")
        details.append(f"Status: {quest.status.value}")
        
        if quest.requirements:
            details.append("Requirements:")
            for requirement, count in quest.requirements.items():
                current = self._get_requirement_progress(requirement)
                details.append(f"  {requirement}: {current}/{count}")
        
        if quest.rewards:
            details.append("Rewards:")
            for item_id, count in quest.rewards.items():
                item = self.state.items.get(item_id)
                item_name = item.name if item else item_id
                details.append(f"  {item_name}: {count}")
        
        if quest.experience_reward > 0:
            details.append(f"Experience Reward: {quest.experience_reward}")
        
        if quest.gold_reward > 0:
            details.append(f"Gold Reward: {quest.gold_reward}")
        
        if quest.is_repeatable:
            details.append("This quest can be repeated.")
        
        return "\n".join(details)
