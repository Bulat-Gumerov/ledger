import logging
from datetime import datetime

from PySide2.QtCore import Qt, Signal, Property, Slot, QEvent
from PySide2.QtSql import QSqlRelationalDelegate
from PySide2.QtWidgets import QDialog, QMessageBox, QStyledItemDelegate, QTreeView

from jal.ui.ui_reference_data_dlg import Ui_ReferenceDataDialog
import widgets.reference_selector as ui     # Full import due to "cyclic" reference
from widgets.helpers import g_tr


# --------------------------------------------------------------------------------------------------------------
# Class to display and edit table with reference data (accounts, categories, tags...)
# --------------------------------------------------------------------------------------------------------------
class ReferenceDataDialog(QDialog, Ui_ReferenceDataDialog):
    # tree_view - table will be displayed as hierarchical tree with help of 2 columns: 'id', 'pid' in sql table
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

        self.model = None
        self.selected_id = 0
        self.p_selected_name = ''
        self._filter_text = ''
        self.selection_enabled = False
        self.group_id = None
        self.group_key_field = None
        self.group_key_index = None
        self.group_fkey_field = None
        self.toggle_state = False
        self.toggle_field = None
        self.search_field = None
        self.search_text = ""
        self.tree_view = False

        self.AddChildBtn.setVisible(False)
        self.GroupLbl.setVisible(False)
        self.GroupCombo.setVisible(False)
        self.SearchFrame.setVisible(False)

        self.AddBtn.setFixedWidth(self.AddBtn.fontMetrics().width("XXX"))
        self.AddChildBtn.setFixedWidth(self.AddChildBtn.fontMetrics().width("XXX"))
        self.RemoveBtn.setFixedWidth(self.RemoveBtn.fontMetrics().width("XXX"))
        self.CommitBtn.setFixedWidth(self.CommitBtn.fontMetrics().width("XXX"))
        self.RevertBtn.setFixedWidth(self.RevertBtn.fontMetrics().width("XXX"))

        self.SearchString.textChanged.connect(self.OnSearchChange)
        self.GroupCombo.currentIndexChanged.connect(self.OnGroupChange)
        self.Toggle.stateChanged.connect(self.OnToggleChange)
        self.AddBtn.clicked.connect(self.OnAdd)
        self.AddChildBtn.clicked.connect(self.OnChildAdd)
        self.RemoveBtn.clicked.connect(self.OnRemove)
        self.CommitBtn.clicked.connect(self.OnCommit)
        self.RevertBtn.clicked.connect(self.OnRevert)
        self.DataView.doubleClicked.connect(self.OnDoubleClicked)
        self.TreeView.doubleClicked.connect(self.OnDoubleClicked)

    def _init_completed(self):
        self.DataView.setVisible(not self.tree_view)
        self.TreeView.setVisible(self.tree_view)
        if self.tree_view:
            self.TreeView.selectionModel().selectionChanged.connect(self.OnRowSelected)
        else:
            self.DataView.selectionModel().selectionChanged.connect(self.OnRowSelected)
        self.model.dataChanged.connect(self.OnDataChanged)
        self.setFilter()

    @Slot()
    def closeEvent(self, event):
        if self.CommitBtn.isEnabled():    # There are uncommitted changed in a table
            if QMessageBox().warning(None, g_tr('ReferenceDataDialog', "Confirmation"),
                                     g_tr('ReferenceDataDialog', "You have uncommited changes. Do you want to close?"),
                                     QMessageBox.Yes, QMessageBox.No) == QMessageBox.No:
                event.ignore()
                return
            else:
                self.model.revertAll()
        event.accept()

    # Overload ancestor method to activate/deactivate filters for table view
    def exec_(self, enable_selection=False, selected=0):
        self.selection_enabled = enable_selection
        self.setFilter()
        if enable_selection:
            self.locateItem(selected)
        res = super().exec_()
        self.resetFilter()
        return res

    def getSelectedName(self):
        if self.selected_id == 0:
            return g_tr('ReferenceDataDialog', "ANY")
        else:
            return self.p_selected_name

    def setSelectedName(self, selected_id):
        pass

    @Signal
    def selected_name_changed(self):
        pass

    SelectedName = Property(str, getSelectedName, setSelectedName, notify=selected_name_changed)

    @Slot()
    def OnDataChanged(self):
        self.CommitBtn.setEnabled(True)
        self.RevertBtn.setEnabled(True)

    @Slot()
    def OnAdd(self):
        if self.tree_view:
            idx = self.TreeView.selectionModel().selection().indexes()
        else:
            idx = self.DataView.selectionModel().selection().indexes()
        current_index = idx[0] if idx else self.model.index(0, 0)
        self.model.addElement(current_index)
        self.CommitBtn.setEnabled(True)
        self.RevertBtn.setEnabled(True)

    @Slot()
    def OnChildAdd(self):
        if self.tree_view:
            idx = self.TreeView.selectionModel().selection().indexes()
            current_index = idx[0] if idx else self.model.index(0, 0)
            self.model.addChildElement(current_index)
            self.CommitBtn.setEnabled(True)
            self.RevertBtn.setEnabled(True)

    @Slot()
    def OnRemove(self):
        if self.tree_view:
            idx = self.TreeView.selectionModel().selection().indexes()
        else:
            idx = self.DataView.selectionModel().selection().indexes()
        current_index = idx[0] if idx else self.model.index(0, 0)
        self.model.removeElement(current_index)
        self.CommitBtn.setEnabled(True)
        self.RevertBtn.setEnabled(True)

    @Slot()
    def OnCommit(self):
        if self.group_key_index is not None:
            record = self.model.record(0)
            group_field = record.value(self.model.fieldIndex(self.group_key_field))
            if not group_field:
                self.model.setData(self.model.index(0, self.group_key_index), self.group_id)
        if not self.model.submitAll():
            logging.fatal(g_tr('ReferenceDataDialog', "Submit failed: ") + self.model.lastError().text())
            return
        self.CommitBtn.setEnabled(False)
        self.RevertBtn.setEnabled(False)

    @Slot()
    def OnRevert(self):
        self.model.revertAll()
        self.CommitBtn.setEnabled(False)
        self.RevertBtn.setEnabled(False)

    def resetFilter(self):
        self.model.setFilter("")

    def setFilter(self):
        conditions = []
        if self.search_text:
            conditions.append(f"{self.search_field} LIKE '%{self.search_text}%'")

        if self.group_id:
            conditions.append(f"{self.table}.{self.group_key_field}={self.group_id}")

        if self.toggle_field:
            if not self.toggle_state:
                conditions.append(f"{self.table}.{self.toggle_field}=1")

        self._filter_text = ""
        for line in conditions:
            self._filter_text += line + " AND "
        self._filter_text = self._filter_text[:-len(" AND ")]

        self.model.setFilter(self._filter_text)

    @Slot()
    def OnSearchChange(self):
        self.search_text = self.SearchString.text()
        self.setFilter()

    @Slot()
    def OnRowSelected(self, selected, _deselected):
        idx = selected.indexes()
        if idx:
            self.selected_id = self.model.getId(idx[0])
            self.p_selected_name = self.model.getName(idx[0])

    @Slot()
    def OnDoubleClicked(self, index):
        self.selected_id = self.model.getId(index)
        self.p_selected_name = self.model.getName(index)
        if self.selection_enabled:
            self.setResult(QDialog.Accepted)
            self.close()

    @Slot()
    def OnGroupChange(self, list_id):
        model = self.GroupCombo.model()
        self.group_id = model.data(model.index(list_id, model.fieldIndex(self.group_fkey_field)))
        self.setFilter()

    @Slot()
    def OnToggleChange(self, state):
        if state == 0:
            self.toggle_state = False
        else:
            self.toggle_state = True
        self.setFilter()

    def locateItem(self, item_id):
        raise NotImplementedError("locateItem() method is not defined in subclass ReferenceDataDialog")

