# region [Imports]

from enum import Enum
from functools import total_ordering
# endregion[Imports]


class RequestStatus(Enum):
    Ok = 200
    NotFound = 404
    NotAuthorized = 401


if __name__ == '__main__':
    pass
