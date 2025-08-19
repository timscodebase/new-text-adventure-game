"""Combat system for the text adventure game."""

import logging
import random
from typing import Dict, List, Optional, Tuple, Any
from game.models import (
    Player, Enemy, Item, Equipment, EnemyType, GameState
)


logger = logging.getLogger(__name__)


class CombatSystem:
    """Handles combat between player and enemies."""
    
    def __init__(self, game_state: GameState) -> None:
        """Initialize the combat system."""
        self.state = game_state
    
    def start_combat(self, enemy_id: str) -> str:
        """Start combat with an enemy."""
        if enemy_id not in self.state.enemies:
            return "Enemy not found."
        
        enemy = self.state.enemies[enemy_id]
        if not enemy.is_alive:
            return f"{enemy.name} is already defeated."
        
        if self.state.player.current_room != enemy.current_room:
            return f"{enemy.name} is not in this room."
        
        # Check if room is a safe zone
        current_room = self.state.rooms[self.state.player.current_room]
        if current_room.is_safe_zone:
            return "Combat is not allowed in this area."
        
        # Start combat
        self.state.combat_log = []
        self.state.combat_log.append(f"Combat begins! You face {enemy.name}!")
        
        # Check for surprise attacks
        if self._check_surprise_attack(enemy):
            self.state.combat_log.append(f"{enemy.name} catches you by surprise!")
            damage = self._calculate_damage(enemy.damage, self._get_player_armor())
            self.state.player.health -= damage
            self.state.combat_log.append(f"You take {damage} damage!")
        
        return "\n".join(self.state.combat_log)
    
    def attack(self, target_name: str = "") -> str:
        """Player attacks an enemy."""
        current_room = self.state.rooms[self.state.player.current_room]
        
        # Find enemy to attack
        enemy = None
        for enemy_id in current_room.enemies:
            if enemy_id in self.state.enemies:
                potential_enemy = self.state.enemies[enemy_id]
                if potential_enemy.is_alive and target_name.lower() in potential_enemy.name.lower():
                    enemy = potential_enemy
                    break
        
        if not enemy:
            # Attack first available enemy
            for enemy_id in current_room.enemies:
                if enemy_id in self.state.enemies:
                    potential_enemy = self.state.enemies[enemy_id]
                    if potential_enemy.is_alive:
                        enemy = potential_enemy
                        break
        
        if not enemy:
            return "There are no enemies to attack."
        
        # Calculate damage
        weapon_damage = self._get_weapon_damage()
        base_damage = max(1, self.state.player.strength // 3)
        total_damage = weapon_damage + base_damage
        
        # Apply damage
        actual_damage = self._calculate_damage(total_damage, enemy.armor)
        enemy.health -= actual_damage
        
        # Log the attack
        weapon_name = "your fists"
        if self.state.player.equipment.weapon:
            weapon_item = self.state.items.get(self.state.player.equipment.weapon)
            if weapon_item:
                weapon_name = weapon_item.name
        
        self.state.combat_log.append(f"You attack {enemy.name} with {weapon_name} for {actual_damage} damage!")
        
        # Check if enemy is defeated
        if enemy.health <= 0:
            enemy.health = 0
            enemy.is_alive = False
            self.state.combat_log.append(f"You have defeated {enemy.name}!")
            
            # Give rewards
            self.state.player.experience += enemy.experience_reward
            self.state.player.gold += enemy.gold_reward
            self.state.combat_log.append(f"You gain {enemy.experience_reward} experience and {enemy.gold_reward} gold!")
            
            # Check for level up
            if self.state.player.experience >= self.state.player.experience_to_next:
                self._level_up()
            
            # Drop enemy inventory
            if enemy.inventory:
                current_room.items.extend(enemy.inventory)
                self.state.combat_log.append(f"{enemy.name} drops some items!")
            
            return "\n".join(self.state.combat_log)
        
        # Enemy counter-attack
        return self._enemy_turn(enemy)
    
    def _enemy_turn(self, enemy: Enemy) -> str:
        """Enemy takes their turn."""
        # Calculate enemy damage
        enemy_damage = self._calculate_damage(enemy.damage, self._get_player_armor())
        self.state.player.health -= enemy_damage
        
        self.state.combat_log.append(f"{enemy.name} attacks you for {enemy_damage} damage!")
        
        # Check if player is defeated
        if self.state.player.health <= 0:
            self.state.player.health = 0
            self.state.player.is_alive = False
            self.state.combat_log.append("You have been defeated!")
            return "\n".join(self.state.combat_log)
        
        # Check for special abilities
        if enemy.special_abilities and random.random() < 0.3:  # 30% chance
            special_effect = self._use_enemy_special_ability(enemy)
            if special_effect:
                self.state.combat_log.append(special_effect)
        
        return "\n".join(self.state.combat_log)
    
    def flee(self) -> str:
        """Attempt to flee from combat."""
        current_room = self.state.rooms[self.state.player.current_room]
        
        # Check if there are enemies
        enemies_present = any(
            enemy_id in self.state.enemies and self.state.enemies[enemy_id].is_alive
            for enemy_id in current_room.enemies
        )
        
        if not enemies_present:
            return "There are no enemies to flee from."
        
        # Calculate flee chance based on dexterity
        flee_chance = min(0.8, self.state.player.dexterity / 20.0)
        
        if random.random() < flee_chance:
            self.state.combat_log.append("You successfully flee from combat!")
            return "\n".join(self.state.combat_log)
        else:
            self.state.combat_log.append("You fail to flee!")
            # Take damage from fleeing
            damage = random.randint(1, 5)
            self.state.player.health -= damage
            self.state.combat_log.append(f"You take {damage} damage while trying to flee!")
            
            # Enemy gets a free attack
            for enemy_id in current_room.enemies:
                if enemy_id in self.state.enemies:
                    enemy = self.state.enemies[enemy_id]
                    if enemy.is_alive:
                        return self._enemy_turn(enemy)
            
            return "\n".join(self.state.combat_log)
    
    def use_item(self, item_name: str) -> str:
        """Use an item during combat."""
        # Find item in inventory
        item = None
        item_id = None
        for inv_item_id in self.state.player.inventory:
            inv_item = self.state.items.get(inv_item_id)
            if inv_item and item_name.lower() in inv_item.name.lower():
                item = inv_item
                item_id = inv_item_id
                break
        
        if not item:
            return f"You don't have a {item_name}."
        
        # Use the item
        if item.item_type == "potion" and item.healing_value > 0:
            old_health = self.state.player.health
            self.state.player.health = min(
                self.state.player.max_health,
                self.state.player.health + item.healing_value
            )
            healing = self.state.player.health - old_health
            
            # Remove item from inventory
            self.state.player.inventory.remove(item_id)
            
            self.state.combat_log.append(f"You use {item.name} and heal {healing} health!")
            
            # Enemy gets a turn
            current_room = self.state.rooms[self.state.player.current_room]
            for enemy_id in current_room.enemies:
                if enemy_id in self.state.enemies:
                    enemy = self.state.enemies[enemy_id]
                    if enemy.is_alive:
                        return self._enemy_turn(enemy)
            
            return "\n".join(self.state.combat_log)
        
        return f"You can't use {item.name} in combat."
    
    def _check_surprise_attack(self, enemy: Enemy) -> bool:
        """Check if enemy gets a surprise attack."""
        # Higher aggression level = higher chance of surprise attack
        surprise_chance = enemy.aggression_level / 20.0
        return random.random() < surprise_chance
    
    def _calculate_damage(self, attack_damage: int, defense: int) -> int:
        """Calculate actual damage after defense."""
        # Simple damage calculation
        damage = max(1, attack_damage - defense)
        # Add some randomness
        damage = max(1, damage + random.randint(-2, 2))
        return damage
    
    def _get_player_armor(self) -> int:
        """Get total armor value from equipped items."""
        total_armor = 0
        
        # Check equipped armor
        if self.state.player.equipment.armor:
            armor_item = self.state.items.get(self.state.player.equipment.armor)
            if armor_item:
                total_armor += armor_item.armor_value
        
        # Check other equipment
        for slot in ['helmet', 'boots', 'gloves']:
            item_id = getattr(self.state.player.equipment, slot)
            if item_id:
                item = self.state.items.get(item_id)
                if item:
                    total_armor += item.armor_value
        
        return total_armor
    
    def _get_weapon_damage(self) -> int:
        """Get damage from equipped weapon."""
        if self.state.player.equipment.weapon:
            weapon_item = self.state.items.get(self.state.player.equipment.weapon)
            if weapon_item:
                return weapon_item.damage
        return 0
    
    def _level_up(self) -> None:
        """Handle player level up."""
        self.state.player.level += 1
        self.state.player.experience -= self.state.player.experience_to_next
        self.state.player.experience_to_next = int(self.state.player.experience_to_next * 1.5)
        
        # Increase stats
        self.state.player.max_health += 10
        self.state.player.health = self.state.player.max_health
        self.state.player.strength += 1
        self.state.player.dexterity += 1
        self.state.player.intelligence += 1
        self.state.player.constitution += 1
        
        self.state.combat_log.append(f"Level up! You are now level {self.state.player.level}!")
        self.state.combat_log.append("Your stats have increased!")
    
    def _use_enemy_special_ability(self, enemy: Enemy) -> Optional[str]:
        """Use a special ability for the enemy."""
        if not enemy.special_abilities:
            return None
        
        ability = random.choice(enemy.special_abilities)
        
        if ability == "poison":
            self.state.player.status_effects["poisoned"] = 3
            return f"{enemy.name} poisons you!"
        
        elif ability == "stun":
            self.state.player.status_effects["stunned"] = 1
            return f"{enemy.name} stuns you!"
        
        elif ability == "heal":
            heal_amount = enemy.max_health // 4
            enemy.health = min(enemy.max_health, enemy.health + heal_amount)
            return f"{enemy.name} heals themselves for {heal_amount} health!"
        
        return None
    
    def get_combat_status(self) -> str:
        """Get current combat status."""
        current_room = self.state.rooms[self.state.player.current_room]
        
        # Check for enemies
        enemies = []
        for enemy_id in current_room.enemies:
            if enemy_id in self.state.enemies:
                enemy = self.state.enemies[enemy_id]
                if enemy.is_alive:
                    enemies.append(enemy)
        
        if not enemies:
            return "No enemies present."
        
        status = [f"Your Health: {self.state.player.health}/{self.state.player.max_health}"]
        
        for enemy in enemies:
            health_percent = (enemy.health / enemy.max_health) * 100
            status.append(f"{enemy.name}: {enemy.health}/{enemy.max_health} ({health_percent:.0f}%)")
        
        return "\n".join(status)
