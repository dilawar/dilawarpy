# Helpful functions.

__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2019-, Dilawar Singh"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"

import sys
import os
import numpy as np

# This one is from here:
# https://scipy-cookbook.readthedocs.io/items/Matplotlib_SigmoidalFunctions.html
def boltzman(x, xmid, tau):
    """
    evaluate the boltzman function with midpoint xmid and time constant tau
    over x
    """
    return 1. / (1. + nx.exp(-(x-xmid)/tau))
