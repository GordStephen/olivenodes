from olivenodes import Graph, ClipNode, ShapeNode

graph = Graph()
square = ShapeNode(graph, "Red Square", size=(300, 300))
clip = ClipNode(graph, "Test", buffer=square, length="30/30")
