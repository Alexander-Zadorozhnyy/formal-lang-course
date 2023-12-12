from pathlib import Path
from typing import Union

import networkx as nx
from pyformlang.cfg import CFG

from project.cf_requests.tensor.tensor_alg import get_tensor_transitive_closure


def cfpq(
    graph: nx.MultiDiGraph,
    request: Union[Path, CFG],
    start_nodes: set = None,
    final_nodes: set = None,
    start_variable: str = "S",
):
    if not start_nodes:
        start_nodes = set(map(int, filter(lambda x: x != "\\n", graph.nodes)))

    if not final_nodes:
        final_nodes = set(map(int, filter(lambda x: x != "\\n", graph.nodes)))

    return {
        sn: set(
            final
            for start, var, final in list(
                filter(
                    lambda x: x[0] == sn,
                    get_tensor_transitive_closure(graph, request, start_variable),
                )
            )
            if final in final_nodes
        )
        for sn in start_nodes
    }
