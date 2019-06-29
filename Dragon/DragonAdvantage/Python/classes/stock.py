import numpy
import requests
import threading
from enum import Enum, unique
from matplotlib import pyplot as plt
from numpy import linspace
from statistics import mean

THIN_LINE_WIDTH = 1.2
MEDIUM_LINE_WIDTH = 1.0
THICK_LINE_WIDTH = 1.5

@unique
class ResponseKeys( Enum ):
    # Only on one day:
    MINUTE = "minute"
    MARKET_AVERAGE = "marketAverage"
    MARKET_NOTIONAL = "marketNotional"
    MARKET_NUMBER_OF_TRADES = "marketNumberOfTrades"
    MARKET_OPEN = "marketOpen"
    MARKET_CLOSE = "marketClose"
    MARKET_HIGH = "marketHigh"
    MARKET_LOW = "marketLow"
    MARKET_VOLUME = "marketVolume"
    MARKET_CHANGE_OVER_TIME = "marketChangeOverTime"
    AVERAGE = "average"
    NOTIONAL = "notional"
    NUMBER_OF_TRADES = "numberOfTrades"
    SIMPLIFY_FACTOR = "simplifyFactor"

    # Available on all charts:
    HIGH = "high",
    LOW = "low",
    VOLUME = "volume",
    LABEL = "label",
    CHANGE_OVER_TIME = "changeOverTime",
    DATE = "date",
    OPEN = "open",
    CLOSE = "close",

    # Available on all charts but not 1 day
    UNADJUSTED_VOLUME = "unadjustedVolume"
    CHANGE = "change"
    CHANGE_PERCENT = "changePercent"
    VWAP = "vwap"

