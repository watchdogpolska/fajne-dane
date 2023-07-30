from typing import List, Any


def sanitize_group_by_args(args: List[Any]):
    # pandas strange requirement to not pass one element lists
    return args[0] if len(args) == 1 else args
