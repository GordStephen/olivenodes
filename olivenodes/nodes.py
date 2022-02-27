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
