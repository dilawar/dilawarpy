"""logger.py: 

Logging support.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import logging

def init_logger( filename = None, level = 'info'):
    logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
            datefmt='%m-%d %H:%M',
            filename= filename
            filemode='a'
            )
    console = logging.StreamHandler()
    console.setLevel( eval('logging.%s'%level.upper() ))
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logger = logging.getLogger('')
    logger.addHandler(console)
    return logger

logger = init_logger()
