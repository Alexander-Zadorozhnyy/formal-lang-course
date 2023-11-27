from dataclasses import dataclass
from pathlib import Path
from typing import Union, Type

from pyformlang.cfg import Variable
from pyformlang.finite_automaton import State
from scipy.sparse import dok_matrix, lil_matrix, csr_matrix, csc_matrix

from project.ecfg.ecfg import ECFG
from project.matrix.matrix import Matrix


@dataclass
class RSM:
    start_symbol: Variable
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

        return RSM(start_symbol=ecfg.start_symbol, automatas=automatas)

    def minimize(self):
        return RSM(
            start_symbol=self.start_symbol,
            automatas={
                key: automata.minimize() for key, automata in self.automatas.items()
            },
        )

    def get_binary_matrix(
        self,
        typed_matrix: Union[
            Type[lil_matrix], Type[dok_matrix], Type[csr_matrix], Type[csc_matrix]
        ],
    ) -> Matrix:
        states, start_states, final_states = set(), set(), set()
        for v, dfa in self.automatas.items():
            for s in dfa.states:
                state = State((v, s.value))
                states.add(state)
                if s in dfa.start_states:
                    start_states.add(state)
                if s in dfa.final_states:
                    final_states.add(state)
        states = list(states)
        states.sort(key=lambda state: (state.value[0].value, state.value[1]))

        indexes = {state: index for index, state in enumerate(states)}
        labels = dict()

        for v, dfa in self.automatas.items():
            for state_from, transitions in dfa.to_dict().items():
                for label, states_to in transitions.items():
                    states_to = states_to if isinstance(states_to, set) else {states_to}
                    for state_to in states_to:
                        if label not in labels:
                            labels[label] = typed_matrix(
                                (len(states), len(states)), dtype=bool
                            )

                        i = indexes[State((v, state_from.value))]
                        j = indexes[State((v, state_to.value))]
                        labels[label][i, j] = True
        return Matrix(
            start_states=start_states,
            final_states=final_states,
            indexes=indexes,
            labels=labels,
        )
