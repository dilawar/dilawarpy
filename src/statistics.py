"""statistics.py: 
"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"


def histogram( vec, bins = 10 ):
    """Histogram of given vector.
    """
    a, b = min( vec ), max( vec )
    s = ( b - a ) / float( bins )
    buckets = [ a + s * x for x in range( bins ) ]
    buckets.append( b )

    hist = [ 0 ] * bins
    for i, bb in enumerate( buckets[1:] ):
        aa = buckets[i]
        for x in vec:
            if x >= aa and x < bb:
                hist[i] += 1

    return hist, buckets


def test( ):
    print( histogram( [1,2,13,32,3,1,3,9,8,3,31] ) )

if __name__ == '__main__':
    test()
