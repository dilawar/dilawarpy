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

float_regex_ = re.compile( r'[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?' )

def to_float( token ):
    val = token
    try:
        val = float( token )
    except Exception as e:
        pass
    return val

def find_all_floats( text ):
    """Find all floats in given string
    """
    global float_regex_
    assert type( text ) == str
    return [ to_float( m.group(0) ) for m  in float_regex_.finditer( text ) ]
