import os
from pathlib import Path

from pyformlang.cfg import CFG, Variable, Terminal, Production

from project.cfg.cfg_func import read_context_free_grammar, convert_cfg_to_weak_cnf
from tests.cfg_ecfg.cases_for_testing_cfg import (
    file_tests,
    test_built_convert_cfg_to_weak_cnf_cases,
)


def check_is_grammar_correct(
    cfg: CFG, terminals: list[Terminal], is_correct: int
) -> None:
    assert cfg.contains(terminals) == is_correct


def test_read_grammar_from_file() -> None:
    file_names = [file for file in os.listdir(os.getcwd()) if ".cfg" in file]
    file_paths = [Path(os.path.join(os.getcwd(), file)) for file in file_names]

    for ind, file in enumerate(file_names):
        cfg = read_context_free_grammar(file_paths[ind], "S")

        for corr_terminals in file_tests[file]["correct"]:
            check_is_grammar_correct(cfg, corr_terminals, 1)

        for incorr_terminals in file_tests[file]["incorrect"]:
            check_is_grammar_correct(cfg, incorr_terminals, 0)


def compare_test_func(
    actual_cfg: CFG,
    weak_cnf_cfg: CFG,
    shift: int,
    contains_terminal_list_test: list[list[Terminal]],
) -> None:
    assert weak_cnf_cfg.terminals == actual_cfg.terminals
    assert len(weak_cnf_cfg.productions) == len(actual_cfg.productions) + shift
    assert len(weak_cnf_cfg.variables) == len(actual_cfg.variables) + shift

    for list_terminals in contains_terminal_list_test:
        assert weak_cnf_cfg.contains(list_terminals) == actual_cfg.contains(
            list_terminals
        )


def build_test_func(
    variables: set[Variable],
    terminals: set[Terminal],
    productions: set[Production],
    start_variable: str,
    shift: int,
    contains_terminal_list_test: list[list[Terminal]],
) -> None:
    actual_cfg = CFG(variables, terminals, Variable(start_variable), productions)
    weak_cnf_cfg = convert_cfg_to_weak_cnf(actual_cfg, start_variable)

    compare_test_func(actual_cfg, weak_cnf_cfg, shift, contains_terminal_list_test)


def test_built_convert_cfg_to_weak_cnf() -> None:
    for test_case in test_built_convert_cfg_to_weak_cnf_cases:
        build_test_func(
            variables=test_case["variables"],
            terminals=test_case["terminals"],
            productions=test_case["productions"],
            start_variable=test_case["start_variable"],
            shift=test_case["shift"],
            contains_terminal_list_test=test_case["contains_terminal_list_test"],
        )
