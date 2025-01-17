import os
from pathlib import Path

from networkx.drawing.nx_pydot import read_dot

from project.cf_requests.hellings.hellings_alg import hellings
from project.cf_requests.hellings.hellings_cfpq import cfpq

from tests.cf_request.cases_for_testing import (
    algorithms_test_cases,
    cfpq_test_cases,
)


CURR_PATH = os.path.dirname(os.path.realpath(__file__))


def test_hellings_algorithms():
    for (graph, cfg, expected_result) in algorithms_test_cases:
        cfg = Path(os.path.join(CURR_PATH, "../static", "cfg", cfg))

        if isinstance(graph, str):
            graph = read_dot(Path(os.path.join(CURR_PATH, "../static", "graph", graph)))

        assert hellings(graph, cfg) == expected_result


def test_hellings_cfpq():
    for (graph, cfg, start, final, expected_result) in cfpq_test_cases:
        cfg = Path(os.path.join(CURR_PATH, "../static", "cfg", cfg))

        if isinstance(graph, str):
            graph = read_dot(Path(os.path.join(CURR_PATH, "../static", "graph", graph)))

        assert cfpq(graph, cfg, start, final) == expected_result
