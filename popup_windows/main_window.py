#!venv/bin/python3

from PySide2 import QtCore
from PySide2.QtCore import Qt, QObject
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QMessageBox, QDialog, QDialogButtonBox
from PySide2.QtGui import QFont, QIcon

from popup_windows.dialog import Dialog


class MainWindow(QObject):
    def __init__(self, parent=None):
        """Main window, holding all user interface including.

        Args:
          parent: parent class of main window
        Returns:
          None
        Raises:
          None
        """
        super(MainWindow, self).__init__()
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

    def set_title(self):
        """Setup label"""
        self._window.title.setText('Welcome to PySide2 Tutorial')

        font = QFont("Arial", 20, QFont.Black)

        self._window.title.setFont(font)
        # set widget size (x, y, width, height)
        self._window.title.setGeometry(0, 0, 600, 30)
        # set alignment
        self._window.title.setAlignment(Qt.AlignBottom | Qt.AlignCenter)

    def set_buttons(self):
        """Setup buttons"""
        self._window.send_btn.setText('Send Msg')
        self._window.exit_btn.setText('Exit')

        self._window.send_btn.setIcon(QIcon('./media/import.svg'))

        self._window.send_btn.clicked.connect(self.send_message)
        self._window.simple_btn.clicked.connect(self.simple_message)
        self._window.custom_btn.clicked.connect(self.custom_message)
        self._window.popup_btn.clicked.connect(self.popup)
        self._window.exit_btn.clicked.connect(self.exit)

    def set_edits(self):
        """Setup line edit and text edit"""
        self._window.title_line.setPlaceholderText('Input Msg Title')
        self._window.msg_edit.setPlaceholderText('Input Msg')

    @QtCore.Slot()
    def send_message(self):
        pass

    @QtCore.Slot()
    def popup(self):
        dialog = Dialog(self._window)
        ret = dialog.window.exec_()
        print(ret)
        print(dialog.data)

    @QtCore.Slot()
    def simple_message(self):
        ret = QMessageBox.information(self._window, 'Inline Msg Box',
                                      'This is inline message box, with return',
                                      QMessageBox.Ok, QMessageBox.Cancel)
        print('press: ' + str(ret))

    @QtCore.Slot()
    def custom_message(self):
        msg_box = QMessageBox(self._window)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle('Custom Box')
        msg_box.setText('Dekban Massage')
        msg_box.setInformativeText('Welcome to tutorial! plz follow us')
        msg_box.setDetailedText('Follow our Bucketing page, and learn more'
                                'about PySide2, Java, Design pattern!\n'
                                'Enjoy!')
        msg_box.addButton('follow', QMessageBox.AcceptRole)
        msg_box.show()

    @QtCore.Slot()
    def exit(self):
        self._window.close()
