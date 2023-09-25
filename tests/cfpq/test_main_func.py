from os import path

from project.cfpq.func import load_graph_info_by_name, create_and_save_two_cycles_graph
from tests.utils import check_is_dot_files_the_same

CURR_PATH = path.dirname(path.realpath(__file__))


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
    actual_path = path.join(CURR_PATH, "actual_graph_main.dot")

    create_and_save_two_cycles_graph(
        first_cycle=(5, "abc"),
        second_cycle=(5, "def"),
        path=actual_path,
    )

    assert check_is_dot_files_the_same(
        CURR_PATH, "expected_graph_main.dot", "actual_graph_main.dot"
    )
