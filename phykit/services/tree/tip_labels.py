import logging
import sys

from Bio import Phylo

from .base import Tree

class TipLabels(Tree):
    def __init__(self, args) -> None:
        super().__init__(**self.process_args(args))

    def run(self):
        tree = self.read_tree_file()
        
        try:
            for leaf in tree.get_terminals():
                print(leaf.name)
        except BrokenPipeError:
            pass
        sys.stderr.close()
    
    def process_args(self, args):
        return dict(tree_file_path=args.tree)