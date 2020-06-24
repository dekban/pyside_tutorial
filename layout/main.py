#!venv/bin/python3

import sys

from PySide2 import QtWidgets

from layout.main_window import MainWindow

if '__main__' == __name__:
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()

    ret = app.exec_()
    sys.exit(ret)
