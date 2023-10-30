from dataclasses import dataclass
from pathlib import Path
from typing import Union

from pyformlang.cfg import Variable

from project.ecfg.ecfg import ECFG


@dataclass
class RSM:
    start: Variable
    automatas: dict

    @staticmethod
    def convert_ecfg_to_rsm(ecfg: Union[str, Path, ECFG], start_symbol: str):
        ecfg = (
            ECFG.convert_str_to_ecfg(ecfg, start_symbol)
            if isinstance(ecfg, str)
            else ECFG.convert_file_to_ecfg(ecfg, start_symbol)
            if isinstance(ecfg, Path)
            else ecfg
        )

        automatas = {
            key: automata.to_epsilon_nfa() for key, automata in ecfg.productions.items()
        }

        return RSM(start=ecfg.start_symbol, automatas=automatas)

    def minimize(self):
        return RSM(
            start=self.start,
            automatas={
                key: automata.minimize() for key, automata in self.automatas.items()
            },
        )
