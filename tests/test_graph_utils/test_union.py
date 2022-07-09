import pytest

from redis.commands.graph import edge, node, path
from redis.commands.graph.subgraph import Subgraph


@pytest.mark.redismod
def test_union():
    # node1 | other object
    node1 = node.Node(node_id=1)
    node2 = node.Node(node_id=2)
    assert node1 | node2 == Subgraph(nodes=[node1, node2])
    edge1 = edge.Edge(node1, None, node2)
    assert node1 | edge1 == Subgraph(nodes=[node1, node2], edges=[edge1])
    subgraph = Subgraph(nodes=[node1, node2], edges=[edge1])
    assert node1 | subgraph == Subgraph(nodes=[node1, node2], edges=[edge1])
    assert node1 | path.Path([], []) == Subgraph(nodes=[node1])
    assert node1 | path.Path([node1, node2], [edge1]) == Subgraph(
        nodes=[node1, node2], edges=[edge1])
    # edge1 | other object
    assert edge1 | node1 == Subgraph(nodes=[node1, node2], edges=[edge1])
    node3 = node.Node(node_id=3)
    assert edge1 | node3 == Subgraph(nodes=[node1, node2, node3], edges=[edge1])
    edge2 = edge.Edge(node1, None, node3)
    assert edge1 | edge2 == Subgraph(nodes=[node1, node2, node3], edges=[edge1, edge2])
    assert edge1 | path.Path([], []) == Subgraph(edges=[edge1])
    assert edge1 | path.Path([node1, node2], [edge1]) == Subgraph(
        nodes=[node1, node2], edges=[edge1])
    assert edge2 | path.Path([node1, node2], [edge1]) == Subgraph(
        nodes=[node1, node2], edges=[edge1, edge2])
    assert edge2 | subgraph == Subgraph(nodes=[node1, node2], edges=[edge1, edge2])
    # path1 | other object
    assert path.Path([], []) | node1 == Subgraph(nodes=[node1])
    assert path.Path([], []) | edge1 == Subgraph(edges=[edge1])
    assert path.Path([], []) | path.Path([], []) == Subgraph()
    assert path.Path([], []) | subgraph == subgraph
    path1 = path.Path([node1, node2], [edge1])
    edge4 = edge.Edge(node2, None, node3)
    path2 = path.Path([node1, node2, node3], [edge1, edge4])
    assert path1 | node1 == Subgraph(nodes=[node1, node2], edges=[edge1])
    assert path1 | edge1 == Subgraph(nodes=[node1, node2], edges=[edge1])
    assert path1 | path1 == Subgraph(nodes=[node1, node2], edges=[edge1])
    assert path1 | path.Path([], []) == Subgraph(nodes=[node1, node2], edges=[edge1])
    assert path1 | subgraph == Subgraph(nodes=[node1, node2], edges=[edge1])
    # subgraph | other object
    assert subgraph | node1 == subgraph
    assert subgraph | node3 == Subgraph(nodes=[node1, node2, node3], edges=[edge1])
    assert subgraph | edge1 == subgraph
    assert subgraph | edge2 == Subgraph(
        nodes=[
            node1, node2, node3], edges=[
            edge1, edge2])
    assert subgraph | path.Path([], []) == subgraph
    assert subgraph | path1 == subgraph
    assert subgraph | path2 == Subgraph(
        nodes=[
            node1, node2, node3], edges=[
            edge1, edge4])
    assert subgraph | subgraph == subgraph
    assert subgraph | Subgraph(
        nodes=[
            node1, node2, node3], edges=[
            edge1, edge4]) == Subgraph(
                nodes=[
                    node1, node2, node3], edges=[
                        edge1, edge4])
