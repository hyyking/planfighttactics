"""
TFT knowledge graph and composition analysis library.

This module provides tools for analyzing Teamfight Tactics compositions using
data from an Obsidian vault as a knowledge graph.

Core Components:
  - Unit: Champion model with traits, cost, recommended items
  - Item: Equipment model with categories and aliases
  - Board: Board representation with unit positions (7x4 grid)
  - Comp: Team composition with board layout and role annotations
  - TFTKnowledgeGraph: Loads and manages all data from Obsidian vault
  - TFTGraph: NetworkX-based analysis with synergy scoring and recommendations

Quick Start:
    >>> from pytft import TFTKnowledgeGraph, TFTGraph
    >>> from pathlib import Path
    >>> 
    >>> # Load knowledge graph from vault
    >>> kg = TFTKnowledgeGraph(root=Path("c:/Users/Leo/Desktop/TFT"))
    >>> kg.load_all()  # Loads units, items, and comps
    >>> 
    >>> # Access board layout
    >>> comp = kg.comps["Piltover Vertical"]
    >>> comp.board.visualize()  # Show board with unit positions
"""

from pytft.models import Unit, Item, Comp, Board, TFTKnowledgeGraph

__all__ = [
    "Unit",
    "Item",
    "Comp",
    "Board",
    "TFTKnowledgeGraph",
]

__version__ = "0.1.0"