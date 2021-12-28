from posixpath import pathsep
from _parser import *
from graphviz import Graph
from pathlib import Path
import os
import sys, random, string


def get_tree(path):
    dot = Graph(comment="syntax tree", format="png")
    dot.attr(size='20,20')
    _tree = Tree(path)
    _tree.print(_tree.getRoot().children[0])
    tree = _tree.tree
    i = 0
    for item in tree:
        item.index = i
        if item.nodeToken.tokenType.lower() in ['read', 'write', 'if', 'assign', 'repeat']:
            dot.node(item.nodeToken.tokenType.lower()+str(i),
                    item.string_operation, shape="rect")
        else:
            dot.node(item.nodeToken.tokenType.lower()+str(i),
                item.string_operation)
        i += 1
    for item in tree:
        for _item in tree:
            if _item in item.children:
                dot.edge(item.nodeToken.tokenType.lower()+str(item.index),
                         _item.nodeToken.tokenType.lower()+str(_item.index))
            if _item == item.right_node:
                dot.edge(item.nodeToken.tokenType.lower()+str(item.index),
                         _item.nodeToken.tokenType.lower()+str(_item.index), constraint="false")
    for item in tree:
        with dot.subgraph() as s:
            s.attr(rank='same')
            i = 0
            for _item in tree:
                if item.right_node == _item:
                    s.node(item.nodeToken.tokenType.lower()+str(item.index))
                    s.node(_item.nodeToken.tokenType.lower()+str(_item.index))
    pay = 'output/graph.gv'
    dot.render(pay, view=True)

