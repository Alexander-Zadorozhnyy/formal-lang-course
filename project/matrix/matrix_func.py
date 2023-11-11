from itertools import product

from pyformlang.finite_automaton import State, NondeterministicFiniteAutomaton
from scipy.sparse import (
    dok_matrix,
    lil_matrix,
    csr_matrix,
    csc_matrix,
    kron,
    vstack,
    block_diag,
)

from project.matrix.matrix import Matrix
from typing import Union, Type


def create_labels(
    shape: tuple[int, int],
    indexes: list,
    typed_matrix: Union[
        Type[lil_matrix], Type[dok_matrix], Type[csr_matrix], Type[csc_matrix]
    ],
) -> Union[lil_matrix, dok_matrix, csr_matrix, csc_matrix]:
    labels = typed_matrix(shape, dtype=bool)
    for label_index in indexes:
        labels[label_index] = 1
    return labels


def get_matrix_transitive_closure(
    matrix: Matrix,
    typed_matrix: Union[
        Type[lil_matrix], Type[dok_matrix], Type[csr_matrix], Type[csc_matrix]
    ] = dok_matrix,
) -> Union[lil_matrix, dok_matrix, csr_matrix, csc_matrix]:
    if not matrix.labels.values():
        return typed_matrix((1, 1))

    len_states = len(matrix.indexes)

    summed_decomposition = sum(
        matrix.labels.values(), start=typed_matrix((len_states, len_states), dtype=bool)
    )
    summed_decomposition.count_nonzero()

    prev_cnt = -1
    curr_cnt = summed_decomposition.nnz
    while prev_cnt != curr_cnt:
        summed_decomposition += summed_decomposition @ summed_decomposition
        prev_cnt = curr_cnt
        curr_cnt = summed_decomposition.nnz

    return summed_decomposition


def convert_nfa_to_matrix(
    automata: NondeterministicFiniteAutomaton,
    typed_matrix: Union[
        Type[lil_matrix], Type[dok_matrix], Type[csr_matrix], Type[csc_matrix]
    ] = dok_matrix,
) -> Matrix:
    indexes = {state: index for index, state in enumerate(automata.states)}
    num_states = len(automata.states)

    labels = dict()

    for label in automata.symbols:
        label_matrix = typed_matrix((num_states, num_states), dtype=bool)
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


def intersect_matrices(
    first_matrix: Matrix,
    second_matrix: Matrix,
    typed_matrix: Union[
        Type[lil_matrix], Type[dok_matrix], Type[csr_matrix], Type[csc_matrix]
    ],
) -> Matrix:
    def make_matrix_kron(
        states_one,
        states_two,
        label,
    ):
        return kron(states_one[label], states_two[label], format=formats[typed_matrix])

    formats = {
        lil_matrix: "lil",
        dok_matrix: "dok",
        csr_matrix: "csr",
        csc_matrix: "csc",
    }

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


def create_matrix_front(
    first_matrix: Matrix,
    second_matrix: Matrix,
    start_states: set,
    typed_matrix: Union[
        Type[lil_matrix], Type[dok_matrix], Type[csr_matrix], Type[csc_matrix]
    ],
) -> Union[lil_matrix, dok_matrix, csr_matrix, csc_matrix]:
    dim_first, dim_second = len(first_matrix.indexes), len(second_matrix.indexes)
    front = typed_matrix((dim_first, dim_first + dim_second), dtype=bool)

    row = typed_matrix((1, dim_first), dtype=bool)
    for i in start_states:
        row[0, i] = True

    for i in second_matrix.start_states:
        front[second_matrix.indexes[i], second_matrix.indexes[i]] = True
        front[second_matrix.indexes[i], dim_second:] = row

    return front


