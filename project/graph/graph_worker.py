from cfpq_data import graph_from_csv, download
from networkx import MultiDiGraph
from networkx.drawing.nx_pydot import to_pydot
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton as NonDA
from pyformlang.regular_expression import Regex

from project.matrix.matrix_func import get_matrix_transitive_closure
from project.regex_and_automata.automata_func import (
    intersect_automatas,
    get_connected_nodes,
)
from project.regex_and_automata.regex_func import convert_regex_to_minimal_dfa


class GraphWorker:
    def __init__(self, graph: MultiDiGraph = MultiDiGraph()):
        self.__graph = graph

    def __get_nodes_by_type(self, node_type: str) -> set:
        view = self.__graph.nodes.data(data=node_type, default=False)
        return (
            set(self.__graph.nodes)
            if not any(is_valid for _, is_valid in view)
            else set()
        )

    def load_graph_by_name(self, name: str) -> None:
        self.__graph = graph_from_csv(path=download(name))

    def update_graph(self, graph: MultiDiGraph) -> None:
        self.__graph = graph

    def get_graph_info(self) -> dict:
        return {
            "num_of_nodes": self.__graph.number_of_nodes(),
            "num_of_edges": self.__graph.number_of_edges(),
            "set_of_labels": {
                label for _, _, label in self.__graph.edges.data("label")
            },
        }

    def convert_to_nfa(self, start: set[int] = None, final: set[int] = None) -> NonDA:
        node_types = {"is_start": start, "is_final": final}

        for node_type, nodes in node_types.items():
            if not nodes:
                nodes = self.__get_nodes_by_type(node_type)

            for node in nodes:
                self.__graph.nodes[node][node_type] = True

        return NonDA.from_networkx(self.__graph).remove_epsilon_transitions()

    def make_regular_request(
            self, request: Regex, start: set[int] = None, final: set[int] = None
    ):
        dfa_request = convert_regex_to_minimal_dfa(request)
        graph_nfa = self.convert_to_nfa(start, final)

        matrix_of_intersected_automatas = intersect_automatas(dfa_request, graph_nfa)

        transitive_closure = get_matrix_transitive_closure(
            matrix_of_intersected_automatas
        )
        return get_connected_nodes(
            automata=graph_nfa,
            start_states=matrix_of_intersected_automatas.start_states,
            final_states=matrix_of_intersected_automatas.final_states,
            closure=transitive_closure,
        )

    def save_as_dot_file(self, path: str) -> bool:
        return to_pydot(self.__graph).write(path)
