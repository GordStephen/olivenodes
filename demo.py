from olivenodes import Graph, ClipNode, ShapeNode

graph = Graph()

square = ShapeNode(graph, "Red Square", size=(300, 300))
circle = ShapeNode(graph, "Blue Circle", type=ShapeNode.Circle, size=(300, 300), color=(0, 0, 1))

merge = square | circle

# As-is, XML will represent loose nodes for pasting into the Node Editor
# Add a Clip node to paste as a single clip into the Timeline

clip = ClipNode(graph, "Test", buffer=merge, length="30/30")

print(graph.to_xml())
