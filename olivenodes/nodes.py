from random import randrange

MAX_PTR = 99999999

class AbstractNode():

    def __init__(self, graph, label=None, **params):

        self.graph = graph
        self.label = label
        self.params = self.defaultparams | params

        self._set_ptr()
        self.graph.nodes[self.ptr] = self

    def _set_ptr(self):

        ptr = str(randrange(MAX_PTR))

        while ptr in self.graph.nodes.keys():
            ptr = str(randrange(MAX_PTR))

        self.ptr = ptr

    def __getitem__(self, param):
        return self.params[param]

    def __setitem__(self, param, value):
        self.params[param] = value

    def __or__(self, other):
        self.graph.checknode(other)
        return MergeNode(self.graph, base=self, blend=other)

    def __add__(self, other):
        self.graph.checknode(other)
        return MathNode(self.graph, method=MathNode.Add, param_a=self, param_b=other)

    def __sub__(self, other):
        self.graph.checknode(other)
        return MathNode(self.graph, method=MathNode.Subtract, param_a=self, param_b=other)

    def __mul__(self, other):
        self.graph.checknode(other)
        return MathNode(self.graph, method=MathNode.Multiply, param_a=self, param_b=other)

    def __truediv__(self, other):
        self.graph.checknode(other)
        return MathNode(self.graph, method=MathNode.Divide, param_a=self, param_b=other)

    def __pow__(self, other):
        self.graph.checknode(other)
        return MathNode(self.graph, method=MathNode.Power, param_a=self, param_b=other)

    def transform(self, **params):
        return TransformNode(self.graph, tex=self, **params)


class ClipNode(AbstractNode):

    id = "org.olivevideoeditor.Olive.clip"

    defaultparams = {
        "buffer": None,
        "length": None,
        "enabled": "true",
        "media_in": "0/1",
        "speed": 1,
        "reverse": "false",
        "maintain_audio_pitch": "false"
    }

    def __init__(self, graph, label=None, **params):

        if graph.clipnode:
            throw(ValueError("Graphs can only have one Clip node"))

        super().__init__(graph, label, **params)
        graph.clipnode = self


class MathNode(AbstractNode):

    id = "org.olivevideoeditor.Olive.math"

    # Methods
    Add = 0
    Subtract = 1
    Multiply = 2
    Divide = 3
    Power = 4

    defaultparams = {
        "method": Add,
        "param_a": 0,
        "param_b": 0
    }


class MergeNode(AbstractNode):

    id = "org.olivevideoeditor.Olive.merge"

    defaultparams = {
        "base": None,
        "blend": None
    }


class ShapeNode(AbstractNode):

    id = "org.olivevideoeditor.Olive.shape"

    # Types
    Rectangle = 0
    Circle = 1

    defaultparams = {
        "type": Rectangle,
        "pos": (0, 0),
        "size": (100, 100),
        "fill": (1.0, 0.0, 0.0)
    }


class TransformNode(AbstractNode):

    id = "org.olivevideoeditor.Olive.transform"

    # Autoscales
    None_ = 0
    Fit = 1
    Fill = 2
    Stretch = 3

    # Interpolations
    NearestNeighbor = 0
    Bilinear = 1
    MipMappedBilinear = 2

    defaultparams = {
            "tex": None,
            "pos": (0, 0),
            "rot": 0,
            "scale": (1, 1),
            "uniform_scale": True,
            "anchor": (0, 0),
            "autoscale": None_,
            "interpolation": MipMappedBilinear
    }
