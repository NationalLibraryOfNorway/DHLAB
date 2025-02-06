import requests
import unittest.mock
from dhlab.api.nb_ngram_api import make_word_graph
import json
from typing import Literal


def _links_to_edge_view(nodes: list[str], links: list[dict[str, int]]) -> dict[tuple[str, str], dict[Literal["weight"], int]]:
    """Converts nodes and links as returned by the API to a dictionary with the same structure as nx.OutEdgeView

    Example
    -------
    >>> _links_to_edge_view(["a", "b", "c"], links=[{"source": 0, "target": 2, "value": 3}])
    {('a', 'c'): {'weight': 3}}
    """
    return {
        (nodes[link["source"]]["name"], nodes[link["target"]]["name"]): {"weight": link["value"]}
        for link in links
    }

def test_deserialises_di_graph() -> None:
    """The word graph is deserialised correctly
    """
    data = {
        "nodes": [
            {"name": "askeladden", "size": 4},
            {"name": "de", "size": 33},
            {"name": "Rødrev", "size": 24},
            {"name": "prinsessen", "size": 33},
        ],
        "links": [
            {"source": 0, "target": 1, "value": 66},
            {"source": 2, "target": 0, "value": 9},
            {"source": 3, "target": 0, "value": 8},
        ],
    }

    session = unittest.mock.MagicMock(spec=requests.Session)
    session.get.return_value.status_code = 200
    session.get.return_value.text = json.dumps(data)

    word_graph = make_word_graph(words="mocked,data", session=session)
    assert len(word_graph.nodes) == len(data["nodes"])
    assert set(word_graph.nodes) == {node["name"] for node in data["nodes"]}
    assert dict(word_graph.edges) == _links_to_edge_view(data["nodes"], data["links"])
