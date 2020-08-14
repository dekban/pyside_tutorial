#!venv/bin/python3

import sys

from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QIcon

from window_feature.main_window import MainWindow

if '__main__' == __name__:
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('./media/dekban.png'))
    mainwindow = MainWindow()
    mainwindow.window.show()

    ret = app.exec_()
    sys.exit(ret)
