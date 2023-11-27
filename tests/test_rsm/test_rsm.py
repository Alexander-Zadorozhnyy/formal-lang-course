from scipy.sparse import dok_matrix

from project.ecfg.ecfg import ECFG
from project.recursive_state_machine.rsm import RSM
from tests.cfg_ecfg.cases_for_testing_ecfg import ecfg_cases, start_symbol
from tests.test_rsm.cases_for_testing import rsm_binary_matrix_cases


def test_convert_ecfg_to_rsm():
    for srt_ecfg, _, _ in ecfg_cases:
        ecfg = ECFG.convert_str_to_ecfg(srt_ecfg, start_symbol)
        rsm = RSM.convert_ecfg_to_rsm(ecfg, start_symbol)

        assert rsm.start_symbol == ecfg.start_symbol
        assert len(rsm.automatas) == len(ecfg.productions)


def test_minimize_rsm():
    for srt_ecfg, _, _ in ecfg_cases:
        rsm = RSM.convert_ecfg_to_rsm(srt_ecfg, start_symbol)
        rsm_minimized = rsm.minimize()

        assert len(rsm_minimized.automatas) == len(rsm.automatas)

        for var in rsm.automatas:
            assert rsm_minimized.automatas[var].is_equivalent_to(rsm.automatas[var])


def test_get_rsm_binary_matrix():
    for srt_ecfg, expected_states, expected_matrix in rsm_binary_matrix_cases:
        ecfg = ECFG.convert_str_to_ecfg(srt_ecfg, start_symbol)
        rsm = RSM.convert_ecfg_to_rsm(ecfg, start_symbol)

        binary_matrix = rsm.get_binary_matrix(dok_matrix)

        assert len(binary_matrix.indexes) == len(expected_states)
        for index, state in enumerate(binary_matrix.indexes):
            expected = expected_states[index]
            assert (state.value[0].value, state.value[1]) == expected[0]
            assert (state in binary_matrix.start_states) == expected[1]
            assert (state in binary_matrix.final_states) == expected[2]

        assert binary_matrix.get_number_of_labels() == len(expected_matrix.keys())
        for key in binary_matrix.labels.keys():
            result = []
            matrix = binary_matrix.labels[key].nonzero()
            for index in range(len(matrix[0])):
                result.append([matrix[0][index], matrix[1][index]])

            assert result == expected_matrix[str(key)]
