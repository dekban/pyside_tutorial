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

        # Setup combobox
        self._window.transportation_combo.addItem('HSR', 'HighSpeedRail')
        self._window.transportation_combo.addItem('Taxi', 'Uber,Taxi')
        self._window.transportation_combo.addItem('Drive', 'Car')
        self._window.transportation_combo.addItem('Scooter', 'Motorcycle')

        # Setup RadioButton / CheckBox
        self._window.yes_radio.setChecked(False)
        self._window.no_radio.setChecked(True)
        vegetarian_group = QButtonGroup(self._window)
        vegetarian_group.setExclusive(True)
        vegetarian_group.addButton(self._window.yes_radio)
        vegetarian_group.addButton(self._window.no_radio)

        self._window.absolutly_check.setChecked(True)
        self._window.maybe_check.setChecked(False)
        self._window.sorry_check.setChecked(False)
        participate_group = QButtonGroup(self._window)
        participate_group.setExclusive(True)
        participate_group.addButton(self._window.absolutly_check)
        participate_group.addButton(self._window.maybe_check)
        participate_group.addButton(self._window.sorry_check)

        # Setup SpinBox
        self._window.members_spin.setRange(1, 10)

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
