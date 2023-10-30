from dataclasses import dataclass
from pathlib import Path
from typing import Union

from pyformlang.cfg import CFG, Variable
from pyformlang.regular_expression import Regex

from project.cfg.cfg_func import read_context_free_grammar


@dataclass
class ECFG:
    variables: set
    start_symbol: Variable
    productions: dict[Variable, Regex]

    @staticmethod
    def convert_cfg_to_ecfg(cfg: Union[CFG, Path], start_symbol: str = "S"):

        if isinstance(cfg, Path):
            cfg = read_context_free_grammar(cfg, start_symbol)

        start_symbol = cfg.start_symbol if cfg.start_symbol else Variable(start_symbol)

        variables = set(cfg.variables) | {start_symbol}
        productions = {production.head: Regex("") for production in cfg.productions}

        productions = {
            production.head: productions[production.head].union(
                Regex(
                    ".".join(var.value for var in production.body)
                    if len(production.body)
                    else " "
                )
            )
            for production in cfg.productions
        }

        return ECFG(
            variables=variables, start_symbol=start_symbol, productions=productions
        )

    @staticmethod
    def convert_str_to_ecfg(str_ecfg: str, start_symbol: str = "S"):
        lines = list(filter(lambda x: x != "", map(str.strip, str_ecfg.splitlines())))

        variables = set()
        productions = {}

        for line in lines:
            split_line = line.split("->")

            if len(split_line) != 2:
                raise ValueError("Invalid production structure!")

            head, body = Variable(split_line[0].replace(" ", "")), Regex(split_line[1])
            variables |= {head}
            productions[head] = body

        return ECFG(
            variables=variables,
            start_symbol=Variable(start_symbol),
            productions=productions,
        )

    @staticmethod
    def convert_file_to_ecfg(file_path: Path, start_symbol):
        with open(file_path) as file:
            return ECFG.convert_str_to_ecfg(file.read(), start_symbol=start_symbol)
