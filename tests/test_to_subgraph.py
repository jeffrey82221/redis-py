import pytest

from redis.commands.graph import Edge, Node, Path, Subgraph
import copy


@pytest.fixture
def client(modclient):
    modclient.flushdb()
    return modclient


@pytest.mark.redismod
def test_to_subgraph(client):
    try:
        graph = client.graph()

        john = Node(
            label="person",
            properties={
                "name": "John Doe",
                "age": 33,
                "gender": "male",
                "status": "single",
            },
        )
        japan = Node(label="country", properties={"name": "Japan"})
        edge = Edge(john, "visited", japan, properties={"purpose": "pleasure"})
        subgraph = Subgraph(nodes=[japan, john], edges=[edge])
        input_graph_str = str(subgraph)
        graph.add_node(john)
        graph.add_node(japan)
        graph.add_edge(edge)
        graph.commit()
        query = (
            'MATCH k=(p:person)-[v:visited {purpose:"pleasure"}]->(c:country) '
            "RETURN k"
        )
        result = graph.query(query)
        assert str(result.to_subgraph()) == input_graph_str
        query = (
            'MATCH (p:person)-[v:visited {purpose:"pleasure"}]->(c:country) '
            "RETURN p, v, c"
        )
        result = graph.query(query)
        assert str(result.to_subgraph()) == input_graph_str
    except BaseException as e:
        raise e
    finally:
        # All done, remove graph.
        graph.delete()
