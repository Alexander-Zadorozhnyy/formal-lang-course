from os import path

from project.cfpq.func import load_graph_info_by_name, create_and_save_two_cycles_graph
from tests.utils import check_is_dot_files_the_same


def test_load_graph_info_by_name():
    actual = load_graph_info_by_name("travel")

    assert 131 == actual["num_of_nodes"]
    assert 277 == actual["num_of_edges"]
    assert {
        "minCardinality",
        "versionInfo",
        "someValuesFrom",
        "equivalentClass",
        "type",
        "range",
        "inverseOf",
        "disjointWith",
        "hasAccommodation",
        "intersectionOf",
        "hasPart",
        "unionOf",
        "comment",
        "oneOf",
        "onProperty",
        "hasValue",
        "subClassOf",
        "rest",
        "differentFrom",
        "complementOf",
        "first",
        "domain",
    } == actual["set_of_labels"]


def test_create_and_save_two_cycles_graph():
    curr_path = path.dirname(path.realpath(__file__))
    expected_path = path.join(curr_path, "expected_graph_main.dot")
    actual_path = path.join(curr_path, "actual_graph_main.dot")

    create_and_save_two_cycles_graph(
        first_cycle=(5, "abc"),
        second_cycle=(5, "def"),
        path=actual_path,
    )

    assert check_is_dot_files_the_same(expected_path, actual_path)