def get_matrices_front(
    first_matrix: Matrix,
    second_matrix: Matrix,
    start_states: set,
    is_single_mode: bool,
    typed_matrix: Union[
        Type[lil_matrix], Type[dok_matrix], Type[csr_matrix], Type[csc_matrix]
    ],
) -> Union[lil_matrix, dok_matrix, csr_matrix, csc_matrix]:
    if not is_single_mode:
        return create_matrix_front(
            first_matrix, second_matrix, start_states, typed_matrix
        )

    single_state_fronts = [
        create_matrix_front(first_matrix, second_matrix, {i}, typed_matrix)
        for i in start_states
    ]
    return vstack(single_state_fronts)


def get_direct_sum_of_matrices(
    first_matrix: Matrix,
    second_matrix: Matrix,
    typed_matrix: Union[
        Type[lil_matrix], Type[dok_matrix], Type[csr_matrix], Type[csc_matrix]
    ],
) -> dict:
    first_labels, second_labels = first_matrix.labels, second_matrix.labels

    return {
        label: typed_matrix(
            block_diag((second_matrix.labels[label], first_matrix.labels[label]))
        )
        for label in set(first_labels.keys()).intersection(set(second_labels.keys()))
    }


def update_front(
    matrix: Matrix,
    front: Union[lil_matrix, dok_matrix, csr_matrix, csc_matrix],
    typed_matrix: Union[
        Type[lil_matrix], Type[dok_matrix], Type[csr_matrix], Type[csc_matrix]
    ],
) -> Union[lil_matrix, dok_matrix, csr_matrix, csc_matrix]:
    new_front = typed_matrix(front.shape, dtype=bool)
    dim_matrix = len(matrix.indexes)

    for i, j in zip(*front.nonzero()):
        if j < dim_matrix and front[i, dim_matrix:].count_nonzero() > 0:
            new_index = i - (i % dim_matrix) + j
            new_front[new_index, j] = True
            new_front[new_index, dim_matrix:] += front[i, dim_matrix:]

    return new_front


def extruct_valid_nodes(
    first_matrix: Matrix,
    second_matrix: Matrix,
    start_states: list,
    visited: Union[lil_matrix, dok_matrix, csr_matrix, csc_matrix],
    is_single_mode: bool,
) -> set:
    result = set()
    first_states = list(first_matrix.indexes.keys())
    second_states = list(second_matrix.indexes.keys())
    second_dim = len(second_matrix.indexes)

    for i, j in zip(*visited.nonzero()):
        if (
            second_dim <= j
            and first_states[j - second_dim] in first_matrix.final_states
            and second_states[i % second_dim] in second_matrix.final_states
        ):
            value = (
                j - second_dim
                if not is_single_mode
                else (
                    start_states[i % (len(start_states) - 1)],
                    j - second_dim,
                )
            )

            result.add(value)

    return result


def make_matrices_bfs_regular_request(
    first_matrix: Matrix,
    second_matrix: Matrix,
    is_single_mode: bool,
    typed_matrix: Union[
        Type[lil_matrix], Type[dok_matrix], Type[csr_matrix], Type[csc_matrix]
    ] = dok_matrix,
) -> set:
    if not first_matrix.start_states:
        return set()

    start_states = [first_matrix.indexes[s] for s in first_matrix.start_states]

    front = get_matrices_front(
        first_matrix, second_matrix, set(start_states), is_single_mode, typed_matrix
    )

    direct_sum = get_direct_sum_of_matrices(first_matrix, second_matrix, typed_matrix)
    visited = typed_matrix(front.shape, dtype=bool)

    visited_save = None
    while (
        visited_save is None or visited_save.count_nonzero() != visited.count_nonzero()
    ):
        visited_save = visited.copy()
        for direct_matrix in direct_sum.values():
            next_front = (front if front is not None else visited) @ direct_matrix
            visited += update_front(second_matrix, next_front, typed_matrix)

        front = None

    return extruct_valid_nodes(
        first_matrix, second_matrix, start_states, visited, is_single_mode
    )
