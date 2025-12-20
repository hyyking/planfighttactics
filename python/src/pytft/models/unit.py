"""
Unit (Champion) model for TFT knowledge graph.
"""
import re
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator
from obsidiantools.api import Vault


class Unit(BaseModel):
    """Represents a TFT unit/champion with validation."""
    
    name: str
    filepath: Optional[Path] = None
    traits: List[str] = Field(default_factory=list)
    cost: int = Field(ge=1, le=7, default=1)  # cost between 1-7
    tags: List[str] = Field(default_factory=list)
    recommended_items: List[str] = Field(default_factory=list)
    unlock: Optional[str] = None

    @field_validator('traits', mode='before')
    @classmethod
    def validate_traits(cls, v):
        """Ensure traits is always a list."""
        if v is None:
            return []
        return v if isinstance(v, list) else [v]

    @field_validator('tags', mode='before')
    @classmethod
    def validate_tags(cls, v):
        """Ensure tags is always a list."""
        if v is None:
            return []
        return v if isinstance(v, list) else [v]

    @field_validator('recommended_items', mode='before')
    @classmethod
    def validate_items(cls, v):
        """Ensure items is always a list."""
        if v is None:
            return []
        return v if isinstance(v, list) else [v]

    @classmethod
    def parse_from_md(cls, filepath: Path, text: str, frontmatter: dict) -> 'Unit':
        """Parse unit from markdown file - legacy method, kept for backwards compat."""
        name = filepath.stem
        traits = frontmatter.get('traits', []) or []
        cost = frontmatter.get('cost', 1)
        tags = frontmatter.get('tags', []) or []
        
        # Extract item links: [item :: [[ItemName]]]
        recommended_items = re.findall(r'\[item\s::\s*\[\[([^\]|]+)', text)
        
        # Extract unlock condition
        unlock_match = re.search(r'unlock:\s*(.+?)$', text, re.IGNORECASE | re.MULTILINE)
        unlock = unlock_match.group(1).strip() if unlock_match else None
        
        return cls(
            name=name,
            filepath=filepath,
            traits=traits,
            cost=cost,
            tags=tags,
            recommended_items=recommended_items,
            unlock=unlock
        )

    @classmethod
    def from_obsidian_note(cls, note_name: str, vault: Vault) -> 'Unit':
        """Parse unit from obsidiantools vault using indices."""
        name = note_name
        
        # Extract frontmatter using vault.front_matter_index
        fm = vault.front_matter_index.get(note_name) or {}
        traits = fm.get('traits', []) or []
        cost = fm.get('cost', 1)
        tags = fm.get('tags', []) or []
        unlock = fm.get('unlock')
        
        # Extract item links by reading the file directly
        recommended_items = []
        file_path = vault.md_file_index.get(note_name)
        
        if file_path:
            # Ensure path is absolute relative to vault root
            if not file_path.is_absolute():
                file_path = vault.dirpath / file_path
            
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                item_pattern = r'\[item\s::\s*\[\[([^\]|]+)'
                recommended_items = re.findall(item_pattern, content)
        
        return cls(
            name=name,
            filepath=file_path,
            traits=traits,
            cost=cost,
            tags=tags,
            recommended_items=recommended_items,
            unlock=unlock
        )

    def __repr__(self):
        items_str = f", items={self.recommended_items}" if self.recommended_items else ""
        return f"Unit({self.name}, cost={self.cost}, traits={self.traits}{items_str})"
