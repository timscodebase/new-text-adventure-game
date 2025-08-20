"Visuals for the text adventure game."

from typing import List, Optional
import random
import os
import glob
from rich.console import Console
from rich.text import Text


class Visuals:
    """Handles all visuals for the game."""
    console = Console()

    ART_BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'art')

    @classmethod
    def _load_art_from_directory(cls, sub_dir: str) -> dict:
        art_dict = {}
        full_path = os.path.join(cls.ART_BASE_PATH, sub_dir)
        if not os.path.exists(full_path):
            return art_dict

        for art_file in glob.glob(os.path.join(full_path, '*.txt')):
            file_name = os.path.basename(art_file)
            key_parts = file_name.replace('.txt', '').split('_')
            key = '_'.join(key_parts[:-1]) if key_parts[-1].isdigit() else '_'.join(key_parts)
            
            with open(art_file, 'r') as f:
                content = f.read()
            
            if key not in art_dict:
                art_dict[key] = []
            art_dict[key].append(content)
        return art_dict

    # Game title banner
    TITLE_BANNER = ""
    # Victory banner
    VICTORY_BANNER = ""
    # Game over banner
    GAME_OVER_BANNER = ""

    ROOM_DECORATIONS = {}
    ENEMY_ART = {}
    ITEM_ART = {}
    NPC_ART = {}
    COMBAT_ART = {}
    STATUS_ART = {}

    def __init__(self):
        self.TITLE_BANNER = self._load_art_from_file('title_banner.txt')
        self.VICTORY_BANNER = self._load_art_from_file('victory_banner.txt')
        self.GAME_OVER_BANNER = self._load_art_from_file('game_over_banner.txt')

        self.ROOM_DECORATIONS = self._load_art_from_directory('rooms')
        self.ENEMY_ART = self._load_art_from_directory('enemies')
        self.ITEM_ART = self._load_art_from_directory('items')
        self.NPC_ART = self._load_art_from_directory('npcs')
        self.COMBAT_ART = self._load_art_from_directory('combat')
        self.STATUS_ART = self._load_art_from_directory('status')

    @classmethod
    def _load_art_from_file(cls, file_name: str) -> str:
        full_path = os.path.join(cls.ART_BASE_PATH, file_name)
        if os.path.exists(full_path):
            with open(full_path, 'r') as f:
                return f.read()
        return ""
    
    @classmethod
    def get_room_visual(cls, room, npcs, enemies) -> str:
        """Get the visual representation of a room."""
        npc_art = [cls.get_npc_art(npc.name) for npc in npcs]
        enemy_art = [cls.get_enemy_art(enemy.enemy_type.value) for enemy in enemies]
        
        # Combine the art
        combined_art = ""
        if npc_art:
            for art in npc_art:
                if art:
                    combined_art += art
        if enemy_art:
            for art in enemy_art:
                if art:
                    combined_art += art
            
        return combined_art

    @classmethod
    def get_title_banner(cls) -> str:
        """Get the game title banner."""
        return cls.TITLE_BANNER
    
    @classmethod
    def get_victory_banner(cls) -> str:
        """Get the victory banner."""
        return cls.VICTORY_BANNER
    
    @classmethod
    def get_game_over_banner(cls) -> str:
        """Get the game over banner."""
        return cls.GAME_OVER_BANNER
    
    @classmethod
    def get_room_decoration(cls, room_id: str) -> Optional[str]:
        """Get room decoration art."""
        if room_id in cls.ROOM_DECORATIONS:
            art_list = cls.ROOM_DECORATIONS[room_id]
            if art_list:
                art = random.choice(art_list)
                # Apply alignment to center the art
                if art:
                    return cls.align_art(art, 60)
        return None
    
    @classmethod
    def get_enemy_art(cls, enemy_type: str) -> Optional[str]:
        """Get enemy art."""
        if enemy_type in cls.ENEMY_ART:
            art = random.choice(cls.ENEMY_ART[enemy_type])
            return cls.align_art(art)
        return None
    
    @classmethod
    def get_item_art(cls, item_name: str) -> Optional[str]:
        """Get item art."""
        for key, art_list in cls.ITEM_ART.items():
            if key.lower() in item_name.lower():
                return random.choice(art_list)
        return None
    
    @classmethod
    def get_npc_art(cls, npc_name: str) -> Optional[str]:
        """Get NPC art."""
        for key, art_list in cls.NPC_ART.items():
            if key.lower() in npc_name.lower():
                return random.choice(art_list)
        return None
    
    @classmethod
    def get_combat_art(cls, action: str) -> Optional[str]:
        """Get combat action art."""
        if action in cls.COMBAT_ART:
            return random.choice(cls.COMBAT_ART[action])
        return None
    
    @classmethod
    def get_status_art(cls, status: str) -> Optional[str]:
        """Get status effect art."""
        if status in cls.STATUS_ART:
            return random.choice(cls.STATUS_ART[status])
        return None
    
    @classmethod
    def create_box(cls, title: str, content: str, width: int = 60) -> str:
        """Create a fancy box around content."""
        lines = content.split('\n')
        box_lines = []
        
        # Top border
        box_lines.append("+ " + "-" * (width - 2) + "+")
        
        # Title
        if title:
            title_line = f"| {title.center(width - 4)} |"
            box_lines.append(title_line)
            box_lines.append("|" + "-" * (width - 2) + "|")
        
        # Content
        for line in lines:
            if line.strip():
                # Truncate or pad line to fit
                if len(line) > width - 4:
                    line = line[:width - 7] + "..."
                else:
                    line = line.ljust(width - 4)
                box_lines.append(f"| {line} |")
        
        # Bottom border
        box_lines.append("+ " + "-" * (width - 2) + "+")
        
        return '\n'.join(box_lines)
    
    @classmethod
    def create_separator(cls, char: str = "-", width: int = 60) -> str:
        """Create a separator line."""
        return char * width
    
    @classmethod
    def center_text(cls, text: str, width: int = 60) -> str:
        """Center text within a given width."""
        return text.center(width)
    
    @classmethod
    def create_progress_bar(cls, current: int, maximum: int, width: int = 20, 
                           filled_char: str = "#", empty_char: str = " ") -> str:
        """Create a visual progress bar."""
        if maximum <= 0:
            return empty_char * width
        
        filled_width = int((current / maximum) * width)
        bar = filled_char * filled_width + empty_char * (width - filled_width)
        return f"[{bar}] {current}/{maximum}"
    
    @classmethod
    def create_health_bar(cls, current: int, maximum: int) -> str:
        """Create a health bar."""
        if maximum <= 0:
            return "[          ] 0/0"
        
        percentage = current / maximum
        width = 10
        
        filled_width = int(percentage * width)
        
        bar_text = Text()
        bar_text.append("[", style="white")
        bar_text.append("#" * filled_width, style="green")
        bar_text.append(" " * (width - filled_width), style="red")
        bar_text.append(f"] {current}/{maximum}", style="white")
        
        with cls.console.capture() as capture:
            cls.console.print(bar_text, end="")
        return capture.get()
    
    @classmethod
    def create_experience_bar(cls, current: int, maximum: int) -> str:
        """Create an experience bar."""
        if maximum <= 0:
            return "[               ] 0/0"
        
        percentage = current / maximum
        width = 15
        filled_width = int(percentage * width)
        
        bar_text = Text()
        bar_text.append("[", style="white")
        bar_text.append("#" * filled_width, style="blue")
        bar_text.append(" " * (width - filled_width), style="gray")
        bar_text.append(f"] {current}/{maximum}", style="white")
        
        with cls.console.capture() as capture:
            cls.console.print(bar_text, end="")
        return capture.get()
    
    @classmethod
    def align_art(cls, art: str, width: int = 60) -> str:
        lines = art.split('\n')
        max_len = max(len(line) for line in lines)
        padding = (width - max_len) // 2
        return '\n'.join(' ' * padding + line for line in lines)
    
    @classmethod
    def create_centered_box(cls, title: str, content: str, width: int = 60) -> str:
        """Create a centered box with title and content."""
        box_width = width
        title_padding = (box_width - len(title)) // 2
        
        top_border = "+" + "-" * (box_width - 2) + "+"
        title_line = "|" + " " * title_padding + title + " " * (box_width - title_padding - len(title)) + "|"
        content_lines = []
        
        for line in content.split('\n'):
            if len(line) > box_width - 4:
                # Truncate long lines
                line = line[:box_width - 7] + "..."
            content_padding = (box_width - len(line) - 2) // 2
            content_lines.append("|" + " " * content_padding + line + " " * (box_width - content_padding - len(line) - 2) + "|")
        
        bottom_border = "+" + "-" * (box_width - 2) + "+"
        
        return f"{top_border}\n{title_line}\n" + "\n".join(content_lines) + f"\n{bottom_border}"