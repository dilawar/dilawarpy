# This file is originall from https://github.com/jtambasco/gnuplotpy

import os
import time
import shutil as sh
import numpy as np
import subprocess
import re
import tempfile

def _read_line(filename, line_number):
    s = None
    with open(filename, 'r') as fs:
        for i, line in enumerate(fs.readlines()):
            if i == line_number:
                s = line
    return s

class _GnuplotDeletingFile:
    def __init__(self, filename):
        self.name = filename

    def __del__(self):
        os.remove(self.name)

class _GnuplotScriptTemp(_GnuplotDeletingFile):
    def __init__(self, gnuplot_cmds):
        _GnuplotDeletingFile.__init__(self, '.tmp_gnuplot.gpi')
        with open(self.name, 'w') as fs:
            fs.write(gnuplot_cmds)

class _GnuplotDataTemp(_GnuplotDeletingFile):
    def __init__(self, *args):
        _GnuplotDeletingFile.__init__(self, '.tmp_gnuplot_data.dat')
        data = np.array(args).T
        with open(self.name, 'wb') as fs:
            np.savetxt(fs, data, delimiter=',')

class _GnuplotDataZMatrixTemp(_GnuplotDeletingFile):
    def __init__(self, z_matrix):
        _GnuplotDeletingFile.__init__(self, '.tmp_gnuplot_data_z_matrix.dat')
        with open(self.name, 'wb') as fs:
            np.savetxt(fs, z_matrix, '%.3f', delimiter=',')

#def gnuplot( script, args_dict={}, data=[]):
def gnuplot( script, **kwargs ):
    '''
    Call a Gnuplot script, passing it arguments and
    datasets.

    Args:
        script(str): The name of the Gnuplot script or the text
        args_dict(dict): A dictionary of parameters to pass
            to the script.  The `key` is the name of the variable
            that the `item` will be passed to the Gnuplot script
            with.
        data(list): A list of lists containing lists to be plotted.
            The lists can be accessed by plotting the variable
            `data` in the Gnuplot script.  The first list in the
            list of lists corresponds to the first column in data,
            and so on.
    Returns:
        str: The Gnuplot command used to call the script.
    '''

    if os.path.exists( script ):
        with open( script ) as f:
            script = f.read( )

    for k in kwargs:
        v = kwargs[k]
        script = script.replace( '@%s@' % k, v )

    # Find rest of the macros.
    for m in re.findall( r'@\S+?@', script ):
        script = script.replace( m, kwargs.get( m.replace( '@',''), '' ) ) 

    # if first argument is a long string then save the string to current
    # directory before running the command.
    # First escape all char.
    script = script.replace( r'"', r"'" ).replace( ';', '' )
    script = ';'.join( filter(None, script.split( '\n' )) );
    script += ';exit;'
    scriptName = '.gnuplot_script'
    with open( scriptName, 'w' ) as f:
        f.write( script )

    while not os.path.isfile( scriptName ):
        time.sleep( 0.0001 )

    subprocess.Popen( [ 'gnuplot', scriptName ] )
    return True

def nx_draw( graph ):
    from networkx.drawing.nx_agraph import write_dot
    fh, dotfile = tempfile.mkstemp( )
    write_dot( graph, dotfile )
    print( "[INFO ] Wrote to %s" % dotfile )
