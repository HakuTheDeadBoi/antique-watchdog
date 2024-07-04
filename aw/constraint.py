from dataclasses import dataclass

class Constraint:
    key: str
    value: str
    relation: str
    keep_literal: str