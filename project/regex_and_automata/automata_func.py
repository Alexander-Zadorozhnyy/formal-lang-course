from scipy.sparse import dok_matrix
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State

from project.matrix.matrix import Matrix
from project.matrix.matrix_func import (
    get_matrix_transitive_closure,
    convert_nfa_to_matrix,
    intersect_matrices,
    convert_matrix_to_nfa,
)


def create_automata_from_scratch(
        transitions: list, starting_states: set = None, final_states: set = None
) -> NondeterministicFiniteAutomaton:
    if not transitions:
        return NondeterministicFiniteAutomaton()

    automata = NondeterministicFiniteAutomaton()

    for state in starting_states:
        automata.add_start_state(State(state))
    for state in final_states:
        automata.add_final_state(State(state))

    automata.add_transitions(transitions)

    return automata


def get_automata_transitive_closure(
        automata: NondeterministicFiniteAutomaton,
) -> dok_matrix:
    return get_matrix_transitive_closure(convert_nfa_to_matrix(automata))


def intersect_automatas(
        first_automata: NondeterministicFiniteAutomaton,
        second_automata: NondeterministicFiniteAutomaton,
) -> Matrix:
    return intersect_matrices(
        convert_nfa_to_matrix(first_automata),
        convert_nfa_to_matrix(second_automata),
    )


def get_connected_nodes(
        automata: NondeterministicFiniteAutomaton,
        start_states: set[int],
        final_states: set[int],
        closure: dok_matrix,
):
    def check_is_valid(start, final):
        return start in start_states and final in final_states

    indexes = {index: state for index, state in enumerate(automata.states)}
    matrix_dim = len(automata.states)

    return {
        (indexes[start % matrix_dim], indexes[final % matrix_dim])
        for start, final in zip(*closure.nonzero())
        if check_is_valid(start, final)
    }
