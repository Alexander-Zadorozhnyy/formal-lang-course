import os
from pathlib import Path

from pyformlang.cfg import Variable

from project.cfg.cfg_func import read_context_free_grammar
from project.ecfg.ecfg import ECFG
from tests.cfg_ecfg.cases_for_testing_ecfg import ecfg_cases, start_symbol


def test_convert_cfg_to_ecfg():
    file_names = [file for file in os.listdir(os.getcwd()) if ".cfg" in file]
    file_paths = [Path(os.path.join(os.getcwd(), file)) for file in file_names]

    for ind, file in enumerate(file_names):
        cfg = read_context_free_grammar(file_paths[ind], start_symbol)
        ecfg = ECFG.convert_cfg_to_ecfg(cfg, start_symbol)

        assert ecfg.start_symbol == cfg.start_symbol
        assert ecfg.variables == cfg.variables

        variables = []
        for var in ecfg.productions.keys():
            assert var not in variables
            variables.append(var)


def test_convert_srt_to_ecfg():
    for srt_ecfg, exp_variables, exp_productions in ecfg_cases:
        ecfg = ECFG.convert_str_to_ecfg(srt_ecfg, start_symbol)

        assert ecfg.variables == set(map(lambda var: Variable(var), exp_variables))
        assert ecfg.start_symbol == start_symbol

        variables = []
        for var in ecfg.productions.keys():
            assert var not in variables
            variables.append(var)