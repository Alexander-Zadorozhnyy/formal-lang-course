start_symbol = "S"

ecfg_cases = [
    ("S -> epsilon", {"S"}, {"S": ""}),
    ("S -> endpoint", {"S"}, {"S": ""}),
    ("S -> x", {"S"}, {"S": "x"}),
    ("S -> x y S", {"S"}, {"S": "x y"}),
    ("S -> (x y) S", {"S"}, {"S": "(x y)"}),
    ("S -> [a b]", {"S"}, {"S": "[a b]"}),
    (
        "S -> x K \n K -> y z M \n M -> epsilon",
        {"S", "K", "M"},
        {"S": "x", "K": "y z", "M": ""},
    ),
]
