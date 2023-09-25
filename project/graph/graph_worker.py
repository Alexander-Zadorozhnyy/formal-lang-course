from cfpq_data import graph_from_csv, download
from networkx import MultiDiGraph
from networkx.drawing.nx_pydot import to_pydot
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton as NonDA


class GraphWorker:
    def __init__(self, graph: MultiDiGraph = MultiDiGraph()):
        self.__graph = graph

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
                view = self.__graph.nodes.data(data=node_type, default=False)
                nodes = (
                    set(self.__graph.nodes)
                    if not any(is_start for _, is_start in view)
                    else {}
                )

            for node in nodes:
                self.__graph.nodes[node][node_type] = True

        return NonDA.from_networkx(self.__graph).remove_epsilon_transitions()

    def save_as_dot_file(self, path: str) -> bool:
        return to_pydot(self.__graph).write(path)
