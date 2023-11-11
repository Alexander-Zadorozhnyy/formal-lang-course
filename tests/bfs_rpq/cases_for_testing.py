regular_request_bfs_cases_without_cycles = [
    {
        "graph": [
            (1, 2, {"label": "a"}),
            (1, 3, {"label": "b"}),
            (1, 4, {"label": "c"}),
        ],
        "regular_request": "a|c",
        "params": [{1}, {2, 3, 4}],
        "expected": {1, 3},
    },
    {
        "graph": [(0, 1, {"label": "a"}), (1, 2, {"label": "b"})],
        "regular_request": "a b",
        "params": [{0}, {2}],
        "expected": {2},
    },
    {
        "graph": [
            (0, 1, {"label": "a"}),
            (1, 2, {"label": "b"}),
            (1, 3, {"label": "c"}),
        ],
        "regular_request": "a*b",
        "params": [{0, 3}, {2}, True],
        "expected": {(0, 2)},
    },
    {
        "graph": [
            (0, 1, {"label": "a"}),
            (2, 1, {"label": "b"}),
            (1, 3, {"label": "c"}),
            (1, 4, {"label": "b"}),
        ],
        "regular_request": "(a|b)*c",
        "params": [{0, 2}, {3}, True],
        "expected": {(0, 3)},
    },
]

regular_request_bfs_cases_with_cycles = [
    {
        "graph": [10, "a", 10, "b"],
        "regular_request": "a",
        "params": [set()],
        "expected": {i for i in range(0, 11)},
    },
    {
        "graph": [10, "a", 10, "b"],
        "regular_request": "(a)(b)",
        "params": [set()],
        "expected": {11},
    },
    {
        "graph": [50, "a", 50, "b"],
        "regular_request": "a",
        "params": [{44}, set(), True],
        "expected": {(44, 45)},
    },
    {
        "graph": [20, "a", 20, "b"],
        "regular_request": "(a*)+b",
        "params": [{10}, {11}, True],
        "expected": {(10, 11)},
    },
    {
        "graph": [20, "a", 20, "b"],
        "regular_request": "(a*)+b",
        "params": [{10}, set(), True],
        "expected": {(10, x) for x in range(0, 21)},
    },
    {
        "graph": [20, "a", 20, "b"],
        "regular_request": "a+(b*)",
        "params": [{10}, set(), True],
        "expected": {(10, 11)},
    },
]
