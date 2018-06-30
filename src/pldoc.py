import numpy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.artist import setp
from matplotlib.backends.backend_pdf import PdfPages

class PlFigure (object) :

    def __init__ (self, 
                  nrows = 1,
                  ncols = 1,
                  figsize = (5, 6)) :

        self.ncols = ncols
        self.current_plot = 0

        # Create a grid of plots on the figure
        self.fig, self.subplots = plt.subplots(nrows = nrows,
                                               ncols = ncols,
                                               figsize = figsize,
                                               dpi=240)
        # Adjust spacing between plots
        self.fig.subplots_adjust(wspace = 0.4, hspace = 0.4)

        i = 1
        for row in range(nrows) :
            for column in range(ncols) :
                # Add some formatting of the axis
                self.subplots[column][row].ticklabel_format(style = 'sci', 
                                                            scilimits = (0.01,100), 
                                                            axis = 'both')
                ++i

    # Get the next unused plot
    def _GetNewPlot (self) :
        column = self.current_plot % self.ncols
        row = int(self.current_plot / self.ncols)
        self.current_plot += 1
        subplot = self.subplots[column][row]

        return subplot

    # Create a bar chart from histogram data
    def AddBarChart (self,
                     histogram,
                     xaxis_label = None) :
        subplot = self._GetNewPlot()
        bins = histogram.Bins()
        title = histogram.Title()
        min, max = histogram.Range()

        # Calculate the x values and the width of each bar
        x = numpy.linspace(min, max, len(bins))
        width = (max - min) / len(bins)

        # Draw the chart
        subplot.bar(x, bins, width)
        subplot.set_title(histogram.Title())
        subplot.grid(color='grey', linestyle='-', linewidth=0.5)
        subplot.set_axisbelow(True)
        if xaxis_label :
            subplot.set_xlabel(xaxis_label)

    def show (self) :
        self.fig.show()

    def save (self, filepath, **kwargs) :
        self.fig.savefig(filepath, **kwargs)
        
