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
import abc


class CommunicationInterface(object):
    """Interface for Communication drivers.
    All Communications must drive from this class."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def session(self):
        """An abstract property indicating the session."""
        raise NotImplementedError

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        """Initializes the class."""
        pass

    @abc.abstractmethod
    def open(self):
        """The abstract method to open the connection."""
        raise NotImplementedError

    @abc.abstractmethod
    def close(self):
        """The abstract method to close the connection."""
        raise NotImplementedError

    @abc.abstractmethod
    def read(self, timeout=None):
        """The abstract method to read."""
        raise NotImplementedError

    @abc.abstractmethod
    def write(self, command, timeout=None, wait_between_characters=None):
        """The abstract method to write. Receives the command to be
        written."""
        raise NotImplementedError

    @abc.abstractmethod
    def query(self, command, timeout=None, wait_between_commands=0):
        """The abstract method for the query."""
        raise NotImplementedError

    @abc.abstractmethod
    def read_until(self, read_until_string, timeout=None):
        """The abstract method to read."""
        raise NotImplementedError

    @abc.abstractmethod
    def query_until(self, command, read_until_string, timeout=None,
                    wait_between_commands=None, wait_between_characters=None):
        """The abstract method for the query."""
        raise NotImplementedError
