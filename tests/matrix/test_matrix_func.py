from scipy.sparse import dok_matrix

from project.matrix.matrix import Matrix
from project.matrix.matrix_func import (
    convert_nfa_to_matrix,
    convert_matrix_to_nfa,
    intersect_matrices,
    get_matrix_transitive_closure,
    create_labels,
)
from project.regex_and_automata.automata_func import create_automata_from_scratch
from tests.matrix.cases_for_testing import (
    transitive_matrix_closure_expected_cases,
    automata_test_cases,
    matrix_intersection_cases,
)


def get_array_data(matrix: dok_matrix):
    return matrix.toarray().data


def test_conversion_between_nfa_and_matrix():
    for test_case in automata_test_cases:
        automata = create_automata_from_scratch(
            test_case["transitions"],
            test_case["start_states"],
            test_case["final_states"],
        )
        automata_matrix = convert_nfa_to_matrix(automata)

        assert convert_matrix_to_nfa(automata_matrix).is_equivalent_to(automata)


def test_matrix_intersection():
    for test_case in matrix_intersection_cases:
        expected = Matrix(
            labels={
                k: create_labels(*v) for k, v in test_case["expected_labels"].items()
            },
            start_states=test_case["expected_start"],
            final_states=test_case["expected_final"],
            indexes=test_case["expected_indexes"],
        )
        actual = intersect_matrices(
            Matrix(
                labels={
                    k: create_labels(*v)
                    for k, v in test_case["actual_1_labels"].items()
                },
                start_states=test_case["actual_1_start"],
                final_states=test_case["actual_1_final"],
                indexes=test_case["actual_1_indexes"],
            ),
            Matrix(
                labels={
                    k: create_labels(*v)
                    for k, v in test_case["actual_2_labels"].items()
                },
                start_states=test_case["actual_2_start"],
                final_states=test_case["actual_2_final"],
                indexes=test_case["actual_2_indexes"],
            ),
        )

        assert {k: v.toarray().tolist() for k, v in actual.labels.items()} == {
            k: v.toarray().tolist() for k, v in expected.labels.items()
        }
        assert actual.start_states == expected.start_states
        assert actual.final_states == expected.final_states
        assert actual.indexes == expected.indexes


def test_matrix_transitive_closure():
    for test_index, test_case in enumerate(automata_test_cases):
        automata = create_automata_from_scratch(
            test_case["transitions"],
            test_case["start_states"],
            test_case["final_states"],
        )
        automata_matrix = convert_nfa_to_matrix(automata)
        closure = get_matrix_transitive_closure(automata_matrix)

        expected_closure = dok_matrix(
            transitive_matrix_closure_expected_cases[test_index]
        )

        assert get_array_data(closure) == get_array_data(expected_closure)