class Stock( object ):

    # use the date feature to pick a specific date, date is yyyymmdd
    def __init__( self, symbol, time_range="1d", date="", last_date="" ):
        # Extra information
        self.symbol = symbol
        self.time_range = time_range
        
        self.last_date = last_date

        if ( date == "" ):
            self.api_url = 'https://api.iextrading.com/1.0/stock/%s/chart/%s' % ( symbol, time_range )
        else:
            self.api_url = 'https://api.iextrading.com/1.0/stock/%s/chart/date/%s' % ( symbol, date )
            print( self.api_url )

        # Direct result from iex /stock/symbol/charts
        self.dates = []
        self.open_prices = []
        self.high_prices = []
        self.low_prices = []
        self.close_prices = []
        self.volumes = []
        self.unadjusted_volumes = []
        self.changes = []
        self.change_percents = []
        self.vwaps = []
        self.labels = []
        self.changes_over_time = []
        
        self.ema_length = 5
        self.sma_length = 5
        self.ema = []
        self.sma = []
        
        self.plotters = {
            ResponseKeys.MINUTE : ( lambda : plt.plot( self.minutes, linewidth=THIN_LINE_WIDTH, label=ResponseKeys.MINUTE.value[ 0 ] ) ),
            ResponseKeys.MARKET_AVERAGE : ( lambda : plt.plot( self.market_averages, linewidth=THIN_LINE_WIDTH, label=ResponseKeys.MARKET_AVERAGE.value[ 0 ] ) ),
            ResponseKeys.MARKET_NOTIONAL : ( lambda : plt.plot( self.market_notionals, linewidth=THIN_LINE_WIDTH, label=ResponseKeys.MARKET_NOTIONAL.value[ 0 ] ) ),
            ResponseKeys.MARKET_NUMBER_OF_TRADES : ( lambda : plt.plot( self.market_number_of_trades, linewidth=THIN_LINE_WIDTH, label=ResponseKeys.MARKET_NUMBER_OF_TRADES.value[ 0 ] ) ),
            ResponseKeys.MARKET_OPEN : ( lambda : plt.plot( self.market_opens, linewidth=THIN_LINE_WIDTH, label=ResponseKeys.MARKET_OPEN.value[ 0 ] ) ),
            ResponseKeys.MARKET_CLOSE : ( lambda : plt.plot( self.market_closes, linewidth=THIN_LINE_WIDTH, label=ResponseKeys.MARKET_CLOSE.value[ 0 ] ) ),
            ResponseKeys.MARKET_HIGH : ( lambda : plt.plot( self.market_highs, linewidth=THIN_LINE_WIDTH, label=ResponseKeys.MARKET_HIGH.value[ 0 ] ) ),
            ResponseKeys.MARKET_LOW : ( lambda : plt.plot( self.market_lows, linewidth=THIN_LINE_WIDTH, label=ResponseKeys.MARKET_LOW.value[ 0 ] ) ),
            ResponseKeys.MARKET_VOLUME : ( lambda : plt.plot( self.market_volumes, linewidth=THIN_LINE_WIDTH, label=ResponseKeys.MARKET_VOLUME.value[ 0 ] ) ),
            ResponseKeys.MARKET_CHANGE_OVER_TIME : ( lambda : plt.plot( self.market_changes_over_time, linewidth=THIN_LINE_WIDTH, label=ResponseKeys.MARKET_CHANGE_OVER_TIME.value[ 0 ] ) ),
            ResponseKeys.AVERAGE : ( lambda : plt.plot( self.averages, linewidth=THIN_LINE_WIDTH, label=ResponseKeys.AVERAGE.value[ 0 ] ) ),
            ResponseKeys.NOTIONAL : ( lambda : plt.plot( self.notionals, linewidth=THIN_LINE_WIDTH, label=ResponseKeys.NOTIONAL.value[ 0 ] ) ),
            ResponseKeys.NUMBER_OF_TRADES : ( lambda : plt.plot( self.number_of_trades, linewidth=THIN_LINE_WIDTH, label=ResponseKeys.NUMBER_OF_TRADES.value[ 0 ] ) ),
            ResponseKeys.SIMPLIFY_FACTOR : ( lambda : plt.plot( self.simplify_factors, linewidth=THIN_LINE_WIDTH, label=ResponseKeys.SIMPLIFY_FACTOR.value[ 0 ] ) ),

            # Available on all charts:
            ResponseKeys.HIGH : ( lambda : plt.plot( self.high_prices, linewidth=THIN_LINE_WIDTH, label=ResponseKeys.HIGH.value[ 0 ] ) ),
            ResponseKeys.LOW : ( lambda : plt.plot( self.low_prices, linewidth=THIN_LINE_WIDTH, label=ResponseKeys.LOW.value[ 0 ] ) ),
            ResponseKeys.VOLUME : ( lambda : plt.plot( self.volumes, linewidth=THIN_LINE_WIDTH, label=ResponseKeys.VOLUME.value[ 0 ] ) ),
            ResponseKeys.LABEL : ( lambda : plt.plot( self.labels, linewidth=THIN_LINE_WIDTH, label=ResponseKeys.LABEL.value[ 0 ] ) ),
            ResponseKeys.CHANGE_OVER_TIME : ( lambda : plt.plot( self.changes_over_time, linewidth=THIN_LINE_WIDTH, label=ResponseKeys.CHANGE_OVER_TIME.value[ 0 ] ) ),
            ResponseKeys.DATE : ( lambda : plt.plot( self.dates, linewidth=THIN_LINE_WIDTH, label=ResponseKeys.DATE.value[ 0 ] ) ),
            ResponseKeys.OPEN : ( lambda : plt.plot( self.open_prices, linewidth=THIN_LINE_WIDTH, label=ResponseKeys.OPEN.value[ 0 ] ) ),
            ResponseKeys.CLOSE : ( lambda : plt.plot( self.close_prices, linewidth=THIN_LINE_WIDTH, label=ResponseKeys.CLOSE.value[ 0 ] ) ),

            # Available on all charts but not 1 day
            ResponseKeys.UNADJUSTED_VOLUME : ( lambda : plt.plot( self.unadjusted_volumes, linewidth=THIN_LINE_WIDTH, label=ResponseKeys.UNADJUSTED_VOLUME.value[ 0 ] ) ),
            ResponseKeys.CHANGE : ( lambda : plt.plot( self.changes, linewidth=THIN_LINE_WIDTH, label=ResponseKeys.CHANGE.value[ 0 ] ) ),
            ResponseKeys.CHANGE_PERCENT : ( lambda : plt.plot( self.change_percents, linewidth=THIN_LINE_WIDTH, label=ResponseKeys.CHANGE_PERCENT.value[ 0 ] ) ),
            ResponseKeys.VWAP : ( lambda : plt.plot( self.vwaps, linewidth=THIN_LINE_WIDTH, label=ResponseKeys.VWAP.value[ 0 ] ) )
        }

    def format_date( self ):
        return self.last_date[:4] + '-' + self.last_date[4:6] + '-' + self.last_date[6:]

    def is_date_ge( self, date ):
        print( "is_date_greater, date=" + date )
        if ( self.time_range == "1d" ):
            return False
        
        date_year = int( date[:4] )
        date_month = int( date[5:7] )
        date_day = int( date[8:] )

        last_date_year = int( self.last_date[:4] )
        last_date_month = int( self.last_date[4:6] )
        last_date_day = int( self.last_date[6:] )
        
        if ( date_year < last_date_year ):
            return False
        elif ( date_year == last_date_year ):
            if ( date_month < last_date_month ):
                return False
            elif ( date_month == last_date_month ):
                if ( date_day < last_date_day ):
                    return False
        return True

    ####################################################
    #       IEX API INTERFACE
    ####################################################
    def fetch_chart( self ):
        request = requests.get( self.api_url )
        if ( request.status_code == requests.codes.ok ):
            chart = request.json()
            for data in chart:
                date = self.try_get_date( data )
                if ( self.is_date_ge( date ) ):
                    # Date limit is reached
                    return True
                self.try_fetch_high_price( data )
                self.try_fetch_low_price( data )
                self.try_fetch_close_price( data )
                self.try_fetch_open_price( data )
                self.try_fetch_volume( data )
                self.try_fetch_unadjusted_volume( data )
                self.try_fetch_change( data )
                self.try_fetch_change_percent( data )
                self.try_fetch_vwap( data )
                self.try_fetch_label( data )
                self.try_fetch_change_over_time( data )
            return True
        else:
            return False

    def compute_moving_average( self, n ):
        self.close_prices

    def try_get_val( self, response_key, data ):
        try:
            # Will throw an exception if key is not in the chart
            value = data[ response_key[ 0 ] ]            
            return value
        except:
            # Integrate a logger
            print( response_key + " is not available in the chart as a response key." )
        return False

    def try_get_date( self, data ):
        value = self.try_get_val( ResponseKeys.DATE.value, data )
        if ( value ):
            return value
        return False

    def try_fetch_high_price( self, data ):
        value = self.try_get_val( ResponseKeys.HIGH.value, data )
        if ( value ):
            self.high_prices.append( value )
        
    def try_fetch_low_price( self, data ):
        value = self.try_get_val( ResponseKeys.LOW.value, data )
        if ( value ):
            self.low_prices.append( value )
    
    def try_fetch_close_price( self, data ):
        value = self.try_get_val( ResponseKeys.CLOSE.value, data )
        if ( value ):
            self.close_prices.append( value )

    def try_fetch_open_price( self, data ):
        value = self.try_get_val( ResponseKeys.OPEN.value, data )
        if ( value ):
            self.open_prices.append( value )

    def try_fetch_volume( self, data ):
        value = self.try_get_val( ResponseKeys.VOLUME.value, data )
        if ( value ):
            self.volumes.append( value )
    
    def try_fetch_unadjusted_volume( self, data ):
        value = self.try_get_val( ResponseKeys.UNADJUSTED_VOLUME.value, data )
        if ( value ):
            self.unadjusted_volumes.append( value )
    
    def try_fetch_change( self, data ):
        value = self.try_get_val( ResponseKeys.CHANGE.value, data )
        if ( value ):
            self.chnages.append( value )
    
    def try_fetch_change_percent( self, data ):
        value = self.try_get_val( ResponseKeys.CHANGE_PERCENT.value, data )
        if ( value ):
            self.change_percents.append( value )

    def try_fetch_vwap( self, data ):
        value = self.try_get_val( ResponseKeys.VWAP.value, data )
        if ( value ):
            self.vwaps.append( value )

    def try_fetch_label( self, data ):
        value = self.try_get_val( ResponseKeys.LABEL.value, data )
        if ( value ):
            self.labels.append( value )
    
    def try_fetch_change_over_time( self, data ):
        value = self.try_get_val( ResponseKeys.CHANGE_OVER_TIME.value, data )
        if ( value ):
            self.changes_over_time.append( value )

    ####################################################
    #       GETTERS
    ####################################################
    def get_open_prices( self ):
        return self.open_prices

    def get_high_prices( self ):
        return self.high_prices

    def get_low_prices( self ):
        return self.low_prices
    
    def get_close_prices( self ):
        return self.close_prices

    def get_volumes( self ):
        return self.volumes
    
    def get_unadjusted_volumes( self ):
        return self.unadjusted_volumes
    
    def get_changes( self ):
        return self.changes
    
    def get_change_percents( self ):
        return self.change_percents

    def get_vwaps( self ):
        return self.vwaps

    def get_labels( self ):
        return self.labels
    
    def get_changes_over_time( self ):
        return self.changes_over_time

    def get_sma( self, n=5 ):
        self.sma_length = n
        lim = len( self.close_prices )
        avgs = []
        for i in range( 0, lim, n ):
            avgs.append( mean( self.close_prices[ i:(i+n) ] ) )
        
        self.sma = avgs
        return avgs
    
    def get_ema( self, n=5 ):
        self.ema_length = n
        lim = len( self.close_prices )
        weighted_close_prices = []

        # Use i/2 as weight to prevent really big numbers
        for i in range( lim ):
            weighted_close_prices.append( float( i/2 ) * self.close_prices[i] )

        avgs = []
        for i in range( 0, lim, n ):
            avgs.append( mean( weighted_close_prices[ i:(i+n) ] ) )
        
        self.ema = avgs
        return avgs

    ####################################################
    #       SETTERS
    ####################################################
    
    # Either set range or date
    def set_range_xor_date( time_interval="", date="" ):
        return

    ####################################################
    #       UTILITIES
    ####################################################
    def plot_key( self, key ):
        try:
            self.plotters[ key ]()
        except:
            print( "error encountered while plotting" )
            return False

    # if wait is set, show will not be invoked right away
    def plot( self, filters=[ "open" ], wait=False ):
        fig = plt.figure( figsize=(12,6), facecolor='tab:grey' )
        try:
            response_keys = list( ResponseKeys )
            for key in response_keys:
                key_str = key.value[ 0 ]
                if ( key_str in filters ):
                    self.plot_key( key )

            if ( self.sma != [] ):
                lim = len( self.close_prices )
                sma_x_vals = linspace( 0, lim, num = int( lim / self.sma_length ) + 1 ) # number of close price / interval is the number of sma points
                plt.plot( sma_x_vals, self.sma, linewidth=THIN_LINE_WIDTH, label=("SMA %s day" % self.sma_length) )
            if ( self.ema != [] ):
                lim = len( self.close_prices )
                ema_x_vals = linspace( 0, lim, num = int( lim / self.ema_length ) + 1 ) # number of close price / interval is the number of sma points
                plt.plot( ema_x_vals, self.sma, linewidth=THIN_LINE_WIDTH, label=("EMA %s day" % self.ema_length) )

            if ( not wait ):
                plt.legend()
                plt.show()
            return True
        except:
            print( "exception in plot" )
            return False
