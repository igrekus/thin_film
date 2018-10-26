from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QSpinBox, QSlider, QHBoxLayout


class SpinSlide(QHBoxLayout):

    valueChanged = pyqtSignal(int)

    def __init__(self, v_min=1, v_max=99, v_current=1, suffix=' мкм', ):
        super().__init__()

        self._spin = QSpinBox()
        self._spin.setMinimum(v_min)
        self._spin.setMaximum(v_max)
        self._spin.setValue(v_current)
        self._spin.setSuffix(suffix)

        self._slider = QSlider(Qt.Horizontal)
        self._slider.setMinimum(v_min)
        self._slider.setMaximum(v_max)
        self._slider.setValue(v_current)

        self.addWidget(self._spin)
        self.addWidget(self._slider)

        self._spin.valueChanged.connect(self._spinChanged)
        self._slider.valueChanged.connect(self._sliderChanged)

    def value(self):
        return self._spin.value()

    def setValue(self, value: int):
        self._spin.setValue(value)

    def setEnabled(self, enabled):
        self._spin.setEnabled(enabled)
        self._slider.setEnabled(enabled)

    def _spinChanged(self, value):
        # self.blockSignals(True)
        self._slider.setValue(value)
        # self.blockSignals(False)
        self.valueChanged.emit(value)

    def _sliderChanged(self, value):
        # self.blockSignals(True)
        self._spin.setValue(value)
        # self.blockSignals(False)
        self.valueChanged.emit(value)


