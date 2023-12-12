import os
from pathlib import Path

from networkx.drawing.nx_pydot import read_dot

from project.cf_requests.matrix.matrix_alg import get_matrix_transitive_closure
from project.cf_requests.matrix.matrix_cfpq import cfpq

from tests.cf_request.cases_for_testing import (
    algorithms_test_cases,
    cfpq_test_cases,
)


CURR_PATH = os.path.dirname(os.path.realpath(__file__))


def test_matrix_algorithms():
    for (graph, cfg, expected_result) in algorithms_test_cases:
        cfg = Path(os.path.join(CURR_PATH, "../static", "cfg", cfg))

        if isinstance(graph, str):
            graph = read_dot(Path(os.path.join(CURR_PATH, "../static", "graph", graph)))

        assert get_matrix_transitive_closure(graph, cfg) == expected_result


def test_matrix_cfpq():
    for (graph, cfg, start, final, expected_result) in cfpq_test_cases:
        cfg = Path(os.path.join(CURR_PATH, "../static", "cfg", cfg))

        if isinstance(graph, str):
            graph = read_dot(Path(os.path.join(CURR_PATH, "../static", "graph", graph)))

        assert cfpq(graph, cfg, start, final) == expected_result
