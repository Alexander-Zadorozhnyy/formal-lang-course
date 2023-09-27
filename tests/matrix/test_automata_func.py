from networkx import MultiDiGraph

from project.graph.graph_worker import GraphWorker
from project.matrix.matrix_func import create_labels
from project.regex_and_automata.automata_func import get_connected_nodes
from tests.matrix.cases_for_testing import (
    rpq_cases_without_cycles,
    automata_get_connected_nodes_test_cases,
)


def test_get_connected_nodes():
    for test_index, test_case in enumerate(rpq_cases_without_cycles):
        gw = GraphWorker(MultiDiGraph(test_case["graph"]))
        graph_nfa = gw.convert_to_nfa(*test_case["regular_request"][1:])

        assert test_case["expected"] == get_connected_nodes(
            graph_nfa,
            automata_get_connected_nodes_test_cases[test_index][0],
            automata_get_connected_nodes_test_cases[test_index][1],
            create_labels(*automata_get_connected_nodes_test_cases[test_index][2]),
        )
