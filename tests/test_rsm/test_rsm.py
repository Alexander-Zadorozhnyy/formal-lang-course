from project.ecfg.ecfg import ECFG
from project.recursive_state_machine.rsm import RSM
from tests.test_ecfg.cases_for_testing import ecfg_cases, start_symbol


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
