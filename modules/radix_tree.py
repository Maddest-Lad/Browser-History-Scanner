from __future__ import annotations
from dataclasses import dataclass
from typing import List

@dataclass
class Node:
    value: str
    parent: Node
    children: List[Node]
    

class UrlRadixTree:
    """A radix tree implementation designed for handling FQDNs and their URL paths
    ex: www.example.com/path/file -> www, example, com, path, file
    """

    def __init__(self):
        self.root = Node("", None, [])

    def insert(self, value: str):
        """Inserts a value into the radix tree"""
        pass

    def search(self, value: str) -> bool:
        """Searches for a value in the radix tree"""
        pass

    def delete(self, value: str):
        """Deletes a value from the radix tree"""
        pass

    def __repr__(self):
        return f"RadixTree({self.root})"


if __name__ == "__main__":
    tree = UrlRadixTree()
    tree.insert("www.example.com")
    tree.insert("www.example.com/path/file")