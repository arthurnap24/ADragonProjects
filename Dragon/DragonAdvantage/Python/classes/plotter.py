from matplotlib import pyplot as plt

# Plotter
#
# This class plots a Plot object
class Plotter( object ):

    def __init__( self ): 
        
    # The xyvals correspond to x values and y values
    # to be plotted: left to right starts from top left
    # to bottom right.
    # xyvals ([x-vals],[y-vals])
    def plot( self, xyvals, line_width, plot_label, is_subplot=True ):
        # plt.figure( self.fig_num )
        if ( not is_subplot ):
            plt.figure( self.fig_num )
            self.plot_pos = 1 #reset plot position when a new figure is created

        if ( is_subplot ):
            # must check if there is already an active figure
            plt.subplot( self.rows, self.cols, self.plot_pos )
            self.plot_pos += 1

        # must have the same number of xvals and yvals
        if ( len( xyvals[ 0 ] ) != len( xyvals[ 1 ] ) ):
            return False

        plt.plot( xyvals[ 0 ], xyvals[ 1 ], linewidth=line_width, label=plot_label )

    def show( self ):
        plt.legend()
        plt.show()
    
    def add_figure( self ):
        return
