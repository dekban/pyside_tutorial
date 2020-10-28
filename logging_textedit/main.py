#!venv/bin/python3

import datetime
import logging
import sys

from PySide2.QtWidgets import QApplication

from clock_time.main_window import MainWindow
from logging_textedit.logger import setup_loggers

if '__main__' == __name__:
    app = QApplication(sys.argv)
    logging.basicConfig(level=logging.DEBUG)

    mainwindow = MainWindow()
    mainwindow.window.show()

    ret = app.exec_()
    sys.exit(ret)
