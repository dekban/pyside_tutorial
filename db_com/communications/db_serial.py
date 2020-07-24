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
"""This is a Serial communication module.

This module has a class used to communicate via serial.

"""

import logging
import serial
import time
import threading

from serial.tools import list_ports

from db_com.communications.communication_interface import CommunicationInterface


class Serial(CommunicationInterface):
    """Class provides method to communicate with devices through Serial."""

    PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE = \
        'N', 'E', 'O', 'M', 'S'
    STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO = (1, 1.5, 2)
    FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS = (5, 6, 7, 8)

    def __init__(self, port, baudrate, databit=EIGHTBITS,
                 parity=PARITY_NONE, stopbits=STOPBITS_ONE, xonxoff=False,
                 rtscts=False, dsrdtr=False, read_terminal_character='\r\n',
                 write_terminal_character='\n', timeout=20, write_timeout=20,
                 read_handler=None):
        """Configure the driver initial values.

        Args:
          port: The serial port to use.
          baudrate: The baudrate to use.
          databit: The data bit to use.  Use FIVEBITS, SIXBITS,
            SEVENBITS or EIGHTBITS.
          parity: The parity to use.  Use PARITY_NONE, PARITY_EVEN,
            PARITY_ODD, PARITY_MARK or PARITY_SPACE.
          stopbits: The stop bits to use.
            Use STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE or STOPBITS_TWO.
          xonxoff: The boolean xonxoff to use.
          rtscts: The boolean rtscts to use.
          dsrdtr: The boolean dsrdtr to use.
          read_terminal_character: The terminal character expected when
            reading from the device.
          write_terminal_character: The terminal character expected when
            writing to the device.
          read_handler: The handler handles read data from read thread.
        Returns:
          None
        Raises:
          None
        """
        super(Serial, self).__init__()
        self._port = port
        self._baudrate = baudrate
        self._databit = databit
        self._parity = parity
        self._stopbits = stopbits
        self._xonxoff = xonxoff
        self._rtscts = rtscts
        self._dsrdtr = dsrdtr
        self._read_terminal_character = read_terminal_character
        self._write_terminal_character = write_terminal_character
        self._timeout = timeout
        self._write_timeout = write_timeout
        self._session = None
        self._reader_alive = None
        self._reader_thread = None
        self._read_handler = read_handler

    @property
    def session(self):
        """A property containing the serial session."""
        return self._session

    @property
    def port(self):
        """A property indicating the port."""
        return self._port

    @port.setter
    def port(self, value):
        """Sets the port."""
        self._port = value

    @property
    def baudrate(self):
        """A property indicating the baudrate."""
        return self._baudrate

    @baudrate.setter
    def baudrate(self, value):
        """Sets the baudrate."""
        self._baudrate = value

    @property
    def databit(self):
        """A property indicating the databit."""
        return self._databit

    @databit.setter
    def databit(self, value):
        """Sets the databit."""
        self._databit = value

    @property
    def parity(self):
        """A property indicating the parity."""
        return self._parity

    @parity.setter
    def parity(self, value):
        """Sets the parity."""
        self._parity = value

    @property
    def stopbits(self):
        """A property indicating the stopbits."""
        return self._stopbits

    @stopbits.setter
    def stopbits(self, value):
        """Sets the stopbits."""
        self._stopbits = value

    @property
    def xonxoff(self):
        """A property indicating the xonxoff."""
        return self._xonxoff

    @xonxoff.setter
    def xonxoff(self, value):
        """Sets the xonxoff."""
        self._xonxoff = value

    @property
    def rtscts(self):
        """A property indicating the rtscts."""
        return self._rtscts

    @rtscts.setter
    def rtscts(self, value):
        """Sets the rtscts."""
        self._rtscts = value

    @property
    def dsrdtr(self):
        """A property indicating the dsrdtr."""
        return self._dsrdtr

    @dsrdtr.setter
    def dsrdtr(self, value):
        """Sets the dsrdtr."""
        self._dsrdtr = value

    @property
    def read_handler(self):
        """The read handler for read thread."""
        return self._read_handler

    @read_handler.setter
    def read_handler(self, value):
        """Set read handler for read thread."""
        self._read_handler = value

    @staticmethod
    def list_ports():
        """List available serial port connections.

        Args:
          None.
        Returns:
          ports: list of available ports.
        Raises:
          None.
        """
        ports = [port for port in list_ports.comports()]

        return ports

    def open(self):
        """Open serial port connection.

        Args:
          None.
        Returns:
          None.
        Raises:
          None.
        """
        self._session = serial.Serial()
        self._session.port = self.port
        self._session.baudrate = self.baudrate
        self._session.bytesize = self.databit
        self._session.parity = self.parity
        self._session.stopbits = self.stopbits
        self._session.xonxoff = self.xonxoff
        self._session.rtscts = self.rtscts
        self._session.dsrdtr = self.dsrdtr
        self._session.timeout = 1
        self._session.open()
        logging.debug('Opened serial connection to {}'.format(self.port))

        if self._read_handler:
            self._start_reader()
            logging.debug('Open serial reader thread.')

    def close(self):
        """Close serial port connection.

        Args:
          None.
        Returns:
          None.
        Raises:
          None.
        """
        if self._session:
            if self._reader_alive:
                self._stop_reader()
            if self._session.isOpen():
                self._session.close()
            self._session = None
            # logging.debug('Closed serial connection to {}'.format(self.port))

    def read(self, timeout=None):
        """Reads data from the device.

        Args:
          timeout: The session timeout.
        Returns:
          read_buffer: The buffer read from device.
        Raises:
          None.
        """
        self._session.timeout = self._timeout
        if timeout is not None:
            self._session.timeout = timeout

        read_buffer = str(self._session.readline(),
                          'utf-8', 'ignore').strip('\x00')
        if read_buffer:
            logging.debug('read : {}'.format(read_buffer.strip(
                self._read_terminal_character)))

        return read_buffer.strip(self._read_terminal_character)

    def write(self, command, timeout=None, wait_between_characters=None):
        """Writes data to the device.

        Args:
          command: The string command to be written.
          timeout: The timeout for the connection.
          wait_between_characters: The time to wait between each character in
            the command to send.
        Returns:
          None.
        Raises:
          None.
        """
        logging.debug('write : {}'.format(command))
        self._session.writeTimeout = self._write_timeout
        if timeout is not None:
            self._session.writeTimeout = timeout

        if wait_between_characters is None:
            self._session.write(bytes(command + self._write_terminal_character,
                                      'utf-8'))
        else:
            for char in command:
                self._session.write(char)
                time.sleep(wait_between_characters)
            self._session.write(self._write_terminal_character)

    def query(self, command, timeout=None, write_timeout=None,
              wait_between_commands=None, wait_between_characters=None):
        """Writes to device and waits response.

        Args:
          command: The command that is sent to the device that generates a
            response.
          timeout: The timeout for reading from the connection.
          write_timeout: The timeout for writing to the connection.
          wait_between_commands: The time to wait between when the command is
            sent and when the read occurs.
          wait_between_characters: The time to wait between each character in
            the command to send.
        Returns:
          The response from the device.
        Raises:
          None.
        """
        logging.debug('query : {}'.format(command))
        self.write(command, write_timeout,
                   wait_between_characters=wait_between_characters)
        if wait_between_commands is not None:
            time.sleep(wait_between_commands)
        return self.read(timeout=timeout)

    def read_untils(self, read_until_list, timeout=None, force_abort=None):
        """Reads info from device until the read_until_list is
        reached or timeout has expired.

        Args:
          read_until_list: The expected list of strings from the device.
          timeout: The timeout for the connection.
          force_abort: The abort callback to force stop.
        Returns:
          response: Response from the device whether or not the
            read_until_list is obtained
        Raises:
          None.
        """
        read_timeout = self._timeout
        if timeout is not None:
            read_timeout = timeout

        start_time = time.time()
        response = ''
        read_buffer = ''

        continue_flag = True

        while continue_flag and (time.time() - start_time) <= read_timeout:
            if force_abort is not None and force_abort():
                return ''

            for key_string in read_until_list:
                if response.find(key_string) != -1 or \
                        read_buffer.find(key_string) != -1:
                    continue_flag = False

            read_data = str(self._session.readline(),
                            'utf-8', 'ignore').strip('\x00')
            if read_data:
                logging.debug(read_data.strip('\r\n'))
            read_buffer += read_data

            if read_buffer.find(self._read_terminal_character) != -1:
                response += read_buffer
                read_buffer = ''

        if read_buffer:
            response += read_buffer

        return response

    def read_until(self, read_until_string, timeout=None, force_abort=None):
        """Reads info from device until the read_until_string is
        reached or timeout has expired.

        Args:
          read_until_string: The expected string from the device.
          timeout: The timeout for the connection.
          force_abort: The abort callback to force stop.
        Returns:
          response: Response from the device whether or not the
            read_until_string is obtained
        Raises:
          None.
        """
        read_until_timeout = self._timeout
        if timeout is not None:
            read_until_timeout = timeout

        start_time = time.time()
        response = ''
        read_buffer = ''
        while response.find(read_until_string) == -1 \
                and read_buffer.find(read_until_string) == -1 \
                and (time.time() - start_time) <= read_until_timeout:
            if force_abort is not None and force_abort():
                return ''

            read_data = str(self._session.readline(),
                            'utf-8', 'ignore').strip('\x00')
            if read_data:
                logging.debug(read_data.strip('\r\n'))
            read_buffer += read_data

            if read_buffer.find(self._read_terminal_character) != -1:
                response += read_buffer
                read_buffer = ''

        if read_buffer:
            response += read_buffer

        return response

    def query_until(self, command, read_until_string, timeout=None,
                    wait_between_commands=None, wait_between_characters=None,
                    write_timeout=None):
        """Writes to device, and reads response until read_until_string or
        timeout has expired.

        Args:
          command: The command that is sent to the device that generates a
            response.
          read_until_string: The expected string from the device.
          timeout: The timeout for reading from the connection.
          wait_between_commands: The time to wait between when the command is
            sent and when the read occurs.
          wait_between_characters: The time to wait between each character in
            the command to send.
          write_timeout: The timeout for writing to the connection.
        Returns:
          Response from the device whether or not the read_until_string is
            obtained.
        Raises:
          None.
        """
        logging.debug('query : {}, until {}'.format(command, read_until_string))
        self.write(command, write_timeout,
                   wait_between_characters=wait_between_characters)
        if wait_between_commands is not None:
            time.sleep(wait_between_commands)
        return self.read_until(read_until_string, timeout=timeout)

    def reader(self):
        """Thread function, reading serial data and send to handler."""
        data = None
        try:
            while self._reader_alive:
                data = self.read()
                if data:
                    self._read_handler(data)
        except self._session.SerialException:
            self._reader_alive = False
            logging.error(data)
            raise

    def _start_reader(self):
        """Start reader thread"""
        self._reader_alive = True
        self._reader_thread = threading.Thread(target=self.reader,
                                               name='Serial_Rx')
        self._reader_thread.daemon = True
        self._reader_thread.start()

    def _stop_reader(self):
        """Stop reader thread only, wait for clean exit of thread"""
        self._reader_alive = False
        if hasattr(self._session, 'cancel_read'):
            self._session.cancel_read()
        self._reader_thread.join()
