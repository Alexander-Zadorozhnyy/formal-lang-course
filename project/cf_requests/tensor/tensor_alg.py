from pathlib import Path
from typing import Union, Type

import networkx as nx
from pyformlang.cfg import CFG, Variable
from scipy.sparse import eye, csr_matrix, lil_matrix, dok_matrix, csc_matrix

from project.cfg.cfg_func import read_context_free_grammar
from project.ecfg.ecfg import ECFG
from project.graph.graph_worker import GraphWorker
from project.matrix.matrix_func import (
    convert_nfa_to_matrix,
    intersect_matrices,
    get_matrix_transitive_closure,
)
from project.recursive_state_machine.rsm import RSM


def get_tensor_transitive_closure(
    graph: nx.MultiDiGraph,
    cfg: Union[Path, CFG],
    start_variable: str = "S",
    typed_matrix: Union[
        Type[lil_matrix], Type[dok_matrix], Type[csr_matrix], Type[csc_matrix]
    ] = csr_matrix,
) -> set:
    nfa = GraphWorker(graph).convert_to_nfa()
    nfa_matrix = convert_nfa_to_matrix(nfa, typed_matrix)
    number_of_indexes = nfa_matrix.get_number_of_indexes()

    cfg = read_context_free_grammar(cfg, start_variable)
    ecfg = ECFG.convert_cfg_to_ecfg(cfg)
    rsm = RSM.convert_ecfg_to_rsm(ecfg, start_variable).minimize()
    rsm_matrix = rsm.get_binary_matrix(typed_matrix)

    diagonal = typed_matrix(eye(number_of_indexes, dtype=bool))
    for variable in cfg.get_nullable_symbols():
        nfa_matrix.labels[variable.value] += diagonal

    prev_size = 0
    while True:
        transitive_closure_intersects = list(
            zip(
                *get_matrix_transitive_closure(
                    intersect_matrices(rsm_matrix, nfa_matrix, csr_matrix)
                ).nonzero()
            )
        )

        curr_size = len(transitive_closure_intersects)

        if curr_size == prev_size:
            break

        prev_size = curr_size

        for i, j in transitive_closure_intersects:
            start_state, final_state = (
                rsm_matrix.get_state_by_index(i // number_of_indexes),
                rsm_matrix.get_state_by_index(j // number_of_indexes),
            )

            if not rsm_matrix.is_start(start_state) or not rsm_matrix.is_final(
                final_state
            ):
                continue

            value = start_state.value[0]

            graph_matrix = typed_matrix(
                ([True], ([i % number_of_indexes], [j % number_of_indexes])),
                shape=(number_of_indexes, number_of_indexes),
                dtype=bool,
            )

            if value in nfa_matrix.labels:
                nfa_matrix.labels[value] += graph_matrix
            else:
                nfa_matrix.labels[value] = graph_matrix.copy()

    return set(
        (
            int(nfa_matrix.get_state_by_index(i).value),
            variable.value,
            int(nfa_matrix.get_state_by_index(j).value),
        )
        for variable, matrix in nfa_matrix.labels.items()
        for i, j in zip(*matrix.nonzero())
        if isinstance(variable, Variable)
    )
