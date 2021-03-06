#!venv/bin/python3

from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtCore import QFile, QSize
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QListWidgetItem, QListView
from PySide2.QtWidgets import QTableWidgetItem, QHeaderView
from PySide2.QtWidgets import QTreeWidgetItem, QTreeWidget
from PySide2.QtGui import QFont, QIcon, QColor


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
        self._list_items = list()

        self.setup_ui()

    @property
    def window(self):
        """The main window object"""
        return self._window

    def setup_ui(self):
        loader = QUiLoader()
        file = QFile('./media/main_window.ui')
        file.open(QFile.ReadOnly)
        self._window = loader.load(file)
        file.close()

        self.set_title()
        self.set_buttons()

        # Setup ListWidget
        self._list_items.append(self.create_item('Play', './media/play.ico', self._window.tool_list))
        self._list_items.append(self.create_item('Pause', './media/pause.ico', self._window.tool_list))
        self._list_items.append(self.create_item('Stop', './media/stop.ico', self._window.tool_list))

        self._window.tool_list.setCurrentRow(0)
        self._window.tool_list.setViewMode(QListView.ListMode)
        # self._window.tool_list.setViewMode(QListView.IconMode)
        self._window.tool_list.setSpacing(3)
        self._window.tool_list.setItemAlignment(QtCore.Qt.AlignCenter)
        self._window.tool_list.setEnabled(True)

        # Setup TableWidget
        data = 'Name Job Level Attack Defense DPS\n' \
               'Arey Newbie 5 30 10 0.3\n' \
               'Alice Witch 30 150 32 1.0\n' \
               'Moly Knight 42 200 70 1.7\n' \
               'Cathy Ranger 35 170 41 2.0' \

        data_list = list()
        for row in data.split('\n'):
            col = row.split(' ')
            data_list.append(col)

        table = self._window.data_table
        table.verticalHeader().setDefaultSectionSize(18)
        table.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalScrollBar().setVisible(False)
        table.horizontalScrollBar().setVisible(False)

        header_data = data_list.pop(0)
        table.setColumnCount(len(header_data))
        table.setRowCount(len(data_list))

        for idx, data in enumerate(header_data):
            header = self.create_cell(data)
            table.setHorizontalHeaderItem(idx, header)

        for row_num, row in enumerate(data_list):
            for col_num, col_data in enumerate(row):
                item = self.create_cell(col_data)
                item.setToolTip('row{},Col{}'.format(row_num, col_num))
                table.setItem(row_num, col_num, item)

        # Setup TreeWidget
        tree = self._window.hero_tree
        tree.setIndentation(5)
        tree.setColumnCount(2)
        tree.setFont(QFont('Free Mono', 11))

        header = QTreeWidgetItem(['Name', 'Value'])
        tree.setHeaderItem(header)

        for hero in data_list:
            hero_root = self.create_root(tree, header_data[0], hero[0])
            for idx in range(1, len(hero)):
                hero_attr = self.create_child(header_data[idx], hero[idx])
                hero_root.addChild(hero_attr)

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

        return item

    def create_cell(self, data: str):
        """Create data cell on UI."""
        cell = QTableWidgetItem(data)
        cell.setFont(QFont('Free Mono', 11))
        cell.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        return cell

    def create_root(self, parent, name, value):
        root = QTreeWidgetItem(parent)
        root.setText(0, name)
        root.setText(1, value)
        root.setTextColor(0, QColor('#ffffff'))
        root.setTextColor(1, QColor('#ffffff'))
        root.setBackgroundColor(0, QColor('#0066cc'))
        root.setBackgroundColor(1, QColor('#0066cc'))

        return root

    def create_child(self, name, value):
        """Create child item of the tree"""
        root = QTreeWidgetItem()
        root.setText(0, name)
        root.setText(1, value)
        root.setTextColor(0, QColor('#0066cc'))
        root.setTextColor(1, QColor('#0066cc'))
        root.setBackgroundColor(0, QColor('#ccffff'))
        root.setBackgroundColor(1, QColor('#ccffff'))

        return root

    @QtCore.Slot()
    def submit_form(self):
        pass

    @QtCore.Slot()
    def exit(self):
        self._window.close()
