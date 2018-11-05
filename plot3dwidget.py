from PyQt5.QtWidgets import QHBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import LinearLocator
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from numpy import array

class Plot3DWidget(QHBoxLayout):

    def __init__(self, parent=None, domainModel=None):
        super().__init__(parent)

        self._domainModel = domainModel
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.addWidget(self.canvas)

        self.axes = self.figure.gca(projection='3d')

        self.axes.set_zlim(0, 1)
        self.axes.w_zaxis.set_major_locator(LinearLocator(6))

    def plotData(self):
        self.axes.cla()
        # self.figure.gca().set_xlabel('λ, нм')
        # self.figure.gca().set_ylabel('Pотр')
        # self.figure.gca().set_title('Поляризация=s, угол=0$^\circ$')
        #
        # self.figure.gca().plot(self._domainModel.xs, self._domainModel.ys)

        # copper
        self.axes.set_xlabel('λ, нм')
        self.axes.set_ylabel('d, нм')
        self.axes.set_zlabel('Pотр')
        self.axes.plot_surface(self._domainModel.X, self._domainModel.Y, self._domainModel.Z, cmap=cm.viridis, linewidth=0)

        self.canvas.draw()


