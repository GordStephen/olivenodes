from olivenodes import Graph, ClipNode, ShapeNode

graph = Graph()
square = ShapeNode(graph, "Red Square", size=(300, 300))

# As-is, XML will represent loose nodes for pasting into the Node Editor
# Add a Clip node to paste as a single clip into the Timeline

clip = ClipNode(graph, "Test", buffer=square, length="30/30")

print(graph.to_xml())
