#!venv/bin/python3

from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QMainWindow
from PySide2.QtWidgets import QPushButton, QLineEdit
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout


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
        self._widget = QWidget()
        self._width = 400
        self._height = 300
        self.setFixedSize(self._width, self._height)

        g_layout = QGridLayout()
        v_layout = self.build_v_layout()
        h_layout = self.build_h_layout()
        f_layout = self.build_f_layout()

        g_layout.addItem(v_layout, 1, 0, 1, 1)
        g_layout.addItem(h_layout, 0, 0, 1, 2)
        g_layout.addItem(f_layout, 1, 1, 1, 1)

        self._widget.setLayout(g_layout)

        self.setCentralWidget(self._widget)

    @staticmethod
    def build_v_layout():
        hello_btn = QPushButton('Hello')
        work_btn = QPushButton('Working')
        play_btn = QPushButton('Playing')
        sleep_btn = QPushButton('Sleeping')

        v_layout = QVBoxLayout()
        v_layout.addWidget(hello_btn)
        v_layout.addWidget(work_btn)
        v_layout.addWidget(play_btn)
        v_layout.addWidget(sleep_btn)

        return v_layout

    @staticmethod
    def build_h_layout():
        hello_btn = QPushButton('Hello')
        work_btn = QPushButton('Working')
        play_btn = QPushButton('Playing')
        sleep_btn = QPushButton('Sleeping')

        h_layout = QHBoxLayout()
        h_layout.addWidget(hello_btn)
        h_layout.addWidget(work_btn)
        h_layout.addWidget(play_btn)
        h_layout.addWidget(sleep_btn)

        return h_layout

    @staticmethod
    def build_f_layout():
        hello_btn = QPushButton('Hello')
        work_btn = QPushButton('Working')
        play_btn = QPushButton('Playing')
        sleep_btn = QPushButton('Sleeping')
        hello_line = QLineEdit()
        work_line = QLineEdit()
        play_line = QLineEdit()
        sleep_line = QLineEdit()

        f_layout = QFormLayout()
        f_layout.addRow(hello_btn, hello_line)
        f_layout.addRow(work_btn, work_line)
        f_layout.addRow(play_btn, play_line)
        f_layout.addRow(sleep_btn, sleep_line)

        return f_layout
