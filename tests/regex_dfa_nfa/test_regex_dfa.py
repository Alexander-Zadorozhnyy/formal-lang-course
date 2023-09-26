from os import path

from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.regular_expression import Regex

from project.regex_and_automata.regex_func import convert_regex_to_minimal_dfa
from tests.utils import check_is_dot_files_the_same

CURR_PATH = path.dirname(path.realpath(__file__))


def test_regex_to_minimal_dfa():
    assert DeterministicFiniteAutomaton() == convert_regex_to_minimal_dfa(Regex(""))


def test_regex_to_minimal_dfa_epsilon():
    actual = convert_regex_to_minimal_dfa(Regex("$"))
    actual.write_as_dot(path.join(CURR_PATH, "actual_dfa_epsilon.dot"))

    assert check_is_dot_files_the_same(
        CURR_PATH, "expected_dfa_epsilon.dot", "actual_dfa_epsilon.dot"
    )
    assert actual.is_deterministic() and len(actual.states) == len(
        actual.minimize().states
    )


def test_regex_to_minimal_dfa_star():
    actual = convert_regex_to_minimal_dfa(Regex("test*"))
    actual.write_as_dot(path.join(CURR_PATH, "actual_dfa_star.dot"))

    assert check_is_dot_files_the_same(
        CURR_PATH, "expected_dfa_star.dot", "actual_dfa_star.dot"
    )
    assert actual.is_deterministic() and len(actual.states) == len(
        actual.minimize().states
    )


def test_regex_to_minimal_dfa_or():
    actual = convert_regex_to_minimal_dfa(Regex("test_one|test_two"))
    actual.write_as_dot(path.join(CURR_PATH, "actual_dfa_or.dot"))

    assert check_is_dot_files_the_same(
        CURR_PATH, "expected_dfa_or_one.dot", "actual_dfa_or.dot"
    ) or check_is_dot_files_the_same(
        CURR_PATH, "expected_dfa_or_two.dot", "actual_dfa_or.dot"
    )
    assert actual.is_deterministic() and len(actual.states) == len(
        actual.minimize().states
    )


def test_regex_to_minimal_space():
    actual = convert_regex_to_minimal_dfa(Regex("test_one test_two"))
    actual.write_as_dot(path.join(CURR_PATH, "actual_dfa_space.dot"))

    assert check_is_dot_files_the_same(
        CURR_PATH, "expected_dfa_space.dot", "actual_dfa_space.dot"
    )
    assert actual.is_deterministic() and len(actual.states) == len(
        actual.minimize().states
    )


def test_regex_to_minimal_dfa_var():
    actual = convert_regex_to_minimal_dfa(Regex("test"))
    actual.write_as_dot(path.join(CURR_PATH, "actual_dfa_var.dot"))

    assert check_is_dot_files_the_same(
        CURR_PATH, "expected_dfa_var.dot", "actual_dfa_var.dot"
    )
    assert actual.is_deterministic() and len(actual.states) == len(
        actual.minimize().states
    )


def test_regex_to_minimal_dfa_parens():
    actual = convert_regex_to_minimal_dfa(Regex("(test)"))
    actual.write_as_dot(path.join(CURR_PATH, "actual_dfa_parens.dot"))

    assert check_is_dot_files_the_same(
        CURR_PATH, "expected_dfa_parens.dot", "actual_dfa_parens.dot"
    )
    assert actual.is_deterministic() and len(actual.states) == len(
        actual.minimize().states
    )


def test_regex_to_minimal_dfa_hard_expr_one():
    actual = convert_regex_to_minimal_dfa(Regex("(0|1)*111"))
    actual.write_as_dot(path.join(CURR_PATH, "actual_dfa_hard_expr.dot"))

    assert check_is_dot_files_the_same(
        CURR_PATH, "expected_dfa_hard_expr_one.dot", "actual_dfa_hard_expr.dot"
    ) or check_is_dot_files_the_same(
        CURR_PATH, "expected_dfa_hard_expr_two.dot", "actual_dfa_hard_expr.dot"
    )

    assert actual.is_deterministic() and len(actual.states) == len(
        actual.minimize().states
    )


def test_regex_to_minimal_dfa_hard_two_expr():
    actual = convert_regex_to_minimal_dfa(Regex("(0|1)*1.1.1"))
    actual.write_as_dot(path.join(CURR_PATH, "actual_dfa_hard_two_expr.dot"))

    assert check_is_dot_files_the_same(
        CURR_PATH, "expected_dfa_hard_two_expr.dot", "actual_dfa_hard_two_expr.dot"
    )

    assert actual.is_deterministic() and len(actual.states) == len(
        actual.minimize().states
    )
