from ..helpers import quote_string
from .subgraph import Subgraph


class Node:
    """
    A node within the graph.
    """

    def __init__(self, node_id=None, alias=None, label=None, properties=None):
        """
        Create a new node.
        """
        self.id = node_id
        self.alias = alias
        if isinstance(label, list):
            label = [inner_label for inner_label in label if inner_label != ""]

        if (
            label is None
            or label == ""
            or (isinstance(label, list) and len(label) == 0)
        ):
            self.label = None
            self.labels = None
        elif isinstance(label, str):
            self.label = label
            self.labels = [label]
        elif isinstance(label, list) and all(
            [isinstance(inner_label, str) for inner_label in label]
        ):
            self.label = label[0]
            self.labels = label
        else:
            raise AssertionError(
                "label should be either None, " "string or a list of strings"
            )

        self.properties = properties or {}

    def nodes(self):
        return [self]

    def edges(self):
        return []

    def to_string(self):
        res = ""
        if self.properties:
            props = ",".join(
                key + ":" + str(quote_string(val))
                for key, val in sorted(self.properties.items())
            )
            res += "{" + props + "}"

        return res

    def __str__(self):
        res = "("
        if self.alias:
            res += self.alias
        if self.labels:
            res += ":" + ":".join(self.labels)
        if self.properties:
            props = ",".join(
                key + ":" + str(quote_string(val))
                for key, val in sorted(self.properties.items())
            )
            res += "{" + props + "}"
        res += ")"

        return res

    def __eq__(self, rhs):
        # Quick positive check, if both IDs are set.
        if self.id is not None and rhs.id is not None and self.id != rhs.id:
            return False

        # Label should match.
        if self.label != rhs.label:
            return False

        # Quick check for number of properties.
        if len(self.properties) != len(rhs.properties):
            return False

        # Compare properties.
        if self.properties != rhs.properties:
            return False

        return True

    def __hash__(self):
        if isinstance(self.id, int):
            return hash(str(self.id)) ^ hash(self.label) ^ hash(self.to_string())
        else:
            return hash(self.label) ^ hash(self.to_string())

    def __or__(self, rhs):
        return Subgraph(set(self.nodes()) | set(rhs.nodes()),
                        set(self.edges()) | set(rhs.edges()))

    def to_subgraph(self):
        return Subgraph(nodes=[self])
