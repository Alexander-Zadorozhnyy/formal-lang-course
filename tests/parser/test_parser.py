import os.path
from os import path

from project.language.parser import check_ast, save_to_dot, parse_to_ast
from cases_for_testing import (
    test_check_true_cases,
    test_check_false_cases,
    test_grammar_ast,
)

CURR_PATH = path.dirname(path.realpath(__file__))


def test_correct_program_parser():
    for test in test_check_true_cases:
        assert check_ast(test)


def test_incorrect_program_parser():
    for test in test_check_false_cases:
        assert not check_ast(test)


def test_save_dot():
    path_actual = os.path.join(CURR_PATH, "static", "actual_ast.dot")
    path_expected = os.path.join(CURR_PATH, "static", "expected_ast.dot")

    parser = parse_to_ast(test_grammar_ast)
    save_to_dot(parser, str(path_actual))

    with open(path_actual, "r") as actual:
        with open(path_expected, "r") as expected:
            assert actual.read() == expected.read()
