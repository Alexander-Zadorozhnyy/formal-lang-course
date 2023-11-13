from pathlib import Path
from typing import Union

import networkx as nx
from pyformlang.cfg import CFG

from project.cfg.cfg_func import convert_cfg_to_weak_cnf


def helling_helper(prev, next, v_prod, n_elem, cond):
    state = set()

    for m_elem in prev:
        f_u, f_h, f_v, s_u, s_h, s_v = cond(*n_elem, *m_elem)
        if f_u == f_v:
            for prod in v_prod:
                if (
                    prod.body[0].value == f_h
                    and prod.body[1].value == s_h
                    and (s_u, prod.head.value, s_v) not in prev
                ):
                    state.add((s_u, prod.head.value, s_v))

    prev.update(state)
    next.update(state)


def hellings(graph: nx.MultiDiGraph, cfg: Union[Path, CFG], start_variable: str):
    weak_cnf = convert_cfg_to_weak_cnf(cfg, start_variable)

    e_prod = [p.head.value for p in weak_cnf.productions if not p.body]
    t_prod = {prod for prod in weak_cnf.productions if len(prod.body) == 1}
    v_prod = {prod for prod in weak_cnf.productions if len(prod.body) == 2}

    prev = {(v, h, v) for v in range(graph.number_of_nodes()) for h in e_prod} | {
        (u, prod.head.value, v)
        for u, v, label in graph.edges(data=True)
        for prod in t_prod
        if prod.body[0].value == label["label"]
    }

    next = prev.copy()
    while next:
        n_elem = next.pop()
        helling_helper(
            prev,
            next,
            v_prod,
            n_elem,
            lambda f_u, f_h, f_v, s_u, s_h, s_v: (s_v, s_h, f_u, s_u, f_h, f_v),
        )
        helling_helper(
            prev,
            next,
            v_prod,
            n_elem,
            lambda f_u, f_h, f_v, s_u, s_h, s_v: (s_u, f_h, f_v, f_u, s_h, s_v),
        )

    return prev


def cfpq(
    graph: nx.MultiDiGraph,
    cfg: Union[Path, CFG],
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
    start_variable: str = "S",
):
    if not start_nodes:
        start_nodes = graph.nodes

    if not final_nodes:
        final_nodes = graph.nodes

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
