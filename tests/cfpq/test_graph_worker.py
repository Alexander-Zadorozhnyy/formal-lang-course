from os import path

from networkx import MultiDiGraph

from project.graph.graph_worker import GraphWorker
from tests.utils import check_is_dot_files_the_same

CURR_PATH = path.dirname(path.realpath(__file__))


def test_empty_graph():
    graph = MultiDiGraph()
    expected = {"num_of_nodes": 0, "num_of_edges": 0, "set_of_labels": set()}

    gw = GraphWorker(graph)

    assert expected == gw.get_graph_info()


def test_load_graph_by_name():
    gw = GraphWorker()
    gw.load_graph_by_name("bzip")
    actual = gw.get_graph_info()

    assert 632 == actual["num_of_nodes"]
    assert 556 == actual["num_of_edges"]
    assert {"a", "d"} == actual["set_of_labels"]


def test_save_as_dot_file():
    graph = MultiDiGraph()
    for i in [5, 10, 15]:
        graph.add_node(i)
    graph.add_edge(5, 15, label="a")
    graph.add_edge(15, 10, label="b")
    graph.add_edge(10, 5, label="c")

    actual_path = path.join(CURR_PATH, "actual_graph_gw.dot")

    gw = GraphWorker(graph)
    gw.save_as_dot_file(actual_path)

    assert check_is_dot_files_the_same(
        CURR_PATH, "expected_graph_gw.dot", "actual_graph_gw.dot"
    )
