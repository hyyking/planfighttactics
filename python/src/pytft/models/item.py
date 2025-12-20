"""
Item model for TFT knowledge graph.
"""
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator
from obsidiantools.api import Vault


class Item(BaseModel):
    """Represents a TFT item with validation."""
    
    name: str
    filepath: Optional[Path] = None
    aliases: List[str] = Field(default_factory=list)
    category: str = "other"

    @field_validator('aliases', mode='before')
    @classmethod
    def validate_aliases(cls, v):
        """Ensure aliases is always a list."""
        if v is None:
            return []
        return v if isinstance(v, list) else [v]

    @classmethod
    def parse_from_md(cls, filepath: Path, text: str, frontmatter: dict) -> 'Item':
        """Parse item from markdown file - legacy method."""
        name = filepath.stem
        aliases = frontmatter.get('aliases', []) or []
        category = frontmatter.get('category', 'other')
        
        return cls(
            name=name,
            filepath=filepath,
            aliases=aliases,
            category=category
        )

    @classmethod
    def from_obsidian_note(cls, note_name: str, vault: Vault) -> 'Item':
        """Parse item from obsidiantools vault using indices."""
        name = note_name
        
        # Extract frontmatter using vault.front_matter_index
        fm = vault.front_matter_index.get(note_name) or {}
        aliases = fm.get('aliases', []) or []
        category = fm.get('category', 'other')
        
        file_path = vault.md_file_index.get(note_name)
        
        # Ensure path is absolute relative to vault root
        if file_path and not file_path.is_absolute():
            file_path = vault.dirpath / file_path
        
        return cls(
            name=name,
            filepath=file_path,
            aliases=aliases,
            category=category
        )

    def __repr__(self):
        aliases_str = f", aliases={self.aliases}" if self.aliases else ""
        return f"Item({self.name}, cat={self.category}{aliases_str})"
