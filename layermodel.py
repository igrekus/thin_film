import datetime

from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant, QDate, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QBrush, QColor, QFont


class LayerModel(QAbstractTableModel):

    _default_header = ['№', 'Толщина', 'К-т преломления']

    ColNum, \
    ColThick, \
    ColReflect, \
    ColCount = range(len(_default_header) + 1)

    def __init__(self, parent=None, domainModel=None):
        super().__init__(parent)

        self._domainModel = domainModel

        self._header = self._default_header
        self._display_data = list()

    def clear(self):
        pass
        # self.beginRemoveRows(QModelIndex(), 0, len(self._data))
        # self._data.clear()
        # self.endRemoveRows()

    def init(self):
        print('init layer model')
        self.beginResetModel()

        self._display_data.clear()
        for idx, layer in enumerate(self._domainModel._layers):
            self._display_data.append([idx + 1, layer.thick, layer.refract])

        self.endResetModel()

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                if section < len(self._header):
                    return QVariant(self._header[section])
        return QVariant()

    def rowCount(self, parent=None, *args, **kwargs):
        if parent is not None and parent.isValid():
            return 0
        return len(self._display_data)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self._header)

    # def setData(self, index, value, role):
    #     if role == Qt.EditRole:
    #         col = index.column()
    #         row = index.row()
    #
    #     return False

    def data(self, index, role=None):
        if not index.isValid():
            return QVariant()

        col = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            return QVariant(str(self._display_data[row][col]))

        return QVariant()

    # def flags(self, index):
    #     f = super().flags(index)
    #     col = index.column()
    #     if col > 0:
    #         f = f | Qt.ItemIsEditable
    #     return f




