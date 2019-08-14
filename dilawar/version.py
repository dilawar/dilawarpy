import datetime
now = datetime.datetime.now().strftime('%Y%M%d')

__version__ = '0.2.%s' % now
