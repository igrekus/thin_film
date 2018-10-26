from PyQt5.QtCore import pyqtSlot
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

    @pyqtSlot()
    def plotData(self):
        self.figure.clf()
        self.figure.gca().set_xlabel('Длина волны')
        self.figure.gca().set_ylabel('Отраженная часть')
        self.figure.gca().set_title('Отражение неполяр. пучка при 0$^\circ$ (син)')
        # plt.savefig('out_light.png', dpi=300)
        #
        self.figure.gca().plot(self._domainModel.xs, self._domainModel.ys)
        self.canvas.draw()
        # print(len(self._domainModel.xs))
        # print(len(self._domainModel.ys))


