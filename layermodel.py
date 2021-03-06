import datetime

from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant, QDate, pyqtSlot, pyqtSignal


class LayerModel(QAbstractTableModel):

    layerEdited = pyqtSignal(int, float)

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

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            row = index.row()

            try:
                val = float(value)
            except ValueError as ex:
                return False

            self.layerEdited.emit(row, val)
            self.dataChanged.emit(index, index, [])
            return True

        return False

    def data(self, index, role=None):
        if not index.isValid():
            return QVariant()

        col = index.column()
        row = index.row()

        if role == Qt.DisplayRole or role == Qt.EditRole:
            return QVariant(str(self._display_data[row][col]))

        return QVariant()

    def flags(self, index):
        f = super().flags(index)
        if index.column() == 1 and index.row() not in (0, len(self._display_data) - 1):
            return f | Qt.ItemIsEditable
        return f

    def updateLayer(self, row):
        updated = self._domainModel._layers[row]
        self._display_data[row] = [row + 1, updated.thick, updated.refract]
        self.dataChanged.emit(self.index(row, 0, QModelIndex()), self.index(row, self.ColCount, QModelIndex()), [Qt.DisplayRole])


