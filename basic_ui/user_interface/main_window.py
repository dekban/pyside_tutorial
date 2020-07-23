#!/usr/bin/python
#
# Copyright © 2020 DekBan - All Right Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Mainwindow of the user interface, host and control the operation.
"""

from collections import OrderedDict

from PySide2 import QtCore
from PySide2.QtCore import QObject, Qt, QSize, QFile
from PySide2.QtGui import QFont, QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QListView, QListWidget, QListWidgetItem
from PySide2.QtWidgets import QStatusBar, QWidget

from basic_ui.user_interface.item_widget import ItemWidget
from basic_ui.user_interface.text_page import TextPage

__copyright__ = 'Copyright © 2020 DekBan - All Right Reserved.'
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


class MainWindow(QObject):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._window = None
        self._option_panel = None
        self._pages = OrderedDict()

        self.ui_setup()

    @property
    def window(self):
        """MainWindow widget."""
        return self._window

    def ui_setup(self):
        """Initialize user interface of main window."""
        loader = QUiLoader()
        file = QFile('./user_interface/form/mainwindow.ui')
        file.open(QFile.ReadOnly)
        self._window = loader.load(file)
        file.close()

        status_bar = QStatusBar(self._window)
        status_bar.showMessage(__copyright__)
        self._window.setStatusBar(status_bar)
        self._window.setWindowIcon(QIcon('./user_interface/media/bucketing_icon.jpeg'))
        self._window.setWindowTitle('PySide2 Project - Basic UI Framework')

        self._option_panel = OptionPanel()
        self._option_panel.add_button('DekBan', './user_interface/media/dekban.png')
        self._option_panel.add_button('Charlie', './user_interface/media/charlie.jpeg')
        self._option_panel.add_button('Simon', './user_interface/media/Simon.jpeg')

        # Add widget to main layout
        main_layout = self._window.main_layout
        main_layout.itemAtPosition(0, 0).setAlignment(QtCore.Qt.AlignCenter)
        main_layout.itemAtPosition(0, 1).setAlignment(QtCore.Qt.AlignVCenter)
        main_layout.addWidget(self._option_panel, 2, 0, 1, 1)

        # Add page widget to stack
        self._pages['item'] = ItemWidget()
        self._pages['text1'] = TextPage(text=PAUSE_TEXT)
        self._pages['text2'] = TextPage(text=STOP_TEXT)

        for index, name in enumerate(self._pages):
            print('pages {} : {} page'.format(index, name))
            self._window.widget_stack.addWidget(self._pages[name].widget)

        self._window.widget_stack.setCurrentIndex(0)

        # Build up signal / slot
        self._option_panel.currentItemChanged.connect(self.set_page)

    @QtCore.Slot(int, int)
    def set_page(self, current, previous):
        """Slot, switch shown page."""
        widget_num = self._option_panel.currentIndex().row()
        self._window.widget_stack.setCurrentIndex(widget_num)


class OptionPanel(QListWidget):
    STYLE = 'QListWidget { border : none; ridge #404244;' \
            'font : 10pt bold \"Source Code Pro\";' \
            'background-color: #3c413f; color: #d3d7cf; outline: none;}' \
            'QListWidget::Item {border-bottom: 1px solid #999999;}' \
            'QListWidget::item:hover { background-color: ' \
            'qlineargradient( x1: 0, y1: 0, x2: 0, y2: 1,' \
            ' stop: 1 #4d4d4d, stop: 0 transparent); color: #d3d7cf;}' \
            'QListView::item:selected { background-color:' \
            'qlineargradient( x1: 0, y1: 0, x2: 0, y2: 1,' \
            ' stop: 1 transparent, stop: 0 #304030); color: #55dd66;}'

    def __init__(self, parent=None):
        super(OptionPanel, self).__init__(parent)
        self._options_buttons = OrderedDict()

        self.setCurrentRow(0)
        self.setMaximumWidth(80)
        self.setMinimumSize(QSize(80, 400))
        self.setViewMode(QListView.IconMode)
        self.setMovement(QListView.Static)
        self.setIconSize(QSize(48, 48))
        self.setSpacing(3)
        self.setItemAlignment(Qt.AlignCenter)
        self.setEnabled(True)
        self.setStyleSheet(self.STYLE)

    def option_buttons(self):
        """List of option buttons"""
        return self._options_buttons

    def add_button(self, name, icon):
        self._options_buttons[name] = self.create_item(name, icon)
        self.addItem(self._options_buttons[name])

    def create_item(self, name, icon):
        """Create a standard list widget item, for option panel.

        Args:
          name: Name of option button
          icon: Icon name of option button
        Returns:
          item: created option button
        """
        item = QListWidgetItem(self)
        item.setText(name)
        item.setIcon(QIcon(icon))
        item.setStatusTip(name)
        item.setSizeHint(QSize(75, 70))
        item.setTextAlignment(Qt.AlignCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        return item
