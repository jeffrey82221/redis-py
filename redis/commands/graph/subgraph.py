from itertools import chain


class Subgraph:
    """
    A subgraph containing a set of nodes and edges.
    """

    def __init__(self, nodes=None, edges=None):
        """
        Create a new subgraph.
        """
        if nodes:
            if not (isinstance(nodes, list) or isinstance(
                    nodes, set) or isinstance(nodes, frozenset)):
                raise TypeError("nodes must be list, set, or frozenset")

        if edges:
            if not (isinstance(edges, list) or isinstance(
                    edges, set) or isinstance(edges, frozenset)):
                raise TypeError("edges must be list, set, or frozenset")

        _nodes = frozenset(nodes or [])
        _edges = frozenset(edges or [])
        _nodes |= frozenset(chain.from_iterable(e.nodes() for e in _edges))
        self._nodes = self.__clean_nodes(_nodes)
        self._edges = self.__clean_edges(self._nodes, _edges)

    def __clean_nodes(self, nodes):
        result = []
        for node in nodes:
            if not isinstance(node, int):
                result.append(node)
        return frozenset(result)

    def __clean_edges(self, nodes, edges):
        node_map = self.__build_node_map(nodes)
        result = []
        for edge in edges:
            if isinstance(edge.src_node, int) and edge.src_node in node_map:
                edge.src_node = node_map[edge.src_node]
            if isinstance(edge.dest_node, int) and edge.dest_node in node_map:
                edge.dest_node = node_map[edge.dest_node]
            result.append(edge)
        return frozenset(result)

    def __build_node_map(self, nodes):
        result = dict()
        for node in nodes:
            if node.id is not None:
                result[node.id] = node
        return result

    def nodes(self):
        return self._nodes

    def edges(self):
        return self._edges

    def nodes_count(self):
        return len(self._nodes)

    def edges_count(self):
        return len(self._edges)

    def labels(self):
        """ Return the set of all node labels in this subgraph.
        """
        return frozenset(chain.from_iterable(
            node.labels for node in self._nodes if node.labels is not None))

    def relations(self):
        """ Return the set of all edge relations in this subgraph.
        """
        return frozenset(e.relation for e in self._edges if e.relation is not None)

    def __str__(self):
        res = ''
        if self._nodes:
            res += '\nNodes:\n'
            nodes_res = []
            for n in self._nodes:
                nodes_res.append(str(n))
            res += ",".join(nodes_res)
        if self._edges:
            res += '\nEdges:\n'
            edges_res = []
            for e in self._edges:
                edges_res.append(str(e))
            res += ",".join(edges_res)
        return res

    def __eq__(self, rhs):
        return set(self.nodes()) == set(rhs.nodes()) and set(
            self.edges()) == set(rhs.edges())

    def __or__(self, rhs):
        return Subgraph(set(self.nodes()) | set(rhs.nodes()),
                        set(self.edges()) | set(rhs.edges()))
