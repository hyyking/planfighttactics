"""
Vault integration and knowledge graph for TFT.
"""
import logging
from pathlib import Path
from typing import Dict, Counter
from collections import Counter as CounterType

from obsidiantools.api import Vault

from .unit import Unit
from .item import Item
from .comp import Comp

logger = logging.getLogger(__name__)


class TFTKnowledgeGraph:
    """Loads and manages TFT data from an Obsidian vault."""
    
    def __init__(self, root: Path = Path(".")):
        """Initialize knowledge graph with vault root path."""
        self.root = Path(root)
        self.units: Dict[str, Unit] = {}
        self.items: Dict[str, Item] = {}
        self.comps: Dict[str, Comp] = {}
        self.vault: Vault | None = None

    def load_vault(self):
        """Create and index the Obsidian vault."""
        self.vault = Vault(self.root)
        self.vault.gather()
        logger.info(f"Vault loaded from {self.root}")
        logger.debug(f"{len(self.vault.md_file_index)} markdown files indexed")
        logger.debug(f"{len(self.vault.front_matter_index)} files with frontmatter")

    def parse_units(self):
        """Parse all unit files from vault."""
        if not self.vault:
            self.load_vault()
        
        for note_name, file_path in self.vault.md_file_index.items():
            if file_path.parent.name != "Units":
                continue
            
            try:
                unit = Unit.from_obsidian_note(note_name, self.vault)
                self.units[note_name] = unit
            except Exception as e:
                logger.warning(f"Failed to parse unit {note_name}: {e}")

    def parse_items(self):
        """Parse all item files from vault."""
        if not self.vault:
            self.load_vault()
        
        for note_name, file_path in self.vault.md_file_index.items():
            if file_path.parent.name != "Item":
                continue
            
            try:
                item = Item.from_obsidian_note(note_name, self.vault)
                self.items[note_name] = item
            except Exception as e:
                logger.warning(f"Failed to parse item {note_name}: {e}")

    def parse_comps(self):
        """Parse all comp files from vault."""
        if not self.vault:
            self.load_vault()
        
        for note_name, file_path in self.vault.md_file_index.items():
            if file_path.parent.name != "Comps":
                continue
            
            try:
                comp = Comp.from_obsidian_note(note_name, self.vault)
                self.comps[note_name] = comp
            except Exception as e:
                logger.warning(f"Failed to parse comp {note_name}: {e}")

    def load_all(self):
        """Load all units, items, and comps from vault."""
        self.parse_units()
        self.parse_items()
        self.parse_comps()
        
        # Populate board positions with full Unit objects
        for comp in self.comps.values():
            comp.populate_board_units(self.units)
        
        logger.info(f"Loaded {len(self.units)} units, {len(self.items)} items, {len(self.comps)} comps")

    def get_comp_traits(self, comp: Comp) -> CounterType:
        """Get trait frequency for a composition."""
        traits = CounterType()
        for unit_name in comp.units:
            if unit_name in self.units:
                unit = self.units[unit_name]
                for trait in unit.traits:
                    traits[trait] += 1
        return traits

    def __repr__(self):
        return f"TFTKnowledgeGraph(root={self.root}, units={len(self.units)}, items={len(self.items)}, comps={len(self.comps)})"
