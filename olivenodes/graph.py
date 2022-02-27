from .nodes import AbstractNode

class Graph():

    def __init__(self):
        self.nodes = {}
        self.clipnode = None

    def checknode(self, node):
        if isinstance(node, AbstractNode) and node.graph is not self:
            throw(ValueError("Node must belong to this graph"))
