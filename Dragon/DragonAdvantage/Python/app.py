from classes.stock import Stock
from classes.plot import Plot

#timeframes = [ "1d", "1m", "3m", "6m", "1y", "2y", "5y", "ytd", "20190301" ]
dates = [ "20190304", "20190116" ]
stocks = []
# for timeframe in timeframes:
for date in dates:
    #stock = Stock( "MSFT", timeframe )
    # stock = Stock( symbol = "MSFT", date = date )
    stock = Stock( symbol = "MSFT", date = date )
    stock.fetch_chart()
    stocks.append( stock )

data_points = []
time_frame_idx = 0
for stock in stocks:
    close_prices = stock.get_close_prices()
    print ( "close_prices: " + str(close_prices) )
    xvals = list( range( 0,len( close_prices ) ) )
    # xyvals = ( xvals,close_prices,timeframes[ time_frame_idx ] )
    xyvals = ( xvals,close_prices,dates[ time_frame_idx ] )
    data_points.append( xyvals )
    time_frame_idx += 1

plot = Plot( rows=2, cols=4, plot_name="MSFT Stock Charts" )
for xyvals in data_points:
    if ( plot.add_subplot( xyvals ) ):
        plot.plot()
    else:
        print( "In app.py, error occured")

plot.show()