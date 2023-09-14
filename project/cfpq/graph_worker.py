from cfpq_data import graph_from_csv, download
from networkx import MultiDiGraph
from networkx.drawing.nx_pydot import to_pydot
from networkx.drawing.nx_agraph import write_dot


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

    def save_as_dot_file(self, path: str) -> bool:
        return write_dot(self.__graph, path)
