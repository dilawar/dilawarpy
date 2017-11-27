# This file is originall from https://github.com/jtambasco/gnuplotpy

import os
import shutil as sh
import numpy as np
import subprocess
import re

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
    script_name = '/tmp/gnuplot_script.gpi'
    with open( script_name, 'w' ) as f:
        f.write( script )

    gnuplot_command = 'gnuplot ' + script_name

    # Don't wait.
    subprocess.Popen( gnuplot_command.split( ) )
    return True

def gnuplot_2d(x, y, filename, title='', x_label='', y_label=''):
    _, ext = os.path.splitext(filename)
    if ext != '.png':
        filename += '.png'

    gnuplot_cmds = \
    '''
    set datafile separator ","
    set term pngcairo size 30cm,25cm
    set out filename

    unset key
    set border lw 1.5
    set grid lt -1 lc rgb "gray80"

    set title "title"
    set xlabel "x_label"
    set ylabel "y_label"
    plot "filename" u 1:2 w lp pt 6 ps 0.5
    '''
    scr = _GnuplotScriptTemp(gnuplot_cmds)
    data = _GnuplotDataTemp(x, y)

    args_dict = {
        'filename': filename,
        'filename_data': data.name,
        'title': title,
        'x_label': x_label,
        'y_label': y_label
    }
    gnuplot(scr.name, args_dict)

def gnuplot_3d(x, y, z, filename, title='', x_label='', y_label='', z_label=''):
    _, ext = os.path.splitext(filename)
    if ext != '.png':
        filename += '.png'

    gnuplot_cmds = \
    '''
    set datafile separator ","
    set term pngcairo size 30cm,25cm
    set out filename

    unset key
    set border lw 1.5
    set view map

    set title title
    set xlabel x_label
    set ylabel y_label
    set zlabel z_label

    splot filename_data u 1:2:3 w pm3d
    '''
    scr = _GnuplotScriptTemp(gnuplot_cmds)
    data = _GnuplotDataTemp(x, y, z)

    args_dict = {
        'filename': filename,
        'filename_data': data.name,
        'title': title,
        'x_label': x_label,
        'y_label': y_label,
        'z_label': z_label
    }
    gnuplot(scr.name, args_dict)

def gnuplot_3d_matrix(z_matrix, filename, title='', x_label='', y_label=''):
    _, ext = os.path.splitext(filename)
    if ext != '.png':
        filename += '.png'

    gnuplot_cmds = \
    '''
    set datafile separator ","
    set term pngcairo size 30cm,25cm
    set out filename

    unset key
    set border lw 1.5
    set view map

    set title title
    set xlabel x_label
    set ylabel y_label

    splot filename_data matrix w pm3d
    '''
    scr = _GnuplotScriptTemp(gnuplot_cmds)
    data = _GnuplotDataZMatrixTemp(z_matrix)

    args_dict = {
        'filename': filename,
        'filename_data': data.name,
        'title': title,
        'x_label': x_label,
        'y_label': y_label
    }
    gnuplot(scr.name, args_dict)

def trim_pad_image(filename, padding=20):
    '''
    Trims and pads an image.

    Args:
        filename(str): The filename of the image to be
            acted on.
        padding(int): The number of pixels in padding to
            add to the image after the image has been
            trimmed.
    '''
    import subprocess
    cmd = 'convert %s -trim -bordercolor white -border %i %s' % \
            (filename, padding, filename)
    subprocess.call( cmd.split( ), shell = True )
