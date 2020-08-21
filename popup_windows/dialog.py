#!venv/bin/python3

from PySide2 import QtCore
from PySide2.QtCore import Qt, QObject
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QPushButton, QVBoxLayout
from PySide2.QtGui import QFont


class Dialog(QObject):
    def __init__(self, parent=None):
        """Dialog.

        Args:
          parent: parent class of main window
        Returns:
          None
        Raises:
          None
        """
        super(Dialog, self).__init__()

        self._window = None
        self._ret = 999
        self._data = None

        self.setup_ui()

    @property
    def window(self):
        """The main window object"""
        return self._window

    def data(self):
        """Collecting dialog data"""
        return self._data

    def setup_ui(self):
        loader = QUiLoader()
        file = QFile('./dialog.ui')
        file.open(QFile.ReadOnly)
        self._window = loader.load(file)
        file.close()

        self.set_title()
        self.set_buttons()

        self._window.finished.connect(self.finish_dialog)

    def set_title(self):
        """Setup label"""
        self._window.title.setText('Sub Window - Dialog')

        font = QFont("Arial", 20, QFont.Black)

        self._window.title.setFont(font)
        # set alignment
        self._window.title.setAlignment(Qt.AlignBottom | Qt.AlignCenter)

    def set_buttons(self):
        """Setup buttons"""
        self._window.send_btn.setText('Send Msg')
        self._window.exit_btn.setText('Exit')

        ret22_button = QPushButton('Ret 22')
        ret10_button = QPushButton('Ret 10')

        self._window.dialogbtn_widget.setLayout(QVBoxLayout())
        self._window.dialogbtn_widget.layout().addWidget(ret22_button)
        self._window.dialogbtn_widget.layout().addWidget(ret10_button)

        ret22_button.clicked.connect(self.ret22_clicked)
        ret10_button.clicked.connect(self.ret10_clicked)
        self._window.exit_btn.clicked.connect(self.exit)

    @QtCore.Slot()
    def ret22_clicked(self):
        self._ret = 22
        self._window.close()

    @QtCore.Slot()
    def ret10_clicked(self):
        self._ret = 10
        self._window.close()

    @QtCore.Slot(int)
    def finish_dialog(self, code):
        self._window.setResult(self._ret)
        self._data = {'title': self._window.title_line.text(),
                      'Message': self._window.msg_edit.toPlainText()}

    @QtCore.Slot()
    def exit(self):
        self._window.close()

