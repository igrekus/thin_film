from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSpinBox, QSlider, QHBoxLayout


class SpinSlide(QHBoxLayout):

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

        self._spin.valueChanged.connect(self._slider.setValue)
        self._slider.valueChanged.connect(self._spin.setValue)

    def value(self):
        return self._spin.value()

    def setValue(self, value: int):
        self._spin.setValue(value)

    def setEnabled(self, enabled):
        self._spin.setEnabled(enabled)
        self._slider.setEnabled(enabled)


