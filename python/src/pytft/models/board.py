"""
Board representation for TFT compositions.
Represents the 7x4 board with unit positions.
"""
import logging
import re
from typing import Optional, List, Dict, Tuple, TYPE_CHECKING, ClassVar
from dataclasses import dataclass, field

from pydantic import BaseModel, Field, field_validator, ConfigDict

if TYPE_CHECKING:
    from .unit import Unit

logger = logging.getLogger(__name__)


@dataclass
class UnitPosition:
    """A unit at a specific board position."""
    name: str
    row: int
    col: int
    role: Optional[str] = None  # carry, tank, support, or None
    unit: Optional['Unit'] = field(default=None, repr=False)  # Full Unit object if available
    
    def __repr__(self):
        role_str = f" ({self.role})" if self.role else ""
        return f"{self.name} at [{self.row},{self.col}]{role_str}"


class Board(BaseModel):
    """
    Represents a 7x4 TFT board with unit positions.
    
    Board dimensions:
    - 7 columns (0-6, left to right)
    - 4 rows (0-3, top to bottom)
    """
    
    COLS: ClassVar[int] = 7
    ROWS: ClassVar[int] = 4
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    units: List[UnitPosition] = Field(default_factory=list)
    
    @field_validator('units', mode='before')
    @classmethod
    def validate_units(cls, v):
        """Validate that all units are within board bounds."""
        if not isinstance(v, list):
            v = [v] if v else []
        
        for unit_pos in v:
            if not isinstance(unit_pos, UnitPosition):
                continue
            
            if not (0 <= unit_pos.row < cls.ROWS):
                logger.warning(f"Unit {unit_pos.name} at row {unit_pos.row} out of bounds (0-{cls.ROWS-1})")
            
            if not (0 <= unit_pos.col < cls.COLS):
                logger.warning(f"Unit {unit_pos.name} at col {unit_pos.col} out of bounds (0-{cls.COLS-1})")
            
            if unit_pos.role and unit_pos.role.lower() not in ('carry', 'tank', 'support', None):
                logger.warning(f"Unit {unit_pos.name} has invalid role: {unit_pos.role}")
        
        return v
    
    @property
    def _board(self) -> List[List[Optional[UnitPosition]]]:
        """Compute board grid from units list (cached representation)."""
        board_grid = [
            [None for _ in range(self.COLS)] for _ in range(self.ROWS)
        ]
        for unit_pos in self.units:
            if 0 <= unit_pos.row < self.ROWS and 0 <= unit_pos.col < self.COLS:
                board_grid[unit_pos.row][unit_pos.col] = unit_pos
        return board_grid
    
    def add_unit(self, name: str, row: int, col: int, role: Optional[str] = None, unit: Optional['Unit'] = None) -> None:
        """Add a unit at a specific position."""
        if not (0 <= row < self.ROWS and 0 <= col < self.COLS):
            raise ValueError(f"Position [{row},{col}] out of bounds (0-{self.ROWS-1}, 0-{self.COLS-1})")
        
        unit_pos = UnitPosition(name=name, row=row, col=col, role=role, unit=unit)
        self.units.append(unit_pos)
        logger.debug(f"Added {unit_pos.name} at [{row},{col}]")
    
    def get_unit_at(self, row: int, col: int) -> Optional[UnitPosition]:
        """Get unit at specific position."""
        if 0 <= row < self.ROWS and 0 <= col < self.COLS:
            return self._board[row][col]
        return None
    
    def get_units_in_row(self, row: int) -> List[UnitPosition]:
        """Get all units in a specific row."""
        if not (0 <= row < self.ROWS):
            return []
        return [u for u in self.units if u.row == row]
    
    def get_units_in_col(self, col: int) -> List[UnitPosition]:
        """Get all units in a specific column."""
        if not (0 <= col < self.COLS):
            return []
        return [u for u in self.units if u.col == col]
    
    def get_units_by_role(self, role: str) -> List[UnitPosition]:
        """Get all units with a specific role."""
        return [u for u in self.units if u.role == role]
    
    def get_all_unit_names(self) -> List[str]:
        """Get list of all unit names (for compatibility)."""
        return [u.name for u in self.units]
    
    def visualize(self) -> str:
        """Create ASCII representation of the board."""
        lines = []
        for row in range(self.ROWS):
            row_str = "| "
            for col in range(self.COLS):
                unit = self._board[row][col]
                if unit:
                    # Show unit name with role indicator
                    role_char = ""
                    if unit.role == "carry":
                        role_char = "*"
                    elif unit.role == "tank":
                        role_char = "="
                    elif unit.role == "support":
                        role_char = "+"
                    
                    cell = f"{unit.name}{role_char}".ljust(15)
                else:
                    cell = " " * 15
                row_str += cell + "| "
            lines.append(row_str)
        
        return "\n".join(lines)
    
    def __repr__(self):
        return f"Board({len(self.units)} units: {', '.join(self.get_all_unit_names())})"
    
    @classmethod
    def from_table(cls, table_text: str) -> 'Board':
        """
        Parse board from markdown table.
        
        Table format (7x4 board):
        |                | [[Vi]]      | [tank::[[Loris]]]  | [[Ornn]] | ... |
        | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
        |                |             |                    |          | ... |
        | [carry::[[T-Rex]]]     |             |                    |          | ... |
        | [carry::[[Seraphine]]] | [[Caitlyn]] | [carry::[[Senna]]] |          | ... |
        
        Args:
            table_text: Markdown table text
            
        Returns:
            Board instance with units positioned
        """
        board = cls()
        
        logger.debug("Parsing board from markdown table")
        
        # Split table into lines
        lines = table_text.strip().split('\n')
        
        row_idx = 0
        for line in lines:
            # Skip empty lines and separator lines (containing ---)
            if not line.strip() or '---' in line:
                continue
            
            # Only process valid rows (up to ROWS)
            if row_idx >= cls.ROWS:
                break
            
            # Split by pipe and process each cell
            cells = line.split('|')[1:-1]  # Remove first and last empty elements
            
            for col_idx, cell in enumerate(cells):
                if col_idx >= cls.COLS:
                    break
                
                cell = cell.strip()
                
                if not cell:
                    continue
                
                # Extract role (if present): [role::[[UnitName]]]
                role_pattern = r'\[(\w+)\s*::\s*\[\[([^\]|]+)\]\]\]'
                role_match = re.search(role_pattern, cell)
                
                if role_match:
                    role = role_match.group(1).lower()
                    unit_name = role_match.group(2).strip()
                    board.add_unit(unit_name, row_idx, col_idx, role=role)
                else:
                    # Extract just unit without role: [[UnitName]]
                    unit_pattern = r'\[\[([^\]|]+)\]\]'
                    unit_match = re.search(unit_pattern, cell)
                    
                    if unit_match:
                        unit_name = unit_match.group(1).strip()
                        board.add_unit(unit_name, row_idx, col_idx, role=None)
            
            # Only increment row_idx after processing a valid data row
            row_idx += 1
        
        logger.debug(f"Parsed board with {len(board.units)} units")
        return board
