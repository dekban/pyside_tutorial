#!venv/bin/python3

from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QListView, QListWidget, QListWidgetItem
from PySide2.QtWidgets import QWidget, QPushButton, QVBoxLayout, QDockWidget, QStackedWidget
from PySide2.QtGui import QFont, QIcon

from container_widget.text_page import TextPage

PLAY_TEXT = 'Music has been described as a universal language. Regardless of age, race, gender or culture,' \
            ' most people feel some positive connection to it. But the impact of music isn’t just an emotional one.' \
            ' Music has been found to be an effective tool in improving the quality of life for patients with' \
            ' physical and mental illnesses. Studies show music therapy can ease anxiety, muscle tension, and' \
            ' the unpleasant side effects of cancer treatment; help in pain relief and physical therapy and' \
            ' rehabilitation; and provide safe emotional release and increased self-esteem.'
PAUSE_TEXT = 'A week after mandating masks at all state facilities, troubling numbers prompted Utah Gov. Gary Herbert' \
             ' to require masks in regions of Utah that are home to several of the state’s famous national parks' \
             ' July 2. He announced a pause in reopening in June.'
STOP_TEXT = 'WASHINGTON (Reuters) - U.S. infectious disease expert Anthony Fauci on Wednesday called the White House' \
            ' effort to discredit him “bizarre” and urged an end to the divisiveness over the country’s response to' \
            ' the coronavirus pandemic, saying “let’s stop this nonsense.”'


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
        self._pages = dict()
        self._tool_list = None

        self.setup_ui()

    @property
    def window(self):
        """The main window object"""
        return self._window

    def setup_ui(self):
        """Initialize and setup user interface"""
        loader = QUiLoader()
        file = QFile('./media/main_window.ui')
        file.open(QFile.ReadOnly)
        self._window = loader.load(file)
        file.close()

        self.set_title()
        self.set_buttons()

        # Setup ListWidget
        self._tool_list = QListWidget(self._window)
        self._tool_list.setCurrentRow(0)
        self._tool_list.setViewMode(QListView.ListMode)
        self._tool_list.setSpacing(3)
        self._tool_list.setItemAlignment(QtCore.Qt.AlignCenter)
        self._tool_list.setEnabled(True)

        self.create_item('Play', './media/play.ico', self._tool_list)
        self.create_item('Pause', './media/pause.ico', self._tool_list)
        self.create_item('Stop', './media/stop.ico', self._tool_list)

        # Setup ToolBox
        self._window.tool_box.removeItem(0)
        self._window.tool_box.addItem(self._tool_list, 'Music Tools')

        # Add another item
        w1 = QWidget(self._window)
        layout = QVBoxLayout()

        layout.addWidget(QPushButton('Hello Btn'))
        layout.addWidget(QPushButton('GoodBye Btn'))
        layout.addWidget(QPushButton('Hug Btn'))
        layout.addWidget(QPushButton('Dont\'t Press Me'))
        w1.setLayout(layout)

        self._window.tool_box.addItem(w1, 'Button Tools')

        # Setup DockWidget
        self.set_docker()
        self.set_stack()

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

    def set_docker(self):
        """Setup dock widget"""
        dock = self._window.dock_tool
        dock.setFeatures(QDockWidget.AllDockWidgetFeatures)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea |
                             Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea)
        data_list = QListWidget(dock)
        data_list.addItems(["John Doe, Harmony Enterprises, 12 Lakeside, Ambleton",
                            "Jane Doe, Memorabilia, 23 Watersedge, Beaton",
                            "Tammy Shea, Tiblanka, 38 Sea Views, Carlton",
                            "Tim Sheen, Caraba Gifts, 48 Ocean Way, Deal",
                            "Sol Harvey, Chicos Coffee, 53 New Springs, Eccleston",
                            "Sally Hobart, Tiroli Tea, 67 Long River, Fedula"])
        dock.setWidget(data_list)

        self._window.addDockWidget(Qt.RightDockWidgetArea, dock)

    def set_stack(self):
        """Setup stack widget"""
        stack_widget = self._window.stack_widget
        self._pages['Play'] = TextPage(text=PLAY_TEXT)
        self._pages['Pause'] = TextPage(text=PAUSE_TEXT)
        self._pages['Stop'] = TextPage(text=STOP_TEXT)

        for index, name in enumerate(self._pages):
            print('pages {} : {} page'.format(index, name))
            stack_widget.addWidget(self._pages[name].widget)

        stack_widget.setCurrentIndex(0)
        self._tool_list.currentItemChanged.connect(self.set_page)

    @QtCore.Slot()
    def set_page(self, current, previous):
        """Slot, switch page of stack widget"""
        widget_num = self._tool_list.currentIndex().row()
        self._window.stack_widget.setCurrentIndex(widget_num)

    def create_item(self, name, icon, parent):
        """Create a standard list widget item, for option panel.

        Args:
          name: Name of option button
          icon: Icon name of option button
          parent: The QListWidget
        Returns:
          item: created option button
        """
        item = QListWidgetItem(parent)
        item.setText(name)
        item.setIcon(QIcon(icon))
        item.setStatusTip(name)
        item.setTextAlignment(Qt.AlignLeft)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

    @QtCore.Slot()
    def submit_form(self):
        pass

    @QtCore.Slot()
    def exit(self):
        self._window.close()
