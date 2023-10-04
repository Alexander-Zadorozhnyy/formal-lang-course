automata_test_cases = [
    {
        "transitions": [(1, "c", 1), (1, "b", 0), (0, "b", 0), (0, "c", 1)],
        "start_states": {1},
        "final_states": {0},
    },
    {
        "transitions": [
            (0, "a", 1),
            (1, "b", 2),
            (2, "c", 3),
            (3, "a", 0),
        ],
        "start_states": {0, 1},
        "final_states": {1},
    },
    {
        "transitions": [
            (0, "b", 0),
        ],
        "start_states": {0},
        "final_states": {1},
    },
    {
        "transitions": [
            (0, "b", 0),
            (1, "a", 1),
        ],
        "start_states": {0, 1},
        "final_states": {0, 1},
    },
    {
        "transitions": [
            (0, "a", 1),
            (1, "b", 2),
            (2, "c", 3),
        ],
        "start_states": {},
        "final_states": {},
    },
]

matrix_intersection_cases = [
    {
        "expected_labels": {"a": [(4, 4), [(0, 1)]]},
        "expected_start": set(),
        "expected_final": set(),
        "expected_indexes": {0: 0, 1: 1, 2: 2, 3: 3},
        "actual_1_labels": {
            "a": [(4, 4), [(0, 1)]],
            "b": [(4, 4), [(0, 2)]],
            "c": [(4, 4), [(0, 3)]],
        },
        "actual_1_start": {0},
        "actual_1_final": {1, 2, 3},
        "actual_1_indexes": {1: 0, 2: 1, 3: 2, 4: 3},
        "actual_2_labels": {"a": [(1, 1), [(0, 0)]]},
        "actual_2_start": {0},
        "actual_2_final": {0},
        "actual_2_indexes": {5: 0},
    },
    {
        "expected_labels": {
            "a": [(12, 12), [(0, 3), (1, 3), (3, 0), (4, 0)]],
            "b": [(12, 12), [(0, 6), (1, 8), (9, 6), (10, 8)]],
        },
        "expected_start": {0, 1, 11, 8},
        "expected_final": {0, 1, 11, 8},
        "expected_indexes": {ind: ind for ind in range(12)},
        "actual_1_labels": {
            "a": [(4, 4), [(0, 1), (1, 0)]],
            "b": [
                (4, 4),
                [
                    (0, 2),
                    (3, 2),
                ],
            ],
        },
        "actual_1_start": {0},
        "actual_1_final": {2, 3},
        "actual_1_indexes": {0: 0, 1: 1, 2: 2, 3: 3},
        "actual_2_labels": {
            "a": [(3, 3), [(0, 0), (1, 0)]],
            "b": [(3, 3), [(0, 0), (1, 2)]],
        },
        "actual_2_start": {0, 1},
        "actual_2_final": {2},
        "actual_2_indexes": {0: 0, 1: 1, 2: 2},
    },
    {
        "expected_labels": {
            "a": [(9, 9), [(0, 4)]],
            "b": [(9, 9), [(4, 8)]],
        },
        "expected_start": {0, 8},
        "expected_final": {0, 8},
        "expected_indexes": {ind: ind for ind in range(9)},
        "actual_1_labels": {
            "a": [(3, 3), [(0, 1)]],
            "b": [(3, 3), [(1, 2)]],
        },
        "actual_1_start": {0},
        "actual_1_final": {2},
        "actual_1_indexes": {ind: ind for ind in range(3)},
        "actual_2_labels": {
            "a": [(3, 3), [(0, 1)]],
            "b": [(3, 3), [(1, 2)]],
        },
        "actual_2_start": {0},
        "actual_2_final": {2},
        "actual_2_indexes": {ind: ind for ind in range(3)},
    },
    {
        "expected_labels": {},
        "expected_start": set(),
        "expected_final": set(),
        "expected_indexes": {},
        "actual_1_labels": {
            "a": [(3, 3), [(0, 1)]],
            "b": [(3, 3), [(1, 2)]],
        },
        "actual_1_start": {0},
        "actual_1_final": {2},
        "actual_1_indexes": {ind: ind for ind in range(3)},
        "actual_2_labels": {},
        "actual_2_start": set(),
        "actual_2_final": set(),
        "actual_2_indexes": set(),
    },
]

