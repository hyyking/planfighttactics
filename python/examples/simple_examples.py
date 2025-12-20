"""
Simple examples showing common pytft usage patterns.
"""

from pathlib import Path
from pytft import TFTKnowledgeGraph


# =============================================================================
# Example 1: Load and explore data
# =============================================================================

def example_load_data():
    """Load knowledge graph and print some basic info."""
    print("Example 1: Loading Data")
    print("-" * 40)
    
    kg = TFTKnowledgeGraph(root=Path(__file__).parent.parent.parent)
    kg.load_all()
    
    # Access units
    print(f"\n✓ Loaded {len(kg.units)} units")
    for unit_name, unit in list(kg.units.items())[:3]:
        print(f"  - {unit.name} (Cost {unit.cost}): {unit.traits}")
    
    # Access items
    print(f"\n✓ Loaded {len(kg.items)} items")
    for item_name, item in list(kg.items.items())[:3]:
        print(f"  - {item.name} ({item.category})")
    
    # Access compositions
    print(f"\n✓ Loaded {len(kg.comps)} compositions")
    for comp_name, comp in list(kg.comps.items())[:3]:
        print(f"  - {comp.name}: {comp.units}")



def example_item_recommendations():
    """Suggest items for a specific unit."""
    print("\n\nExample 2: Item Recommendations")
    print("-" * 40)
    
    kg = TFTKnowledgeGraph(root=Path(__file__).parent.parent.parent)
    kg.load_all()
    
    if not kg.units:
        print("No units loaded")
        return
    
    # Pick a unit
    unit_name = list(kg.units.keys())[0]
    unit = kg.units[unit_name]
    
    print(f"\nUnit: {unit_name}")
    print(f"  Cost: {unit.cost}")
    print(f"  Traits: {unit.traits}")
    print(f"  Recommended Items: {unit.recommended_items}")

if __name__ == "__main__":
    example_load_data()
    example_item_recommendations()


