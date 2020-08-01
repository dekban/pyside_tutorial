#!venv/bin/python3

from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QLabel, QPushButton, QLineEdit, QColorDialog
from PySide2.QtGui import QFont, QIcon, QColor, qRgb, QPalette


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
        file = QFile('./main_window.ui')
        file.open(QFile.ReadOnly)
        self._window = loader.load(file)
        file.close()

        self.set_title()
        self.set_buttons()
        self.set_edits()

    def set_title(self):
        """Setup label"""
        self._window.title.setText('This is PySide2 Tutorial')

        # set color
        a_color = QColor('#55aa55')
        b_color = QColor(qRgb(125, 22, 100))
        c_color = QColor('red')

        print(a_color.name())
        print(b_color.name())
        print(c_color.name())

        a_cmyk = a_color.toCmyk()
        print(a_cmyk)

        # set font
        font = QFont("Arial", 20, QFont.Bold)
        self._window.title.setFont(font)
        # set widget size (x, y, width, height)
        self._window.title.setGeometry(0, 0, 600, 30)
        # set alignment
        self._window.title.setAlignment(Qt.AlignBottom | Qt.AlignCenter)

    def set_buttons(self):
        """Setup buttons"""
        self._window.color_btn.setText('Choose Color')
        self._window.exit_btn.setText('Exit')
        self._window.palette_btn.setText('Set Palette')

        self._window.color_btn.setIcon(QIcon('./media/paint.png'))

        self._window.color_btn.clicked.connect(self.choose_color)
        self._window.palette_btn.clicked.connect(self.set_palette)
        self._window.exit_btn.clicked.connect(self.exit)

    def set_edits(self):
        """Setup line edit and text edit"""
        self._window.input_line.setPlaceholderText('Input item to import')
        self._window.output_text.setPlaceholderText('Import Item')

    @QtCore.Slot()
    def choose_color(self):
        color_dialog = QColorDialog()
        color = color_dialog.getColor()
        color_name = color.name()
        self._window.input_line.setText(color_name)

    @QtCore.Slot()
    def set_palette(self):
        palette = self._window.palette()
        color = QColor(self._window.input_line.text())
        if color.isValid():
            palette.setColor(QPalette.Normal, QPalette.Background, color)
            self._window.setPalette(palette)
            self._window.update()

    @QtCore.Slot()
    def exit(self):
        self._window.close()
