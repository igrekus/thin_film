from PyQt5.QtWidgets import QHBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class PlotWidget(QHBoxLayout):

    def __init__(self, parent=None, domainModel=None):
        super().__init__(parent)

        self._domainModel = domainModel
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.addWidget(self.canvas)

    def plotData(self):
        self.figure.clf()
        self.figure.gca().set_xlabel('λ, нм')
        self.figure.gca().set_ylabel('Pотр')
        self.figure.gca().set_title(f'Поляризация=s, α={self._domainModel.angle}$^\circ$')

        self.figure.gca().plot(self._domainModel.xs, self._domainModel.ys)
        self.canvas.draw()
        # print(len(self._domainModel.xs))
        # print(len(self._domainModel.ys))

    def saveImage(self):
        self.figure.savefig('out.png', dpi=300)
