import pytest

from redis.commands.graph import edge, node, path, subgraph


@pytest.mark.redismod
def test_init():
    with pytest.raises(TypeError):
        subgraph.Subgraph(nodes=1, edges=None)
    with pytest.raises(TypeError):
        subgraph.Subgraph(node=dict(), edges=None)
    with pytest.raises(TypeError):
        subgraph.Subgraph(node=None, edges=1)
    with pytest.raises(TypeError):
        subgraph.Subgraph(node=None, edges=dict())

    assert isinstance(subgraph.Subgraph(), subgraph.Subgraph)


@pytest.mark.redismod
def test_nodes():
    node1 = node.Node(node_id=1)
    subgraph1 = subgraph.Subgraph(nodes=[node1])
    assert list(subgraph1.nodes())[0] == node1
    node2 = node.Node(node_id=2)
    subgraph1 = subgraph.Subgraph(nodes=[node1, node2])
    assert subgraph1.nodes() == frozenset([node1, node2])


@pytest.mark.redismod
def test_edges():
    assert len(subgraph.Subgraph().edges()) == 0
    node1 = node.Node(node_id=1)
    node2 = node.Node(node_id=2)
    edge1 = edge.Edge(node1, None, node2)
    assert subgraph.Subgraph(edges=[edge1]).edges() == frozenset([edge1])
    assert subgraph.Subgraph(edges=[edge1, edge1]).edges() == frozenset([edge1])
    edge2 = edge.Edge(node1, None, node1)
    assert subgraph.Subgraph(edges=[edge1, edge2]).edges() == frozenset([edge1, edge2])


@pytest.mark.redismod
def test_nodes_count():
    assert subgraph.Subgraph().nodes_count() == 0
    assert subgraph.Subgraph(nodes=[node.Node(node_id=1)]).nodes_count() == 1
    assert subgraph.Subgraph(
        nodes=[
            node.Node(
                node_id=1), node.Node(
                node_id=2)]).nodes_count() == 2
    assert subgraph.Subgraph(
        nodes=[
            node.Node(
                node_id=1), node.Node(
                node_id=1)]).nodes_count() == 1


@pytest.mark.redismod
def test_edges_count():
    assert subgraph.Subgraph().edges_count() == 0
    node1 = node.Node(node_id=1)
    node2 = node.Node(node_id=2)
    edge1 = edge.Edge(node1, None, node2)
    edge2 = edge.Edge(node1, None, node1)
    assert subgraph.Subgraph(edges=[edge1]).edges_count() == 1
    assert subgraph.Subgraph(edges=[edge1, edge2]).edges_count() == 2
    assert subgraph.Subgraph(edges=[edge1, edge1]).edges_count() == 1


@pytest.mark.redismod
def test_labels():
    assert subgraph.Subgraph().labels() == frozenset()
    assert subgraph.Subgraph(nodes=[node.Node(node_id=1)]).labels() == frozenset()
    assert subgraph.Subgraph(
        nodes=[
            node.Node(
                node_id=1,
                label='User')]).labels() == frozenset(
        ['User'])
    assert subgraph.Subgraph(nodes=[
        node.Node(node_id=1, label='User'),
        node.Node(node_id=1, label='User')
    ]).labels() == frozenset(['User'])
    assert subgraph.Subgraph(nodes=[
        node.Node(node_id=1, label='User'),
        node.Node(node_id=1, label='Object')
    ]).labels() == frozenset(['User', 'Object'])
    assert subgraph.Subgraph(nodes=[
        node.Node(node_id=1, label='User'),
        node.Node(node_id=1)
    ]).labels() == frozenset(['User'])
    assert subgraph.Subgraph(nodes=[
        node.Node(node_id=1, label=['User', 'Object']),
        node.Node(node_id=1)
    ]).labels() == frozenset(['User', 'Object'])


@pytest.mark.redismod
def test_relations():
    assert subgraph.Subgraph().relations() == frozenset()
    node1 = node.Node(node_id=1)
    node2 = node.Node(node_id=2)
    edge1 = edge.Edge(node1, None, node2)
    edge2 = edge.Edge(node1, 'Love', node2)
    assert edge2.relation == 'Love'
    assert edge1 != edge2
    assert subgraph.Subgraph(edges=[edge1]).relations() == frozenset([''])
    assert subgraph.Subgraph(edges=[edge1, edge1]).relations() == frozenset([''])
    assert subgraph.Subgraph(edges=[edge2]).relations() == frozenset(['Love'])
    assert subgraph.Subgraph(edges=[edge2, edge2]).relations() == frozenset(['Love'])
    assert subgraph.Subgraph(
        edges=[edge1, edge2]).relations() == frozenset(['', 'Love'])


@pytest.mark.redismod
def test_compare():
    node1 = node.Node(node_id=1)
    node2 = node.Node(node_id=2)
    edge1 = edge.Edge(node1, None, node2)
    assert subgraph.Subgraph() == subgraph.Subgraph()
    assert subgraph.Subgraph(
        nodes=[
            node1,
            node2],
        edges=[edge1]) == subgraph.Subgraph(
            nodes=[
                node1,
                node2],
        edges=[edge1])
    assert subgraph.Subgraph(
        nodes=[node1],
        edges=[]) != subgraph.Subgraph(
        nodes=[],
        edges=[])
    assert subgraph.Subgraph(
        nodes=[node1],
        edges=[]) != subgraph.Subgraph(
        nodes=[node2],
        edges=[])
    assert subgraph.Subgraph(
        nodes=[node1],
        edges=[edge1]) != subgraph.Subgraph(
        nodes=[node1],
        edges=[])
    assert subgraph.Subgraph(
        nodes=[node1],
        edges=[edge1]) == subgraph.Subgraph(
        nodes=[node2],
        edges=[edge1])


@pytest.mark.redismod
def test_union():
    node1 = node.Node(node_id=1)
    node2 = node.Node(node_id=2)
    node3 = node.Node(node_id=3)
    edge1 = edge.Edge(node1, None, node2)
    edge2 = edge.Edge(node1, None, node3)
    path1 = path.Path([node1, node2], [edge1])
    edge4 = edge.Edge(node2, None, node3)
    path2 = path.Path([node1, node2, node3], [edge1, edge4])
    subgraph1 = subgraph.Subgraph(nodes=[node1, node2], edges=[edge1])
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
