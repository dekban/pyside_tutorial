#!venv/bin/python3

from PySide2 import QtCore
from PySide2.QtCore import Signal
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QMainWindow
from PySide2.QtWidgets import QPushButton, QLineEdit
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout


class MainWindow(QMainWindow):
    hello_signal = Signal(str)

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
        self._widget = QWidget()
        self._width = 400
        self._height = 300
        self.setFixedSize(self._width, self._height)

        g_layout = QGridLayout()
        h_layout = self.build_h_layout()

        g_layout.addItem(h_layout, 0, 0, 1, 1)

        self._widget.setLayout(g_layout)

        self.setCentralWidget(self._widget)
        self.hello_signal.connect(self.say_hello)
        self.hello_signal.emit('Pyside2!')

    def build_h_layout(self):
        hello_btn = QPushButton('Hello')
        work_btn = QPushButton('Working')
        play_btn = QPushButton('Playing')
        sleep_btn = QPushButton('Sleeping')

        h_layout = QHBoxLayout()
        h_layout.addWidget(hello_btn)
        h_layout.addWidget(work_btn)
        h_layout.addWidget(play_btn)
        h_layout.addWidget(sleep_btn)

        sleep_btn.clicked.connect(self.exit)

        return h_layout

    @QtCore.Slot()
    def exit(self):
        self.close()

    @QtCore.Slot(str)
    def say_hello(self, msg):
        print('Hello ' + msg)
