#!venv/bin/python3

from PySide2 import QtCore
from PySide2.QtCore import Qt, QObject
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QSystemTrayIcon, QMenu, QDesktopWidget, QTextEdit
from PySide2.QtGui import QFont, QIcon


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
        self._old_pos = None

        self._tray = QSystemTrayIcon(self._window)
        if self._tray.isSystemTrayAvailable():
            self._tray.setIcon(QIcon('./media/dekban.png'))
        else:
            self._tray = None

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

        self._window.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self._window.installEventFilter(self)

        self.center()
        self._old_pos = self._window.pos()

        self.set_title()
        self.set_buttons()
        self.set_edits()
        self.set_icon_combo()
        self.set_tray()

        self._tray.show()

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
        self._window.exit_btn.clicked.connect(self.exit)

    def set_edits(self):
        """Setup line edit and text edit"""
        self._window.title_line.setPlaceholderText('Input Msg Title')
        self._window.msg_edit.setPlaceholderText('Input Msg')

    def set_icon_combo(self):
        """Setup options in icon select combobox."""
        # self._window.icon_combo = QComboBox()
        self._window.icon_combo.addItem(QIcon('./media/font.png'), 'font')
        self._window.icon_combo.addItem(QIcon('./media/paint.png'), 'paint')
        self._window.icon_combo.addItem(QIcon('./media/dekban.png'), 'default')
        self._window.icon_combo.currentIndexChanged.connect(self.set_icon)

    def set_tray(self):
        menu = QMenu(self._window)
        action_show = menu.addAction("Show/Hide")
        action_show.triggered.connect(
            lambda: self._window.hide()
            if self._window.isVisible() else self._window.show())
        action_quit = menu.addAction("Quit")
        action_quit.triggered.connect(self._window.close)

        self._tray.setContextMenu(menu)

    def eventFilter(self, obj, event):
        if obj is self._window:
            if event.type() == QtCore.QEvent.MouseButtonPress:
                self.mouse_press_event(event)
            elif event.type() == QtCore.QEvent.MouseMove:
                self.mouse_move_event(event)
        return super(MainWindow, self).eventFilter(obj, event)

    def center(self):
        qr = self._window.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self._window.move(qr.topLeft())

    def mouse_press_event(self, event):
        self._old_pos = event.globalPos()

    def mouse_move_event(self, event):
        delta_x = int(event.globalPos().x()) - self._old_pos.x()
        delta_y = int(event.globalPos().y()) - self._old_pos.y()
        self._window.move(self._window.x() + delta_x,
                          self._window.y() + delta_y)
        self._old_pos = event.globalPos()

    @QtCore.Slot(int)
    def set_icon(self, index):
        icon = self._window.icon_combo.itemIcon(index)
        self._tray.setIcon(icon)

    @QtCore.Slot()
    def send_message(self):
        title = self._window.title_line.text()
        msg = self._window.msg_edit.toPlainText()

        self._tray.showMessage(title, msg,
                               QIcon('./media/dekban.png'))

    @QtCore.Slot()
    def exit(self):
        self._window.close()
