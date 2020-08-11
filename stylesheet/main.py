#!venv/bin/python3

import sys

from PySide2.QtWidgets import QApplication

from stylesheet.main_window import MainWindow

if '__main__' == __name__:
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.window.show()

    ret = app.exec_()
    sys.exit(ret)
