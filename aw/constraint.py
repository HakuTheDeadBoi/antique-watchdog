from dataclasses import dataclass

@dataclass
class Constraint:
    """
    Represents a constraint with attributes describing a key-value relation.

    Attributes:
        key (str): Record attribute name targeted with this constraint. Usage: getattr(record_inst, constraint_inst.key).
        value (str): The value associated with constraint record_inst need to meet to pass.
        relation (str): The relation between record_inst attribute and constraint_inst.value
        asciize (bool, optional): If True, normalize the value to ASCII characters (default is True).
    """
    id: int
    key: str
    value: str
    relation: str
    asciize: bool = True