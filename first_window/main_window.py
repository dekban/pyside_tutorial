#!venv/bin/python3

from PySide2.QtWidgets import QLabel
from PySide2.QtWidgets import QMainWindow
from PySide2.QtWidgets import QPushButton


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        """Main window, holding all user interface including.

        Args:
          parent: parent class of main window
        Returns:
          None
        Raises:
          None
        """
        super(MainWindow, self).__init__(parent)
        self._width = 800
        self._height = 600
        self._title = QLabel('PySide2 is Great', self)
        self._exit_btn = QPushButton('Exit', self)

        self.setMinimumSize(self._width, self._height)
