from pyformlang.cfg import Terminal, Epsilon, Variable, Production

variable = Variable("S")
variable_ul_1 = Variable("UL1")
variable_ul_2 = Variable("UL2")
variable_ul_3 = Variable("UL3")

terminal_a = Terminal("a")
terminal_b = Terminal("b")
terminal_c = Terminal("c")
terminal_m = Terminal("m")
terminal_k = Terminal("k")

terminal_open = Terminal("(")
terminal_closed = Terminal(")")

file_tests = {
    "test_epsilon.cfg": {
        "correct": [[Epsilon()]],
        "incorrect": [[terminal_a], [terminal_b], [terminal_a, terminal_b]],
    },
    "test_hard.cfg": {
        "correct": [
            [Epsilon()],
            [terminal_a, terminal_b],
            [terminal_a, terminal_b, terminal_a, terminal_b],
            [terminal_a, terminal_a, terminal_b, terminal_b],
        ],
        "incorrect": [
            [terminal_a],
            [terminal_b],
            [terminal_a, terminal_a],
            [terminal_b, terminal_a],
        ],
    },
    "test_hard_2.cfg": {
        "correct": [
            [terminal_m, terminal_k],
            [terminal_m, terminal_m, terminal_k],
            [terminal_k],
        ],
        "incorrect": [[terminal_a], [terminal_m, terminal_k, terminal_k]],
    },
    "test_or.cfg": {
        "correct": [
            [Epsilon()],
            [terminal_a],
            [terminal_b],
            [terminal_a, terminal_b],
            [terminal_a, terminal_b, terminal_a, terminal_b],
            [terminal_a, terminal_a, terminal_b, terminal_b],
        ],
        "incorrect": [[terminal_c]],
    },
    "test_simple.cfg": {"correct": [[terminal_a]], "incorrect": [[terminal_b]]},
}

useless_variable = {
    "variables": {variable},
    "terminals": {terminal_a, terminal_b},
    "productions": {
        Production(variable, [variable_ul_1]),
        Production(variable_ul_1, [variable_ul_2]),
        Production(variable_ul_2, [variable_ul_3]),
        Production(variable_ul_3, [terminal_b]),
        Production(variable_ul_3, [terminal_a]),
    },
    "start_variable": "S",
    "shift": -3,
    "contains_terminal_list_test": [[terminal_a], [terminal_b]],
}

balanced_parentheses = {
    "variables": {variable},
    "terminals": {terminal_open, terminal_closed},
    "productions": {
        Production(variable, [variable, variable]),
        Production(variable, [terminal_open, variable, terminal_closed]),
        Production(variable, [Epsilon()]),
    },
    "start_variable": "S",
    "shift": 3,
    "contains_terminal_list_test": [
        [Epsilon()],
        *[[terminal_open] * n + [terminal_closed] * n for n in range(10)],
        *[[terminal_open, terminal_closed] * n for n in range(10)],
        [
            terminal_open,
            terminal_open,
            terminal_closed,
            terminal_open,
            terminal_closed,
            terminal_closed,
        ],
    ],
}

regex_1 = {
    "variables": {variable},
    "terminals": {terminal_a},
    "productions": {
        Production(variable, [terminal_a, variable]),
        Production(variable, [Epsilon()]),
    },
    "start_variable": "S",
    "shift": 1,
    "contains_terminal_list_test": [
        [Epsilon()],
        [terminal_a],
        [terminal_a, terminal_a],
    ],
}

regex_2 = {
    "variables": {variable},
    "terminals": {terminal_a, terminal_b},
    "productions": {
        Production(variable, [terminal_a, variable, terminal_b]),
        Production(variable, [terminal_a, terminal_b]),
    },
    "start_variable": "S",
    "shift": 3,
    "contains_terminal_list_test": [
        [Epsilon()],
        *[[terminal_a] * n + [terminal_b] * n for n in range(10)],
    ],
}
test_built_convert_cfg_to_weak_cnf_cases = [
    regex_1,
    regex_2,
    useless_variable,
    balanced_parentheses,
]
