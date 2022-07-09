import pytest

from redis.commands.graph import node
from redis.commands.graph.subgraph import Subgraph


@pytest.fixture
def fixture():
    no_args = node.Node()
    no_props = node.Node(node_id=1, alias="alias", label="l")
    props_only = node.Node(properties={"a": "a", "b": 10})
    no_label = node.Node(node_id=1, alias="alias", properties={"a": "a"})
    multi_label = node.Node(node_id=1, alias="alias", label=["l", "ll"])
    return no_args, no_props, props_only, no_label, multi_label


@pytest.mark.redismod
def test_nodes():
    this_node = node.Node(node_id=1, alias="alias", label="l")
    assert len(this_node.nodes()) == 1
    assert this_node == this_node.nodes()[0]


@pytest.mark.redismod
def test_edges():
    this_node = node.Node(node_id=1, alias="alias", label="l")
    assert len(this_node.edges()) == 0


@pytest.mark.redismod
def test_to_string(fixture):
    no_args, no_props, props_only, no_label, multi_label = fixture
    assert no_args.to_string() == ""
    assert no_props.to_string() == ""
    assert props_only.to_string() == '{a:"a",b:10}'
    assert no_label.to_string() == '{a:"a"}'
    assert multi_label.to_string() == ""


@pytest.mark.redismod
def test_stringify(fixture):
    no_args, no_props, props_only, no_label, multi_label = fixture
    assert str(no_args) == "()"
    assert str(no_props) == "(alias:l)"
    assert str(props_only) == '({a:"a",b:10})'
    assert str(no_label) == '(alias{a:"a"})'
    assert str(multi_label) == "(alias:l:ll)"


@pytest.mark.redismod
def test_comparision():
    assert node.Node() == node.Node()
    assert node.Node(node_id=1) == node.Node(node_id=1)
    assert node.Node(node_id=1) != node.Node(node_id=2)
    assert node.Node(node_id=1, alias="a") == node.Node(node_id=1, alias="b")
    assert node.Node(node_id=1, alias="a") == node.Node(node_id=1, alias="a")
    assert node.Node(node_id=1, label="a") == node.Node(node_id=1, label="a")
    assert node.Node(node_id=1, label="a") != node.Node(node_id=1, label="b")
    assert node.Node(node_id=1, alias="a", label="l") == node.Node(
        node_id=1, alias="a", label="l"
    )
    assert node.Node(alias="a", label="l") != node.Node(alias="a", label="l1")
    assert node.Node(properties={"a": 10}) == node.Node(properties={"a": 10})
    assert node.Node() != node.Node(properties={"a": 10})


@pytest.mark.redismod
def test_hash():
    assert hash(node.Node()) == hash(node.Node())
    assert hash(node.Node(node_id=1)) == hash(node.Node(node_id=1))
    assert hash(node.Node(node_id=1)) != hash(node.Node(node_id=2))
    assert hash(
        node.Node(
            node_id=1,
            alias="a")) == hash(
        node.Node(
            node_id=1,
            alias="b"))
    assert hash(
        node.Node(
            node_id=1,
            alias="a")) == hash(
        node.Node(
            node_id=1,
            alias="a"))
    assert hash(
        node.Node(
            node_id=1,
            label="a")) == hash(
        node.Node(
            node_id=1,
            label="a"))
    assert hash(
        node.Node(
            node_id=1,
            label="a")) != hash(
        node.Node(
            node_id=1,
            label="b"))
    assert hash(node.Node(node_id=1, alias="a", label="l")) == hash(node.Node(
        node_id=1, alias="a", label="l"
    ))
    assert hash(
        node.Node(
            alias="a",
            label="l")) != hash(
        node.Node(
            alias="a",
            label="l1"))
    assert hash(
        node.Node(
            properties={
                "a": 10})) == hash(
        node.Node(
            properties={
                "a": 10}))
    assert hash(node.Node()) != hash(node.Node(properties={"a": 10}))
