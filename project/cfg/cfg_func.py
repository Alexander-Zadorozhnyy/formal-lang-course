from pathlib import Path
from typing import Union

from pyformlang.cfg import CFG, Variable


def read_context_free_grammar(path_to_grammar: Path, start_variable: str) -> CFG:
    with open(path_to_grammar, "r") as f:
        text = "\n".join(f.readlines())
        return CFG.from_text(text, Variable(start_variable))


def convert_cfg_to_weak_cnf(cfg: Union[Path, CFG], start_variable: str) -> CFG:

    if isinstance(cfg, Path):
        cfg = read_context_free_grammar(cfg, start_variable)

    if cfg.is_normal_form():
        return cfg

    updated_cfg = (
        cfg.remove_useless_symbols()
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )

    productions = set(
        updated_cfg._decompose_productions(
            updated_cfg._get_productions_with_only_single_terminals()
        )
    )

    return CFG(
        variables=updated_cfg.variables,
        terminals=updated_cfg.terminals,
        start_symbol=updated_cfg.start_symbol,
        productions=productions,
    )
