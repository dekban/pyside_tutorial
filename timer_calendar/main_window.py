#!venv/bin/python3

from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtCore import QFile, QTimer, QDate
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QFont, QColor, QBrush, QTextCharFormat


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
        self._counter = 100
        self._count_timer = None

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
        self.set_calendar()
        self.set_date_edit()

        self._count_timer = QTimer(self._window)
        self._count_timer.timeout.connect(self.count_down)
        if not self._count_timer.isActive():
            self._count_timer.start(1000)

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

    def set_calendar(self):
        """Setup Calendar widget"""
        calendar = self._window.calendar
        calendar.setGridVisible(True)
        calendar.setMinimumDate(QDate(1900, 1, 1))
        calendar.setMaximumDate(QDate.currentDate())
        calendar.setFirstDayOfWeek(Qt.Thursday)
        weekend_format = QTextCharFormat()
        weekend_format.setForeground(QBrush(Qt.green, Qt.SolidPattern))
        calendar.setWeekdayTextFormat(Qt.Saturday, weekend_format)
        calendar.setWeekdayTextFormat(Qt.Sunday, weekend_format)
        weekend_format.setForeground(QBrush(QColor('#8800BB'), Qt.SolidPattern))
        calendar.setDateTextFormat(QDate.currentDate(), weekend_format)

        calendar.clicked.connect(self._window.date_edit.setDate)

    def set_date_edit(self):
        date_edit = self._window.date_edit
        date_edit.setDisplayFormat('yyyy-MM-dd')
        date_edit.setDate(QDate(2020, 1, 1))
        # This will make calendar as a pop window
        # date_edit.setCalendarPopup(True)
        date_edit.setCalendarWidget(self._window.calendar)

    def set_buttons(self):
        """Setup buttons"""
        self._window.exit_btn.setText('Exit')

        self._window.exit_btn.setToolTip('Close Window')
        self._window.exit_btn.setStatusTip('This button will close the window')

        self._window.exit_btn.clicked.connect(self.exit)

    @QtCore.Slot()
    def count_down(self):
        self._counter -= 1
        print(self._counter)

        if self._counter is 0 and self._count_timer.isActive():
            self._count_timer.stop()

    @QtCore.Slot()
    def exit(self):
        self._window.close()
