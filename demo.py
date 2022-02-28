from olivenodes import Graph, ClipNode, ShapeNode, SolidNode

graph = Graph()

# Create leaf nodes

solid = SolidNode(graph, color=(0.1, 0.1, 0.1))

square = ShapeNode(graph, "Red Square", size=(300, 300)) \
    .transform(pos=(-100, 0), rot=45)

circle = ShapeNode(graph, "Blue Circle", type=ShapeNode.Circle, size=(300, 300), color=(0, 0, 1)) \
    .transform(pos=(100, 0))

# Combine textures

root = solid | (square + circle)

# As-is, XML will represent loose nodes for pasting into the Node Editor
# Add a Clip node to paste as a single clip into the Timeline

clip = ClipNode(graph, "Test", buffer=root, length="30/30")

print(graph.to_xml())
