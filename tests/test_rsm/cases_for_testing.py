rsm_binary_matrix_cases = [
    ("S -> a", [(("S", 0), True, False), (("S", 1), False, True)], {"a": [[0, 1]]}),
    (
        "S -> A\nA -> a",
        [
            (("A", 0), True, False),
            (("A", 1), False, True),
            (("S", 0), True, False),
            (("S", 1), False, True),
        ],
        {
            "a": [[0, 1]],
            "A": [[2, 3]],
        },
    ),
    (
        "S -> A\nA -> a\nA -> b",
        [
            (("A", 0), True, False),
            (("A", 1), False, True),
            (("S", 0), True, False),
            (("S", 1), False, True),
        ],
        {"A": [[2, 3]], "b": [[0, 1]]},
    ),
    (
        "S -> A\nA -> B a\nA -> b\nA -> c\nB -> k\nB -> l",
        [
            (("A", 0), True, False),
            (("A", 1), False, True),
            (("B", 0), True, False),
            (("B", 1), False, True),
            (("S", 0), True, False),
            (("S", 1), False, True),
        ],
        {
            "A": [[4, 5]],
            "c": [[0, 1]],
            "l": [[2, 3]],
        },
    ),
    (
        "S -> A\nA -> B C\nB -> b\nC -> c",
        [
            (("A", 0), True, False),
            (("A", 1), False, True),
            (("A", 2), False, False),
            (("A", 3), False, False),
            (("B", 0), True, False),
            (("B", 1), False, True),
            (("C", 0), True, False),
            (("C", 1), False, True),
            (("S", 0), True, False),
            (("S", 1), False, True),
        ],
        {
            "A": [[8, 9]],
            "B": [[0, 2]],
            "C": [[3, 1]],
            "b": [[4, 5]],
            "c": [[6, 7]],
            "epsilon": [[2, 3]],
        },
    ),
]
