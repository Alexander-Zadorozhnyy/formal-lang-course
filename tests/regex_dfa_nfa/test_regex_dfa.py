from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.regular_expression import Regex

from project.regex_dfa_builder.min_dfa_builder import regex_to_minimal_dfa


def test_regex_to_minimal_dfa():
    assert DeterministicFiniteAutomaton() == regex_to_minimal_dfa(Regex(""))


def test_regex_to_minimal_dfa_epsilon():
    expected = DeterministicFiniteAutomaton()
    expected.add_start_state(0)
    expected.add_final_state(0)

    actual = regex_to_minimal_dfa(Regex("$"))
    print(actual.to_dict())

    assert expected == actual
    assert actual.is_deterministic() and len(actual.states) == len(
        actual.minimize().states
    )


def test_regex_to_minimal_dfa_star():
    expected = DeterministicFiniteAutomaton()
    expected.add_start_state(0)
    expected.add_final_state(0)
    expected.add_transitions([(0, "test", 0)])

    actual = regex_to_minimal_dfa(Regex("test*"))

    assert expected == actual
    assert actual.is_deterministic() and len(actual.states) == len(
        actual.minimize().states
    )


def test_regex_to_minimal_dfa_or_plus():
    expected = DeterministicFiniteAutomaton()
    expected.add_start_state(0)
    expected.add_final_state(1)
    expected.add_transitions([(0, "test_one", 1), (0, "test_two", 1)])

    actual_1 = regex_to_minimal_dfa(Regex("test_one|test_two"))
    actual_2 = regex_to_minimal_dfa(Regex("test_one+test_two"))

    assert expected == actual_1
    assert expected == actual_2
    assert actual_1.is_deterministic() and len(actual_1.states) == len(
        actual_1.minimize().states
    )
    assert actual_2.is_deterministic() and len(actual_2.states) == len(
        actual_2.minimize().states
    )


def test_regex_to_minimal_space():
    expected = DeterministicFiniteAutomaton()
    expected.add_start_state(0)
    expected.add_final_state(2)
    expected.add_transitions([(0, "test_one", 1), (1, "test_two", 2)])

    actual = regex_to_minimal_dfa(Regex("test_one test_two"))

    assert expected == actual
    assert actual.is_deterministic() and len(actual.states) == len(
        actual.minimize().states
    )


def test_regex_to_minimal_dfa_var():
    expected = DeterministicFiniteAutomaton()
    expected.add_start_state(0)
    expected.add_final_state(1)
    expected.add_transitions([(0, "test", 1)])

    actual = regex_to_minimal_dfa(Regex("test"))
    print(actual.to_dict())

    assert expected == actual
    assert actual.is_deterministic() and len(actual.states) == len(
        actual.minimize().states
    )


def test_regex_to_minimal_dfa_parens():
    expected = DeterministicFiniteAutomaton()
    expected.add_start_state(0)
    expected.add_final_state(1)
    expected.add_transitions([(0, "test", 1)])

    actual = regex_to_minimal_dfa(Regex("(test)"))

    assert expected == actual
    assert actual.is_deterministic() and len(actual.states) == len(
        actual.minimize().states
    )


def test_regex_to_minimal_dfa_hard_expr():
    expected = DeterministicFiniteAutomaton()
    expected.add_start_state(0)
    expected.add_transitions([(0, "0", 0)])
    expected.add_transitions([(0, "1", 0)])
    expected.add_transitions([(0, "111", 1)])
    expected.add_final_state(1)

    actual = regex_to_minimal_dfa(Regex("(0|1)*111"))

    assert expected == actual
    assert actual.is_deterministic() and len(actual.states) == len(
        actual.minimize().states
    )
