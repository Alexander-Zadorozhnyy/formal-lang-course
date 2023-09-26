from dataclasses import dataclass


@dataclass
class Matrix:
    start_states: set
    final_states: set
    indexes: dict
    labels: dict
