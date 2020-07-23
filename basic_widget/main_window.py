#!venv/bin/python3

from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QLabel, QPushButton, QLineEdit
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
        file = QFile('./user_interface/form/main_window.ui')
        file.open(QFile.ReadOnly)
        self._window = loader.load(file)
        file.close()

        self.set_title()
        self.set_buttons()
        self.set_edits()

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
        self._window.import_btn.setText('Import')
        self._window.exit_btn.setText('Exit')

        self._window.import_btn.setIcon(QIcon('./media/import.svg'))

        self._window.import_btn.clicked.connect(self.import_item)
        self._window.exit_btn.clicked.connect(self.exit)

    def set_edits(self):
        """Setup line edit and text edit"""
        self._window.input_line.setPlaceholderText('Input item to import')
        self._window.output_text.setPlaceholderText('Import Item')

    @QtCore.Slot()
    def import_item(self):
        import_item = self._window.input_line.text()
        self._window.output_text.append(import_item)

    @QtCore.Slot()
    def exit(self):
        self._window.close()
