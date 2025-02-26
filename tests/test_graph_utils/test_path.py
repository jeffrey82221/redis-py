import pytest

from redis.commands.graph import edge, node, path, subgraph


@pytest.mark.redismod
def test_init():
    with pytest.raises(TypeError):
        path.Path(None, None)
        path.Path([], None)
        path.Path(None, [])

    assert isinstance(path.Path([], []), path.Path)


@pytest.mark.redismod
def test_new_empty_path():
    new_empty_path = path.Path.new_empty_path()
    assert isinstance(new_empty_path, path.Path)
    assert new_empty_path._nodes == []
    assert new_empty_path._edges == []


@pytest.mark.redismod
def test_wrong_flows():
    node_1 = node.Node(node_id=1)
    node_2 = node.Node(node_id=2)
    node_3 = node.Node(node_id=3)

    edge_1 = edge.Edge(node_1, None, node_2)
    edge_2 = edge.Edge(node_1, None, node_3)

    p = path.Path.new_empty_path()
    with pytest.raises(AssertionError):
        p.add_edge(edge_1)

    p.add_node(node_1)
    with pytest.raises(AssertionError):
        p.add_node(node_2)

    p.add_edge(edge_1)
    with pytest.raises(AssertionError):
        p.add_edge(edge_2)


@pytest.mark.redismod
def test_nodes_and_edges():
    node_1 = node.Node(node_id=1)
    node_2 = node.Node(node_id=2)
    edge_1 = edge.Edge(node_1, None, node_2)

    p = path.Path.new_empty_path()
    assert p.nodes() == []
    p.add_node(node_1)
    assert [] == p.edges()
    assert 0 == p.edge_count()
    assert [node_1] == p.nodes()
    assert node_1 == p.get_node(0)
    assert node_1 == p.first_node()
    assert node_1 == p.last_node()
    assert 1 == p.nodes_count()
    p.add_edge(edge_1)
    assert [edge_1] == p.edges()
    assert 1 == p.edge_count()
    assert edge_1 == p.get_relationship(0)
    p.add_node(node_2)
    assert [node_1, node_2] == p.nodes()
    assert node_1 == p.first_node()
    assert node_2 == p.last_node()
    assert 2 == p.nodes_count()


@pytest.mark.redismod
def test_compare():
    node_1 = node.Node(node_id=1)
    node_2 = node.Node(node_id=2)
    edge_1 = edge.Edge(node_1, None, node_2)

    assert path.Path.new_empty_path() == path.Path.new_empty_path()
    assert path.Path(nodes=[node_1, node_2], edges=[edge_1]) == path.Path(
        nodes=[node_1, node_2], edges=[edge_1]
    )
    assert path.Path(nodes=[node_1], edges=[]) != path.Path(nodes=[], edges=[])
    assert path.Path(nodes=[node_1], edges=[]) != path.Path(nodes=[], edges=[])
    assert path.Path(nodes=[node_1], edges=[]) != path.Path(nodes=[node_2], edges=[])
    assert path.Path(nodes=[node_1], edges=[edge_1]) != path.Path(
        nodes=[node_1], edges=[]
    )
    assert path.Path(nodes=[node_1], edges=[edge_1]) != path.Path(
        nodes=[node_2], edges=[edge_1]
    )


@pytest.mark.redismod
def test_union():
    node1 = node.Node(node_id=1)
    node2 = node.Node(node_id=2)
    edge1 = edge.Edge(node1, None, node2)
    subgraph1 = subgraph.Subgraph(nodes=[node1, node2], edges=[edge1])
    # path1 | other object
    assert path.Path([], []) | node1 == subgraph.Subgraph(nodes=[node1])
    assert path.Path([], []) | edge1 == subgraph.Subgraph(edges=[edge1])
    assert path.Path([], []) | path.Path([], []) == subgraph.Subgraph()
    assert path.Path([], []) | subgraph1 == subgraph1
    path1 = path.Path([node1, node2], [edge1])
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


@pytest.mark.redismod
def test_to_subgraph():
    node1 = node.Node(node_id=1)
    node2 = node.Node(node_id=2)
    edge1 = edge.Edge(node1, None, node2)
    this_path = path.Path(nodes=[node1, node2], edges=[edge1])
    assert isinstance(this_path.to_subgraph(), subgraph.Subgraph)
    assert this_path.to_subgraph() == subgraph.Subgraph(
        nodes=[node1, node2], edges=[edge1])
