"""text_processing.py: 

Text processing functions.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2016, Dilawar Singh"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import re

float_regex = re.compile( r'[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?' )

def find_all_floats( x ):
    """Find all floats in given string
    """
    return float_regex.findall( x )
