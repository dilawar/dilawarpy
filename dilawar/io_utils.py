# -*- coding: utf-8 -*-
__author__ = "Dilawar Singh"
__email__ = "dilawars@ncbs.res.in"

from pathlib import Path

# These are helper functions to store metadata to HDF5.
# Snippets originally from https://stackoverflow.com/a/29130146/1805129
def h5store(filename: Path, df, key: str = "mydata", **kwargs):
    import pandas as pd

    store = pd.HDFStore(filename, mode=kwargs.get("mode", "w"))
    store.put(key, df)
    store.get_storer(key).attrs.metadata = kwargs
    store.close()


def h5load(filename, key: str = "mydata"):
    import pandas as pd

    store = pd.HDFStore(filename)
    data = store[key]
    metadata = store.get_storer(key).attrs.metadata
    return data, metadata


save_df = h5store
load_df = h5load


def test_io_utils():
    import numpy as np
    import pandas as pd
    import tempfile

    store = tempfile.NamedTemporaryFile(suffix='.h5')
    data = np.random.rand(100, 100)
    df = pd.DataFrame(data)
    h5store(store.name, df, me="dilawar", mynum=301810)
    s, m = h5load(store.name)
    store.close()
    assert df.equals(s)
    assert m == dict(me="dilawar", mynum=301810)
