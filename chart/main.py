#!venv/bin/python3

import logging
import sys

from PySide2.QtWidgets import QApplication

from logging_text.main_window import MainWindow

if '__main__' == __name__:
    app = QApplication(sys.argv)
    logging.basicConfig(level=logging.DEBUG)

    mainwindow = MainWindow()
    mainwindow.window.show()

    ret = app.exec_()
    sys.exit(ret)
