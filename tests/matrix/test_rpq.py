from networkx import MultiDiGraph
from pyformlang.regular_expression import Regex

from project.cfpq.utils import create_labeled_two_cycles_graph
from project.graph.graph_worker import GraphWorker

from tests.matrix.cases_for_testing import (
    rpq_cases_without_cycles,
    rpq_cases_with_cycles,
)


def test_rpq_empty():
    gw = GraphWorker(MultiDiGraph())
    assert set() == gw.make_regular_request(Regex("a"))


def test_rpq_without_cycle():
    for test_case in rpq_cases_without_cycles:
        gw = GraphWorker(MultiDiGraph(test_case["graph"]))
        assert test_case["expected"] == gw.make_regular_request(
            Regex(test_case["regular_request"][0]), *test_case["regular_request"][1:]
        )


def test_rpq_with_cycle():
    for test_case in rpq_cases_with_cycles:
        gw = GraphWorker(create_labeled_two_cycles_graph(*test_case["graph"]))
        assert test_case["expected"] == gw.make_regular_request(
            Regex(test_case["regular_request"][0]), *test_case["regular_request"][1:]
        )
