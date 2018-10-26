import sys

from PyQt5.QtWidgets import QApplication

from mainwondow import MainWindow

app = QApplication(sys.argv)

win = MainWindow()
win.show()

sys.exit(app.exec_())



