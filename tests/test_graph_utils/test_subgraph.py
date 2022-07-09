import pytest

from redis.commands.graph import edge, node, path
from redis.commands.graph.subgraph import Subgraph


@pytest.mark.redismod
def test_init():
    with pytest.raises(TypeError):
        Subgraph(nodes=1, edges=None)
    with pytest.raises(TypeError):
        Subgraph(node=dict(), edges=None)
    with pytest.raises(TypeError):
        Subgraph(node=None, edges=1)
    with pytest.raises(TypeError):
        Subgraph(node=None, edges=dict())

    assert isinstance(Subgraph(), Subgraph)


@pytest.mark.redismod
def test_nodes():
    node1 = node.Node(node_id=1)
    subgraph = Subgraph(nodes=[node1])
    assert list(subgraph.nodes())[0] == node1
    node2 = node.Node(node_id=2)
    subgraph = Subgraph(nodes=[node1, node2])
    assert subgraph.nodes() == frozenset([node1, node2])


@pytest.mark.redismod
def test_edges():
    assert len(Subgraph().edges()) == 0
    node1 = node.Node(node_id=1)
    node2 = node.Node(node_id=2)
    edge1 = edge.Edge(node1, None, node2)
    assert Subgraph(edges=[edge1]).edges() == frozenset([edge1])
    assert Subgraph(edges=[edge1, edge1]).edges() == frozenset([edge1])
    edge2 = edge.Edge(node1, None, node1)
    assert Subgraph(edges=[edge1, edge2]).edges() == frozenset([edge1, edge2])


@pytest.mark.redismod
def test_nodes_count():
    assert Subgraph().nodes_count() == 0
    assert Subgraph(nodes=[node.Node(node_id=1)]).nodes_count() == 1
    assert Subgraph(
        nodes=[
            node.Node(
                node_id=1), node.Node(
                node_id=2)]).nodes_count() == 2
    assert Subgraph(
        nodes=[
            node.Node(
                node_id=1), node.Node(
                node_id=1)]).nodes_count() == 1


@pytest.mark.redismod
def test_edges_count():
    assert Subgraph().edges_count() == 0
    node1 = node.Node(node_id=1)
    node2 = node.Node(node_id=2)
    edge1 = edge.Edge(node1, None, node2)
    edge2 = edge.Edge(node1, None, node1)
    assert Subgraph(edges=[edge1]).edges_count() == 1
    assert Subgraph(edges=[edge1, edge2]).edges_count() == 2
    assert Subgraph(edges=[edge1, edge1]).edges_count() == 1


@pytest.mark.redismod
def test_labels():
    assert Subgraph().labels() == frozenset()
    assert Subgraph(nodes=[node.Node(node_id=1)]).labels() == frozenset()
    assert Subgraph(
        nodes=[
            node.Node(
                node_id=1,
                label='User')]).labels() == frozenset(
        ['User'])
    assert Subgraph(nodes=[
        node.Node(node_id=1, label='User'),
        node.Node(node_id=1, label='User')
    ]).labels() == frozenset(['User'])
    assert Subgraph(nodes=[
        node.Node(node_id=1, label='User'),
        node.Node(node_id=1, label='Object')
    ]).labels() == frozenset(['User', 'Object'])
    assert Subgraph(nodes=[
        node.Node(node_id=1, label='User'),
        node.Node(node_id=1)
    ]).labels() == frozenset(['User'])
    assert Subgraph(nodes=[
        node.Node(node_id=1, label=['User', 'Object']),
        node.Node(node_id=1)
    ]).labels() == frozenset(['User', 'Object'])


@pytest.mark.redismod
def test_relations():
    assert Subgraph().relations() == frozenset()
    node1 = node.Node(node_id=1)
    node2 = node.Node(node_id=2)
    edge1 = edge.Edge(node1, None, node2)
    edge2 = edge.Edge(node1, 'Love', node2)
    assert edge2.relation == 'Love'
    assert edge1 != edge2
    assert Subgraph(edges=[edge1]).relations() == frozenset([''])
    assert Subgraph(edges=[edge1, edge1]).relations() == frozenset([''])
    assert Subgraph(edges=[edge2]).relations() == frozenset(['Love'])
    assert Subgraph(edges=[edge2, edge2]).relations() == frozenset(['Love'])
    assert Subgraph(edges=[edge1, edge2]).relations() == frozenset(['', 'Love'])


@pytest.mark.redismod
def test_compare():
    node1 = node.Node(node_id=1)
    node2 = node.Node(node_id=2)
    edge1 = edge.Edge(node1, None, node2)
    assert Subgraph() == Subgraph()
    assert Subgraph(
        nodes=[
            node1,
            node2],
        edges=[edge1]) == Subgraph(
            nodes=[
                node1,
                node2],
        edges=[edge1])
    assert Subgraph(nodes=[node1], edges=[]) != Subgraph(nodes=[], edges=[])
    assert Subgraph(nodes=[node1], edges=[]) != Subgraph(nodes=[node2], edges=[])
    assert Subgraph(nodes=[node1], edges=[edge1]) != Subgraph(nodes=[node1], edges=[])
    assert Subgraph(
        nodes=[node1],
        edges=[edge1]) == Subgraph(
        nodes=[node2],
        edges=[edge1])
