from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSpinBox, QSlider, QHBoxLayout


class SpinSlide(QHBoxLayout):

    def __init__(self, v_min=1, v_max=99, v_current=1, prefix=' мкм', ):
        super().__init__()

        self._spin = QSpinBox()
        self._spin.setMinimum(v_min)
        self._spin.setMaximum(v_max)
        self._spin.setValue(v_current)
        self._spin.setPrefix(prefix)

        self._slider = QSlider(Qt.Horizontal)
        self._slider.setMinimum(v_min)
        self._slider.setMaximum(v_max)
        self._slider.setValue(v_current)

        self.addWidget(self._spin)
        self.addWidget(self._slider)

