#!venv/bin/python3

import logging
from datetime import datetime

from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QFont

from logging_text.logger import setup_loggers, add_text_handler


class MainWindow(object):
    def __init__(self, parent=None):
        """Main window, holding all user interface including.

        Args:
          parent: parent class of main window
        Returns:
          None
        Raises:
          None
        """
        self._window = None

        self.setup_ui()
        self.set_logger()

        logging.debug('this is debug level')
        logging.info('this is info level')
        logging.warning('this is warning level')
        logging.error('this is error level')

    @property
    def window(self):
        """The main window object"""
        return self._window

    def setup_ui(self):
        loader = QUiLoader()
        file = QFile('./main_window.ui')
        file.open(QFile.ReadOnly)
        self._window = loader.load(file)
        file.close()

        self.set_title()
        self.set_buttons()

    def set_title(self):
        """Setup label"""
        self._window.title.setText('This is PySide2 Tutorial')
        # set font
        font = QFont("Arial", 20, QFont.Bold)
        self._window.title.setFont(font)
        # set widget size (x, y, width, height)
        self._window.title.setGeometry(0, 0, 600, 30)
        # set alignment
        self._window.title.setAlignment(Qt.AlignBottom | Qt.AlignCenter)

    def set_buttons(self):
        """Setup buttons"""
        self._window.exit_btn.setText('Exit')

        self._window.exit_btn.setToolTip('Close Window')
        self._window.exit_btn.setStatusTip('This button will close the window')

        self._window.exit_btn.clicked.connect(self.exit)

    def set_logger(self):
        now = datetime.now().strftime('%Y%m%d')
        print(setup_loggers(now))
        add_text_handler(self.logger_callback)

    def logger_callback(self, msg):
        self._window.log_text.append(msg)

    @QtCore.Slot()
    def exit(self):
        self._window.close()
