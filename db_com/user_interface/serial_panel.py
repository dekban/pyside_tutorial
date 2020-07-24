# !/usr/bin/python
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

"""
serial_panel.py:
    user interface used to set up serial port.
"""

import logging
from collections import OrderedDict

from PySide2 import QtCore
from PySide2.QtGui import QColor, QFont
from PySide2.QtWidgets import QComboBox, QPushButton
from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem

from db_com.communications.db_serial import Serial

TITLE_COLOR = '#0066cc'
TXT_COLOR = '#eeeeee'
ODD_COLOR = '#ccffff'
EVEN_COLOR = '#eeffff'
COMBO_BOX_STYLE = 'background: #eeeeee;; color: #2d2d2d'


class SerialPanel(QTreeWidget):
    def __init__(self, parent=None):
        super(SerialPanel, self).__init__(parent)
        self._title = None
        self._refresh_button = QPushButton('Refresh')
        self._open_button = QPushButton('Open')
        self._close_button = QPushButton('Close')

        self._items_name = ['port', 'baud', 'data_bit', 'parity'
                            , 'stop_bit', 'flow_ctrl']
        self._items = OrderedDict()
        self._combo_boxes = OrderedDict()

        self.ui_setup()

        self._refresh_button.clicked.connect(self.refresh_ports)

    @property
    def open_button(self):
        return self._open_button

    @property
    def close_button(self):
        return self._close_button

    def ui_setup(self):
        """Create setup user interface of serial port."""
        self.setHeaderHidden(True)
        self.setFixedSize(205, 205)
        self.setIndentation(0)
        self.setColumnCount(2)
        self.setColumnWidth(0, 100)
        self.setColumnWidth(1, 90)

        self._items['title'] = QTreeWidgetItem(self)
        self._items['title'].setText(0, 'Serial Port')
        self._items['title'].setTextColor(0, QColor(TXT_COLOR))
        self._items['title'].setFont(0, QFont('ubuntu', 11, QFont.Bold))
        self._items['title'].setBackgroundColor(0, QColor(TITLE_COLOR))
        self._items['title'].setBackgroundColor(1, QColor(TITLE_COLOR))

        for name in self._items_name:
            self._items[name] = QTreeWidgetItem(self)
            self._combo_boxes[name] = QComboBox(self)
            self._combo_boxes[name].setFixedSize(100, 24)
            self._combo_boxes[name].setStyleSheet(COMBO_BOX_STYLE)

        self._items['port'].setText(0, 'PortName')
        self._items['port'].setTextColor(0, QColor(TITLE_COLOR))
        self._items['port'].setBackgroundColor(0, QColor(ODD_COLOR))
        self._items['port'].setBackgroundColor(1, QColor(ODD_COLOR))
        for port in Serial.list_ports():
            if port.name:
                self._combo_boxes['port'].addItem(port.name, port.device)

        self._items['baud'].setText(0, 'BaudRate')
        self._items['baud'].setTextColor(0, QColor(TITLE_COLOR))
        self._items['baud'].setBackgroundColor(0, QColor(EVEN_COLOR))
        self._items['baud'].setBackgroundColor(1, QColor(EVEN_COLOR))
        self._combo_boxes['baud'].addItem('115200', 115200)
        self._combo_boxes['baud'].addItem('57600', 57600)
        self._combo_boxes['baud'].addItem('38400', 38400)
        self._combo_boxes['baud'].addItem('9600', 9600)

        self._items['data_bit'].setText(0, 'DataBit')
        self._items['data_bit'].setTextColor(0, QColor(TITLE_COLOR))
        self._items['data_bit'].setBackgroundColor(0, QColor(EVEN_COLOR))
        self._items['data_bit'].setBackgroundColor(1, QColor(EVEN_COLOR))
        self._combo_boxes['data_bit'].addItem('8', Serial.EIGHTBITS)
        self._combo_boxes['data_bit'].addItem('7', Serial.SEVENBITS)
        self._combo_boxes['data_bit'].addItem('6', Serial.SIXBITS)
        self._combo_boxes['data_bit'].addItem('5', Serial.FIVEBITS)

        self._items['parity'].setText(0, 'Parity')
        self._items['parity'].setTextColor(0, QColor(TITLE_COLOR))
        self._items['parity'].setBackgroundColor(0, QColor(ODD_COLOR))
        self._items['parity'].setBackgroundColor(1, QColor(ODD_COLOR))
        self._combo_boxes['parity'].addItem('None', Serial.PARITY_NONE)
        self._combo_boxes['parity'].addItem('Even', Serial.PARITY_EVEN)
        self._combo_boxes['parity'].addItem('Odd', Serial.PARITY_ODD)
        self._combo_boxes['parity'].addItem('Mark', Serial.PARITY_MARK)
        self._combo_boxes['parity'].addItem('Space', Serial.PARITY_SPACE)

        self._items['stop_bit'].setText(0, 'StopBit')
        self._items['stop_bit'].setTextColor(0, QColor(TITLE_COLOR))
        self._items['stop_bit'].setBackgroundColor(0, QColor(EVEN_COLOR))
        self._items['stop_bit'].setBackgroundColor(1, QColor(EVEN_COLOR))
        self._combo_boxes['stop_bit'].addItem('1', Serial.STOPBITS_ONE)
        self._combo_boxes['stop_bit'].addItem('1.5',
                                              Serial.STOPBITS_ONE_POINT_FIVE)
        self._combo_boxes['stop_bit'].addItem('2', Serial.STOPBITS_TWO)

        self._items['flow_ctrl'].setText(0, 'FlowCtrl')
        self._items['flow_ctrl'].setTextColor(0, QColor(TITLE_COLOR))
        self._items['flow_ctrl'].setBackgroundColor(0, QColor(ODD_COLOR))
        self._items['flow_ctrl'].setBackgroundColor(1, QColor(ODD_COLOR))
        self._combo_boxes['flow_ctrl'].addItem('None', None)
        self._combo_boxes['flow_ctrl'].addItem('xonxoff', 'xonxoff')
        self._combo_boxes['flow_ctrl'].addItem('rtscts', 'rtscts')
        self._combo_boxes['flow_ctrl'].addItem('dsrdtr', 'dsrdtr')

        self._refresh_button.setFixedSize(90, 25)
        self.setItemWidget(self._items['title'], 1, self._refresh_button)

        for name in self._items_name:
            self.setItemWidget(self._items[name], 1, self._combo_boxes[name])

        opt_item = QTreeWidgetItem(self)
        opt_item.setBackgroundColor(0, QColor(EVEN_COLOR))
        opt_item.setBackgroundColor(1, QColor(EVEN_COLOR))

        self._close_button.setEnabled(False)
        self._open_button.setEnabled(True)
        self.setItemWidget(opt_item, 1, self._close_button)
        self.setItemWidget(opt_item, 0, self._open_button)

    @QtCore.Slot()
    def refresh_ports(self):
        """Slot to refresh serial port name list.

        Args:
          None.
        Returns:
          None
        Raises:
          None
        """
        logging.debug('Refresh ports')
        self._combo_boxes['port'].clear()

        for port in Serial.list_ports():
            if port.device:
                self._combo_boxes['port'].addItem(port.device, port.device)

    def port_kwargs(self):
        """Return dict of current serial port setup.

        Args:
          None.
        Returns:
          None
        Raises:
          port_kwargs: dict of serial port setup.
        """
        port_kwargs = OrderedDict()
        for name in self._items_name:
            port_kwargs[name] = self._combo_boxes[name].currentData()

        return port_kwargs
