from enum import StrEnum


class Stock(StrEnum):
    valid = "valid"
    defect = "defect"
    not_found = "not_found"
