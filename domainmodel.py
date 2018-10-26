import matplotlib.pyplot as plt

from PyQt5.QtCore import QObject, pyqtSignal, QStringListModel
from attr import attrs, attrib
from numpy import linspace
from scipy.constants import degree
from tmm import coh_tmm, unpolarized_RT, inf


@attrs
class Layer(object):
    thick = attrib()
    refract = attrib()


class DomainModel(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)

        self._layers = list()

    def init(self):
        print("init domain model")

        self._layers = [
            Layer(thick=inf, refract=1),
            Layer(thick=100, refract=1.46),
            Layer(thick=100, refract=2.88),
            Layer(thick=100, refract=1.46),
            Layer(thick=100, refract=2.88),
            Layer(thick=500, refract=1.79),
            Layer(thick=100, refract=1.46),
            Layer(thick=100, refract=2.88),
            Layer(thick=100, refract=1.46),
            Layer(thick=100, refract=2.88),
            Layer(thick=inf, refract=1000),
        ]

    def getFilm(self):
        pass

    def calcReflect(self):
        print('calc reflect')

        thick_list = list()
        refract_list = list()

        for layer in self._layers:
            thick_list.append(layer.thick)
            refract_list.append(layer.refract)

        lnms = linspace(300, 800, num=400)
        Rn = list()
        for l in lnms:
            Rn.append(coh_tmm('s', refract_list, thick_list, 0, l)['R'])

        plt.figure()
        plt.plot(lnms, Rn, 'blue')
        plt.xlabel('длина волны')
        plt.ylabel('Отраженная часть')
        # plt.xlim(300, 700)
        plt.title('Отражение неполяр. пучка при 0$^\circ$ (син)')
        plt.savefig('out_light.png', dpi=300)

        print('calc done')



