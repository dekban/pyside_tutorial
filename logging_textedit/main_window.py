#!venv/bin/python3

from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtCore import QFile, QTime, QTimer
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QFont

from clock_time.analog_clock import AnalogClock


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
        self._analog_clock = None
        self._clock_timer = QTimer()

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
        self.set_clock()
        self.set_time_edit()
        self.set_lcd()

        self._clock_timer.timeout.connect(self.update_clock)

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
        self._window.exit_btn.setText('Exit')

        self._window.exit_btn.setToolTip('Close Window')
        self._window.exit_btn.setStatusTip('This button will close the window')

        self._window.exit_btn.clicked.connect(self.exit)

    def set_time_edit(self):
        time_edit = self._window.time_edit
        time_edit.setMaximumTime(QTime(18, 0, 0))
        time_edit.setMinimumTime(QTime(8, 0, 0))
        time_edit.setDisplayFormat('hh:mm:ss.zzz')

    def set_lcd(self):
        lcd = self._window.lcd
        lcd.setDecMode()

        self._clock_timer.start(1000)

    def set_clock(self):
        self._analog_clock = AnalogClock(self._window, 500)
        self._window.v_layout.addWidget(self._analog_clock)

    @QtCore.Slot()
    def update_clock(self):
        time = QTime.currentTime()
        s_time = time.toString('hh:mm')

        if time.second() % 2 == 0:
            s_time = s_time.replace(':', '.')

        self._window.lcd.display(s_time)
        self._analog_clock.time = time

    @QtCore.Slot()
    def exit(self):
        self._window.close()
