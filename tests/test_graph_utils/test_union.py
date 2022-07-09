import pytest

from redis.commands.graph import edge, node, path, subgraph


@pytest.mark.redismod
def test_union():
    # node1 | other object
    node1 = node.Node(node_id=1)
    node2 = node.Node(node_id=2)
    assert node1 | node2 == subgraph.Subgraph(nodes=[node1, node2])
    edge1 = edge.Edge(node1, None, node2)
    assert node1 | edge1 == subgraph.Subgraph(nodes=[node1, node2], edges=[edge1])
    subgraph1 = subgraph.Subgraph(nodes=[node1, node2], edges=[edge1])
    assert node1 | subgraph1 == subgraph.Subgraph(nodes=[node1, node2], edges=[edge1])
    assert node1 | path.Path([], []) == subgraph.Subgraph(nodes=[node1])
    assert node1 | path.Path([node1, node2], [edge1]) == subgraph.Subgraph(
        nodes=[node1, node2], edges=[edge1])
    # edge1 | other object
    assert edge1 | node1 == subgraph.Subgraph(nodes=[node1, node2], edges=[edge1])
    node3 = node.Node(node_id=3)
    assert edge1 | node3 == subgraph.Subgraph(
        nodes=[node1, node2, node3], edges=[edge1])
    edge2 = edge.Edge(node1, None, node3)
    assert edge1 | edge2 == subgraph.Subgraph(
        nodes=[
            node1, node2, node3], edges=[
            edge1, edge2])
    assert edge1 | path.Path([], []) == subgraph.Subgraph(edges=[edge1])
    assert edge1 | path.Path([node1, node2], [edge1]) == subgraph.Subgraph(
        nodes=[node1, node2], edges=[edge1])
    assert edge2 | path.Path([node1, node2], [edge1]) == subgraph.Subgraph(
        nodes=[node1, node2], edges=[edge1, edge2])
    assert edge2 | subgraph1 == subgraph.Subgraph(
        nodes=[node1, node2], edges=[edge1, edge2])
    # path1 | other object
    assert path.Path([], []) | node1 == subgraph.Subgraph(nodes=[node1])
    assert path.Path([], []) | edge1 == subgraph.Subgraph(edges=[edge1])
    assert path.Path([], []) | path.Path([], []) == subgraph.Subgraph()
    assert path.Path([], []) | subgraph1 == subgraph1
    path1 = path.Path([node1, node2], [edge1])
    edge4 = edge.Edge(node2, None, node3)
    path2 = path.Path([node1, node2, node3], [edge1, edge4])
    assert path1 | node1 == subgraph.Subgraph(nodes=[node1, node2], edges=[edge1])
    assert path1 | edge1 == subgraph.Subgraph(nodes=[node1, node2], edges=[edge1])
    assert path1 | path1 == subgraph.Subgraph(nodes=[node1, node2], edges=[edge1])
    assert path1 | path.Path(
        [],
        []) == subgraph.Subgraph(
        nodes=[
            node1,
            node2],
        edges=[edge1])
    assert path1 | subgraph1 == subgraph.Subgraph(nodes=[node1, node2], edges=[edge1])
    # subgraph1 | other object
    assert subgraph1 | node1 == subgraph1
    assert subgraph1 | node3 == subgraph.Subgraph(
        nodes=[node1, node2, node3], edges=[edge1])
    assert subgraph1 | edge1 == subgraph1
    assert subgraph1 | edge2 == subgraph.Subgraph(
        nodes=[
            node1, node2, node3], edges=[
            edge1, edge2])
    assert subgraph1 | path.Path([], []) == subgraph1
    assert subgraph1 | path1 == subgraph1
    assert subgraph1 | path2 == subgraph.Subgraph(
        nodes=[
            node1, node2, node3], edges=[
            edge1, edge4])
    assert subgraph1 | subgraph1 == subgraph1
    assert subgraph1 | subgraph.Subgraph(
        nodes=[
            node1, node2, node3], edges=[
            edge1, edge4]) == subgraph.Subgraph(
                nodes=[
                    node1, node2, node3], edges=[
                        edge1, edge4])
