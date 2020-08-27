#!venv/bin/python3

from PySide2 import QtCore
from PySide2.QtCore import Qt, QObject
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QAction, QMenu, QWhatsThis
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
        file = QFile('./main_window.ui')
        file.open(QFile.ReadOnly)
        self._window = loader.load(file)
        file.close()

        self.set_title()
        self.set_buttons()
        self.set_edits()

        menu_bar = self._window.menuBar()
        menu = QMenu('&File')
        new_action = menu.addAction(QIcon('./media/paint.png'), '&New')
        open_action = menu.addAction(QIcon('./media/font.png'), '&Open')

        sub_menu = QMenu('Copies')
        path_action = sub_menu.addAction('Copy Path')
        file_action = sub_menu.addAction('Copy File')
        config_action = sub_menu.addAction('Copy Config')
        menu.addMenu(sub_menu)

        menu_bar.addMenu(menu)

        path_action.triggered.connect(self.copy_path)
        file_action.triggered.connect(self.copy_file)
        config_action.triggered.connect(self.copy_config)

        edit_menu = QMenu('&Edit')

        cut_action = self.create_action('font.png', 'Cut', 'Ctrl+X')
        paste_action = self.create_action('font.png', 'Paste', 'Ctrl+P')
        copy_action = self.create_action('font.png', 'Copy', 'Ctrl+C')
        undo_action = self.create_action('font.png', 'Undo', 'Ctrl+Z')

        edit_menu.addAction(cut_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        edit_menu.addSeparator()
        edit_menu.addAction(undo_action)

        menu_bar.addMenu(edit_menu)

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

        self._window.exit_btn.setToolTip('Close Window')
        self._window.exit_btn.setStatusTip('This button will close the window')

        self._window.import_btn.setIcon(QIcon('./media/import.svg'))

        self._window.import_btn.clicked.connect(self.import_item)
        self._window.exit_btn.clicked.connect(self.exit)

    def set_edits(self):
        """Setup line edit and text edit"""
        self._window.input_line.setPlaceholderText('Input item to import')
        self._window.output_text.setPlaceholderText('Import Item')

        self._window.output_text.setWhatsThis('Output data here')

    def create_action(self, icon, name, short_cut, checkable=False):
        """Create an action an return"""
        action = QAction(QIcon('./media/{}'.format(icon)), name, self._window)
        action.setShortcut(short_cut)
        action.setCheckable(checkable)
        action.setToolTip(name)

        return action

    @QtCore.Slot()
    def import_item(self):
        import_item = self._window.input_line.text()
        self._window.output_text.append(import_item)

    @QtCore.Slot()
    def copy_path(self):
        print('Triggered : Copy Path')

    @QtCore.Slot()
    def copy_file(self):
        print('Triggered : Copy File')

    @QtCore.Slot()
    def copy_config(self):
        print('Triggered : Copy Config')

    @QtCore.Slot()
    def exit(self):
        self._window.close()
