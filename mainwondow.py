from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow

from domainmodel import DomainModel
from layermodel import LayerModel


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        self._ui = uic.loadUi("mainwindow.ui", self)

        self._domainModel = DomainModel(self)
        self._layerModel = LayerModel(self, self._domainModel)

        self._init()

    def _init(self):
        self._domainModel.init()

        self._ui.tableLayer.setModel(self._layerModel)
        self._layerModel.init()

        self._ui.btnAddLayer.clicked.connect(self.onBtnAddLayerClicked)
        self._ui.btnDelLayer.clicked.connect(self.onBtnDelLayerClicked)
        self._ui.btnCalc.clicked.connect(self.onBtnCalcClicked)

    def refreshView(self):
        self._ui.tableLayer.resizeColumnsToContents()

    # ui events
    def onBtnAddLayerClicked(self):
        print('add layer')

    def onBtnDelLayerClicked(self):
        print('del layer')

    def onBtnCalcClicked(self):
        self._domainModel.calcReflect()

    # misc events
    def resizeEvent(self, event):
        self.refreshView()



