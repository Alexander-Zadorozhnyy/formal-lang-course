from dataclasses import dataclass


@dataclass
class Matrix:
    start_states: set
    final_states: set
    indexes: dict
    labels: dict

    def get_state_by_index(self, index):
        for state, idx in self.indexes.items():
            if idx == index:
                return state

    def get_number_of_indexes(self):
        return len(self.indexes.keys())

    def get_number_of_labels(self):
        return len(self.labels.keys())

    def is_start(self, state):
        return state in self.start_states

    def is_final(self, state):
        return state in self.final_states
