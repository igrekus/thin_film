import datetime
import os

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from domainmodel import DomainModel
from doublespinslide import DoubleSpinSlide
from layermodel import LayerModel
from mytools.mapmodel import MapModel
from plot3dwidget import Plot3DWidget
from plotwidget import PlotWidget
from spinslide import SpinSlide


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self._filePath = './'
        self._screenshotIndex = 0

        # create instance variables
        self._ui = uic.loadUi("mainwindow.ui", self)

        self._ui.spinSlideAngle = SpinSlide(v_min=0.0, v_max=90, v_current=0, suffix=' °')
        self._ui.gridControl.addLayout(self._ui.spinSlideAngle, 0, 1)
        self._ui.spinSlideThick = DoubleSpinSlide(v_min=0.0, v_max=1000, v_current=100, decimals=2, suffix=' нм')
        self._ui.gridControl.addLayout(self._ui.spinSlideThick, 1, 1)
        self._ui.spinSlideRefractRe = DoubleSpinSlide(v_min=0.001, v_max=100.000, v_current=0.0, decimals=3)
        self._ui.gridControl.addLayout(self._ui.spinSlideRefractRe, 2, 1)
        self._ui.spinSlideRefractIm = DoubleSpinSlide(v_min=0.000, v_max=10.000, v_current=0.0, decimals=3)
        self._ui.gridControl.addLayout(self._ui.spinSlideRefractIm, 3, 1)

        self._domainModel = DomainModel(self)
        self._layerModel = LayerModel(parent=self, domainModel=self._domainModel)
        self._labels = {
            0: 'Воздух',
            1: 'Зеркало',
            2: 'Матовая пов-ть'
        }
        self._mats = {
            0: 1 + 0j,
            1: 100 + 0j,
            2: 3 + 3j,
        }
        self._materialModel = MapModel(parent=self, data=self._labels, sort=True)

        self._plotWidget = PlotWidget(parent=self, domainModel=self._domainModel)
        self._plot3dWidget = Plot3DWidget(parent=self, domainModel=self._domainModel)

        self._ui.framePlot.setLayout(self._plotWidget)
        self._ui.frame3d.setLayout(self._plot3dWidget)

        self._init()

    def _init(self):
        self._domainModel.init()
        self._layerModel.init()
        self._loadPresets()
        self._materialModel.initModel(self._labels)

        self._ui.tableLayer.setModel(self._layerModel)
        self._ui.comboMaterial.setModel(self._materialModel)

        self.setupSignals()

        self.updateControls()

        self._plotWidget.plotData()

    def _loadPresets(self):
        name = './presets.txt'
        self._mats.clear()
        self._labels.clear()
        if os.path.isfile(name):
            with open(file=name, mode='rt', encoding='utf-8') as f:
                for index, line in enumerate(f.readlines()):
                    if line:
                        mat, label = line.strip().split(';')
                        self._mats[index] = complex(mat)
                        self._labels[index] = label

    def setupSignals(self):

        self._ui.btnAddLayer.clicked.connect(self.onBtnAddLayerClicked)
        self._ui.btnDelLayer.clicked.connect(self.onBtnDelLayerClicked)
        self._ui.btnSaveImage.clicked.connect(self.onBtnSaveImageClicked)

        self._ui.spinLambda1.editingFinished.connect(self.onLambda1Changed)
        self._ui.spinLambda2.editingFinished.connect(self.onLambda2Changed)
        self._ui.spinSamples.editingFinished.connect(self.onSamplesChanged)

        self._domainModel.dataReady.connect(self._plotWidget.plotData)
        self._domainModel.dataReady3d.connect(self._plot3dWidget.plotData)
        self._domainModel.layerChanged.connect(self._layerModel.updateLayer)

        self._ui.spinSlideThick.valueChanged.connect(self.onSpinSlideThickChanged)
        self._ui.spinSlideRefractRe.valueChanged.connect(self.onSpinSlideRefractReChanged)
        self._ui.spinSlideRefractIm.valueChanged.connect(self.onSpinSlideRefractImChanged)
        self._ui.spinSlideAngle.valueChanged.connect(self.onSpinSlideAngleChanged)

        self._ui.tableLayer.selectionModel().selectionChanged.connect(self.onTableLayerSelectionChanged)

        self._layerModel.layerEdited.connect(self._domainModel.updateLayerThickness)

    def refreshView(self):
        self._ui.tableLayer.resizeColumnsToContents()

    # ui events
    def hasSelection(self, msg: str):
        if not self._ui.tableLayer.selectionModel().hasSelection():
            print(msg)
            return False
        return True

    def onBtnAddLayerClicked(self):
        if not self.hasSelection('select layer to add past to'):
            return

        selectedIndex = self._ui.tableLayer.selectionModel().selectedIndexes()[1]

        targetRow = selectedIndex.row() + 1
        if targetRow == self._ui.tableLayer.model().rowCount():
            targetRow = targetRow - 1

        try:
            self._domainModel.addLayer(targetRow)
            self._layerModel.init()
        except Exception as ex:
            print(ex)

    def onBtnDelLayerClicked(self):
        if not self.hasSelection('select layer to delete'):
            return

        selectedIndex = self._ui.tableLayer.selectionModel().selectedIndexes()[1]
        if selectedIndex.data(Qt.DisplayRole) == 'inf':
            print('can\'t delete inf layer')
            return

        row = selectedIndex.row()
        print('remove row', row)

        self._domainModel.delLayer(selectedIndex.row())
        self._layerModel.init()

    @pyqtSlot()
    def on_actLoad_triggered(self):
        filename, _ = QFileDialog.getOpenFileName(parent=self, caption='Открыть файл...',
                                                  directory=self._filePath, filter='Text (*.txt)')

        self._filePath = os.path.dirname(filename)

        try:
            self._domainModel.init(filename)
            self._layerModel.init()
        except Exception as ex:
            print(ex)

    @pyqtSlot()
    def on_actSave_triggered(self):
        filename, _ = QFileDialog.getSaveFileName(parent=self, caption='Сохранить как...',
                                                  directory=self._filePath, filter='Text (*.txt)')

        self._filePath = os.path.dirname(filename)

        try:
            self._domainModel.saveLayers(filename)
        except Exception as ex:
            print(ex)

    @pyqtSlot()
    def on_actNew_triggered(self):
        self._domainModel.newFilm()
        self._layerModel.init()

    @pyqtSlot(int)
    def on_comboMaterial_currentIndexChanged(self, index):
        if not self.hasSelection('select layer to apply preset'):
            return

        mat = self._ui.comboMaterial.currentData(MapModel.RoleNodeId)
        print('preset', mat, self._mats[mat])
        rowIndex, thickIndex, refractIndex = self._ui.tableLayer.selectionModel().selectedIndexes()
        rawThick = thickIndex.data(Qt.DisplayRole)
        thick = rawThick if rawThick == 'inf' else float(rawThick)
        refract = self._mats[mat]
        self._domainModel.updateLayer(rowIndex.row(), thick, refract)

    def onBtnSaveImageClicked(self):
        self._plotWidget.saveImage(self.screenShotName)

    def onTableLayerSelectionChanged(self, new, old):
        rowIndex, thickIndex, refractIndex = new.indexes()

        if thickIndex.data(Qt.DisplayRole) == 'inf':
            self.updateControls(0, complex(refractIndex.data(Qt.DisplayRole)), False, True)
        else:
            self.updateControls(float(thickIndex.data(Qt.DisplayRole)), complex(refractIndex.data(Qt.DisplayRole)), True, True)

        try:
            self._domainModel._calc3d(rowIndex.row())
        except Exception as ex:
            print(ex)

    def updateControls(self, thick=0.0, refract: complex=(1.0+0j), f_thick=False, f_refract=False):
        self._ui.spinSlideThick.setEnabled(f_thick)

        self._ui.spinSlideRefractRe.setEnabled(f_refract)
        self._ui.spinSlideRefractIm.setEnabled(f_refract)

        if f_refract:
            self._ui.spinSlideRefractRe.setValue(refract.real)
            self._ui.spinSlideRefractIm.setValue(refract.imag)

        if f_thick:
            self._ui.spinSlideThick.setValue(thick)

    # misc events
    def resizeEvent(self, event):
        self.refreshView()

    # parameter widget events
    def onLambda1Changed(self):
        self._domainModel.lambda1 = self._ui.spinLambda1.value()

    def onLambda2Changed(self):
        self._domainModel.lambda2 = self._ui.spinLambda2.value()

    def onSamplesChanged(self):
        self._domainModel.samples = self._ui.spinSamples.value()

    def onSpinSlideThickChanged(self, value):
        selected = self._ui.tableLayer.selectionModel().selectedIndexes()[0]
        self._domainModel.updateLayerThickness(selected.row(), value)

    def onSpinSlideRefractReChanged(self, value):
        selected = self._ui.tableLayer.selectionModel().selectedIndexes()[-1]
        re = value
        im = complex(selected.data(Qt.DisplayRole)).imag
        com_value = complex(re, im)
        self._domainModel.updateLayerRefract(selected.row(), com_value)

    def onSpinSlideRefractImChanged(self, value):
        selected = self._ui.tableLayer.selectionModel().selectedIndexes()[-1]
        re = complex(selected.data(Qt.DisplayRole)).real
        im = value
        com_value = complex(re, im)
        self._domainModel.updateLayerRefract(selected.row(), com_value)

    def onSpinSlideAngleChanged(self, value):
        self._domainModel.angle = value

    @property
    def screenShotName(self):
        shot = f'{datetime.datetime.now().date().isoformat()}_{self._screenshotIndex:02d}.png'
        self._screenshotIndex += 1
        return shot


