__author__ = "yourname"
__email__ = "yourname@email.com"

import math

def argmax(ls : list) -> int:
    """argmax: Returns the index i such that max(ls) == ls[i]
    """
    _m, _mi = -math.inf, 0
    for i, v in enumerate(ls):
        if v > _m:
            _m = v
            _mi = i
    return _mi
