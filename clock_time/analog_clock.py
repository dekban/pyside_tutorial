#!venv/bin/python3

import math

from PySide2 import QtCore
from PySide2.QtCore import QPoint, QRect, Qt, QTime
from PySide2.QtGui import QColor, QBrush, QFont, QPainter, QPolygon
from PySide2.QtWidgets import QWidget

basic_size = 50


class AnalogClock(QWidget):
    hour_pin = QPolygon([
        QPoint(2, 5),
        QPoint(-2, 5),
        QPoint(0, -45)
    ])
    minute_pin = QPolygon([
        QPoint(2, 5),
        QPoint(-2, 5),
        QPoint(0, -75),
    ])

    hour_pin_color = QColor('#da8602')
    min_pin_color = QColor('#2196f3')

    background_color = QColor(255, 255, 255, 32)
    edge_color = QColor(255, 255, 255, 96)
    text_color = QColor(120, 255, 255, 128)

    def __init__(self, parent=None, size=basic_size):
        super(AnalogClock, self).__init__(parent)
        self._time = QTime.currentTime()

        self.setAttribute(Qt.WA_TranslucentBackground)

        if size is None:
            size = basic_size
            self.resize(size, size)
        else:
            if size < basic_size:
                size = basic_size
            self.resize(size, size)

        font = QFont()
        font.setStyleHint(QFont.SansSerif)
        font.setFamily('monospace')
        font.setPointSize(12)
        self.font = font

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value: QTime):
        self._time = value
        self.update_frame()

    def paintEvent(self, event):
        side = min(self.width(), self.height())
        curr_time = self._time

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)

        # draw clock frame
        painter.setBrush(QBrush(self.background_color))
        r = side/2
        painter.drawEllipse(QPoint(0, 0), side/2, side/2)

        for i in range(0, 12):
            x, y = self.rotate_point(0, -r * 0.95, i * 360/12)
            painter.drawEllipse(x - 3, y - 3, 6, 6)

        painter.setPen(self.text_color)
        for i in range(0, 12):
            x, y = self.rotate_point(0, -r * 0.85, i * 360/12)
            painter.drawText(QRect(x - 10, y - 10, 20, 20),
                             Qt.AlignCenter, "%d" % i)

        painter.setPen(self.background_color)
        painter.setBrush(QBrush(self.min_pin_color))
        for j in range(0, 60):
            if j % 5 != 0:
                x, y = self.rotate_point(0, -r * 0.95, j * 360/60)
                painter.drawEllipse(x - 1, y - 1, 2, 2)
        painter.setClipping(False)

        # draw hands
        painter.setBrush(QBrush(self.hour_pin_color))

        painter.save()
        self.hour_pin[2] = QPoint(0, int(-r * 0.6))
        painter.rotate(30.0 * (curr_time.hour() + curr_time.minute() / 60.0))
        painter.drawConvexPolygon(self.hour_pin)
        painter.restore()

        painter.setBrush(QBrush(self.min_pin_color))

        painter.save()
        self.minute_pin[2] = QPoint(0, int(-r * 0.9))
        painter.rotate(6.0 * (curr_time.minute() + curr_time.second() / 60.0))
        painter.drawConvexPolygon(self.minute_pin)
        painter.restore()

        painter.end()

    @QtCore.Slot()
    def update_frame(self):
        time = QTime.currentTime()
        if time.second() % 10 == 0:
            self.update()

    @staticmethod
    def rotate_point(x, y, degree):
        theta = degree * math.pi / 180
        sin = math.sin(theta)
        cos = math.cos(theta)
        return x * cos - y * sin, x * sin + y * cos
