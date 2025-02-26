import pytest

from redis.commands.graph import edge, node, path, subgraph


@pytest.mark.redismod
def test_init():

    with pytest.raises(AssertionError):
        edge.Edge(None, None, None)
        edge.Edge(node.Node(), None, None)
        edge.Edge(None, None, node.Node())

    assert isinstance(
        edge.Edge(node.Node(node_id=1), None, node.Node(node_id=2)), edge.Edge
    )


@pytest.mark.redismod
def test_nodes():
    nodes = edge.Edge(node.Node(node_id=1), None, node.Node(node_id=2)).nodes()
    assert nodes[0].id == 1
    assert nodes[1].id == 2
    nodes = edge.Edge(node.Node(node_id=2), None, node.Node(node_id=1)).nodes()
    assert nodes[0].id == 2
    assert nodes[1].id == 1


@pytest.mark.redismod
def test_edges():
    this_edge = edge.Edge(node.Node(node_id=1), None, node.Node(node_id=2))
    edges = this_edge.edges()
    assert len(edges) == 1
    assert edges[0] == this_edge


@pytest.mark.redismod
def test_to_string():
    props_result = edge.Edge(
        node.Node(), None, node.Node(), properties={"a": "a", "b": 10}
    ).to_string()
    assert props_result == '{a:"a",b:10}'

    no_props_result = edge.Edge(
        node.Node(), None, node.Node(), properties={}
    ).to_string()
    assert no_props_result == ""


@pytest.mark.redismod
def test_stringify():
    john = node.Node(
        alias="a",
        label="person",
        properties={"name": "John Doe", "age": 33, "someArray": [1, 2, 3]},
    )
    japan = node.Node(alias="b", label="country", properties={"name": "Japan"})
    edge_with_relation = edge.Edge(
        john, "visited", japan, properties={"purpose": "pleasure"}
    )
    assert (
        '(a:person{age:33,name:"John Doe",someArray:[1, 2, 3]})'
        '-[:visited{purpose:"pleasure"}]->'
        '(b:country{name:"Japan"})' == str(edge_with_relation)
    )

    edge_no_relation_no_props = edge.Edge(japan, "", john)
    assert (
        '(b:country{name:"Japan"})'
        "-[]->"
        '(a:person{age:33,name:"John Doe",someArray:[1, 2, 3]})'
        == str(edge_no_relation_no_props)
    )

    edge_only_props = edge.Edge(john, "", japan, properties={"a": "b", "c": 3})
    assert (
        '(a:person{age:33,name:"John Doe",someArray:[1, 2, 3]})'
        '-[{a:"b",c:3}]->'
        '(b:country{name:"Japan"})' == str(edge_only_props)
    )


@pytest.mark.redismod
def test_comparision():
    node1 = node.Node(node_id=1)
    node2 = node.Node(node_id=2)
    node3 = node.Node(node_id=3)

    edge1 = edge.Edge(node1, None, node2)
    assert edge1 == edge.Edge(node1, None, node2)
    assert edge1 != edge.Edge(node1, "bla", node2)
    assert edge1 != edge.Edge(node1, None, node3)
    assert edge1 != edge.Edge(node3, None, node2)
    assert edge1 != edge.Edge(node2, None, node1)
    assert edge1 != edge.Edge(node1, None, node2, properties={"a": 10})


@pytest.mark.redismod
def test_hash():
    node1 = node.Node(node_id=1)
    node2 = node.Node(node_id=2)
    node3 = node.Node(node_id=3)

    edge1 = edge.Edge(node1, None, node2)
    assert hash(edge1) == hash(edge.Edge(node1, None, node2))
    assert hash(edge1) != hash(edge.Edge(node1, "bla", node2))
    assert hash(edge1) != hash(edge.Edge(node1, None, node3))
    assert hash(edge1) != hash(edge.Edge(node3, None, node2))
    assert hash(edge1) != hash(edge.Edge(node2, None, node1))
    assert hash(edge1) != hash(edge.Edge(node1, None, node2, properties={"a": 10}))


@pytest.mark.redismod
def test_union():
    node1 = node.Node(node_id=1)
    node2 = node.Node(node_id=2)
    edge1 = edge.Edge(node1, None, node2)
    subgraph1 = subgraph.Subgraph(nodes=[node1, node2], edges=[edge1])
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


@pytest.mark.redismod
def test_to_subgraph():
    node1 = node.Node(node_id=1)
    node2 = node.Node(node_id=2)
    edge1 = edge.Edge(node1, None, node2)
    assert isinstance(edge1.to_subgraph(), subgraph.Subgraph)
    assert edge1.to_subgraph() == subgraph.Subgraph(edges=[edge1])
