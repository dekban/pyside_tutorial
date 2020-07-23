#!venv/bin/python3

import sys

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication

from basic_ui.user_interface.main_window import MainWindow

if '__main__' == __name__:
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('./user_interface/media/bucketing_icon.jpeg'))
    main_window = MainWindow()
    main_window.window.show()

    ret = app.exec_()
    sys.exit(ret)
