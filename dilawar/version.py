import datetime
now = datetime.datetime.now().strftime('%Y%M%d')

__version__ = '0.4.%s' % now
