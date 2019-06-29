from matplotlib import pyplot as plt

LINEWIDTH = 1.0

# Plot
#
# This class represents a figure, a figure can have multiple
# subplots.
class Plot( object ):

    def __init__( self, rows=1, cols=1, max_subplots=1, plot_name="Generic Plot", figsize=(16,6) ):
        self.rows = rows
        self.cols = cols
        self.max_subplots = max_subplots
        self.current_subplots = 0
        self.plot_name = plot_name

        # data points is a list of xs,ys,label triples
        self.data_points = []
        if ( figsize == "max" ):
            mng = plt.get_current_fig_manager()
            mng.frame.Maximize(True)
        else:
            plt.figure( plot_name, figsize=figsize )

        


    # add_subplot()
    #
    # Returns True if adding the data point is successful, which 
    # means that the max number of subplots is not yet exceeded.
    def add_subplot( self, xs, ys, label="value" ):
        if ( self.current_subplots >= self.max_subplots):
            print( "Plot::add_subplot, maximum number of subplots exceeded" )
            return False
        self.data_points.append( (xs,ys,label) )
        self.max_subplots += 1
        return True

    def add_subplot( self, xyvals ):
        if ( self.current_subplots >= self.max_subplots):
            print( "Plot::add_subplot, maximum number of subplots exceeded" )
        if ( len(xyvals) == 3 ):
            self.data_points.append( xyvals )
            self.max_subplots += 1
            return True
        print( "Plot::add_subplot, length of xyvals invalid" )
        return False

    def get_subplot( self, subplot_index=0 ):
        try:
            return self.data_points[ subplot_index ]
        except IndexError as error:
            print( "Plot::get_subplot, subplot_index invalid" )
            return False

    def get_subplots( self ):
        return self.data_points

    def set_subplot( self, subplot_index=0, xyvals=([],[],"val") ):
        try:
            if ( len(xyvals) == 3 ):
                print( "Plot::set_subplot, length of xyvals invalid" )
                self.data_points[ subplot_index ] = xyvals
                return True
        except IndexError as error:
            print( "Plot::set_subplot, subplot_index invalid" )
        return False

    def set_subplots( self, data_points ):
        if ( self.validate_xyvals( data_points )):
            self.current_subplots = len( data_points )
            self.data_points = data_points
            return True
        return False

    def validate_xyvals( self, xyvals ):
        for ( triple ) in xyvals:
            if ( len( triple ) != 3 ):
                print( "Plot::set_subplot, xyvals need labels" )
                return False
        return True

    def plot( self ):
        try:
            idx = 1
            for ( xs,ys,label ) in self.data_points:
                subplot = plt.subplot( self.rows, self.cols, idx, label=label )
                subplot.set_title( label )
                plt.plot( xs, ys, linewidth=LINEWIDTH )
                idx += 1
        except BaseException as error:
            print( "Plot::plot, unexpected error occured: " + str(error) )
            return False

    def show( self ):
        plt.show()

# plot = Plot( rows = 1, cols = 2 )
# xyvals1 = ( [1,2,3,4,5],[1,2,3,2,1],"xyvals1" )
# xyvals2 = ( [1,2,3,4,5],[1,2,3,2,1],"xyvals2" )
# plot.add_subplot( xyvals1 )
# plot.add_subplot( xyvals2 )
# plot.plot()
# plot.show()