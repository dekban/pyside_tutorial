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

"""
utilities_widget.py:
    This widget include all application utilities.
"""

import logging


from PySide2 import QtCore
from PySide2.QtGui import QPalette, QFontDatabase
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout
from PySide2.QtWidgets import QLabel, QTextEdit, QLineEdit, QPushButton

from db_com.user_interface.serial_panel import SerialPanel
from db_com.communications.db_serial import Serial


class QSerial(QtCore.QObject):
    ready_read = QtCore.Signal(str)


class UtilWidget(QWidget, QtCore.QObject):
    def __init__(self, serial=None, parent=None):
        super(UtilWidget, self).__init__(parent)
        self._serial = None
        self._title = QLabel('Utilities')
        self._main_layout = None
        self._reader_alive = None
        self._reader_thread = None
        self._serial_panel = SerialPanel()
        self._serial_recv_box = QTextEdit()
        self._serial_send_box = QLineEdit()
        self._send_button = QPushButton('Send')

        self._ui_setup()
        self._serial_panel.refresh_ports()

        self._qserial = QSerial()

        self._send_button.clicked.connect(self.send_command)
        self._serial_panel.open_button.clicked.connect(self.open_port)
        self._serial_panel.close_button.clicked.connect(self.close_port)
        self._qserial.ready_read.connect(self.read_handler)

        self._serial = Serial('', '115200', read_handler=self.ready_read)

    def _ui_setup(self):
        """Initialize user interface, and set color, size, alignment .etc."""
        cmd_palette = QPalette()
        font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        cmd_palette.setColor(QPalette.Base, QtCore.Qt.black)
        cmd_palette.setColor(QPalette.Text, QtCore.Qt.green)

        self._serial_recv_box.setFont(font)
        self._serial_recv_box.setReadOnly(True)
        self._serial_recv_box.setPalette(cmd_palette)

        self._send_button.setEnabled(False)

        cmd_layout = QHBoxLayout()
        cmd_layout.addWidget(self._serial_send_box)
        cmd_layout.addWidget(self._send_button)

        self._main_layout = QVBoxLayout(self)
        self._main_layout.addWidget(self._title)
        self._main_layout.addWidget(self._serial_panel)
        self._main_layout.addWidget(self._serial_recv_box)
        self._main_layout.addLayout(cmd_layout)

        self.setLayout(self._main_layout)

    @property
    def serial_recv_box(self):
        return self._serial_recv_box

    @property
    def ready_read(self):
        return self._qserial.ready_read.emit

    @QtCore.Slot()
    def open_port(self):
        """Get serial parameters from serial panel and connect to serial."""
        if not self._serial:
            logging.warning('Serial port not initialized yet.')
            return

        self._serial.close()
        logging.debug('Closed serial port before open.')

        port_kwargs = self._serial_panel.port_kwargs()
        try:
            self._serial.port = port_kwargs['port']
            self._serial.baudrate = port_kwargs['baud']
            self._serial.databit = port_kwargs['data_bit']
            self._serial.parity = port_kwargs['parity']
            self._serial.stopbits = port_kwargs['stop_bit']

            if port_kwargs['flow_ctrl'] == 'xonxoff':
                self._serial.xonxoff = True
            elif port_kwargs['flow_ctrl'] == 'rtscts':
                self._serial.rtscts = True
            elif port_kwargs['flow_ctrl'] == 'dsrdtr':
                self._serial.dsrdtr = True
        except ValueError:
            logging.debug('Having error in port parameters')
            logging.debug('port_kwargs = {}'.format(port_kwargs))

        try:
            self._serial.open()
            self._send_button.setEnabled(True)
            self._serial_panel.open_button.setEnabled(False)
            self._serial_panel.close_button.setEnabled(True)
        except IOError:
            logging.debug('Open serial port error')

    @QtCore.Slot()
    def close_port(self):
        """Terminate serial connection and destroy session object."""
        self._serial_panel.open_button.setEnabled(True)
        self._serial_panel.close_button.setEnabled(False)
        self._send_button.setEnabled(False)

        self._serial.close()
        logging.debug('Serial port closed')

    @QtCore.Slot()
    def send_command(self):
        """Slot to send command trough serial port."""
        self._serial.write(self._serial_send_box.text())

    @QtCore.Slot()
    def read_handler(self, data):
        self._serial_recv_box.append(data)
