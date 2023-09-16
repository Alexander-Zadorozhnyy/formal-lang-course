from networkx import MultiDiGraph
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from project.graph.graph_worker import GraphWorker


def test_convert_to_nfa_empty():
    gw = GraphWorker()
    assert NondeterministicFiniteAutomaton() == gw.convert_to_nfa()


def test_convert_to_nfa_with_labels():
    expected = NondeterministicFiniteAutomaton()
    for s in range(0, 3):
        expected.add_start_state(s), expected.add_final_state(s)
    expected.add_transitions([(0, "test_one", 1), (1, "test_two", 2)])

    gw = GraphWorker(
        MultiDiGraph([(0, 1, {"label": "test_one"}), (1, 2, {"label": "test_two"})])
    )

    assert expected == gw.convert_to_nfa()


def test_convert_to_nfa_without_labels():
    expected = NondeterministicFiniteAutomaton()
    for s in range(1, 4):
        expected.add_start_state(s), expected.add_final_state(s)

    gw = GraphWorker(MultiDiGraph([(0, 1), (1, 2), (2, 3)]))

    assert expected == gw.convert_to_nfa()


def test_convert_to_nfa_with_graph_start_nodes():
    expected = NondeterministicFiniteAutomaton()
    expected.add_start_state(1)
    expected.add_start_state(2)

    for s in range(0, 4):
        expected.add_final_state(s)

    graph = MultiDiGraph([(0, 1), (1, 2), (2, 3)])
    graph.add_node(1, is_start=True)
    graph.add_node(2, is_start=True)

    gw = GraphWorker(graph)

    assert expected == gw.convert_to_nfa()


def test_convert_graph_to_nfa_with_graph_final_nodes():
    expected = NondeterministicFiniteAutomaton()
    expected.add_final_state(3)
    for s in range(0, 4):
        expected.add_start_state(s)

    graph = MultiDiGraph([(0, 1), (1, 2), (2, 3)])
    graph.add_node(3, is_final=True)
    gw = GraphWorker(graph)

    assert expected == gw.convert_to_nfa()


def test_convert_graph_to_nfa_with_start_nodes():
    expected = NondeterministicFiniteAutomaton()
    expected.add_start_state(0)
    for s in range(0, 4):
        expected.add_final_state(s)

    gw = GraphWorker(MultiDiGraph([(0, 1), (1, 2), (2, 3)]))

    assert expected == gw.convert_to_nfa(start={0})


def test_convert_graph_to_nfa_with_final_nodes():
    expected = NondeterministicFiniteAutomaton()
    expected.add_final_state(0)
    for s in range(0, 4):
        expected.add_start_state(s)

    gw = GraphWorker(MultiDiGraph([(0, 1), (1, 2), (2, 3)]))

    assert expected == gw.convert_to_nfa(final={0})
