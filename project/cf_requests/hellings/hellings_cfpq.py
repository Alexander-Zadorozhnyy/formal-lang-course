from pathlib import Path
from typing import Union

import networkx as nx
from pyformlang.cfg import CFG

from project.cf_requests.hellings.hellings_alg import hellings


def cfpq(
    graph: nx.MultiDiGraph,
    cfg: Union[Path, CFG],
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
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
                filter(lambda x: x[0] == sn, hellings(graph, cfg, start_variable))
            )
            if final in final_nodes
        )
        for sn in start_nodes
    }
