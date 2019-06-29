from classes.stock import Stock
from classes.plot import Plot

#timeframes = [ "1d", "1m", "3m", "6m", "1y", "2y", "5y", "ytd", "20190301" ]
#dates = [ "20190304", "20190116" ]
dates = ["6m" ]
stocks = []
# for timeframe in timeframes:
for date in dates:
    #stock = Stock( "MSFT", timeframe )
    # stock = Stock( symbol = "MSFT", date = date )
    stock = Stock( symbol = "MSFT", time_range = date, last_date = "20190304" )
    stock.fetch_chart()
    stocks.append( stock )

data_points = []
time_frame_idx = 0
for stock in stocks:
    close_prices = stock.get_close_prices()
    # print ( "close_prices: " + str(close_prices) )
    xvals = list( range( 0,len( close_prices ) ) )
    # xyvals = ( xvals,close_prices,timeframes[ time_frame_idx ] )
    xyvals = ( xvals,close_prices,dates[ time_frame_idx ] )
    data_points.append( xyvals )
    time_frame_idx += 1

plot = Plot( rows=1, cols=1, plot_name="MSFT Stock Charts" )
for xyvals in data_points:
    if ( plot.add_subplot( xyvals ) ):
        plot.plot()
    else:
        print( "In app.py, error occured")

plot.show()