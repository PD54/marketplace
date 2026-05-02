from enum import StrEnum


class ProductStock(StrEnum):
    valid = "valid"
    defect = "defect"
    not_found = "not_found"
