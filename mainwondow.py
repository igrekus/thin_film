from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QMainWindow

from domainmodel import DomainModel
from doublespinslide import DoubleSpinSlide
from layermodel import LayerModel
from plotwidget import PlotWidget
from spinslide import SpinSlide


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        self._ui = uic.loadUi("mainwindow.ui", self)

        self._ui.spinSlideThick = SpinSlide(v_min=0, v_max=1000, v_current=100, suffix=' мкм')
        self._ui.gridControl.addLayout(self._ui.spinSlideThick, 0, 1)
        self._ui.spinSlideRefractRe = DoubleSpinSlide(v_min=0.001, v_max=10.000, v_current=0.0, decimals=3)
        self._ui.gridControl.addLayout(self._ui.spinSlideRefractRe, 1, 1)
        self._ui.spinSlideRefractIm = DoubleSpinSlide(v_min=0.001, v_max=10.000, v_current=0.0, decimals=3)
        self._ui.gridControl.addLayout(self._ui.spinSlideRefractIm, 2, 1)

        self._domainModel = DomainModel(self)
        self._layerModel = LayerModel(parent=self, domainModel=self._domainModel)
        self._plotWidget = PlotWidget(parent=self, domainModel=self._domainModel)

        self._ui.framePlot.setLayout(self._plotWidget)

        self._init()

    def _init(self):
        self._domainModel.init()

        self._ui.tableLayer.setModel(self._layerModel)
        self._layerModel.init()

        self.setupSignals()

        self.updateControls()

        self._plotWidget.plotData()

    def setupSignals(self):

        self._ui.btnAddLayer.clicked.connect(self.onBtnAddLayerClicked)
        self._ui.btnDelLayer.clicked.connect(self.onBtnDelLayerClicked)
        self._ui.btnCalc.clicked.connect(self.onBtnCalcClicked)

        self._ui.spinLambda1.editingFinished.connect(self.onLambda1Changed)
        self._ui.spinLambda2.editingFinished.connect(self.onLambda2Changed)
        self._ui.spinSamples.editingFinished.connect(self.onSamplesChanged)

        self._domainModel.dataReady.connect(self._plotWidget.plotData)
        self._domainModel.layerChanged.connect(self._layerModel.updateLayer)

        self._ui.spinSlideThick.valueChanged.connect(self.onSpinSlideThickChanged)
        self._ui.spinSlideRefractRe.valueChanged.connect(self.onSpinSlideRefractReChanged)
        self._ui.spinSlideRefractIm.valueChanged.connect(self.onSpinSlideRefractImChanged)

        self._ui.tableLayer.selectionModel().selectionChanged.connect(self.onTableLayerSelectionChanged)


    def refreshView(self):
        self._ui.tableLayer.resizeColumnsToContents()

    # ui events
    def onBtnAddLayerClicked(self):
        if not self._ui.tableLayer.selectionModel().hasSelection():
            print('select layer to add past to')
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
        if not self._ui.tableLayer.selectionModel().hasSelection():
            print('select layer to delete')
            return

        selectedIndex = self._ui.tableLayer.selectionModel().selectedIndexes()[1]
        if selectedIndex.data(Qt.DisplayRole) == 'inf':
            print('can\'t delete inf layer')
            return

        self._domainModel.delLayer(selectedIndex.row())
        self._layerModel.init()

    def onBtnCalcClicked(self):
        self._domainModel._calcReflect()

    def onTableLayerSelectionChanged(self, new, old):
        rowIndex, thickIndex, refractIndex = new.indexes()

        if thickIndex.data(Qt.DisplayRole) == 'inf':
            self.updateControls()
        else:
            try:
                self.updateControls(int(thickIndex.data(Qt.DisplayRole)), complex(refractIndex.data(Qt.DisplayRole)), True, True, False)
            except Exception as ex:
                print(ex)

    def updateControls(self, thick=0, refract: complex=1.0, f_thick=False, f_refract=False, f_radio=False):
        self._ui.spinSlideThick.setEnabled(f_thick)

        self._ui.spinSlideRefractRe.setEnabled(f_refract)
        self._ui.spinSlideRefractIm.setEnabled(f_refract)

        # self._ui.radioAir.setEnabled(f_radio)
        # self._ui.radioMirror.setEnabled(f_radio)

        if f_thick and f_refract:
            self._ui.spinSlideThick.setValue(thick)
            self._ui.spinSlideRefractRe.setValue(refract.real)
            self._ui.spinSlideRefractIm.setValue(refract.imag)

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



