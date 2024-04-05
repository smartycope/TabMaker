# This Python file uses the following encoding: utf-8
from math import floor
from clipboard import copy, paste
import os
import random
import re
import sys
from copy import deepcopy
import EasyRegex as er

from PyQt6 import uic
from PyQt6.QtCore import QEvent, QFile, QSize, Qt, QPoint, QModelIndex, QTimer
from PyQt6.QtGui import QBrush, QColor, QIcon, QImage, QPalette, QPixmap, QStandardItemModel, QStandardItem, QShortcut, QKeyEvent
from PyQt6.QtWidgets import (QAbstractButton, QAbstractSpinBox, QApplication, QComboBox, QHBoxLayout, QDoubleSpinBox, QMenu, QMenuBar,
                             QCommonStyle, QDialogButtonBox, QFileDialog, QItemDelegate, QStyledItemDelegate, QPushButton,
                             QListView, QListWidget, QMainWindow, QMdiArea,QHeaderView, QTableView, QLineEdit, QSpinBox,
                             QMdiSubWindow, QMessageBox, QProxyStyle, QSlider,QTableWidgetItem, QLabel,
                             QStyle, QStyleFactory, QWidget, QCheckBox, QAbstractItemView)


DEFAULT_NOTE = '-------'
half = DEFAULT_NOTE[0] * floor((len(DEFAULT_NOTE) / 2))

class Note(QStyledItemDelegate):
    def __init__(self, model, *args, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)

    def setModelData(self, editor, model, index):
        # half = DEFAULT_NOTE[0] * floor(len(DEFAULT_NOTE) / 2)
        # model.setData(index, half + str(editor.value()) + half)
        model.setData(index, editor.text())

    def setEditorData(self, editor, index):
        # s = self.model.data(index)
        # if s == DEFAULT_NOTE:
        #     editor.setValue(int(0))
        # else:
        #     m = re.match('.+(\d+).+', s).groups()[0]
        #     if m is not None:
        #         editor.setValue(int(m))
        editor.setText(self.model.data(index))

    def createEditor(self, parent, option, index):
        # spin = QSpinBox(parent)
        # spin.setMinimum(0)
        # spin.setMaximum(30)
        # spin.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # return spin
        # return QWidget(parent)
        return QLabel(parent)

class NoteModel(QAbstractTableModel):
    # def rowCount(const QModelIndex & /* parent */) const
        # return modelImage.height();
    # int ImageModel::columnCount(const QModelIndex & /* parent */) const
        # return modelImage.width();


# The data() function returns data for the item that corresponds to a given model index in a format that is suitable for a particular role:
    def data(index, role):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None
        return
"""
    def headerData(section, orientation, role):
        if role == Qt.ItemDataRole.SizeHintRole:
            return QSize(1, 1)
        return None
 """

class MainWindow(QTableView):
    START_COL_COUNT = 100
    ADD_COL_AMT = 10
    def __init__(self):
        super().__init__()
        self.menu = QMenuBar(self)
        # self.menu.addMenu('file')
        self.fileMenu = QMenu('file', self.menu)
        self.fileMenu.addAction('Save', self.save)
        self.fileMenu.addAction('Open', self.load)
        self.fileMenu.addAction('Copy to Clipboard', lambda: copy(self.serialize()))
        self.fileMenu.addAction('Load from Clipboard', lambda: self.deserialize(paste()))
        self.menu.addMenu(self.fileMenu)

        self.editMenu = QMenu('edit', self.menu)
        self.editMenu.addAction('Add More Rows', lambda: self.addCol(amt=self.ADD_COL_AMT), 'n')
        self.editMenu.addAction('Add 1 More Row', self.addCol, 'n')
        self.menu.addMenu(self.editMenu)

        self.setWindowTitle('Tab Maker')
        self.setEditTriggers(QAbstractItemView.EditTrigger.AnyKeyPressed | QAbstractItemView.EditTrigger.DoubleClicked | QAbstractItemView.EditTrigger.SelectedClicked | QAbstractItemView.EditTrigger.EditKeyPressed)
        self.setDragEnabled(False)
        # self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectColumns)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.setTextElideMode(Qt.TextElideMode.ElideNone)
        self.horizontalHeader().setMinimumSectionSize(5)
        self.horizontalHeader().setDefaultSectionSize(5)
        self.setShowGrid(False)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setSizeAdjustPolicy(QAbstractItemView.SizeAdjustPolicy.AdjustToContents)

        self.addMoreShortcut = QShortcut(self)
        self.addMoreShortcut.activated.connect(lambda: self.addCol(amt=self.ADD_COL_AMT))

        self.model = QStandardItemModel(0, 0)
        self.model.setVerticalHeaderLabels(['e', 'a', 'd', 'g', 'b', 'e'])
        self.setModel(self.model)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.setItemDelegate(Note(self.model, self))

        for _ in range(self.START_COL_COUNT):
            self.addCol()

    def keyPressEvent(self, e):
        index = self.currentIndex()
        if e.text() == '0':
            self.model.setData(index, half + '0' + half)
        elif e.text() == '1':
            self.model.setData(index, half + '1' + half)
        elif e.text() == '2':
            self.model.setData(index, half + '2' + half)
        elif e.text() == '3':
            self.model.setData(index, half + '3' + half)
        elif e.text() == '4':
            self.model.setData(index, half + '4' + half)
        elif e.text() == '5':
            self.model.setData(index, half + '5' + half)
        elif e.text() == '6':
            self.model.setData(index, half + '6' + half)
        elif e.text() == '7':
            self.model.setData(index, half + '7' + half)
        elif e.text() == '8':
            self.model.setData(index, half + '8' + half)
        elif e.text() == '9':
            self.model.setData(index, half + '9' + half)
        elif e.text() == 'h':
            s = self.model.data(index)
            # if s != DEFAULT_NOTE:
                # if re.match('.+(\d+).+', string)

        super().keyPressEvent(e)

    def addCol(self, notes=[DEFAULT_NOTE] * 6, amt=1):
        for _ in range(amt):
            self.model.appendColumn([QStandardItem(i) for i in notes])

    def getFile(self, save=True):
        # Promts the user for a filepath
        if save:
            file = QFileDialog.getSaveFileName(self,
                    caption='Save Your Tab',
                    filter="*.txt",
                    initialFilter="*.txt"
                )[0]
        else:
            file = QFileDialog.getOpenFileName(self,
                caption='Load a Tab',
                filter="*.txt",
                initialFilter="*.txt"
            )[0]

        if file != '' and file is not None:
            if not file.endswith(('.txt',)):
                file = file + '.txt'

        return file

    def getRow(self, index):
        rtn = []
        for i in range(self.model.columnCount()):
            if (item := self.model.item(index, i)) is not None:
                rtn.append(item.text())
        return rtn

    def load(self):
        # Try to save, and even if you don't want to or can't load anyway
        # self.save(False)
        file = self.getFile(save=False)
        if file != '':
            with open(file, 'r') as f:
                self.deserialize(f.read())
                # j = json.load(f)
            # toast(f'Loaded {self.name.text()}', self)

    def save(self, assureSave=True) -> bool:
        file = self.getFile(save=True)
        if file is not None and file != '':
            with open(file, 'w') as f:
                f.write(self.serialize())
                print(f'{file} saved!')
            return True

    def serialize(self):
        rtn = ''
        for i in range(6):
            rtn += ''.join(self.getRow(i)) + '\n'
        return rtn

    def deserialize(self, s):
        pass

if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
