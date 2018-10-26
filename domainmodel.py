import matplotlib.pyplot as plt

from PyQt5.QtCore import QObject, pyqtSignal
from attr import attrs, attrib
from numpy import linspace, ndarray
from tmm import coh_tmm, inf


@attrs
class Layer(object):
    thick = attrib()
    refract = attrib()


class DomainModel(QObject):

    dataReady = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self._lambda1 = 300   # nm
        self._lambda2 = 800   # nm
        self._samples = 100

        self._layers = list()

        self._thicks = list()
        self._refracts = list()
        self._lambdas = list()
        self._Rn = list()

    def init(self):
        print("init domain model")

        self._layers = [
            Layer(thick=inf, refract=1),
            Layer(thick=100, refract=2.78),
            Layer(thick=inf, refract=1000),
        ]

        self._prepLists()
        self._calcReflect()

    def _prepLists(self):
        self._thicks.clear()
        self._refracts.clear()

        for layer in self._layers:
            self._thicks.append(layer.thick)
            self._refracts.append(layer.refract)

    def _calcReflect(self):
        print('calc reflect')
        self._lambdas = linspace(self._lambda1, self._lambda2, self._samples)

        self._Rn.clear()
        for l in self._lambdas:
            self._Rn.append(coh_tmm('s', self._refracts, self._thicks, 0, l)['R'])

        self.dataReady.emit()

    def addLayer(self, row: int):
        self._layers.insert(row, Layer(100, 1.5))
        self._prepLists()
        self._calcReflect()

    def delLayer(self, row: int):
        self._layers.remove(self._layers[row])
        self._prepLists()
        self._calcReflect()

    @property
    def xs(self):
        return self._lambdas

    @property
    def ys(self):
        return self._Rn

    @property
    def lambda1(self):
        return self._lambda1

    @property
    def lambda2(self):
        return self._lambda2

    @property
    def samples(self):
        return self._samples

    @lambda1.setter
    def lambda1(self, value):
        self._lambda1 = value
        self._calcReflect()

    @lambda2.setter
    def lambda2(self, value):
        self._lambda2 = value
        self._calcReflect()

    @samples.setter
    def samples(self, value):
        self._samples = value
        self._calcReflect()



