from enum import Enum
from enum import unique
from enum import auto


@unique
class EnumMoveAndReplaceResultTypes(
        Enum):
    SUCCESS = \
        auto()

    FAILURE = \
        auto()