transitive_matrix_closure_expected_cases = [
    [[1, 1], [1, 1]],
    [[1, 1, 1, 1] for _ in range(4)],
    [[1, 0], [0, 0]],
    [[1, 0], [0, 1]],
    [[0, 1, 1, 1], [0, 0, 1, 1], [0, 0, 0, 1], [0, 0, 0, 0]],
]

rpq_cases_without_cycles = [
    {
        "graph": [
            (1, 2, {"label": "a"}),
            (1, 3, {"label": "b"}),
            (1, 4, {"label": "c"}),
        ],
        "regular_request": ["a|c", {1}, {2, 3, 4}],
        "expected": {(1, 2), (1, 4)},
    },
    {
        "graph": [(0, 1, {"label": "a"}), (1, 2, {"label": "b"})],
        "regular_request": ["a b", {0}, {2}],
        "expected": {(0, 2)},
    },
    {
        "graph": [
            (0, 1, {"label": "a"}),
            (1, 2, {"label": "b"}),
            (1, 3, {"label": "c"}),
        ],
        "regular_request": ["a*b", {0, 3}, {2}],
        "expected": {(0, 2)},
    },
    {
        "graph": [
            (0, 1, {"label": "a"}),
            (1, 2, {"label": "b"}),
            (1, 3, {"label": "c"}),
        ],
        "regular_request": ["$"],
        "expected": set(),
    },
    {
        "graph": [
            (0, 1, {"label": "a"}),
            (2, 1, {"label": "b"}),
            (1, 3, {"label": "c"}),
            (1, 4, {"label": "b"}),
        ],
        "regular_request": ["(a|b)*c", {0, 2}, {3}],
        "expected": {(2, 3), (0, 3)},
    },
    {
        "graph": [
            (0, 1, {"label": "a"}),
            (2, 1, {"label": "b"}),
            (1, 3, {"label": "c"}),
            (1, 4, {"label": "b"}),
        ],
        "regular_request": ["(a|b)*c", {0, 2}, {0}],
        "expected": set(),
    },
]

rpq_cases_with_cycles = [
    {
        "graph": [2, "a", 2, "b"],
        "regular_request": ["a*b", {1, 3}],
        "expected": {(1, 1), (1, 3), (3, 4)},
    },
    {
        "graph": [3, "a", 2, "b"],
        "regular_request": ["a*|b"],
        "expected": {
            (0, 1),
            (1, 2),
            (0, 4),
            (2, 1),
            (3, 1),
            (0, 2),
            (2, 2),
            (1, 0),
            (3, 2),
            (1, 3),
            (0, 0),
            (1, 1),
            (0, 3),
            (2, 0),
            (3, 0),
            (2, 3),
            (4, 5),
            (3, 3),
            (5, 0),
        },
    },
    {
        "graph": [3, "a", 2, "b"],
        "regular_request": ["t|m"],
        "expected": set(),
    },
    {
        "graph": [3, "a", 3, "c"],
        "regular_request": ["a*(c|a)|c", {1, 3, 2, 5}, {6, 2}],
        "expected": {(1, 2), (2, 2), (3, 2), (5, 6)},
    },
    {
        "graph": [2, "a", 2, "c"],
        "regular_request": [""],
        "expected": set(),
    },
    {
        "graph": [2, "a", 3, "c"],
        "regular_request": ["c", {0}, {1, 2, 3}],
        "expected": {(0, 3)},
    },
]

automata_get_connected_nodes_test_cases = [
    [{1, 2, 3, 4}, {1, 2, 3, 4}, [(8, 8), [(4, 1), (4, 3)]]],
    [{0, 5}, {0, 5}, [(9, 9), [(0, 5), (0, 7), (7, 5)]]],
    [{2, 4, 7}, {2, 4, 7}, [(8, 8), [(4, 2), (4, 5), (5, 2)]]],
    [{0, 1, 2, 3}, {0, 1, 2, 3}, [(1, 1), []]],
    [
        {0, 8, 2},
        {0, 8, 2},
        [(10, 10), [(0, 1), (0, 4), (0, 8), (1, 4), (1, 8), (2, 1), (2, 4), (2, 8)]],
    ],
    [
        {0, 2, 5},
        {0, 2, 5},
        [(10, 10), [(0, 1), (0, 4), (0, 8), (1, 4), (1, 8), (2, 1), (2, 4), (2, 8)]],
    ],
]
