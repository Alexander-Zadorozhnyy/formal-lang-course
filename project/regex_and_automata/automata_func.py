from typing import Union, Type

from scipy.sparse import dok_matrix, lil_matrix, csr_matrix, csc_matrix
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State

from project.matrix.matrix import Matrix
from project.matrix.matrix_func import (
    convert_nfa_to_matrix,
    intersect_matrices,
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


def intersect_automatas(
    first_automata: NondeterministicFiniteAutomaton,
    second_automata: NondeterministicFiniteAutomaton,
    typed_matrix: Union[
        Type[lil_matrix], Type[dok_matrix], Type[csr_matrix], Type[csc_matrix]
    ] = dok_matrix,
) -> Matrix:
    return intersect_matrices(
        convert_nfa_to_matrix(first_automata),
        convert_nfa_to_matrix(second_automata),
        typed_matrix,
    )


def get_connected_nodes(
    automata: NondeterministicFiniteAutomaton,
    start_states: set[int],
    final_states: set[int],
    closure: Union[lil_matrix, dok_matrix, csr_matrix, csc_matrix],
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
