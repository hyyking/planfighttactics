"""
Minimal getting started example for pytft.

This is the simplest possible example to get you started:
  1. Load knowledge graph
  2. Rank compositions
  3. Analyze the best one
"""

from pathlib import Path
from pytft import TFTKnowledgeGraph


# Load knowledge graph from your Obsidian vault
kg = TFTKnowledgeGraph(root=Path(__file__).parent.parent.parent)
kg.load_all()

print(kg)

