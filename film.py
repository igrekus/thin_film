import sys

from PyQt5.QtWidgets import QApplication

from mainwindow import MainWindow

app = QApplication(sys.argv)

win = MainWindow()
win.show()

sys.exit(app.exec_())

# TODO implement screen shot & layer file naming

# https://refractiveindex.info/?shelf=main&book=Ag&page=Johnson
# http://sjbyrnes.com/multilayer-film-optics-programs/
# https://habr.com/post/259791/

# performance:
# https://stackoverflow.com/questions/8955869/why-is-plotting-with-matplotlib-so-slow/8956211#8956211
# https://bastibe.de/2013-05-30-speeding-up-matplotlib.html


