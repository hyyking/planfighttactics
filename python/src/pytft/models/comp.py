"""
Comp (Team Composition) model for TFT knowledge graph.
"""
import logging
import re
from pathlib import Path
from typing import List, Optional, Dict

from pydantic import BaseModel, Field, field_validator, ConfigDict
from obsidiantools.api import Vault

from .board import Board

logger = logging.getLogger(__name__)


class Comp(BaseModel):
    """Represents a TFT team composition with validation."""
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    name: str
    filepath: Optional[Path] = None
    board: Optional[Board] = None  # Board representation with unit positions and roles
    tags: List[str] = Field(default_factory=list)
    description: Optional[str] = None
    tips: Optional[str] = None
    planner_code: Optional[str] = None

    @property
    def units(self) -> List[str]:
        """All unit names in composition (derived from board)."""
        return self.board.get_all_unit_names() if self.board else []

    @field_validator('tags', mode='before')
    @classmethod
    def validate_lists(cls, v):
        """Ensure all list fields are actually lists."""
        if v is None:
            return []
        return v if isinstance(v, list) else [v]

    @field_validator('board', mode='before')
    @classmethod
    def validate_board(cls, v):
        """Log warning if board is None."""
        if v is None:
            logger.warning("Comp initialized with no board")
        return v

    @classmethod
    def parse_from_md(cls, filepath: Path, text: str, frontmatter: dict) -> 'Comp':
        """Parse comp from markdown file - legacy method."""
        name = filepath.stem
        tags = frontmatter.get('tags', []) or []
        
        # Extract comp table section
        table_match = re.search(r'## Comp\n(.*?)(?=##|\Z)', text, re.IGNORECASE | re.DOTALL)
        table_text = table_match.group(1) if table_match else text
        
        # Parse board table to get Board object
        board = Board.from_table(table_text)
        
        # Extract tips
        tips_match = re.search(r'##\s*Tips\s*\n(.+?)(?=##|\Z)', text, re.IGNORECASE | re.DOTALL)
        tips = tips_match.group(1).strip() if tips_match else None
        
        # Extract description
        desc_match = re.search(r'##\s*Description\s*\n(.+?)(?=##|\Z)', text, re.IGNORECASE | re.DOTALL)
        description = desc_match.group(1).strip() if desc_match else None
        
        # Extract planner code
        planner_match = re.search(r'planner[_-]code:\s*(.+?)$', text, re.IGNORECASE | re.MULTILINE)
        planner_code = planner_match.group(1).strip() if planner_match else None
        
        return cls(
            name=name,
            filepath=filepath,
            board=board,
            tags=tags,
            description=description,
            tips=tips,
            planner_code=planner_code
        )

    @classmethod
    def from_obsidian_note(cls, note_name: str, vault: Vault) -> 'Comp':
        """Parse comp from obsidiantools vault using indices."""
        name = note_name
        
        # Extract frontmatter
        fm = vault.front_matter_index.get(note_name) or {}
        tags = fm.get('tags', []) or []
        
        # Read file for content extraction
        board = None
        description = None
        tips = None
        planner_code = None
        
        file_path = vault.md_file_index.get(note_name)
        
        if not file_path:
            logger.warning(f"Comp '{note_name}' not found in vault index")
            return cls(name=name, filepath=None, board=None, tags=tags)
        
        # Ensure path is absolute relative to vault root
        if not file_path.is_absolute():
            file_path = vault.dirpath / file_path
        
        if not file_path.exists():
            logger.warning(f"Comp file not found: {file_path}")
            return cls(name=name, filepath=file_path, board=None, tags=tags)
        
        logger.debug(f"Loading comp from {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract comp table section
        table_match = re.search(r'## Comp\n(.*?)(?=##|\Z)', content, re.IGNORECASE | re.DOTALL)
        table_text = table_match.group(1) if table_match else content
        
        # Parse board table to get Board object
        board = Board.from_table(table_text)
        
        # Extract tips
        tips_match = re.search(r'##\s*Tips\s*\n(.+?)(?=##|\Z)', content, re.IGNORECASE | re.DOTALL)
        tips = tips_match.group(1).strip() if tips_match else None
        
        # Extract description
        desc_match = re.search(r'##\s*Description\s*\n(.+?)(?=##|\Z)', content, re.IGNORECASE | re.DOTALL)
        description = desc_match.group(1).strip() if desc_match else None
        
        # Extract planner code
        planner_match = re.search(r'planner[_-]code:\s*(.+?)$', content, re.IGNORECASE | re.MULTILINE)
        planner_code = planner_match.group(1).strip() if planner_match else None
        
        return cls(
            name=name,
            filepath=file_path,
            board=board,
            tags=tags,
            description=description,
            tips=tips,
            planner_code=planner_code
        )

    def populate_board_units(self, units_dict: Dict[str, 'Unit']) -> None:
        """
        Populate board with full Unit objects from a units dictionary.
        This adds unit details (traits, cost, etc.) to the board positions.
        
        Args:
            units_dict: Dictionary of Unit objects keyed by unit name
        """
        if not self.board:
            return
        
        for unit_pos in self.board.units:
            if unit_pos.name in units_dict:
                unit_pos.unit = units_dict[unit_pos.name]

    def __repr__(self):
        return f"Comp({self.name}, units={len(self.units)})"
