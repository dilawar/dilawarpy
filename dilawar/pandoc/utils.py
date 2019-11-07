__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2019-, Dilawar Singh"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"

import os
import re
import sys
import subprocess
from pathlib import Path

sdir_ = Path(__file__).parent

all_ = [ 'pandoc-imagine'
        , 'pandoc-crossref'
        , 'pandoc-citeproc' 
        , 'pantable'
        , sdir_ / 'dilawar.py'
        ]

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
    return [str(x) for x in cmds if x is not None]


def execute_pandoc(*args):
    """Top level command.
    """
    argStr = ' '.join(*args)
    extra = ''
    pandoc = which('pandoc')
    if re.search(r'-t\s+latex'):
        extra += ' --pdf-engine lualatex --number-section -s'
    if re.search(r'-t\s+html\S*'):
        extra += ' --self-contained --katex'
    filters = ' '.join([f'-F {f}' for f in available_pandoc_filters()])
    cmd = f'{pandoc} {filters} {extra} ' + argStr
    p = subprocess.run(cmd.split()
            , stdin=sys.stdin
            , capture_output=True
            , text=True
            )
    msg = p.stdout
    if p.returncode:
        msg += p.stderr
        print(f'ERROR FROM dilawar.pandoc:\n{msg}')
    return p.returncode

