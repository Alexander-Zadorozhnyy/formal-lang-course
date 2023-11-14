import os
from pathlib import Path

from networkx.drawing.nx_pydot import read_dot

from project.cf_requests.hellings.hellings_alg import hellings
from project.cf_requests.hellings.hellings_cfpq import cfpq

from tests.hellings.cases_for_testing import (
    hellings_algorithms_test_cases,
    hellings_cfpq_test_cases,
)


def test_hellings_algorithms():
    for (graph, cfg, expected_result) in hellings_algorithms_test_cases:
        cfg = Path(os.path.join(os.getcwd(), "static", "cfg", cfg))

        if isinstance(graph, str):
            graph = read_dot(Path(os.path.join(os.getcwd(), "static", "graph", graph)))

        assert hellings(graph, cfg) == expected_result


def test_hellings_cfpq():
    for (graph, cfg, start, final, expected_result) in hellings_cfpq_test_cases:
        cfg = Path(os.path.join(os.getcwd(), "static", "cfg", cfg))

        if isinstance(graph, str):
            graph = read_dot(Path(os.path.join(os.getcwd(), "static", "graph", graph)))

        assert cfpq(graph, cfg, start, final) == expected_result
