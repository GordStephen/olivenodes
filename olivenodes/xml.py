import xml.etree.ElementTree as ET
from uuid import uuid4
from random import random

from .nodes import AbstractNode, ClipNode

OLIVE_VERSION = "211228"

class XMLOutput():

    def __init__(self):

        self.root = ET.Element("olive")
        ET.SubElement(self.root, "version").text = OLIVE_VERSION

        self.project = ET.SubElement(self.root, "project")
        ET.SubElement(self.project, "uuid").text = randuuid()

        self.nodes = ET.SubElement(self.project, "nodes")
        self.positions = ET.SubElement(self.project, "positions")
        self.properties = ET.SubElement(self.project, "properties")

        self.layout = ET.SubElement(self.project, "layout")
        ET.SubElement(self.layout, "folders")
        ET.SubElement(self.layout, "timeline")
        ET.SubElement(self.layout, "state")

        self.tree = ET.ElementTree(self.root)

    def add_clipnode(self, clipnode):

        self.positions_context = ET.SubElement(self.positions, "context")
        self.positions_context.set("ptr", clipnode.ptr)
        self.add_node(clipnode)

    def add_node(self, node):

        xmlnode = ET.SubElement(self.nodes, "node")
        xmlnode.set("id", node.id)

        ET.SubElement(xmlnode, "ptr").text = node.ptr
        ET.SubElement(xmlnode, "uuid").text = randuuid()
        ET.SubElement(xmlnode, "label").text = node.label
        ET.SubElement(xmlnode, "color").text = "-1"

        ET.SubElement(xmlnode, "links")
        connections = ET.SubElement(xmlnode, "connections")
        hints = ET.SubElement(xmlnode, "hints")
        ET.SubElement(xmlnode, "custom")

        is_clip = isinstance(node, ClipNode)

        if is_clip:

            props_node = ET.SubElement(self.properties, "node")
            props_node.set("ptr", node.ptr)
            ET.SubElement(props_node, "in").text = "0/1"
            ET.SubElement(props_node, "track").text = "v:0"
            add_cliphint(hints)

        for (param, val) in node.params.items():

            param_name = param + "_in"

            if isinstance(val, AbstractNode):
                add_input(xmlnode, param_name, is_clip, None)
                add_connection(connections, param_name, val.ptr)

            elif isinstance(val, dict):
                dicts = split_tracks(val)
                add_input(xmlnode, param_name, is_clip, *dicts)

            elif isinstance(val, tuple):
                add_input(xmlnode, param_name, is_clip, *val)

            else:
                add_input(xmlnode, param_name, is_clip, val)

        if node.graph.clipnode:
            add_position(self.positions_context, node.ptr)

        else:
            add_position(self.properties, node.ptr)

    def to_string(self):
        return ET.tostring(self.root, encoding="unicode")



def add_input(node, id, is_clip, *tracks):

    is_keyframes = isinstance(tracks[0], dict)

    input = ET.SubElement(node, "input")
    input.set("id", id)

    primary = ET.SubElement(input, "primary")

    if not is_clip:
        keyframing = ET.SubElement(primary, "keyframing")
        keyframing.text = "1" if is_keyframes else "0"

    standard = ET.SubElement(primary, "standard")
    keyframes = ET.SubElement(primary, "keyframes")

    for track in tracks:

        keyframes_track = ET.SubElement(keyframes, "track")
        standard_track = ET.SubElement(standard, "track")

        if is_keyframes:
            add_keyframes(keyframes_track, id, track)
            standard_track.text = "0"

        elif track:
            standard_track.text = str(track)

    ET.SubElement(input, "subelements").set("count", "0")

    return input

def add_keyframes(keyframes, id, track):

    for (t, val) in track.items():

        key = ET.SubElement(keyframes, "key")

        key.set("input", id)
        key.set("time", t)

        # TODO: Beziers
        key.set("type", "0")
        key.set("inhandlex", "0")
        key.set("inhandley", "0")
        key.set("outhandlex", "0")
        key.set("outhandley", "0")

        key.text = str(val)

def add_connection(connections, input, output):

    connection = ET.SubElement(connections, "connection")
    connection.set("input", input)
    connection.set("element", "-1")
    ET.SubElement(connection, "output").text = output

def add_position(context, ptr):

    node = ET.SubElement(context, "node")
    node.set("ptr", ptr)

    # TODO: Something neater...
    ET.SubElement(node, "x").text = str(2*random()-1)
    ET.SubElement(node, "y").text = str(2*random()-1)
    ET.SubElement(node, "expanded").text = "0"

def add_cliphint(hints):

    hint = ET.SubElement(hints, "hint")
    hint.set("input", "buffer_in")
    hint.set("element", "-1")

    types = ET.SubElement(hint, "types")
    ET.SubElement(types, "type").text = "10"
    ET.SubElement(types, "type").text = "11"

    ET.SubElement(hint, "index").text = "-1"
    ET.SubElement(hint, "tag")

def randuuid():
    return "{" + str(uuid4()) + "}"

def split_tracks(d):

    dicts = tuple({} for _ in next(iter(d.values())))

    for (t, tracks) in d.items():
        for (i, track) in enumerate(tracks):
            dicts[i][t] = track

    return dicts
