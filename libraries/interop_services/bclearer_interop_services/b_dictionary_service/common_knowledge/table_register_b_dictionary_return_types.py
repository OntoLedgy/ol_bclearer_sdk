from enum import Enum
from enum import auto


class TableRegisterBDictionaryReturnTypes(
        Enum):
    NOT_SET = \
        auto()

    TABLE_ALREADY_EXISTS = \
        auto()

    TABLE_CREATED = \
        auto()

    TABLE_ADDED = \
        auto()