# ===================================================================================================================
# Delegates to customize view of columns
# ===================================================================================================================
# Display '*' if true and empty cell if false
# Toggle True/False by mouse click
class ReferenceBoolDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        self._parent = parent
        QStyledItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):
        painter.save()
        model = index.model()
        status = model.data(index, Qt.DisplayRole)
        if status:
            text = ' * '
        else:
            text = ''
        painter.drawText(option.rect, Qt.AlignHCenter, text)
        # Extra code for tree views - to draw grid lines
        if type(self._parent) == QTreeView:
            pen = painter.pen()
            pen.setWidth(1)
            pen.setStyle(Qt.DotLine)
            pen.setColor(Qt.GlobalColor.lightGray)
            painter.setPen(pen)
            painter.drawRect(option.rect)
        painter.restore()

    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.MouseButtonPress:
            if model.data(index, Qt.DisplayRole):  # Toggle value - from 1 to 0 and from 0 to 1
                model.setData(index, 0)
            else:
                model.setData(index, 1)
        return True

# -------------------------------------------------------------------------------------------------------------------
# Make integer alignment to the right
class ReferenceIntDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        self._parent = parent
        QStyledItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):
        painter.save()
        model = index.model()
        value = model.data(index, Qt.DisplayRole)
        painter.drawText(option.rect, Qt.AlignRight, f"{value} ")
        # Extra code for tree views - to draw grid lines
        if type(self._parent) == QTreeView:
            pen = painter.pen()
            pen.setWidth(1)
            pen.setStyle(Qt.DotLine)
            pen.setColor(Qt.GlobalColor.lightGray)
            painter.setPen(pen)
            painter.drawRect(option.rect)
        painter.restore()

# -------------------------------------------------------------------------------------------------------------------
# Format unix timestamp into readable form '%d/%m/%Y %H:%M:%S'
class ReferenceTimestampDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        QStyledItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):
        painter.save()
        model = index.model()
        timestamp = model.data(index, Qt.DisplayRole)
        if timestamp:
            text = datetime.utcfromtimestamp(timestamp).strftime('%d/%m/%Y %H:%M:%S')
        else:
            text = ""
        painter.drawText(option.rect, Qt.AlignLeft, text)
        painter.restore()

# -------------------------------------------------------------------------------------------------------------------
# The class itself is empty but it activates built-in editors for lookup tables
class ReferenceLookupDelegate(QSqlRelationalDelegate):
    def __init__(self, parent=None):
        QSqlRelationalDelegate.__init__(self, parent)

# -----------------------------------------------------------------------------------------------------------------------
# Delegate to display tag editor
class ReferencePeerDelegate(QSqlRelationalDelegate):
    def __init__(self, parent=None):
        QSqlRelationalDelegate.__init__(self, parent)

    def createEditor(self, aParent, option, index):
        peer_selector = ui.PeerSelector(aParent)
        return peer_selector

    def setModelData(self, editor, model, index):
        model.setData(index, editor.selected_id)