from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QDoubleSpinBox, QSlider, QHBoxLayout


class DoubleSpinSlide(QHBoxLayout):

    def __init__(self, v_min=0.000, v_max=99.000, v_current=0.000, decimals=2, suffix='', ):
        super().__init__()

        self._spin = QDoubleSpinBox()
        self._spin.setDecimals(decimals)
        self._spin.setMinimum(v_min)
        self._spin.setMaximum(v_max)
        self._spin.setValue(v_current)
        self._spin.setSuffix(suffix)
        self._spin.setSingleStep(0.1)

        self._slider = QSlider(Qt.Horizontal)
        self._slider.setMinimum(v_min * 10 ** decimals)
        self._slider.setMaximum(v_max * 10 ** decimals)
        self._slider.setValue(v_current * 10 ** decimals)

        self.addWidget(self._spin)
        self.addWidget(self._slider)

        self._spin.valueChanged.connect(self._spinChanged)
        self._slider.valueChanged.connect(self._sliderChanged)

    def value(self):
        return self._spin.value()

    def setValue(self, value: float):
        self._spin.setValue(value)

    def setEnabled(self, enabled):
        self._spin.setEnabled(enabled)
        self._slider.setEnabled(enabled)

    @pyqtSlot(float)
    def _spinChanged(self, value: float):
        self._slider.setValue(int(self._spin.value() * 10 ** self._spin.decimals()))

    @pyqtSlot(int)
    def _sliderChanged(self, value: int):
        self._spin.setValue(float(self._slider.value() / 10 ** self._spin.decimals()))

