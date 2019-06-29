from stock import Stock
from threading import Thread
from time import sleep

class DataReplayer( object ):
    
    def __init__( self, symbol, date ):
        self.stock = Stock( symbol=symbol, date=date )
        self.bars = []
        self.bar_idx = 0
        self.stock.fetch_chart()

    def calculate_bars( self ):
        open_prices = self.stock.get_open_prices()
        close_prices = self.stock.get_close_prices()
        low_prices = self.stock.get_low_prices()
        high_prices = self.stock.get_high_prices()

        # theoretically these price collections have the same length
        lim = len( open_prices )
        for i in range( lim ):
            bar = { 'open': open_prices[ i ],
                    'close': close_prices[ i ],
                    'low': low_prices[ i ],
                    'high': high_prices[ i ] 
                  }
            self.bars.append( bar )

    def print_next_bar( self ):
        lim = len( self.bars )
        for i in range( lim ):
            print( self.bars[ self.bar_idx ] )
            self.bar_idx += 1
            sleep( 1 )

    def start_replay( self ):
        self.calculate_bars()
        thread = Thread( target=self.print_next_bar )
        thread.start()
        thread.join()

player = DataReplayer( 'X', '20190304' )
player.start_replay()