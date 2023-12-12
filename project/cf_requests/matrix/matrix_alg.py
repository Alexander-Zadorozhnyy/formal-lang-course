from pathlib import Path
from typing import Union

import networkx as nx
from pyformlang.cfg import CFG
from scipy.sparse import dok_matrix

from project.cfg.cfg_func import convert_cfg_to_weak_cnf


def get_boolean_decomposition(graph: nx.MultiDiGraph, weak_cnf: CFG) -> dict:
    number_of_nodes = graph.number_of_nodes()

    e_prod = {p.head.value for p in weak_cnf.productions if not p.body}
    t_prod = {prod for prod in weak_cnf.productions if len(prod.body) == 1}

    boolean_decomposition = {
        v.value: dok_matrix((number_of_nodes, number_of_nodes), dtype=int)
        for v in weak_cnf.variables
    }

    valid_prod = {(v, h, v) for v in range(number_of_nodes) for h in e_prod} | {
        (int(u), prod.head.value, int(v))
        for u, v, label in graph.edges(data=True)
        for prod in t_prod
        if prod.body[0].value == label["label"]
    }

    for i, var, j in valid_prod:
        boolean_decomposition[var][i, j] = 1

    return boolean_decomposition


def get_matrix_transitive_closure(
    graph: nx.MultiDiGraph, cfg: Union[Path, CFG], start_variable: str = "S"
) -> set:
    def update_matrix(matrix, prod):
        matrix[prod.head.value] += (
            matrix[prod.body[0].value] @ matrix[prod.body[1].value]
        )
        return matrix

    weak_cnf = convert_cfg_to_weak_cnf(cfg, start_variable)
    v_prod = list({prod for prod in weak_cnf.productions if len(prod.body) == 2})

    boolean_decomposition = get_boolean_decomposition(graph, weak_cnf)

    if v_prod:
        prev = curr = None
        while prev is None or prev != curr:
            for prod in v_prod:
                prev = boolean_decomposition[prod.head.value].nnz
                boolean_decomposition = update_matrix(boolean_decomposition, prod)

            curr = boolean_decomposition[v_prod[-1].head.value].nnz

    return {
        (u, var, v)
        for var in weak_cnf.variables
        for u, v in zip(*boolean_decomposition[var].nonzero())
    }
