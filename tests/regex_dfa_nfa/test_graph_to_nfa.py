from os import path

from networkx import MultiDiGraph
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton

from project.cfpq.utils import create_labeled_two_cycles_graph
from project.graph.graph_worker import GraphWorker
from tests.utils import check_is_dot_files_the_same

CURR_PATH = path.dirname(path.realpath(__file__))


def test_convert_to_nfa_empty():
    gw = GraphWorker()
    assert NondeterministicFiniteAutomaton() == gw.convert_to_nfa()


def test_convert_to_nfa_with_labels():
    gw = GraphWorker(
        MultiDiGraph([(0, 1, {"label": "test_one"}), (1, 2, {"label": "test_two"})])
    )
    gw.convert_to_nfa().write_as_dot(path.join(CURR_PATH, "actual_nfa_with_labels.dot"))

    assert check_is_dot_files_the_same(
        CURR_PATH, "expected_nfa_with_labels.dot", "actual_nfa_with_labels.dot"
    )


def test_convert_to_nfa_without_labels():
    gw = GraphWorker(MultiDiGraph([(0, 1), (1, 2), (2, 3)]))
    gw.convert_to_nfa().write_as_dot(
        path.join(CURR_PATH, "actual_nfa_without_labels.dot")
    )

    assert check_is_dot_files_the_same(
        CURR_PATH, "expected_nfa_without_labels.dot", "actual_nfa_without_labels.dot"
    )


def test_convert_to_nfa_with_graph_start_nodes():
    graph = MultiDiGraph([(0, 1), (1, 2), (2, 3)])
    graph.add_node(1, is_start=True)
    graph.add_node(2, is_start=True)

    gw = GraphWorker(graph)
    gw.convert_to_nfa().write_as_dot(path.join(CURR_PATH, "actual_nfa_start_nodes.dot"))

    assert check_is_dot_files_the_same(
        CURR_PATH, "expected_nfa_start_nodes.dot", "actual_nfa_start_nodes.dot"
    )


def test_convert_graph_to_nfa_with_graph_final_nodes():
    graph = MultiDiGraph([(0, 1), (1, 2), (2, 3)])
    graph.add_node(3, is_final=True)
    gw = GraphWorker(graph)
    gw.convert_to_nfa().write_as_dot(
        path.join(CURR_PATH, "actual_nfa_with_graph_final_nodes.dot")
    )

    assert check_is_dot_files_the_same(
        CURR_PATH,
        "expected_nfa_with_graph_final_nodes.dot",
        "actual_nfa_with_graph_final_nodes.dot",
    )


def test_convert_graph_to_nfa_with_graph_start_final_nodes():
    graph = MultiDiGraph([(1, 0), (1, 2), (2, 3)])
    graph.add_node(3, is_final=True)
    graph.add_node(1, is_start=True)
    gw = GraphWorker(graph)
    gw.convert_to_nfa().write_as_dot(
        path.join(CURR_PATH, "actual_nfa_with_graph_start_final_nodes.dot")
    )

    assert check_is_dot_files_the_same(
        CURR_PATH,
        "expected_nfa_with_graph_start_final_nodes.dot",
        "actual_nfa_with_graph_start_final_nodes.dot",
    )


def test_convert_graph_to_nfa_with_start_nodes():
    gw = GraphWorker(MultiDiGraph([(0, 1), (1, 2), (2, 3)]))
    gw.convert_to_nfa(start={0}).write_as_dot(
        path.join(CURR_PATH, "actual_nfa_with_start_nodes.dot")
    )

    assert check_is_dot_files_the_same(
        CURR_PATH,
        "expected_nfa_with_start_nodes.dot",
        "actual_nfa_with_start_nodes.dot",
    )


def test_convert_graph_to_nfa_with_final_nodes():
    gw = GraphWorker(MultiDiGraph([(0, 1), (1, 2), (2, 3)]))
    gw.convert_to_nfa(final={0}).write_as_dot(
        path.join(CURR_PATH, "actual_nfa_with_final_nodes.dot")
    )

    assert check_is_dot_files_the_same(
        CURR_PATH,
        "expected_nfa_with_final_nodes.dot",
        "actual_nfa_with_final_nodes.dot",
    )


def test_convert_graph_to_nfa_with_final_start_nodes():
    gw = GraphWorker(MultiDiGraph([(1, 0), (1, 2)]))
    gw.convert_to_nfa(final={0}, start={1}).write_as_dot(
        path.join(CURR_PATH, "actual_nfa_with_final_start_nodes.dot")
    )

    assert check_is_dot_files_the_same(
        CURR_PATH,
        "expected_nfa_with_final_start_nodes.dot",
        "actual_nfa_with_final_start_nodes.dot",
    )


def test_convert_two_cycled_graph_to_nfa():
    gw = GraphWorker(
        create_labeled_two_cycles_graph(
            2,
            "0",
            2,
            "1",
        )
    )
    gw.convert_to_nfa(final={0}).write_as_dot(
        path.join(CURR_PATH, "actual_two_cycled_graph_to_nfa.dot")
    )

    assert check_is_dot_files_the_same(
        CURR_PATH,
        "expected_two_cycled_graph_to_nfa.dot",
        "actual_two_cycled_graph_to_nfa.dot",
    )
