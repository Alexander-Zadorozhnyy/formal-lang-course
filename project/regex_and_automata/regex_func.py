from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.regular_expression import Regex


def convert_regex_to_minimal_dfa(regex_expr: Regex) -> DeterministicFiniteAutomaton:
    return regex_expr.to_epsilon_nfa().minimize()
