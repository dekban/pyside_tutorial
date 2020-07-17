#!/usr/bin/python

"""The Help Page, perform helping massages.

Provide helping massage to users.
"""

from PySide2.QtWidgets import QWidget, QTextEdit, QGridLayout
from PySide2.QtGui import QFont


class TextPage(QWidget):
    def __init__(self, parent=None, text=''):
        super(TextPage, self).__init__(parent)
        self._widget = None
        self._help_edit = None
        self._text = text

        self.ui_setup()

    @property
    def widget(self):
        return self._widget

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    def ui_setup(self):
        self._widget = QWidget()
        self._help_edit = QTextEdit()

        text_font = QFont()
        text_font.setFixedPitch(True)
        text_font.setFamily('monospace')

        style = 'color: rgb(6, 117, 0);' \
                'background-color: rgb(230, 255, 230);' \
                'border: no-border;'

        self._help_edit.setFont(text_font)
        self._help_edit.setStyleSheet(style)
        self._help_edit.setText(self.text)

        main_layout = QGridLayout()
        main_layout.addWidget(self._help_edit, 0, 0, 1, 1)

        self._widget.setLayout(main_layout)
