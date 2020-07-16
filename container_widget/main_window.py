#!venv/bin/python3

from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QRadioButton, QButtonGroup
from PySide2.QtGui import QFont, QIcon


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

    @property
    def window(self):
        """The main window object"""
        return self._window

    def setup_ui(self):
        loader = QUiLoader()
        file = QFile('./media/main_window.ui')
        file.open(QFile.ReadOnly)
        self._window = loader.load(file)
        file.close()

        self.set_title()
        self.set_buttons()

    def set_title(self):
        """Setup label"""
        # set alignment
        self._window.title.setAlignment(Qt.AlignBottom | Qt.AlignCenter)

    def set_buttons(self):
        """Setup buttons"""
        self._window.submit_btn.setText('Submit')
        self._window.exit_btn.setText('Exit')

        self._window.submit_btn.setIcon(QIcon('./media/import.svg'))

        self._window.submit_btn.clicked.connect(self.submit_form)
        self._window.exit_btn.clicked.connect(self.exit)

    @QtCore.Slot()
    def submit_form(self):
        pass

    @QtCore.Slot()
    def exit(self):
        self._window.close()
