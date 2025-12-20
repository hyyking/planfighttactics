"""
Example: Working with Board layouts and unit positions.
Demonstrates the new Board class for accessing unit positions on the 7x4 TFT board.
"""

from pathlib import Path
from pytft import TFTKnowledgeGraph, Board


def main():
    """Show board layouts and unit positioning."""
    
    # Load knowledge graph
    kg = TFTKnowledgeGraph(root=Path(__file__).parent.parent.parent)
    kg.load_all()
    
    if not kg.comps:
        print("No compositions loaded")
        return
    
    # Get a composition with a board
    comp = list(kg.comps.values())[2]
    
    if not comp.board:
        print(f"{comp.name} has no board layout")
        return
    
    print("=" * 80)
    print(f"BOARD LAYOUT: {comp.name}")
    print("=" * 80)
    
    # Show board visualization
    print("\nBoard Visualization:")
    print("(* = carry, = = tank, + = support)\n")
    print(comp.board.visualize())
    
    # Show unit information
    print("\n" + "-" * 80)
    print("UNIT POSITIONS")
    print("-" * 80)
    
    for unit in comp.board.units:
        role_str = f" ({unit.role})" if unit.role else ""
        print(f"  {unit.name}{role_str:12} at row {unit.row}, col {unit.col}")
    
    # Show units by role
    print("\n" + "-" * 80)
    print("UNITS BY ROLE")
    print("-" * 80)
    
    carries = comp.board.get_units_by_role("carry")
    tanks = comp.board.get_units_by_role("tank")
    supports = comp.board.get_units_by_role("support")
    
    print(f"\nCarries ({len(carries)}):")
    for unit in carries:
        print(f"  • {unit.name} at [{unit.row},{unit.col}]")
    
    print(f"\nTanks ({len(tanks)}):")
    for unit in tanks:
        print(f"  • {unit.name} at [{unit.row},{unit.col}]")
    
    print(f"\nSupports ({len(supports)}):")
    for unit in supports:
        print(f"  • {unit.name} at [{unit.row},{unit.col}]")
    
    # Show units in specific rows/cols
    print("\n" + "-" * 80)
    print("UNITS BY POSITION")
    print("-" * 80)
    
    print("\nFront Line (Row 0):")
    for unit in comp.board.get_units_in_row(0):
        print(f"  • {unit.name} at col {unit.col}")
    
    print("\nBack Line (Row 3):")
    for unit in comp.board.get_units_in_row(3):
        print(f"  • {unit.name} at col {unit.col}")
    
    print("\nLeft Side (Col 0):")
    for unit in comp.board.get_units_in_col(0):
        print(f"  • {unit.name} at row {unit.row}")
    
    print("\nRight Side (Col 6):")
    for unit in comp.board.get_units_in_col(6):
        print(f"  • {unit.name} at row {unit.row}")
    
    # Show board info
    print("\n" + "-" * 80)
    print("BOARD INFO")
    print("-" * 80)
    print(f"\nBoard dimensions: {Board.COLS} columns × {Board.ROWS} rows")
    print(f"Total units: {len(comp.board.units)}")
    print(f"Board: {comp.board}")


if __name__ == "__main__":
    main()
