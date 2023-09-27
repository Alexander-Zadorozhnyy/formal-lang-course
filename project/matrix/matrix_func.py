from itertools import product

from pyformlang.finite_automaton import State, NondeterministicFiniteAutomaton
from scipy.sparse import dok_matrix, kron

from project.matrix.matrix import Matrix


def create_labels(shape: tuple[int, int], indexes: list) -> dok_matrix:
    labels = dok_matrix(shape, dtype=bool)
    for label_index in indexes:
        labels[label_index] = 1
    return labels


def get_matrix_transitive_closure(matrix: Matrix) -> dok_matrix:
    if not matrix.labels.values():
        return dok_matrix((1, 1))

    len_states = len(matrix.indexes)

    summed_decomposition = sum(
        matrix.labels.values(), start=dok_matrix((len_states, len_states), dtype=bool)
    )
    summed_decomposition.count_nonzero()

    prev_cnt = -1
    curr_cnt = summed_decomposition.nnz
    while prev_cnt != curr_cnt:
        summed_decomposition += summed_decomposition @ summed_decomposition
        prev_cnt = curr_cnt
        curr_cnt = summed_decomposition.nnz

    return summed_decomposition


def convert_nfa_to_matrix(automata: NondeterministicFiniteAutomaton) -> Matrix:
    indexes = {state: index for index, state in enumerate(automata.states)}
    num_states = len(automata.states)

    labels = dict()

    for label in automata.symbols:
        label_matrix = dok_matrix((num_states, num_states), dtype=bool)
        states = automata.to_dict()

        for from_state in states:
            to_states = (
                (
                    states[from_state][label]
                    if isinstance(states[from_state][label], set)
                    else {states[from_state][label]}
                )
                if label in states[from_state]
                else set()
            )

            for to_state in to_states:
                label_matrix[indexes[from_state], indexes[to_state]] = True

        labels[label] = label_matrix

    return Matrix(automata.start_states, automata.final_states, indexes, labels)


def convert_matrix_to_nfa(matrix: Matrix) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton()

    for label in matrix.labels.keys():
        marked_array = matrix.labels[label].toarray()
        for from_state, to_state in product(range(len(marked_array)), repeat=2):
            if marked_array[from_state][to_state]:
                nfa.add_transition(
                    matrix.indexes[State(from_state)],
                    label,
                    matrix.indexes[State(to_state)],
                )

    for start_state in matrix.start_states:
        nfa.add_start_state(matrix.indexes[State(start_state)])
    for final_state in matrix.final_states:
        nfa.add_final_state(matrix.indexes[State(final_state)])

    return nfa


def intersect_matrices(first_matrix: Matrix, second_matrix: Matrix) -> Matrix:
    def make_matrix_kron(states_one, states_two, label):
        return kron(states_one[label], states_two[label], format="dok")

    def check_is_valid(first, second, state_type):
        if state_type:
            return (
                first in first_matrix.start_states
                and second in second_matrix.start_states
            )
        return (
            first in first_matrix.final_states and second in second_matrix.final_states
        )

    labels = first_matrix.labels.keys() & second_matrix.labels.keys()
    matrix = {
        label: make_matrix_kron(first_matrix.labels, second_matrix.labels, label)
        for label in labels
    }
    first_indexes = first_matrix.indexes
    second_indexes = second_matrix.indexes

    start_states = final_states = set()
    new_indexes = {}

    for state_one in first_indexes:
        for state_two in second_indexes:
            new_index = (
                first_indexes[state_one] * len(second_indexes)
                + second_indexes[state_two]
            )
            new_indexes[new_index] = new_index

            if check_is_valid(state_one, state_two, 1):
                start_states.add(new_index)
            if check_is_valid(state_one, state_two, 0):
                final_states.add(new_index)

    return Matrix(start_states, final_states, new_indexes, matrix)
