from ..helpers import quote_string
from .node import Node
from .subgraph import Subgraph


class Edge:
    """
    An edge connecting two nodes.
    """

    def __init__(self, src_node, relation, dest_node, edge_id=None, properties=None):
        """
        Create a new edge.
        """
        if src_node is None or dest_node is None:
            # NOTE(bors-42): It makes sense to change AssertionError to
            #                ValueError here
            raise AssertionError("Both src_node & dest_node must be provided")

        self.id = edge_id
        self.relation = relation or ""
        self.properties = properties or {}
        self.src_node = src_node
        self.dest_node = dest_node

    def nodes(self):
        return [self.src_node, self.dest_node]

    def edges(self):
        return [self]

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
        # Source node.
        if isinstance(self.src_node, Node):
            res = str(self.src_node)
        else:
            res = "()"

        # Edge
        res += "-["
        if self.relation:
            res += ":" + self.relation
        if self.properties:
            props = ",".join(
                key + ":" + str(quote_string(val))
                for key, val in sorted(self.properties.items())
            )
            res += "{" + props + "}"
        res += "]->"

        # Dest node.
        if isinstance(self.dest_node, Node):
            res += str(self.dest_node)
        else:
            res += "()"

        return res

    def __eq__(self, rhs):
        # Quick positive check, if both IDs are set.
        if self.id is not None and rhs.id is not None and self.id == rhs.id:
            return True

        # Source and destination nodes should match.
        if self.src_node != rhs.src_node:
            return False

        if self.dest_node != rhs.dest_node:
            return False

        # Relation should match.
        if self.relation != rhs.relation:
            return False

        # Quick check for number of properties.
        if len(self.properties) != len(rhs.properties):
            return False

        # Compare properties.
        if self.properties != rhs.properties:
            return False

        return True

    def __hash__(self):
        value = hash(self.src_node) ^ hash(self.dest_node)
        value ^= hash(f'{hash(self.src_node)}{hash(self.dest_node)}')
        value ^= hash(self.relation)
        value ^= hash(self.to_string())
        if isinstance(self.id, int):
            return value ^ hash(str(self.id))
        else:
            return value

    def __or__(self, rhs):
        return Subgraph(set(self.nodes()) | set(rhs.nodes()),
                        set(self.edges()) | set(rhs.edges()))

    def to_subgraph(self):
        return Subgraph(edges=[self])
