import os
import datetime
from setuptools import setup

version_ = '0.1.0'
stamp = datetime.datetime.now().strftime('%Y%m%d')
if os.environ.get('TRAVIS'):
    version_ += '.dist%s' % stamp
print( "[INFO ] Packing %s" % version_ )

with open("README.md") as f:
    readme = f.read()

setup(
    name = "dilawar",
    version = version_,
    description = "My personal utilities. See the README.md file.",
    long_description = readme,
    packages = [ "dilawar" ],
    package_dir = { "dilawar" : 'src' },
    install_requires = [ ],
    author = "Dilawar Singh",
    author_email = "dilawars@ncbs.res.in",
    url = "http://github.com/dilawar/ajgar",
    license='GPLv3'
)
