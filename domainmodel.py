import os

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from attr import attrs, attrib
from numpy import linspace, meshgrid, array
from tmm import coh_tmm, inf, pi


@attrs
class Layer(object):
    thick = attrib()
    refract = attrib()


class DomainModel(QObject):

    dataReady = pyqtSignal()
    dataReady3d = pyqtSignal()
    layerChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._lambda1 = 400   # nm
        self._lambda2 = 700   # nm
        self._samples = 50
        self._angle = 0       # deg

        self._layers = list()

        self._thicks = list()
        self._refracts = list()
        self._lambdas = list()
        self._Rn = list()

        self.X = list()
        self.Y = list()
        self.Z = list()

    def init(self, filename='./default_layers.txt'):
        print("init domain model")
        self._layers.clear()
        if os.path.isfile(filename):
            with open(filename, 'rt', encoding='utf-8') as f:
                lines = [line.strip() for line in f.readlines()]
                if len(lines) > 2:
                    if 'inf;' in lines[0] and 'inf;' in lines[-1]:
                        for line in lines:
                            thick, refract = line.split(';')
                            if ' ' in thick:
                                print('error parsing data file', thick)
                                break
                            if thick == 'inf':
                                thick = inf
                            else:
                                thick = float(thick)
                            self._layers.append(Layer(thick=thick, refract=complex(refract)))
        else:
            self._layers = [
                Layer(thick=inf, refract=1.0 + 0j),
                Layer(thick=100.0, refract=2.78 + 0j),
                Layer(thick=100.0, refract=3.0 + 3.3j),
                Layer(thick=inf, refract=10000 + 0j),
            ]

        self._prepLists()
        self._calcReflect()
        self._calc3d(row=1)

    def _prepLists(self):
        self._thicks.clear()
        self._refracts.clear()

        for layer in self._layers:
            self._thicks.append(layer.thick)
            self._refracts.append(layer.refract)

    def _calcReflect(self):
        self._lambdas = linspace(self._lambda1, self._lambda2, self._samples)

        self._Rn.clear()
        for l in self._lambdas:
            self._Rn.append(coh_tmm('s', self._refracts, self._thicks, self._angle * pi / 180, l)['R']*100)

        self.dataReady.emit()

    def _calc3d(self, row):
        lambdas = linspace(self.lambda1, self.lambda2, self.samples)
        thicks = linspace(0, 500, self.samples)
        ts_range = [x.thick for x in self._layers]

        self.X, self.Y = meshgrid(lambdas, thicks)

        ps = list()
        for t_row, l_row in zip(self.Y, self.X):
            new_row = list()
            for t, l in zip(t_row, l_row):
                ts_range[row] = t
                new_row.append(coh_tmm('s', self._refracts, ts_range, self._angle * pi / 180, l)['R'])
            ps.append(new_row)

        self.Z = array(ps)

        self.dataReady3d.emit()

    def saveLayers(self, filename):
        with open(filename, 'wt', encoding='utf-8') as f:
            for layer in self._layers:
                line = f'{layer.thick};{str(layer.refract).strip("()")}\n'
                f.write(line)

    def newFilm(self):
        self._layers = [
            Layer(thick=inf, refract=1.0 + 0j),
            Layer(thick=inf, refract=10000 + 0j),
        ]
        self._prepLists()
        self._calcReflect()

    def addLayer(self, row: int):
        self._layers.insert(row, Layer(100.0, 1.5+0j))
        self._prepLists()
        self._calcReflect()

    def delLayer(self, row: int):
        del self._layers[row]
        # self._layers.remove(self._layers[row])
        self._prepLists()
        self._calcReflect()

    @pyqtSlot(int, float)
    def updateLayerThickness(self, row: int, value: float):
        self._layers[row].thick = value
        self._prepLists()
        self._calcReflect()

        self.layerChanged.emit(row)

    def updateLayerRefract(self, row, value):
        self._layers[row].refract = value
        self._prepLists()
        self._calcReflect()

        self.layerChanged.emit(row)

    def updateLayer(self, row, thick, refract):
        self._layers[row].thick = thick
        self._layers[row].refract = refract
        self._prepLists()
        self._calcReflect()

        self.layerChanged.emit(row)

    @property
    def angle(self):
        return self._angle

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

    @angle.setter
    def angle(self, value):
        self._angle = value
        try:
            self._calcReflect()
        except Exception as ex:
            print(ex)

