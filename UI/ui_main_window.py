# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

from CustomUI.reference_selector import AccountSelector
from CustomUI.reference_selector import AssetSelector
from CustomUI.account_select import AccountButton
from CustomUI.reference_selector import PeerSelector
from CustomUI.trade_action import TradeAction
from CustomUI.log_viewer import LogViewer
from CustomUI.account_select import CurrencyCombo
from CustomUI.amount_editor import AmountEdit


class Ui_LedgerMainWindow(object):
    def setupUi(self, LedgerMainWindow):
        if not LedgerMainWindow.objectName():
            LedgerMainWindow.setObjectName(u"LedgerMainWindow")
        LedgerMainWindow.resize(1700, 900)
        LedgerMainWindow.setMinimumSize(QSize(0, 0))
        self.actionExit = QAction(LedgerMainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionExit.setMenuRole(QAction.QuitRole)
        self.action_Re_build_Ledger = QAction(LedgerMainWindow)
        self.action_Re_build_Ledger.setObjectName(u"action_Re_build_Ledger")
        self.action_Load_quotes = QAction(LedgerMainWindow)
        self.action_Load_quotes.setObjectName(u"action_Load_quotes")
        self.actionLoad_Statement = QAction(LedgerMainWindow)
        self.actionLoad_Statement.setObjectName(u"actionLoad_Statement")
        self.actionAccountTypes = QAction(LedgerMainWindow)
        self.actionAccountTypes.setObjectName(u"actionAccountTypes")
        self.actionAccounts = QAction(LedgerMainWindow)
        self.actionAccounts.setObjectName(u"actionAccounts")
        self.actionAssets = QAction(LedgerMainWindow)
        self.actionAssets.setObjectName(u"actionAssets")
        self.actionPeers = QAction(LedgerMainWindow)
        self.actionPeers.setObjectName(u"actionPeers")
        self.actionCategories = QAction(LedgerMainWindow)
        self.actionCategories.setObjectName(u"actionCategories")
        self.actionBackup = QAction(LedgerMainWindow)
        self.actionBackup.setObjectName(u"actionBackup")
        self.actionRestore = QAction(LedgerMainWindow)
        self.actionRestore.setObjectName(u"actionRestore")
        self.PrepareTaxForms = QAction(LedgerMainWindow)
        self.PrepareTaxForms.setObjectName(u"PrepareTaxForms")
        self.MakeDealsReport = QAction(LedgerMainWindow)
        self.MakeDealsReport.setObjectName(u"MakeDealsReport")
        self.actionTags = QAction(LedgerMainWindow)
        self.actionTags.setObjectName(u"actionTags")
        self.MakePLReport = QAction(LedgerMainWindow)
        self.MakePLReport.setObjectName(u"MakePLReport")
        self.MakeCategoriesReport = QAction(LedgerMainWindow)
        self.MakeCategoriesReport.setObjectName(u"MakeCategoriesReport")
        self.centralwidget = QWidget(LedgerMainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.MainTabs = QTabWidget(self.centralwidget)
        self.MainTabs.setObjectName(u"MainTabs")
        self.MainTabs.setTabPosition(QTabWidget.West)
        self.MainTabs.setTabShape(QTabWidget.Triangular)
        self.BalanceTransactionTab = QWidget()
        self.BalanceTransactionTab.setObjectName(u"BalanceTransactionTab")
        self.horizontalLayout = QHBoxLayout(self.BalanceTransactionTab)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.BalanceOperationsSplitter = QSplitter(self.BalanceTransactionTab)
        self.BalanceOperationsSplitter.setObjectName(u"BalanceOperationsSplitter")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BalanceOperationsSplitter.sizePolicy().hasHeightForWidth())
        self.BalanceOperationsSplitter.setSizePolicy(sizePolicy)
        self.BalanceOperationsSplitter.setOrientation(Qt.Horizontal)
        self.BalanceBox = QGroupBox(self.BalanceOperationsSplitter)
        self.BalanceBox.setObjectName(u"BalanceBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.BalanceBox.sizePolicy().hasHeightForWidth())
        self.BalanceBox.setSizePolicy(sizePolicy1)
        self.BalanceBox.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(self.BalanceBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.BalanceConfigFrame = QFrame(self.BalanceBox)
        self.BalanceConfigFrame.setObjectName(u"BalanceConfigFrame")
        self.BalanceConfigFrame.setMinimumSize(QSize(408, 0))
        self.BalanceConfigFrame.setMaximumSize(QSize(16777215, 44))
        self.BalanceConfigFrame.setFrameShape(QFrame.Panel)
        self.BalanceConfigFrame.setFrameShadow(QFrame.Plain)
        self.BalanceConfigFrame.setLineWidth(0)
        self.horizontalLayout_2 = QHBoxLayout(self.BalanceConfigFrame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.BalanceDate = QDateEdit(self.BalanceConfigFrame)
        self.BalanceDate.setObjectName(u"BalanceDate")
        self.BalanceDate.setCalendarPopup(True)

        self.horizontalLayout_2.addWidget(self.BalanceDate)

        self.CurrencyLbl = QLabel(self.BalanceConfigFrame)
        self.CurrencyLbl.setObjectName(u"CurrencyLbl")
        self.CurrencyLbl.setLayoutDirection(Qt.LeftToRight)
        self.CurrencyLbl.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.CurrencyLbl)

        self.BalancesCurrencyCombo = CurrencyCombo(self.BalanceConfigFrame)
        self.BalancesCurrencyCombo.setObjectName(u"BalancesCurrencyCombo")

        self.horizontalLayout_2.addWidget(self.BalancesCurrencyCombo)

        self.ShowInactiveCheckBox = QCheckBox(self.BalanceConfigFrame)
        self.ShowInactiveCheckBox.setObjectName(u"ShowInactiveCheckBox")

        self.horizontalLayout_2.addWidget(self.ShowInactiveCheckBox)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addWidget(self.BalanceConfigFrame)

        self.BalancesTableView = QTableView(self.BalanceBox)
        self.BalancesTableView.setObjectName(u"BalancesTableView")
        self.BalancesTableView.setFrameShape(QFrame.Panel)
        self.BalancesTableView.setAlternatingRowColors(True)
        self.BalancesTableView.setGridStyle(Qt.DotLine)
        self.BalancesTableView.setWordWrap(False)
        self.BalancesTableView.verticalHeader().setVisible(False)
        self.BalancesTableView.verticalHeader().setMinimumSectionSize(20)
        self.BalancesTableView.verticalHeader().setDefaultSectionSize(20)

        self.verticalLayout.addWidget(self.BalancesTableView)

        self.BalanceOperationsSplitter.addWidget(self.BalanceBox)
        self.OperationsBox = QGroupBox(self.BalanceOperationsSplitter)
        self.OperationsBox.setObjectName(u"OperationsBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(4)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.OperationsBox.sizePolicy().hasHeightForWidth())
        self.OperationsBox.setSizePolicy(sizePolicy2)
        self.OperationsBox.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.verticalLayout_2 = QVBoxLayout(self.OperationsBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.OperationConfigFrame = QFrame(self.OperationsBox)
        self.OperationConfigFrame.setObjectName(u"OperationConfigFrame")
        self.OperationConfigFrame.setEnabled(True)
        self.OperationConfigFrame.setMinimumSize(QSize(0, 0))
        self.OperationConfigFrame.setFrameShape(QFrame.Panel)
        self.OperationConfigFrame.setFrameShadow(QFrame.Plain)
        self.OperationConfigFrame.setLineWidth(0)
        self.horizontalLayout_3 = QHBoxLayout(self.OperationConfigFrame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.DateRangeLbl = QLabel(self.OperationConfigFrame)
        self.DateRangeLbl.setObjectName(u"DateRangeLbl")

        self.horizontalLayout_3.addWidget(self.DateRangeLbl)

        self.DateRangeCombo = QComboBox(self.OperationConfigFrame)
        self.DateRangeCombo.addItem("")
        self.DateRangeCombo.addItem("")
        self.DateRangeCombo.addItem("")
        self.DateRangeCombo.addItem("")
        self.DateRangeCombo.addItem("")
        self.DateRangeCombo.setObjectName(u"DateRangeCombo")

        self.horizontalLayout_3.addWidget(self.DateRangeCombo)

        self.AccountLbl = QLabel(self.OperationConfigFrame)
        self.AccountLbl.setObjectName(u"AccountLbl")

        self.horizontalLayout_3.addWidget(self.AccountLbl)

        self.ChooseAccountBtn = AccountButton(self.OperationConfigFrame)
        self.ChooseAccountBtn.setObjectName(u"ChooseAccountBtn")

        self.horizontalLayout_3.addWidget(self.ChooseAccountBtn)

        self.SearchLbl = QLabel(self.OperationConfigFrame)
        self.SearchLbl.setObjectName(u"SearchLbl")

        self.horizontalLayout_3.addWidget(self.SearchLbl)

        self.SearchString = QLineEdit(self.OperationConfigFrame)
        self.SearchString.setObjectName(u"SearchString")

        self.horizontalLayout_3.addWidget(self.SearchString)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addWidget(self.OperationConfigFrame)

        self.OperationsDetailsSplitter = QSplitter(self.OperationsBox)
        self.OperationsDetailsSplitter.setObjectName(u"OperationsDetailsSplitter")
        self.OperationsDetailsSplitter.setOrientation(Qt.Vertical)
        self.OperationsTableView = QTableView(self.OperationsDetailsSplitter)
        self.OperationsTableView.setObjectName(u"OperationsTableView")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(4)
        sizePolicy3.setHeightForWidth(self.OperationsTableView.sizePolicy().hasHeightForWidth())
        self.OperationsTableView.setSizePolicy(sizePolicy3)
        self.OperationsTableView.setAlternatingRowColors(True)
        self.OperationsTableView.setWordWrap(False)
        self.OperationsDetailsSplitter.addWidget(self.OperationsTableView)
        self.OperationsTableView.verticalHeader().setVisible(False)
        self.OperationsTableView.verticalHeader().setMinimumSectionSize(1)
        self.OperationsTableView.verticalHeader().setDefaultSectionSize(1)
        self.OperationDetails = QFrame(self.OperationsDetailsSplitter)
        self.OperationDetails.setObjectName(u"OperationDetails")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(1)
        sizePolicy4.setHeightForWidth(self.OperationDetails.sizePolicy().hasHeightForWidth())
        self.OperationDetails.setSizePolicy(sizePolicy4)
        self.OperationDetails.setMinimumSize(QSize(0, 100))
        self.OperationDetails.setMaximumSize(QSize(16777215, 300))
        self.OperationDetails.setFrameShape(QFrame.Panel)
        self.OperationDetails.setFrameShadow(QFrame.Plain)
        self.OperationDetails.setLineWidth(0)
        self.horizontalLayout_4 = QHBoxLayout(self.OperationDetails)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.OperationsTabs = QStackedWidget(self.OperationDetails)
        self.OperationsTabs.setObjectName(u"OperationsTabs")
        self.ActionDetailsTab = QWidget()
        self.ActionDetailsTab.setObjectName(u"ActionDetailsTab")
        self.gridLayout_4 = QGridLayout(self.ActionDetailsTab)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(2, 2, 2, 2)
        self.ActionAccountWidget = AccountSelector(self.ActionDetailsTab)
        self.ActionAccountWidget.setObjectName(u"ActionAccountWidget")

        self.gridLayout_4.addWidget(self.ActionAccountWidget, 1, 2, 1, 1)

        self.ActionDetailsTableView = QTableView(self.ActionDetailsTab)
        self.ActionDetailsTableView.setObjectName(u"ActionDetailsTableView")
        self.ActionDetailsTableView.setAlternatingRowColors(True)
        self.ActionDetailsTableView.verticalHeader().setVisible(False)
        self.ActionDetailsTableView.verticalHeader().setMinimumSectionSize(20)
        self.ActionDetailsTableView.verticalHeader().setDefaultSectionSize(20)

        self.gridLayout_4.addWidget(self.ActionDetailsTableView, 3, 0, 1, 6)

        self.PeerLbl = QLabel(self.ActionDetailsTab)
        self.PeerLbl.setObjectName(u"PeerLbl")

        self.gridLayout_4.addWidget(self.PeerLbl, 2, 1, 1, 1)

        self.ActionDetailBtnFrame = QFrame(self.ActionDetailsTab)
        self.ActionDetailBtnFrame.setObjectName(u"ActionDetailBtnFrame")
        self.ActionDetailBtnFrame.setFrameShape(QFrame.NoFrame)
        self.ActionDetailBtnFrame.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_6 = QHBoxLayout(self.ActionDetailBtnFrame)
        self.horizontalLayout_6.setSpacing(8)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.AddActionDetail = QPushButton(self.ActionDetailBtnFrame)
        self.AddActionDetail.setObjectName(u"AddActionDetail")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.AddActionDetail.sizePolicy().hasHeightForWidth())
        self.AddActionDetail.setSizePolicy(sizePolicy5)
        self.AddActionDetail.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_6.addWidget(self.AddActionDetail)

        self.CopyActionDetail = QPushButton(self.ActionDetailBtnFrame)
        self.CopyActionDetail.setObjectName(u"CopyActionDetail")
        sizePolicy5.setHeightForWidth(self.CopyActionDetail.sizePolicy().hasHeightForWidth())
        self.CopyActionDetail.setSizePolicy(sizePolicy5)
        self.CopyActionDetail.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_6.addWidget(self.CopyActionDetail)

        self.RemoveActionDetail = QPushButton(self.ActionDetailBtnFrame)
        self.RemoveActionDetail.setObjectName(u"RemoveActionDetail")
        sizePolicy5.setHeightForWidth(self.RemoveActionDetail.sizePolicy().hasHeightForWidth())
        self.RemoveActionDetail.setSizePolicy(sizePolicy5)
        self.RemoveActionDetail.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_6.addWidget(self.RemoveActionDetail)


        self.gridLayout_4.addWidget(self.ActionDetailBtnFrame, 2, 0, 1, 1)

        self.ActionPeerWidget = PeerSelector(self.ActionDetailsTab)
        self.ActionPeerWidget.setObjectName(u"ActionPeerWidget")

        self.gridLayout_4.addWidget(self.ActionPeerWidget, 2, 2, 1, 1)

        self.ActionDetailsSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_4.addItem(self.ActionDetailsSpacer, 1, 3, 1, 1)

        self.ActionAccountLabel = QLabel(self.ActionDetailsTab)
        self.ActionAccountLabel.setObjectName(u"ActionAccountLabel")

        self.gridLayout_4.addWidget(self.ActionAccountLabel, 1, 1, 1, 1)

        self.ActionTimestampEdit = QDateTimeEdit(self.ActionDetailsTab)
        self.ActionTimestampEdit.setObjectName(u"ActionTimestampEdit")
        self.ActionTimestampEdit.setCalendarPopup(True)

        self.gridLayout_4.addWidget(self.ActionTimestampEdit, 1, 0, 1, 1)

        self.ActionTabLbl = QLabel(self.ActionDetailsTab)
        self.ActionTabLbl.setObjectName(u"ActionTabLbl")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.ActionTabLbl.setFont(font)

        self.gridLayout_4.addWidget(self.ActionTabLbl, 0, 0, 1, 1)

        self.OperationsTabs.addWidget(self.ActionDetailsTab)
        self.TradeDetailsTab = QWidget()
        self.TradeDetailsTab.setObjectName(u"TradeDetailsTab")
        self.TradeDetailsTab.setEnabled(True)
        self.gridLayout_3 = QGridLayout(self.TradeDetailsTab)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(2, 2, 2, 2)
        self.TradePriceEdit = AmountEdit(self.TradeDetailsTab)
        self.TradePriceEdit.setObjectName(u"TradePriceEdit")
        self.TradePriceEdit.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.TradePriceEdit, 4, 2, 1, 1)

        self.TradeFeeLbl = QLabel(self.TradeDetailsTab)
        self.TradeFeeLbl.setObjectName(u"TradeFeeLbl")

        self.gridLayout_3.addWidget(self.TradeFeeLbl, 5, 3, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_2, 7, 0, 1, 1)

        self.TradeSettlementEdit = QDateEdit(self.TradeDetailsTab)
        self.TradeSettlementEdit.setObjectName(u"TradeSettlementEdit")
        self.TradeSettlementEdit.setMinimumDate(QDate(2000, 1, 1))
        self.TradeSettlementEdit.setCalendarPopup(True)

        self.gridLayout_3.addWidget(self.TradeSettlementEdit, 5, 0, 1, 1)

        self.label = QLabel(self.TradeDetailsTab)
        self.label.setObjectName(u"label")

        self.gridLayout_3.addWidget(self.label, 4, 3, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_5, 2, 5, 1, 1)

        self.TradeNumberEdit = QLineEdit(self.TradeDetailsTab)
        self.TradeNumberEdit.setObjectName(u"TradeNumberEdit")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.TradeNumberEdit.sizePolicy().hasHeightForWidth())
        self.TradeNumberEdit.setSizePolicy(sizePolicy6)

        self.gridLayout_3.addWidget(self.TradeNumberEdit, 2, 0, 1, 1)

        self.TradeTabLbl = QLabel(self.TradeDetailsTab)
        self.TradeTabLbl.setObjectName(u"TradeTabLbl")
        self.TradeTabLbl.setFont(font)

        self.gridLayout_3.addWidget(self.TradeTabLbl, 0, 0, 1, 1)

        self.TradeFeeEdit = AmountEdit(self.TradeDetailsTab)
        self.TradeFeeEdit.setObjectName(u"TradeFeeEdit")
        self.TradeFeeEdit.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.TradeFeeEdit, 5, 4, 1, 1)

        self.TradeTimestampEdit = QDateTimeEdit(self.TradeDetailsTab)
        self.TradeTimestampEdit.setObjectName(u"TradeTimestampEdit")
        self.TradeTimestampEdit.setCalendarPopup(True)

        self.gridLayout_3.addWidget(self.TradeTimestampEdit, 1, 0, 1, 1)

        self.TradePriceLbl = QLabel(self.TradeDetailsTab)
        self.TradePriceLbl.setObjectName(u"TradePriceLbl")

        self.gridLayout_3.addWidget(self.TradePriceLbl, 4, 1, 1, 1)

        self.TradeQtyEdit = AmountEdit(self.TradeDetailsTab)
        self.TradeQtyEdit.setObjectName(u"TradeQtyEdit")
        self.TradeQtyEdit.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.TradeQtyEdit, 4, 4, 1, 1)

        self.TradeAccountWidget = AccountSelector(self.TradeDetailsTab)
        self.TradeAccountWidget.setObjectName(u"TradeAccountWidget")

        self.gridLayout_3.addWidget(self.TradeAccountWidget, 1, 2, 1, 3)

        self.TradeAssetWidget = AssetSelector(self.TradeDetailsTab)
        self.TradeAssetWidget.setObjectName(u"TradeAssetWidget")

        self.gridLayout_3.addWidget(self.TradeAssetWidget, 2, 2, 1, 3)

        self.TradeAccountLbl = QLabel(self.TradeDetailsTab)
        self.TradeAccountLbl.setObjectName(u"TradeAccountLbl")

        self.gridLayout_3.addWidget(self.TradeAccountLbl, 1, 1, 1, 1)

        self.TradeSymbolLbl = QLabel(self.TradeDetailsTab)
        self.TradeSymbolLbl.setObjectName(u"TradeSymbolLbl")

        self.gridLayout_3.addWidget(self.TradeSymbolLbl, 2, 1, 1, 1)

        self.TradeActionWidget = TradeAction(self.TradeDetailsTab)
        self.TradeActionWidget.setObjectName(u"TradeActionWidget")

        self.gridLayout_3.addWidget(self.TradeActionWidget, 4, 0, 1, 1)

        self.TradeCouponLbl = QLabel(self.TradeDetailsTab)
        self.TradeCouponLbl.setObjectName(u"TradeCouponLbl")

        self.gridLayout_3.addWidget(self.TradeCouponLbl, 5, 1, 1, 1)

        self.TradeCouponEdit = AmountEdit(self.TradeDetailsTab)
        self.TradeCouponEdit.setObjectName(u"TradeCouponEdit")
        self.TradeCouponEdit.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.TradeCouponEdit, 5, 2, 1, 1)

        self.OperationsTabs.addWidget(self.TradeDetailsTab)
        self.DividendDetailsTab = QWidget()
        self.DividendDetailsTab.setObjectName(u"DividendDetailsTab")
        self.gridLayout_2 = QGridLayout(self.DividendDetailsTab)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(2, 2, 2, 2)
        self.DividendSymbolLbl = QLabel(self.DividendDetailsTab)
        self.DividendSymbolLbl.setObjectName(u"DividendSymbolLbl")
        self.DividendSymbolLbl.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.DividendSymbolLbl, 6, 2, 1, 1)

        self.DividendTaxEdit = AmountEdit(self.DividendDetailsTab)
        self.DividendTaxEdit.setObjectName(u"DividendTaxEdit")
        self.DividendTaxEdit.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.DividendTaxEdit, 8, 2, 1, 1)

        self.DividendAccountWidget = AccountSelector(self.DividendDetailsTab)
        self.DividendAccountWidget.setObjectName(u"DividendAccountWidget")
        self.DividendAccountWidget.setMinimumSize(QSize(32, 0))

        self.gridLayout_2.addWidget(self.DividendAccountWidget, 2, 3, 1, 1)

        self.DividendTimestampEdit = QDateTimeEdit(self.DividendDetailsTab)
        self.DividendTimestampEdit.setObjectName(u"DividendTimestampEdit")
        self.DividendTimestampEdit.setCalendarPopup(True)

        self.gridLayout_2.addWidget(self.DividendTimestampEdit, 2, 1, 1, 1)

        self.DividendTaxLbl = QLabel(self.DividendDetailsTab)
        self.DividendTaxLbl.setObjectName(u"DividendTaxLbl")
        self.DividendTaxLbl.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.DividendTaxLbl, 8, 1, 1, 1)

        self.DividendSumEdit = AmountEdit(self.DividendDetailsTab)
        self.DividendSumEdit.setObjectName(u"DividendSumEdit")
        self.DividendSumEdit.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.DividendSumEdit, 7, 2, 1, 1)

        self.DividendNumberEdit = QLineEdit(self.DividendDetailsTab)
        self.DividendNumberEdit.setObjectName(u"DividendNumberEdit")
        sizePolicy6.setHeightForWidth(self.DividendNumberEdit.sizePolicy().hasHeightForWidth())
        self.DividendNumberEdit.setSizePolicy(sizePolicy6)

        self.gridLayout_2.addWidget(self.DividendNumberEdit, 6, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 9, 1, 1, 1)

        self.DividendTabLbl = QLabel(self.DividendDetailsTab)
        self.DividendTabLbl.setObjectName(u"DividendTabLbl")
        self.DividendTabLbl.setFont(font)

        self.gridLayout_2.addWidget(self.DividendTabLbl, 0, 1, 1, 1)

        self.DividendAccountLbl = QLabel(self.DividendDetailsTab)
        self.DividendAccountLbl.setObjectName(u"DividendAccountLbl")
        self.DividendAccountLbl.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.DividendAccountLbl, 2, 2, 1, 1)

        self.DividendSumLbl = QLabel(self.DividendDetailsTab)
        self.DividendSumLbl.setObjectName(u"DividendSumLbl")
        self.DividendSumLbl.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.DividendSumLbl, 7, 1, 1, 1)

        self.DividendAssetWidget = AssetSelector(self.DividendDetailsTab)
        self.DividendAssetWidget.setObjectName(u"DividendAssetWidget")
        self.DividendAssetWidget.setMinimumSize(QSize(32, 0))

        self.gridLayout_2.addWidget(self.DividendAssetWidget, 6, 3, 1, 1)

        self.DividendSumDescription = QLineEdit(self.DividendDetailsTab)
        self.DividendSumDescription.setObjectName(u"DividendSumDescription")
        self.DividendSumDescription.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.DividendSumDescription, 7, 3, 1, 2)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_6, 2, 4, 1, 1)

        self.DividendTaxDescription = QLineEdit(self.DividendDetailsTab)
        self.DividendTaxDescription.setObjectName(u"DividendTaxDescription")

        self.gridLayout_2.addWidget(self.DividendTaxDescription, 8, 3, 1, 2)

        self.OperationsTabs.addWidget(self.DividendDetailsTab)
        self.TransferDetailsTab = QWidget()
        self.TransferDetailsTab.setObjectName(u"TransferDetailsTab")
        self.gridLayout_5 = QGridLayout(self.TransferDetailsTab)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(2, 2, 2, 2)
        self.TransferNote = QLineEdit(self.TransferDetailsTab)
        self.TransferNote.setObjectName(u"TransferNote")

        self.gridLayout_5.addWidget(self.TransferNote, 5, 1, 1, 4)

        self.TransferFromAmount = AmountEdit(self.TransferDetailsTab)
        self.TransferFromAmount.setObjectName(u"TransferFromAmount")
        self.TransferFromAmount.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.TransferFromAmount, 2, 3, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_4, 3, 4, 1, 1)

        self.TransferFeeAmount = AmountEdit(self.TransferDetailsTab)
        self.TransferFeeAmount.setObjectName(u"TransferFeeAmount")
        self.TransferFeeAmount.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.TransferFeeAmount, 4, 3, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_5.addItem(self.verticalSpacer_5, 6, 2, 1, 1)

        self.TransferTextLbl = QLabel(self.TransferDetailsTab)
        self.TransferTextLbl.setObjectName(u"TransferTextLbl")
        self.TransferTextLbl.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.TransferTextLbl, 5, 0, 1, 1)

        self.TransferFromAccountWidget = AccountSelector(self.TransferDetailsTab)
        self.TransferFromAccountWidget.setObjectName(u"TransferFromAccountWidget")

        self.gridLayout_5.addWidget(self.TransferFromAccountWidget, 2, 2, 1, 1)

        self.TransferFromTimestamp = QDateTimeEdit(self.TransferDetailsTab)
        self.TransferFromTimestamp.setObjectName(u"TransferFromTimestamp")
        self.TransferFromTimestamp.setCalendarPopup(True)

        self.gridLayout_5.addWidget(self.TransferFromTimestamp, 2, 0, 1, 1)

        self.TransferFeeAccountWidget = AccountSelector(self.TransferDetailsTab)
        self.TransferFeeAccountWidget.setObjectName(u"TransferFeeAccountWidget")

        self.gridLayout_5.addWidget(self.TransferFeeAccountWidget, 4, 2, 1, 1)

        self.TransferFromLbl = QLabel(self.TransferDetailsTab)
        self.TransferFromLbl.setObjectName(u"TransferFromLbl")

        self.gridLayout_5.addWidget(self.TransferFromLbl, 2, 1, 1, 1)

        self.TransferToAccountWidget = AccountSelector(self.TransferDetailsTab)
        self.TransferToAccountWidget.setObjectName(u"TransferToAccountWidget")

        self.gridLayout_5.addWidget(self.TransferToAccountWidget, 3, 2, 1, 1)

        self.TransferToAmount = AmountEdit(self.TransferDetailsTab)
        self.TransferToAmount.setObjectName(u"TransferToAmount")
        self.TransferToAmount.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.TransferToAmount, 3, 3, 1, 1)

        self.TransferTabLbl = QLabel(self.TransferDetailsTab)
        self.TransferTabLbl.setObjectName(u"TransferTabLbl")
        self.TransferTabLbl.setFont(font)

        self.gridLayout_5.addWidget(self.TransferTabLbl, 0, 0, 1, 1)

        self.TransferFeeLbl = QLabel(self.TransferDetailsTab)
        self.TransferFeeLbl.setObjectName(u"TransferFeeLbl")

        self.gridLayout_5.addWidget(self.TransferFeeLbl, 4, 1, 1, 1)

        self.TransferFeeTimestamp = QDateTimeEdit(self.TransferDetailsTab)
        self.TransferFeeTimestamp.setObjectName(u"TransferFeeTimestamp")
        self.TransferFeeTimestamp.setMinimumDate(QDate(2000, 1, 1))
        self.TransferFeeTimestamp.setCalendarPopup(True)

        self.gridLayout_5.addWidget(self.TransferFeeTimestamp, 4, 0, 1, 1)

        self.TransferToLbl = QLabel(self.TransferDetailsTab)
        self.TransferToLbl.setObjectName(u"TransferToLbl")

        self.gridLayout_5.addWidget(self.TransferToLbl, 3, 1, 1, 1)

        self.TransferToTimestamp = QDateTimeEdit(self.TransferDetailsTab)
        self.TransferToTimestamp.setObjectName(u"TransferToTimestamp")
        self.TransferToTimestamp.setCalendarPopup(True)

        self.gridLayout_5.addWidget(self.TransferToTimestamp, 3, 0, 1, 1)

        self.OperationsTabs.addWidget(self.TransferDetailsTab)

        self.horizontalLayout_4.addWidget(self.OperationsTabs)

        self.OperationsButtons = QFrame(self.OperationDetails)
        self.OperationsButtons.setObjectName(u"OperationsButtons")
        self.OperationsButtons.setMinimumSize(QSize(100, 0))
        self.OperationsButtons.setFrameShape(QFrame.Panel)
        self.OperationsButtons.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_3 = QVBoxLayout(self.OperationsButtons)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.NewOperationBtn = QPushButton(self.OperationsButtons)
        self.NewOperationBtn.setObjectName(u"NewOperationBtn")

        self.verticalLayout_3.addWidget(self.NewOperationBtn)

        self.CopyOperationBtn = QPushButton(self.OperationsButtons)
        self.CopyOperationBtn.setObjectName(u"CopyOperationBtn")

        self.verticalLayout_3.addWidget(self.CopyOperationBtn)

        self.DeleteOperationBtn = QPushButton(self.OperationsButtons)
        self.DeleteOperationBtn.setObjectName(u"DeleteOperationBtn")

        self.verticalLayout_3.addWidget(self.DeleteOperationBtn)

        self.line = QFrame(self.OperationsButtons)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.SaveOperationBtn = QPushButton(self.OperationsButtons)
        self.SaveOperationBtn.setObjectName(u"SaveOperationBtn")
        self.SaveOperationBtn.setEnabled(False)

        self.verticalLayout_3.addWidget(self.SaveOperationBtn)

        self.RevertOperationBtn = QPushButton(self.OperationsButtons)
        self.RevertOperationBtn.setObjectName(u"RevertOperationBtn")
        self.RevertOperationBtn.setEnabled(False)

        self.verticalLayout_3.addWidget(self.RevertOperationBtn)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_4)


        self.horizontalLayout_4.addWidget(self.OperationsButtons)

        self.OperationsDetailsSplitter.addWidget(self.OperationDetails)

        self.verticalLayout_2.addWidget(self.OperationsDetailsSplitter)

        self.BalanceOperationsSplitter.addWidget(self.OperationsBox)

        self.horizontalLayout.addWidget(self.BalanceOperationsSplitter)

        self.MainTabs.addTab(self.BalanceTransactionTab, "")
        self.HoldingsTab = QWidget()
        self.HoldingsTab.setObjectName(u"HoldingsTab")
        self.verticalLayout_4 = QVBoxLayout(self.HoldingsTab)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.HoldingsTab)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_7 = QHBoxLayout(self.frame)
        self.horizontalLayout_7.setSpacing(6)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(2, 2, 2, 2)
        self.HoldingsDate = QDateEdit(self.frame)
        self.HoldingsDate.setObjectName(u"HoldingsDate")
        self.HoldingsDate.setCalendarPopup(True)

        self.horizontalLayout_7.addWidget(self.HoldingsDate)

        self.HoldingsCurrencyLbl = QLabel(self.frame)
        self.HoldingsCurrencyLbl.setObjectName(u"HoldingsCurrencyLbl")

        self.horizontalLayout_7.addWidget(self.HoldingsCurrencyLbl)

        self.HoldingsCurrencyCombo = CurrencyCombo(self.frame)
        self.HoldingsCurrencyCombo.setObjectName(u"HoldingsCurrencyCombo")

        self.horizontalLayout_7.addWidget(self.HoldingsCurrencyCombo)

        self.horizontalSpacer_3 = QSpacerItem(1411, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_3)


        self.verticalLayout_4.addWidget(self.frame)

        self.HoldingsTableView = QTableView(self.HoldingsTab)
        self.HoldingsTableView.setObjectName(u"HoldingsTableView")
        self.HoldingsTableView.setAlternatingRowColors(True)
        self.HoldingsTableView.verticalHeader().setVisible(False)
        self.HoldingsTableView.verticalHeader().setMinimumSectionSize(20)
        self.HoldingsTableView.verticalHeader().setDefaultSectionSize(20)

        self.verticalLayout_4.addWidget(self.HoldingsTableView)

        self.MainTabs.addTab(self.HoldingsTab, "")
        self.LoggingTab = QWidget()
        self.LoggingTab.setObjectName(u"LoggingTab")
        self.verticalLayout_5 = QVBoxLayout(self.LoggingTab)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.Logs = LogViewer(self.LoggingTab)
        self.Logs.setObjectName(u"Logs")

        self.verticalLayout_5.addWidget(self.Logs)

        self.MainTabs.addTab(self.LoggingTab, "")

        self.gridLayout.addWidget(self.MainTabs, 0, 0, 1, 1)

        LedgerMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(LedgerMainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1700, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menu_DAta = QMenu(self.menubar)
        self.menu_DAta.setObjectName(u"menu_DAta")
        self.menuPredefined_data = QMenu(self.menu_DAta)
        self.menuPredefined_data.setObjectName(u"menuPredefined_data")
        self.menuLoad = QMenu(self.menubar)
        self.menuLoad.setObjectName(u"menuLoad")
        self.menu_Reports = QMenu(self.menubar)
        self.menu_Reports.setObjectName(u"menu_Reports")
        LedgerMainWindow.setMenuBar(self.menubar)
        self.StatusBar = QStatusBar(LedgerMainWindow)
        self.StatusBar.setObjectName(u"StatusBar")
        LedgerMainWindow.setStatusBar(self.StatusBar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu_DAta.menuAction())
        self.menubar.addAction(self.menuLoad.menuAction())
        self.menubar.addAction(self.menu_Reports.menuAction())
        self.menuFile.addAction(self.actionExit)
        self.menu_DAta.addSeparator()
        self.menu_DAta.addAction(self.actionAccounts)
        self.menu_DAta.addAction(self.actionAssets)
        self.menu_DAta.addAction(self.actionPeers)
        self.menu_DAta.addAction(self.actionCategories)
        self.menu_DAta.addAction(self.actionTags)
        self.menu_DAta.addAction(self.menuPredefined_data.menuAction())
        self.menu_DAta.addSeparator()
        self.menu_DAta.addAction(self.actionBackup)
        self.menu_DAta.addAction(self.actionRestore)
        self.menu_DAta.addAction(self.action_Re_build_Ledger)
        self.menuPredefined_data.addAction(self.actionAccountTypes)
        self.menuLoad.addAction(self.action_Load_quotes)
        self.menuLoad.addAction(self.actionLoad_Statement)
        self.menu_Reports.addAction(self.MakeCategoriesReport)
        self.menu_Reports.addAction(self.MakeDealsReport)
        self.menu_Reports.addAction(self.MakePLReport)
        self.menu_Reports.addAction(self.PrepareTaxForms)

        self.retranslateUi(LedgerMainWindow)

        self.MainTabs.setCurrentIndex(0)
        self.OperationsTabs.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(LedgerMainWindow)
    # setupUi

    def retranslateUi(self, LedgerMainWindow):
        LedgerMainWindow.setWindowTitle(QCoreApplication.translate("LedgerMainWindow", u"Ledger", None))
        self.actionExit.setText(QCoreApplication.translate("LedgerMainWindow", u"&Exit", None))
        self.action_Re_build_Ledger.setText(QCoreApplication.translate("LedgerMainWindow", u"Re-build &Ledger...", None))
        self.action_Load_quotes.setText(QCoreApplication.translate("LedgerMainWindow", u"Load &Quotes...", None))
        self.actionLoad_Statement.setText(QCoreApplication.translate("LedgerMainWindow", u"Load &Statement...", None))
        self.actionAccountTypes.setText(QCoreApplication.translate("LedgerMainWindow", u"Account &Types", None))
        self.actionAccounts.setText(QCoreApplication.translate("LedgerMainWindow", u"&Accounts", None))
        self.actionAssets.setText(QCoreApplication.translate("LedgerMainWindow", u"A&ssets", None))
        self.actionPeers.setText(QCoreApplication.translate("LedgerMainWindow", u"&Peers", None))
        self.actionCategories.setText(QCoreApplication.translate("LedgerMainWindow", u"&Categories", None))
        self.actionBackup.setText(QCoreApplication.translate("LedgerMainWindow", u"&Backup...", None))
        self.actionRestore.setText(QCoreApplication.translate("LedgerMainWindow", u"&Restore...", None))
        self.PrepareTaxForms.setText(QCoreApplication.translate("LedgerMainWindow", u"Report for &taxes [RU]", None))
        self.MakeDealsReport.setText(QCoreApplication.translate("LedgerMainWindow", u"&Deals report", None))
        self.actionTags.setText(QCoreApplication.translate("LedgerMainWindow", u"&Tags", None))
        self.MakePLReport.setText(QCoreApplication.translate("LedgerMainWindow", u"&Profit/Loss report", None))
        self.MakeCategoriesReport.setText(QCoreApplication.translate("LedgerMainWindow", u"&Income/Spending report", None))
        self.BalanceBox.setTitle(QCoreApplication.translate("LedgerMainWindow", u"Balances", None))
        self.BalanceDate.setDisplayFormat(QCoreApplication.translate("LedgerMainWindow", u"dd/MM/yyyy", None))
        self.CurrencyLbl.setText(QCoreApplication.translate("LedgerMainWindow", u"Sum Currency:", None))
        self.ShowInactiveCheckBox.setText(QCoreApplication.translate("LedgerMainWindow", u"Show &Inactive", None))
        self.OperationsBox.setTitle(QCoreApplication.translate("LedgerMainWindow", u"Operations", None))
        self.DateRangeLbl.setText(QCoreApplication.translate("LedgerMainWindow", u"Time range:", None))
        self.DateRangeCombo.setItemText(0, QCoreApplication.translate("LedgerMainWindow", u"Week", None))
        self.DateRangeCombo.setItemText(1, QCoreApplication.translate("LedgerMainWindow", u"Month", None))
        self.DateRangeCombo.setItemText(2, QCoreApplication.translate("LedgerMainWindow", u"Quarter", None))
        self.DateRangeCombo.setItemText(3, QCoreApplication.translate("LedgerMainWindow", u"Year", None))
        self.DateRangeCombo.setItemText(4, QCoreApplication.translate("LedgerMainWindow", u"All", None))

        self.AccountLbl.setText(QCoreApplication.translate("LedgerMainWindow", u"Account:", None))
        self.ChooseAccountBtn.setText(QCoreApplication.translate("LedgerMainWindow", u"All", None))
        self.SearchLbl.setText(QCoreApplication.translate("LedgerMainWindow", u"Search:", None))
        self.PeerLbl.setText(QCoreApplication.translate("LedgerMainWindow", u"Peer:", None))
        self.AddActionDetail.setText(QCoreApplication.translate("LedgerMainWindow", u" + ", None))
        self.CopyActionDetail.setText(QCoreApplication.translate("LedgerMainWindow", u">>", None))
        self.RemoveActionDetail.setText(QCoreApplication.translate("LedgerMainWindow", u" \u2014 ", None))
        self.ActionAccountLabel.setText(QCoreApplication.translate("LedgerMainWindow", u"Account:", None))
        self.ActionTimestampEdit.setDisplayFormat(QCoreApplication.translate("LedgerMainWindow", u"dd/MM/yyyy hh:mm:ss", None))
        self.ActionTabLbl.setText(QCoreApplication.translate("LedgerMainWindow", u"Income / Spending", None))
        self.TradeFeeLbl.setText(QCoreApplication.translate("LedgerMainWindow", u"Fee broker:", None))
#if QT_CONFIG(tooltip)
        self.TradeSettlementEdit.setToolTip(QCoreApplication.translate("LedgerMainWindow", u"Trade settlement date", None))
#endif // QT_CONFIG(tooltip)
        self.TradeSettlementEdit.setSpecialValueText(QCoreApplication.translate("LedgerMainWindow", u"N/A", None))
        self.TradeSettlementEdit.setDisplayFormat(QCoreApplication.translate("LedgerMainWindow", u"dd/MM/yyyy", None))
        self.label.setText(QCoreApplication.translate("LedgerMainWindow", u"Quantity", None))
#if QT_CONFIG(tooltip)
        self.TradeNumberEdit.setToolTip(QCoreApplication.translate("LedgerMainWindow", u"Trade operation number", None))
#endif // QT_CONFIG(tooltip)
        self.TradeTabLbl.setText(QCoreApplication.translate("LedgerMainWindow", u"Buy / Sell", None))
        self.TradeTimestampEdit.setDisplayFormat(QCoreApplication.translate("LedgerMainWindow", u"dd/MM/yyyy hh:mm:ss", None))
        self.TradePriceLbl.setText(QCoreApplication.translate("LedgerMainWindow", u"Price:", None))
        self.TradeAccountLbl.setText(QCoreApplication.translate("LedgerMainWindow", u"Account:", None))
        self.TradeSymbolLbl.setText(QCoreApplication.translate("LedgerMainWindow", u"Symbol:", None))
        self.TradeCouponLbl.setText(QCoreApplication.translate("LedgerMainWindow", u"Coupon:", None))
        self.DividendSymbolLbl.setText(QCoreApplication.translate("LedgerMainWindow", u"Symbol:", None))
#if QT_CONFIG(tooltip)
        self.DividendTaxEdit.setToolTip(QCoreApplication.translate("LedgerMainWindow", u"Tax amount", None))
#endif // QT_CONFIG(tooltip)
        self.DividendTimestampEdit.setDisplayFormat(QCoreApplication.translate("LedgerMainWindow", u"dd/MM/yyyy hh:mm:ss", None))
        self.DividendTaxLbl.setText(QCoreApplication.translate("LedgerMainWindow", u"Tax amount:", None))
#if QT_CONFIG(tooltip)
        self.DividendSumEdit.setToolTip(QCoreApplication.translate("LedgerMainWindow", u"Dividend amount", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.DividendNumberEdit.setToolTip(QCoreApplication.translate("LedgerMainWindow", u"Dividend operation number", None))
#endif // QT_CONFIG(tooltip)
        self.DividendTabLbl.setText(QCoreApplication.translate("LedgerMainWindow", u"Dividend", None))
        self.DividendAccountLbl.setText(QCoreApplication.translate("LedgerMainWindow", u"Account:", None))
        self.DividendSumLbl.setText(QCoreApplication.translate("LedgerMainWindow", u"Dividend amount:", None))
#if QT_CONFIG(tooltip)
        self.DividendSumDescription.setToolTip(QCoreApplication.translate("LedgerMainWindow", u"Dividend description", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.DividendTaxDescription.setToolTip(QCoreApplication.translate("LedgerMainWindow", u"Tax description", None))
#endif // QT_CONFIG(tooltip)
        self.TransferTextLbl.setText(QCoreApplication.translate("LedgerMainWindow", u"Text:", None))
        self.TransferFromTimestamp.setDisplayFormat(QCoreApplication.translate("LedgerMainWindow", u"dd/MM/yyyy hh:mm:ss", None))
        self.TransferFromLbl.setText(QCoreApplication.translate("LedgerMainWindow", u"From:", None))
        self.TransferTabLbl.setText(QCoreApplication.translate("LedgerMainWindow", u"Transfer", None))
        self.TransferFeeLbl.setText(QCoreApplication.translate("LedgerMainWindow", u"Fee:", None))
        self.TransferFeeTimestamp.setSpecialValueText(QCoreApplication.translate("LedgerMainWindow", u"N/A", None))
        self.TransferFeeTimestamp.setDisplayFormat(QCoreApplication.translate("LedgerMainWindow", u"dd/MM/yyyy hh:mm:ss", None))
        self.TransferToLbl.setText(QCoreApplication.translate("LedgerMainWindow", u"To:", None))
        self.TransferToTimestamp.setDisplayFormat(QCoreApplication.translate("LedgerMainWindow", u"dd/MM/yyyy hh:mm:ss", None))
        self.NewOperationBtn.setText(QCoreApplication.translate("LedgerMainWindow", u"New", None))
        self.CopyOperationBtn.setText(QCoreApplication.translate("LedgerMainWindow", u"Copy", None))
        self.DeleteOperationBtn.setText(QCoreApplication.translate("LedgerMainWindow", u"Del", None))
        self.SaveOperationBtn.setText(QCoreApplication.translate("LedgerMainWindow", u"Save", None))
        self.RevertOperationBtn.setText(QCoreApplication.translate("LedgerMainWindow", u"Revert", None))
        self.MainTabs.setTabText(self.MainTabs.indexOf(self.BalanceTransactionTab), QCoreApplication.translate("LedgerMainWindow", u"Balance && Operations", None))
        self.HoldingsDate.setDisplayFormat(QCoreApplication.translate("LedgerMainWindow", u"dd/MM/yyyy", None))
        self.HoldingsCurrencyLbl.setText(QCoreApplication.translate("LedgerMainWindow", u"Common currency:", None))
        self.MainTabs.setTabText(self.MainTabs.indexOf(self.HoldingsTab), QCoreApplication.translate("LedgerMainWindow", u"Holdings", None))
        self.MainTabs.setTabText(self.MainTabs.indexOf(self.LoggingTab), QCoreApplication.translate("LedgerMainWindow", u"Log messages", None))
        self.menuFile.setTitle(QCoreApplication.translate("LedgerMainWindow", u"&File", None))
        self.menu_DAta.setTitle(QCoreApplication.translate("LedgerMainWindow", u"&Data", None))
        self.menuPredefined_data.setTitle(QCoreApplication.translate("LedgerMainWindow", u"Predefined data", None))
        self.menuLoad.setTitle(QCoreApplication.translate("LedgerMainWindow", u"&Load", None))
        self.menu_Reports.setTitle(QCoreApplication.translate("LedgerMainWindow", u"&Reports", None))
    # retranslateUi

