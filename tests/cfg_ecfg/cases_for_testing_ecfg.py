from pyformlang.cfg import Variable
from pyformlang.regular_expression import Regex

start_symbol = "S"

ecfg_cases = [
    ("S -> epsilon", {"S"}, {Variable("S"): Regex("$")}),
    ("S -> endpoint", {"S"}, {Variable("S"): Regex("endpoint")}),
    ("S -> $ | m", {"S"}, {Variable("S"): Regex("$ | m")}),
    ("S -> S | S", {"S"}, {Variable("S"): Regex("S | S")}),
    ("S -> x", {"S"}, {Variable("S"): Regex("x")}),
    ("S -> x y z", {"S"}, {Variable("S"): Regex("x y z")}),
    ("S -> x y S", {"S"}, {Variable("S"): Regex("x y S")}),
    ("S -> (x y) S", {"S"}, {Variable("S"): Regex("(x y) S")}),
    ("S -> [a b]", {"S"}, {Variable("S"): Regex("[a b]")}),
    ("S -> a . b", {"S"}, {Variable("S"): Regex("a . b")}),
    ("S -> a | b", {"S"}, {Variable("S"): Regex("a | b")}),
    ("S -> a *", {"S"}, {Variable("S"): Regex("a *")}),
    ("S -> a ?", {"S"}, {Variable("S"): Regex("a ?")}),
    ("S -> a +", {"S"}, {Variable("S"): Regex("a +")}),
    (
        "S -> T ? S \n T -> S | T",
        {"S", "T"},
        {Variable("S"): Regex("T ? S"), Variable("T"): Regex("S | T")},
    ),
    (
        "S -> a . (b | A) \n A -> S | S | k",
        {"S", "A"},
        {Variable("S"): Regex("a . (b | A)"), Variable("A"): Regex("S | S | k")},
    ),
    (
        "S -> x K \n K -> y z M \n M -> epsilon",
        {"S", "K", "M"},
        {
            Variable("S"): Regex("x K"),
            Variable("K"): Regex("y z M"),
            Variable("M"): Regex("$"),
        },
    ),
    ("S -> x * y", {"S"}, {Variable("S"): Regex("x * y")}),
    (
        "S -> A ? B \n A -> m p \n B -> p q | S",
        {"S", "A", "B"},
        {
            Variable("S"): Regex("A ? B"),
            Variable("A"): Regex("m p"),
            Variable("B"): Regex("p q | S"),
        },
    ),
    (
        "S -> q w (A) e r t {B} y u k {B} \n A -> m p | v c \n B -> cool | S",
        {"S", "A", "B"},
        {
            Variable("S"): Regex("q w (A) e r t {B} y u k {B}"),
            Variable("A"): Regex("m p | v c"),
            Variable("B"): Regex("cool | S"),
        },
    ),
]
