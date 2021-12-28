from posixpath import pathsep
from _parser import *
from graphviz import Digraph, Graph
import os


def get_tree(path):
    total = []
    dot = Graph(comment="syntax tree", format="png")
    dot.attr(size='20,20')
    _tree = Tree(path)
    _tree.print(_tree.getRoot().children[0])
    i = 0
    for item in tree:
        item.index = i
        dot.node(item.nodeToken.tokenType.lower()+str(i),
                 item.nodeToken.tokenValue.lower())
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

    os.environ["path"] += os.pathsep+'D:\compilers'+'\Lib\Graphviz\\bin'
    dot.render(directory='test-output', view=False)



_tree = Tree("test.txt")
root = _tree.getRoot()

