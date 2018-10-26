from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QMainWindow

from domainmodel import DomainModel
from layermodel import LayerModel
from plotwidget import PlotWidget


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        self._ui = uic.loadUi("mainwindow.ui", self)

        self._domainModel = DomainModel(self)
        self._layerModel = LayerModel(parent=self, domainModel=self._domainModel)
        self._plotWidget = PlotWidget(parent=self, domainModel=self._domainModel)

        self._ui.framePlot.setLayout(self._plotWidget)

        self._init()

    def _init(self):
        self._domainModel.init()

        self._ui.tableLayer.setModel(self._layerModel)
        self._layerModel.init()

        self._ui.btnAddLayer.clicked.connect(self.onBtnAddLayerClicked)
        self._ui.btnDelLayer.clicked.connect(self.onBtnDelLayerClicked)
        self._ui.btnCalc.clicked.connect(self.onBtnCalcClicked)

        self._ui.spinLambda1.editingFinished.connect(self.onLambda1Changed)
        self._ui.spinLambda2.editingFinished.connect(self.onLambda2Changed)
        self._ui.spinSamples.editingFinished.connect(self.onSamplesChanged)

        self._domainModel.dataReady.connect(self._plotWidget.plotData)

        self._ui.tableLayer.selectionModel().selectionChanged.connect(self.onTableLayerSelectionChanged)

        self.updateControls()

        self._plotWidget.plotData()

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
            self._domainModel.addRow(targetRow)
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

        self._domainModel.delRow(selectedIndex.row())
        self._layerModel.init()

    def onBtnCalcClicked(self):
        self._domainModel._calcReflect()

    def onTableLayerSelectionChanged(self, new, old):
        rowIndex, thickIndex, reflectIndex = new.indexes()

        if thickIndex.data(Qt.DisplayRole) == 'inf':
            self.updateControls()
        else:
            try:
                self.updateControls(int(thickIndex.data(Qt.DisplayRole)), float(reflectIndex.data(Qt.DisplayRole)), True, True, False)
            except Exception as ex:
                print(ex)

    def updateControls(self, thick=0, reflect=1, f_thick=False, f_reflect=False, f_radio=False):
        self._ui.spinThick.setEnabled(f_thick)
        self._ui.slideThick.setEnabled(f_thick)

        self._ui.spinReflect.setEnabled(f_reflect)
        self._ui.slideReflect.setEnabled(f_reflect)

        self._ui.radioAir.setEnabled(f_radio)
        self._ui.radioMirror.setEnabled(f_radio)

        if f_thick and f_reflect:
            self._ui.spinThick.setValue(thick)
            self._ui.spinReflect.setValue(reflect)

    # misc events
    def resizeEvent(self, event):
        self.refreshView()

    # slots
    @pyqtSlot()
    def onLambda1Changed(self):
        self._domainModel.lambda1 = self._ui.spinLambda1.value()

    @pyqtSlot()
    def onLambda2Changed(self):
        self._domainModel.lambda2 = self._ui.spinLambda2.value()

    @pyqtSlot()
    def onSamplesChanged(self):
        self._domainModel.samples = self._ui.spinSamples.value()

