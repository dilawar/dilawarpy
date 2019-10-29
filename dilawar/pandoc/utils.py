__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2019-, Dilawar Singh"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"

import os
import sys
import subprocess
from pathlib import Path
import logging
logger = logging.getLogger('dilawar.pandoc')
logger.setLevel(logging.INFO)

sdir_ = Path(__file__).parent

all_ = [ 'pandoc-imagine'
        , 'pandoc-crossref'
        , 'pandoc-citeproc' 
        , 'pantable'
        , sdir_ / 'dilawar.py'
        ]

def _print(*args):
    print(f'dilawar.pandoc >>> ', *args, file=sys.stderr)

# This is from  https://stackoverflow.com/a/377028/1805129
def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


def available_pandoc_filters():
    global all_
    cmds = [ which(prog) for prog in all_]
    return [x for x in cmds if x is not None]


def execute_pandoc(arglst):
    pandoc = which('pandoc')
    filters = [f'-F {x}' for x in available_pandoc_filters()]
    cmd = [pandoc] + filters + arglst
    _print(f"Executing {' '.join(cmd)}")
    proc  = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        _print(f'>>> {line}')
    return 0

