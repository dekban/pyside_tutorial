#!venv/bin/python3

from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QFontDialog
from PySide2.QtGui import QFont, QIcon


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
        self.set_edits()

        # set label stylesheet
        label_style = 'QLabel{' \
                      'border-radius: 5px;' \
                      'background-color :' \
                      'QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1,' \
                      'stop: 0 #ff5500, stop: 1 #0055ff);' \
                      'border-image:url(\'./media/hot_article.png\');' \
                      'font: bold 14px;' \
                      '}'
        ss_label = self._window.stylesheet_label
        ss_label.setStyleSheet(label_style)
        ss_label.setFixedSize(203, 72)

        # set button stylesheet
        button_style = """
            QPushButton {
                border: 2px solid #0033aa;
                border-radius: 6px;
                background-color: #00aaff;
                color: #000000;
                
                min-width: 80px;
            }
            
            QPushButton:hover {
                color: #ffffff;
                background-color: QLinearGradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                                  stop: 0 #000000, stop: 1 #00aaff);
            }
            
            QPushButton:pressed {
                background-color: #FFA823;
                color: #000000;
                font: bold 14px;
            }
        """
        ss_btn = self._window.stylesheet_btn
        ss_btn.setText('Style Sheet')
        ss_btn.setStyleSheet(button_style)

        # set progress bar
        self._window.add_btn.clicked.connect(self.add_ten)
        self._window.reset_btn.clicked.connect(self.reset_progress)
        self._window.progress_bar.valueChanged.connect(
            lambda v: self._window.output_text.append(str(v)))

        progress_style = """
            QProgressBar {
                border: 2px solid #ee9933;
                border-radius: 3px;
                text-align: center;
            }
            
            QProgressBar:chunk {
                background-color: QLinearGradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                                  stop: 0 #000000, stop: 1 #00ff33);
                width: 20px;
                margin: 1px;
            }
        """
        self._window.progress_bar.setStyleSheet(progress_style)

    def set_title(self):
        """Setup label"""
        self._window.title.setText('This is PySide2 Tutorial')

        # set font
        font = QFont("Arial", 20, QFont.Black)
        # font.setLetterSpacing(QFont.AbsoluteSpacing, 5)
        font.setWordSpacing(10.0)

        self._window.title.setFont(font)
        # set widget size (x, y, width, height)
        self._window.title.setGeometry(0, 0, 600, 30)
        # set alignment
        self._window.title.setAlignment(Qt.AlignBottom | Qt.AlignCenter)

    def set_buttons(self):
        """Setup buttons"""
        self._window.color_btn.setText('Choose Font')
        self._window.exit_btn.setText('Exit')
        self._window.palette_btn.setText('Set Font')

        self._window.color_btn.setIcon(QIcon('./media/font.png'))

        self._window.color_btn.clicked.connect(self.choose_font)
        self._window.palette_btn.clicked.connect(self.set_palette)
        self._window.exit_btn.clicked.connect(self.exit)

    def set_edits(self):
        """Setup line edit and text edit"""
        self._window.input_line.setPlaceholderText('Input item to import')
        self._window.output_text.setPlaceholderText('Import Item')

    @QtCore.Slot()
    def choose_font(self):
        (ret, r_font) = QFontDialog().getFont(self._window.font(), self._window, 'Get some font',
                                              QFontDialog.ScalableFonts | QFontDialog.MonospacedFonts)
        if ret:
            print('select ok')
            self._window.input_line.setText(r_font.__repr__())
        else:
            print('select cancelled')

    @QtCore.Slot()
    def add_ten(self):
        value = self._window.progress_bar.value()
        if value < 90:
            value += 10
        else:
            value = 100

        self._window.progress_bar.setValue(value)

    @QtCore.Slot()
    def reset_progress(self):
        self._window.progress_bar.reset()

    @QtCore.Slot()
    def exit(self):
        self._window.close()
