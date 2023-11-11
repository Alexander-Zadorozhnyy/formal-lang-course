from networkx import MultiDiGraph
from pyformlang.regular_expression import Regex

from project.cfpq.utils import create_labeled_two_cycles_graph
from project.graph.graph_worker import GraphWorker
from tests.bfs_rpq.cases_for_testing import (
    regular_request_bfs_cases_without_cycles,
    regular_request_bfs_cases_with_cycles,
)


def test_bfs_without_cycles() -> None:
    for case in regular_request_bfs_cases_without_cycles:
        gw = GraphWorker(MultiDiGraph(case["graph"]))
        regex = Regex(case["regular_request"])
        assert case["expected"] == gw.make_regular_request_bfs(regex, *case["params"])


def test_bfs_with_cycles() -> None:
    for case in regular_request_bfs_cases_with_cycles:
        gw = GraphWorker(create_labeled_two_cycles_graph(*case["graph"]))
        regex = Regex(case["regular_request"])
        assert case["expected"] == gw.make_regular_request_bfs(regex, *case["params"])
