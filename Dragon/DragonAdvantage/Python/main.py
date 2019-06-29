import requests
import numpy
from matplotlib import pyplot as plt

API_HOST_PREFIX = 'https://api.iextrading.com/1.0/stock/aapl/chart/1d'

def function():
    x = 5
    return x

def get_symbol_chart( symbol='' ):
    if ( symbol == '' ):
        return
    
    request = requests.get( API_HOST_PREFIX )

    if ( request.status_code == requests.codes.ok ):
        return request.json()

def get_close_prices( symbol='' ):
    if ( symbol == '' ):
        return
    
    chart = get_symbol_chart( symbol )

    prices = []
    for data in chart:
        prices.append( data[ 'close' ] )

    return prices

def get_open_prices( symbol='' ):
    if ( symbol == '' ):
        return
    
    chart = get_symbol_chart( symbol )

    prices = []
    for data in chart:
        prices.append( data[ 'open' ] )

    return prices

def plot_prices( symbol='', instant_show=False ):
    if ( symbol == '' ):
        return False

    plt.plot( get_open_prices( symbol ) )

    if ( instant_show == True ):
        plt.show()
        return True

# default to 10 day sma
def get_sma_values( symbol='', interval=10, prices=[] ):
    if ( symbol == '' or prices == [] ):
        return False

    sma_values = []
    num_days = len( prices )
    for i in range( 0, num_days, interval ):
        numerator = 0
        for j in range( interval ):
            numerator += prices[ i + j ]
        sma = numerator / interval
        sma_values.append( sma )
        print( sma )

    return sma_values

def plot_sma( symbol='', prices=[], interval = 10, instant_show=False ):
    if ( symbol == '' ):
        return False

    num_days = len( prices )
    x_vals = numpy.linspace( 0, len( prices ), num = (num_days / interval) )
    plt.plot( x_vals, get_sma_values( symbol, interval, prices ) )

    if ( instant_show ):
        plt.show()
        return True

def show_graph():
    plt.show()

prices = get_open_prices( 'AAPL' )
plot_prices( 'AAPL' )
plot_sma( 'AAPL', prices )
show_graph()
