from .nodes import AbstractNode
from .xml import XMLOutput

class Graph():

    def __init__(self):
        self.nodes = {}
        self.clipnode = None

    def checknode(self, node):
        if isinstance(node, AbstractNode) and node.graph is not self:
            throw(ValueError("Node must belong to this graph"))

    def to_xml(self):

        xml = XMLOutput()

        if self.clipnode:
            xml.add_clipnode(self.clipnode)

        for node in self.nodes.values():
            if node is not self.clipnode:
                xml.add_node(node)

        return xml.to_string()
