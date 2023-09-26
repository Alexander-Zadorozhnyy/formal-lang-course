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
