import logging

from datetime import datetime
from math import copysign
from functools import partial
from jal.constants import Setup, BookAccount, TransactionType, ActionSubtype, TransferSubtype, CorporateAction, \
    PredefinedCategory, PredefinedPeer
from PySide2.QtCore import Qt, Slot, QDate, QDateTime
from PySide2.QtWidgets import QDialog, QMessageBox, QMenu, QAction
from jal.db.helpers import executeSQL, readSQL, readSQLrecord, get_asset_name, get_account_id, get_asset_id
from jal.db.routines import calculateBalances, calculateHoldings
from jal.ui_custom.helpers import g_tr
from jal.ui.ui_rebuild_window import Ui_ReBuildDialog
from jal.db.tax_estimator import TaxEstimator


class RebuildDialog(QDialog, Ui_ReBuildDialog):
    def __init__(self, parent, frontier):
        QDialog.__init__(self)
        self.setupUi(self)

        self.LastRadioButton.toggle()
        self.frontier = frontier
        frontier_text = datetime.utcfromtimestamp(frontier).strftime('%d/%m/%Y')
        self.FrontierDateLabel.setText(frontier_text)
        self.CustomDateEdit.setDate(QDate.currentDate())

        # center dialog with respect to parent window
        x = parent.x() + parent.width()/2 - self.width()/2
        y = parent.y() + parent.height()/2 - self.height()/2
        self.setGeometry(x, y, self.width(), self.height())

    def isFastAndDirty(self):
        return self.FastAndDirty.isChecked()

    def getTimestamp(self):
        if self.LastRadioButton.isChecked():
            return self.frontier
        elif self.DateRadionButton.isChecked():
            return self.CustomDateEdit.dateTime().toSecsSinceEpoch()
        else:  # self.AllRadioButton.isChecked()
            return 0


# ===================================================================================================================
# TODO Check are there positive lines for Incomes
# TODO Check are there negative lines for Costs
# ===================================================================================================================
class Ledger:
    SILENT_REBUILD_THRESHOLD = 50

    def __init__(self, db):
        self.db = db
        self.current = {}
        self.current_seq = -1
        self.balances_view = None
        self.holdings_view = None
        self.balance_active_only = 1
        self.balance_currency = None
        self.balance_date = QDateTime.currentSecsSinceEpoch()
        self.holdings_date = QDateTime.currentSecsSinceEpoch()
        self.holdings_currency = None
        self.holdings_index = None
        self.estimator = None

    def setViews(self, balances, holdings):
        self.balances_view = balances
        self.holdings_view = holdings
        self.holdings_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.holdings_view.customContextMenuRequested.connect(self.onHoldingsContextMenu)

    def setActiveBalancesOnly(self, active_only):
        if self.balance_active_only != active_only:
            self.balance_active_only = active_only
            self.updateBalancesView()

    def setBalancesDate(self, balance_date):
        if self.balance_date != balance_date:
            self.balance_date = balance_date
            self.updateBalancesView()

    def setBalancesCurrency(self, currency_id, currency_name):
        if self.balance_currency != currency_id:
            self.balance_currency = currency_id
            balances_model = self.balances_view.model()
            balances_model.setHeaderData(balances_model.fieldIndex("balance_adj"), Qt.Horizontal,
                                         g_tr('Ledger', "Balance, ") + currency_name)
            self.updateBalancesView()

    def updateBalancesView(self):
        if self.balances_view is None:
            return
        calculateBalances(self.db, self.balance_date, self.balance_currency, self.balance_active_only)
        self.balances_view.model().select()

    def setHoldingsDate(self, holdings_date):
        if self.holdings_date != holdings_date:
            self.holdings_date = holdings_date
            self.updateHoldingsView()

    def setHoldingsCurrency(self, currency_id, currency_name):
        if self.holdings_currency != currency_id:
            self.holdings_currency = currency_id
            holidings_model = self.holdings_view.model()
            holidings_model.setHeaderData(holidings_model.fieldIndex("value_adj"), Qt.Horizontal,
                                          g_tr('Ledger', "Value, ") + currency_name)
            self.updateHoldingsView()

    def updateHoldingsView(self):
        if self.holdings_view is None:
            return
        calculateHoldings(self.db, self.holdings_date, self.holdings_currency)
        holdings_model = self.holdings_view.model()
        holdings_model.select()
        for row in range(holdings_model.rowCount()):
            if holdings_model.data(holdings_model.index(row, 1)):
                self.holdings_view.setSpan(row, 3, 1, 3)
        self.holdings_view.show()

    @Slot()
    def onHoldingsContextMenu(self, pos):
        self.holdings_index = self.holdings_view.indexAt(pos)
        contextMenu = QMenu(self.holdings_view)
        actionEstimateTax = QAction(text=g_tr('Ledger', "Estimate Russian Tax"), parent=self.holdings_view)
        actionEstimateTax.triggered.connect(
            partial(self.estimateRussianTax, self.holdings_view.viewport().mapToGlobal(pos)))
        contextMenu.addAction(actionEstimateTax)
        contextMenu.popup(self.holdings_view.viewport().mapToGlobal(pos))

    # Returns timestamp of last operations that were calculated into ledger
    def getCurrentFrontier(self):
        current_frontier = readSQL(self.db, "SELECT ledger_frontier FROM frontier")
        if current_frontier == '':
            current_frontier = 0
        return current_frontier

    # Add one more transaction to 'book' of ledger.
    # If book is Assets and value is not None then amount contains Asset Quantity and Value contains amount
    #    of money in current account currency. Otherwise Amount contains only money value.
    # Method uses Account, Asset,Peer, Category and Tag values from current transaction
    def appendTransaction(self, book, amount, value=None):
        seq_id = self.current_seq
        timestamp = self.current['timestamp']
        if book == BookAccount.Assets:
            asset_id = self.current['asset']
        else:
            asset_id = self.current['currency']
        account_id = self.current['account']
        if book == BookAccount.Costs or book == BookAccount.Incomes:
            peer_id = self.current['peer']
            category_id = self.current['category']
            tag_id = None if self.current['tag'] == '' else self.current['tag']
        else:
            peer_id = None
            category_id = None
            tag_id = None
        try:
            old_sid, old_amount, old_value = readSQL(self.db,
                "SELECT sid, sum_amount, sum_value FROM ledger_sums "
                "WHERE book_account = :book AND asset_id = :asset_id "
                "AND account_id = :account_id AND sid <= :seq_id "
                "ORDER BY sid DESC LIMIT 1",
                [(":book", book), (":asset_id", asset_id), (":account_id", account_id), (":seq_id", seq_id)])
        except:
            old_sid = -1
            old_amount = 0.0
            old_value = 0.0
        new_amount = old_amount + amount
        if value is None:
            new_value = old_value
        else:
            new_value = old_value + value
        if (abs(new_amount - old_amount) + abs(new_value - old_value)) <= (2 * Setup.CALC_TOLERANCE):
            return  # we have zero amount - no reason to put it into ledger

        _ = executeSQL(self.db, "INSERT INTO ledger (timestamp, sid, book_account, asset_id, account_id, "
                                "amount, value, peer_id, category_id, tag_id) "
                                "VALUES(:timestamp, :sid, :book, :asset_id, :account_id, "
                                ":amount, :value, :peer_id, :category_id, :tag_id)",
                       [(":timestamp", timestamp), (":sid", seq_id), (":book", book), (":asset_id", asset_id),
                        (":account_id", account_id), (":amount", amount), (":value", value),
                        (":peer_id", peer_id), (":category_id", category_id), (":tag_id", tag_id)])
        if seq_id == old_sid:
            _ = executeSQL(self.db, "UPDATE ledger_sums SET sum_amount = :new_amount, sum_value = :new_value"
                                    " WHERE sid = :sid AND book_account = :book"
                                    " AND asset_id = :asset_id AND account_id = :account_id",
                           [(":new_amount", new_amount), (":new_value", new_value), (":sid", seq_id),
                            (":book", book), (":asset_id", asset_id), (":account_id", account_id)])
        else:
            _ = executeSQL(self.db, "INSERT INTO ledger_sums(sid, timestamp, book_account, "
                                    "asset_id, account_id, sum_amount, sum_value) "
                                    "VALUES(:sid, :timestamp, :book, :asset_id, "
                                    ":account_id, :new_amount, :new_value)",
                           [(":sid", seq_id), (":timestamp", timestamp), (":book", book), (":asset_id", asset_id),
                            (":account_id", account_id), (":new_amount", new_amount), (":new_value", new_value)])
        self.db.commit()

    # TODO check that condition <= is really correct for timestamp in this function
    # Returns Amount measured in current account currency or asset_id that 'book' has at current ledger frontier
    def getAmount(self, book, asset_id=None):
        if asset_id is None:
            amount = readSQL(self.db,
                               "SELECT sum_amount FROM ledger_sums WHERE book_account = :book AND "
                               "account_id = :account_id AND timestamp <= :timestamp ORDER BY sid DESC LIMIT 1",
                               [(":book", book), (":account_id", self.current['account']),
                                (":timestamp", self.current['timestamp'])])
        else:
            amount = readSQL(self.db, "SELECT sum_amount FROM ledger_sums WHERE book_account = :book "
                                        "AND account_id = :account_id AND asset_id = :asset_id "
                                        "AND timestamp <= :timestamp ORDER BY sid DESC LIMIT 1",
                               [(":book", book), (":account_id", self.current['account']),
                                (":asset_id", asset_id), (":timestamp", self.current['timestamp'])])
        amount = float(amount) if amount is not None else 0.0
        return amount

    def takeCredit(self, operation_amount):
        money_available = self.getAmount(BookAccount.Money)
        credit = 0
        if money_available < operation_amount:
            credit = operation_amount - money_available
            self.appendTransaction(BookAccount.Liabilities, -credit)
        return credit

    def returnCredit(self, operation_amount):
        current_credit_value = -1.0 * self.getAmount(BookAccount.Liabilities)
        debit = 0
        if current_credit_value > 0:
            if current_credit_value >= operation_amount:
                debit = operation_amount
            else:
                debit = current_credit_value
        if debit > 0:
            self.appendTransaction(BookAccount.Liabilities, debit)
        return debit

    def processActionDetails(self):
        query = executeSQL(self.db, "SELECT sum as amount, category_id, tag_id FROM action_details AS d WHERE pid=:pid",
                           [(":pid", self.current['id'])])
        while query.next():
            amount, self.current['category'], self.current['tag'] = readSQLrecord(query)
            book = BookAccount.Costs if amount < 0 else BookAccount.Incomes
            self.appendTransaction(book, -amount)

    def processAction(self):
        action_amount = self.current['amount']
        if action_amount < 0:
            credit_taken = self.takeCredit(-action_amount)
            self.appendTransaction(BookAccount.Money, -(-action_amount - credit_taken))
        else:
            credit_returned = self.returnCredit(action_amount)
            if credit_returned < action_amount:
                self.appendTransaction(BookAccount.Money, action_amount - credit_returned)
        if self.current['subtype'] == ActionSubtype.SingleIncome:
            self.appendTransaction(BookAccount.Incomes, -action_amount)
        elif self.current['subtype'] == ActionSubtype.SingleSpending:
            self.appendTransaction(BookAccount.Costs, -action_amount)
        else:
            self.processActionDetails()

    def processDividend(self):
        if self.current['peer'] == '':
            logging.error(g_tr('Ledger', "Can't process dividend as bank isn't set for investment account"))
            return
        dividend_amount = self.current['amount']
        tax_amount = self.current['fee_tax']
        credit_returned = self.returnCredit(dividend_amount - tax_amount)
        if credit_returned < dividend_amount:
            self.appendTransaction(BookAccount.Money, dividend_amount - credit_returned)
        self.appendTransaction(BookAccount.Incomes, -dividend_amount)
        if tax_amount:
            self.appendTransaction(BookAccount.Money, -tax_amount)
            self.current['category'] = PredefinedCategory.Taxes
            self.appendTransaction(BookAccount.Costs, tax_amount)

    # Process buy or sell operation base on self.current['amount'] (>0 - buy, <0 - sell)
    def processTrade(self):
        if self.current['peer'] == '':
            logging.error(g_tr('Ledger', "Can't process trade as bank isn't set for investment account"))
            return

        seq_id = self.current_seq
        account_id = self.current['account']
        asset_id = self.current['asset']
        type = copysign(1, self.current['amount'])  # 1 is buy, -1 is sell
        qty = type * self.current['amount']
        price = self.current['price']

        trade_value = round(price * qty, 2) + type * self.current['fee_tax'] + self.current['coupon']

        processed_qty = 0
        processed_value = 0
        # Get asset amount accumulated before current operation
        asset_amount = self.getAmount(BookAccount.Assets, asset_id)
        if ((-type) * asset_amount) > 0:  # Process deal match if we have asset that is opposite to operation
            last_type = readSQL(self.db, "SELECT s.type FROM deals AS d "
                                         "LEFT JOIN sequence AS s ON d.close_sid=s.id "
                                         "WHERE d.account_id=:account_id AND d.asset_id=:asset_id "
                                         "ORDER BY d.close_sid DESC, d.open_sid DESC LIMIT 1",
                                [(":account_id", account_id), (":asset_id", asset_id)])
            if last_type is None or last_type == TransactionType.Trade:
                # Get information about last deal with quantity of opposite sign
                last_sid = readSQL(self.db, "SELECT "
                                            "CASE WHEN (:type)*qty<0 THEN open_sid ELSE close_sid END AS last_sid "
                                            "FROM deals "
                                            "WHERE account_id=:account_id AND asset_id=:asset_id "
                                            "ORDER BY close_sid DESC, open_sid DESC LIMIT 1",
                                   [(":type", type), (":account_id", account_id), (":asset_id", asset_id)])
                last_sid = 0 if last_sid is None else last_sid
                # Next get information about abs trade quantity that was in this last deal
                # It may be a corporate action - its quantity calculation is a bit more complicated
                last_qty = readSQL(self.db,
                                              "SELECT coalesce(SUM(qty), 0) AS qty FROM ( "
                                              "SELECT ABS(t.qty) AS qty "
                                              "FROM sequence AS s "
                                              "LEFT JOIN trades AS t ON t.id=s.operation_id AND s.type=3 "
                                              "WHERE s.id=:last_sid "
                                              "UNION ALL "
                                              "SELECT "
                                              "CASE "
                                              "    WHEN ca.type = 2 AND ca.asset_id=:asset_id THEN ca.qty "
                                              "    ELSE ca.qty_new "
                                              "END AS qty "
                                              "FROM sequence AS s "
                                              "LEFT JOIN corp_actions AS ca ON ca.id=s.operation_id AND s.type=5 "
                                              "WHERE s.id=:last_sid "
                                              ")",
                                              [(":asset_id", asset_id), (":last_sid", last_sid)])
                # Collect quantity of all deals where this last opposite trade participated (positive value)
                # If it was a corporate action we need to take only where it was an opening of the deal
                deals_qty = readSQL(self.db, "SELECT coalesce(SUM(ABS(qty)), 0) "   
                                             "FROM deals AS d "
                                             "LEFT JOIN sequence AS s ON s.id=d.close_sid "
                                             "WHERE account_id=:account_id AND asset_id=:asset_id "
                                             "AND (open_sid=:last_sid OR close_sid=:last_sid) AND s.type!=5",
                                    [(":account_id", account_id), (":asset_id", asset_id), (":last_sid", last_sid)])
                reminder = last_qty - deals_qty
                # if last trade is fully matched (reminder<=0) we start from next trade, otherwise we need to shift by 1
                if reminder > 0:
                    last_sid -= 1
            elif last_type == TransactionType.CorporateAction:
                last_sid, ca_type = readSQL(self.db,
                                            "SELECT d.close_sid, c.type FROM deals AS d "
                                            "LEFT JOIN sequence AS s ON d.close_sid=s.id "
                                            "LEFT JOIN corp_actions AS c ON s.operation_id=c.id "
                                            "WHERE d.account_id=:account_id AND d.asset_id=:asset_id "
                                            "ORDER BY d.close_sid DESC, d.open_sid DESC LIMIT 1",
                                            [(":account_id", account_id), (":asset_id", asset_id)])
                if ca_type == CorporateAction.Split \
                        or ca_type == CorporateAction.StockDividend or ca_type == CorporateAction.SpinOff:
                    last_sid -= 1
                reminder = 0

            # Get a list of all previous not matched trades or corporate actions of opposite direction (type parameter)
            query = executeSQL(self.db,
                               "SELECT * FROM ("
                               "SELECT s.id, ABS(t.qty), t.price FROM trades AS t "
                               "LEFT JOIN sequence AS s ON s.type = 3 AND s.operation_id=t.id "
                               "WHERE (:type)*qty < 0 AND t.asset_id = :asset_id AND t.account_id = :account_id "
                               "AND s.id < :sid AND s.id > :last_sid "
                               "UNION ALL "
                               "SELECT s.id, "
                               "CASE "
                               "    WHEN c.type = 2 AND c.asset_id=:asset_id THEN c.qty "
                               "    ELSE c.qty_new "
                               "END AS qty, "
                               "CASE "
                               "    WHEN c.type = 2 AND c.asset_id=:asset_id THEN coalesce(l.value/c.qty, 0) "
                               "    ELSE coalesce(l.value/c.qty_new, 0) "
                               "END AS price "
                               "FROM corp_actions AS c "
                               "LEFT JOIN sequence AS s ON s.type = 5 AND s.operation_id=c.id "
                               "LEFT JOIN ledger AS l ON s.id = l.sid AND l.asset_id=:asset_id AND l.value > 0 "
                               "WHERE (:type)*c.qty_new < 0 AND (c.asset_id_new=:asset_id OR (c.asset_id=:asset_id AND c.type=2)) AND c.account_id=:account_id "
                               "AND s.id < :sid AND s.id > :last_sid "
                               ")ORDER BY id",
                               [(":type", type), (":asset_id", asset_id), (":account_id", account_id),
                                (":sid", seq_id), (":last_sid", last_sid)])
            while query.next():  # Perform match ("closure") of previous trades
                deal_sid, deal_qty, deal_price = readSQLrecord(query)    # deal_sid -> trade_sid
                if reminder > 0:
                    next_deal_qty = reminder
                    reminder = 0
                else:
                    next_deal_qty = deal_qty
                if (processed_qty + next_deal_qty) >= qty:  # We can't process more than qty of current trade
                    next_deal_qty = qty - processed_qty     # If it happens - just process the remainder of the trade
                # Create a deal with relevant sign of quantity (-1 for short, +1 for long)
                _ = executeSQL(self.db, "INSERT INTO deals(account_id, asset_id, open_sid, close_sid, qty) "
                                        "VALUES(:account_id, :asset_id, :open_sid, :close_sid, :qty)",
                               [(":account_id", account_id), (":asset_id", asset_id), (":open_sid", deal_sid),
                                (":close_sid", seq_id), (":qty", (-type)*next_deal_qty)])
                processed_qty += next_deal_qty
                processed_value += (next_deal_qty * deal_price)
                if processed_qty == qty:
                    break
        if type > 0:
            credit_value = self.takeCredit(trade_value)
        else:
            credit_value = self.returnCredit(trade_value)
        if credit_value < trade_value:
            self.appendTransaction(BookAccount.Money, (-type)*(trade_value - credit_value))
        if processed_qty > 0:  # Add result of closed deals
            # decrease (for sell) or increase (for buy) amount of assets in ledger
            self.appendTransaction(BookAccount.Assets, type*processed_qty, type*processed_value)
            self.current['category'] = PredefinedCategory.Profit
            self.appendTransaction(BookAccount.Incomes, type * ((price * processed_qty) - processed_value))
        if processed_qty < qty:  # We have reminder that opens a new position
            self.appendTransaction(BookAccount.Assets, type*(qty - processed_qty), type*(qty - processed_qty) * price)
        if self.current['coupon']:
            self.current['category'] = PredefinedCategory.Dividends
            if type> 0:
                self.appendTransaction(BookAccount.Costs, self.current['coupon'])
            else:
                self.appendTransaction(BookAccount.Incomes, type*self.current['coupon'])
        if self.current['fee_tax']:
            self.current['category'] = PredefinedCategory.Fees
            self.appendTransaction(BookAccount.Costs, self.current['fee_tax'])

    def processTransferOut(self):
        amount = -self.current['amount']
        credit_taken = self.takeCredit(amount)
        self.appendTransaction(BookAccount.Money, -(amount - credit_taken))
        self.appendTransaction(BookAccount.Transfers, amount)

    def processTransferIn(self):
        amount = self.current['amount']
        credit_returned = self.returnCredit(amount)
        if credit_returned < amount:
            self.appendTransaction(BookAccount.Money, (amount - credit_returned))
        self.appendTransaction(BookAccount.Transfers, -amount)

    def processTransferFee(self):
        fee = -self.current['amount']
        credit_taken = self.takeCredit(fee)
        self.current['peer'] = PredefinedPeer.Financial
        self.appendTransaction(BookAccount.Money, -(fee - credit_taken))
        self.current['category'] = PredefinedCategory.Fees
        self.appendTransaction(BookAccount.Costs, fee)

    def processTransfer(self):
        operationTransfer = {
            TransferSubtype.Outgoing: self.processTransferOut,
            TransferSubtype.Fee: self.processTransferFee,
            TransferSubtype.Incoming: self.processTransferIn
        }
        operationTransfer[self.current['subtype']]()

    def updateStockDividendAssets(self):
        asset_amount = self.getAmount(BookAccount.Assets, self.current['asset'])
        self.current['price'] = self.current['price'] + asset_amount
        self.current['amount'] = asset_amount
        asset = get_asset_name(self.db, self.current['asset'])
        QMessageBox().information(None, g_tr('Ledger', "Confirmation"),
                                  g_tr('Ledger', "Stock dividend for was updated for ") + asset +
                                  f" @{datetime.utcfromtimestamp(self.current['timestamp']).strftime('%d.%m.%Y')}\n" +
                                  g_tr('Ledger', "Please check that quantity is correct."),
                                  QMessageBox.Ok)
        _ = executeSQL(self.db, "DROP TRIGGER IF EXISTS corp_after_update")  # FIXME improve code with triggers
        _ = executeSQL(self.db, "UPDATE corp_actions SET qty=:qty, qty_new=:qty_new WHERE id=:id",
                       [(":id", self.current['id']),
                        (":qty", self.current['amount']), (":qty_new", self.current['price'])])
        _ = executeSQL(self.db, "CREATE TRIGGER corp_after_update "
                                "AFTER UPDATE OF timestamp, account_id, type, asset_id, qty, asset_id_new, qty_new "
                                "ON corp_actions FOR EACH ROW "
                                "BEGIN "
                                "DELETE FROM ledger WHERE timestamp >= OLD.timestamp OR timestamp >= NEW.timestamp; "
                                "DELETE FROM sequence WHERE timestamp >= OLD.timestamp OR timestamp >= NEW.timestamp; "
                                "DELETE FROM ledger_sums WHERE timestamp >= OLD.timestamp OR timestamp >= NEW.timestamp; "
                                "END")

    def processCorporateAction(self):
        # Stock dividends are imported without initial stock amounts -> correction happens here
        if self.current['subtype'] == CorporateAction.StockDividend and self.current['amount'] < 0:
            self.updateStockDividendAssets()

        seq_id = self.current_seq
        account_id = self.current['account']
        asset_id = self.current['asset']
        qty = self.current['amount']

        processed_qty = 0
        processed_value = 0
        # Get asset amount accumulated before current operation
        asset_amount = self.getAmount(BookAccount.Assets, asset_id)
        if asset_amount < (qty - 2*Setup.CALC_TOLERANCE):
            logging.fatal(g_tr('Ledger', "Asset amount is not enough for corporate action processing. Date: ")
                          + f"{datetime.utcfromtimestamp(self.current['timestamp']).strftime('%d/%m/%Y %H:%M:%S')}")
            return
        # Get information about last deal
        last_sid = readSQL(self.db, "SELECT "
                                    "CASE WHEN qty>0 THEN open_sid ELSE close_sid END AS last_sid "
                                    "FROM deals "
                                    "WHERE account_id=:account_id AND asset_id=:asset_id "
                                    "ORDER BY close_sid DESC, open_sid DESC LIMIT 1",
                           [(":account_id", account_id), (":asset_id", asset_id)])
        last_sid = 0 if last_sid is None else last_sid
        # Next get information about abs trade quantity that was in this last deal
        last_qty = readSQL(self.db, "SELECT coalesce(ABS(t.qty), 0)+coalesce(ABS(ca.qty_new) , 0) AS qty "
                                    "FROM sequence AS s "
                                    "LEFT JOIN trades AS t ON t.id=s.operation_id AND s.type=3 "
                                    "LEFT JOIN corp_actions AS ca ON ca.id=s.operation_id AND s.type=5 "
                                    "WHERE s.id=:last_sid", [(":last_sid", last_sid)])
        last_qty = 0 if last_qty is None else last_qty
        # Collect quantity of all deals where this last opposite trade participated (positive value)
        deals_qty = readSQL(self.db, "SELECT coalesce(SUM(ABS(qty)), 0) "
                                     "FROM deals AS d "
                                     "WHERE account_id=:account_id AND asset_id=:asset_id "
                                     "AND (open_sid=:last_sid OR close_sid=:last_sid)",
                            [(":account_id", account_id), (":asset_id", asset_id), (":last_sid", last_sid)])
        reminder = last_qty - deals_qty
        # if last trade is fully matched (reminder<=0) we start from next trade, otherwise we need to shift by 1
        if reminder > 0:
            last_sid = last_sid - 1

        # Get a list of all previous not matched trades or corporate actions of opposite direction (type parameter)
        query = executeSQL(self.db,
                           "SELECT * FROM ("
                           "SELECT s.id, ABS(t.qty), t.price FROM trades AS t "
                           "LEFT JOIN sequence AS s ON s.type = 3 AND s.operation_id=t.id "
                           "WHERE qty > 0 AND t.asset_id = :asset_id AND t.account_id = :account_id "
                           "AND s.id < :sid AND s.id > :last_sid "
                           "UNION ALL "
                           "SELECT s.id, ABS(c.qty_new), coalesce(l.value/c.qty_new, 0) AS price FROM corp_actions AS c "
                           "LEFT JOIN sequence AS s ON s.type = 5 AND s.operation_id=c.id "
                           "LEFT JOIN ledger AS l ON s.id = l.sid AND l.asset_id=c.asset_id_new AND l.value > 0 "
                           "WHERE c.qty_new > 0 AND c.asset_id_new=:asset_id AND c.account_id=:account_id "
                           "AND s.id < :sid AND s.id > :last_sid "
                           ")ORDER BY id",
                           [(":asset_id", asset_id), (":account_id", account_id),
                            (":sid", seq_id), (":last_sid", last_sid)])
        while query.next():  # Perform match ("closure") of previous trades
            deal_sid, deal_qty, deal_price = readSQLrecord(query)  # deal_sid -> trade_sid
            if reminder > 0:
                next_deal_qty = reminder
                reminder = 0
            else:
                next_deal_qty = deal_qty
            if (processed_qty + next_deal_qty) >= qty:  # We can't process more than qty of current trade
                next_deal_qty = qty - processed_qty  # If it happens - just process the remainder of the trade
            # Create a deal with relevant sign of quantity (-1 for short, +1 for long)
            _ = executeSQL(self.db, "INSERT INTO deals(account_id, asset_id, open_sid, close_sid, qty) "
                                    "VALUES(:account_id, :asset_id, :open_sid, :close_sid, :qty)",
                           [(":account_id", account_id), (":asset_id", asset_id), (":open_sid", deal_sid),
                            (":close_sid", seq_id), (":qty", next_deal_qty)])
            processed_qty += next_deal_qty
            processed_value += (next_deal_qty * deal_price)
            if processed_qty == qty:
                break
        # Asset allocations for different corporate actions:
        # +-----------------+-------+-----+------------+-----------+----------+---------------+--------------------+
        # |                 | Asset | Qty | cost basis | Asset new | Qty new  | cost basis    | The same algo for: |
        # +-----------------+-------+-----+------------+-----------+----------+---------------+--------------------+
        # | Symbol Change   |   A   |  N  |  100 %     |     B     |    N     |   100%        |                    |
        # | (R-)Split       |   A   |  N  |  100 %     |     A     |    M     |   100%        | Stock Dividend     |
        # | Merger          |   A   |  N  |  100 %     |     B     |    M     |   100%        |                    |
        # | Spin-Off        |   A   |  N  |  100 %     |   A & B   | AxN, BxM | X% & (100-X)% |                    |
        # +-----------------+-------+-----+------------+-----------+----------+---------------+--------------------+
        # Withdraw value with old quantity of old asset as it common for all corporate action
        self.appendTransaction(BookAccount.Assets, -processed_qty, -processed_value)

        # Prepare details about new asset
        new_asset = self.current['peer']
        new_qty = self.current['price']
        new_value = processed_value
        if self.current['subtype'] == CorporateAction.SpinOff:
            new_value = processed_value * self.current['fee_tax']
            # Modify value for old asset
            self.appendTransaction(BookAccount.Assets, self.current['amount'], processed_value - new_value)
        # Create value for new asset
        self.current['asset'] = new_asset
        self.appendTransaction(BookAccount.Assets, new_qty, new_value)

    # Rebuild transaction sequence and recalculate all amounts
    # timestamp:
    # -1 - re-build from last valid operation (from ledger frontier)
    #      will asks for confirmation if we have more than SILENT_REBUILD_THRESHOLD operations require rebuild
    # 0 - re-build from scratch
    # any - re-build all operations after given timestamp
    def rebuild(self, from_timestamp=-1, fast_and_dirty=False, silent=True):
        operationProcess = {
            TransactionType.Action: self.processAction,
            TransactionType.Dividend: self.processDividend,
            TransactionType.Trade: self.processTrade,
            TransactionType.Transfer: self.processTransfer,
            TransactionType.CorporateAction: self.processCorporateAction
        }

        if from_timestamp >= 0:
            frontier = from_timestamp
            silent = False
        else:
            frontier = self.getCurrentFrontier()
            operations_count = readSQL(self.db, "SELECT COUNT(id) FROM all_transactions WHERE timestamp >= :frontier",
                               [(":frontier", frontier)])
            if operations_count > self.SILENT_REBUILD_THRESHOLD:
                silent = False
                if QMessageBox().warning(None, g_tr('Ledger', "Confirmation"), f"{operations_count}" +
                                         g_tr('Ledger', " operations require rebuild. Do you want to do it right now?"),
                                         QMessageBox.Yes, QMessageBox.No) == QMessageBox.No:
                    return
        if not silent:
            logging.info(g_tr('Ledger', "Re-build ledger from: ") +
                         f"{datetime.utcfromtimestamp(frontier).strftime('%d/%m/%Y %H:%M:%S')}")
        start_time = datetime.now()
        _ = executeSQL(self.db, "DELETE FROM deals WHERE close_sid >= "
                                "(SELECT coalesce(MIN(id), 0) FROM sequence WHERE timestamp >= :frontier)",
                       [(":frontier", frontier)])
        _ = executeSQL(self.db, "DELETE FROM ledger WHERE timestamp >= :frontier", [(":frontier", frontier)])
        _ = executeSQL(self.db, "DELETE FROM sequence WHERE timestamp >= :frontier", [(":frontier", frontier)])
        _ = executeSQL(self.db, "DELETE FROM ledger_sums WHERE timestamp >= :frontier", [(":frontier", frontier)])
        self.db.commit()

        if fast_and_dirty:  # For 30k operations difference of execution time is - with 0:02:41 / without 0:11:44
            _ = executeSQL(self.db, "PRAGMA synchronous = OFF")
        query = executeSQL(self.db, "SELECT type, id, timestamp, subtype, account, currency, asset, amount, "
                                    "category, price, fee_tax, coupon, peer, tag FROM all_transactions "
                                    "WHERE timestamp >= :frontier", [(":frontier", frontier)])
        while query.next():
            self.current = readSQLrecord(query, named=True)
            seq_query = executeSQL(self.db, "INSERT INTO sequence(timestamp, type, operation_id) "
                                            "VALUES(:timestamp, :type, :operation_id)",
                                   [(":timestamp", self.current['timestamp']), (":type", self.current['type']),
                                    (":operation_id", self.current['id'])])
            self.current_seq = seq_query.lastInsertId()
            operationProcess[self.current['type']]()
            if not silent and (query.at() % 1000) == 0:
                logging.info(g_tr('Ledger', "Processed ") + f"{int(query.at()/1000)}" +
                             g_tr('Ledger', "k records, current frontier: ") +
                             f"{datetime.utcfromtimestamp(self.current['timestamp']).strftime('%d/%m/%Y %H:%M:%S')}")
        if fast_and_dirty:
            _ = executeSQL(self.db, "PRAGMA synchronous = ON")

        if not silent:
            logging.info(g_tr('Ledger', "Ledger is complete. Elapsed time: ") + f"{datetime.now() - start_time}" +
                         g_tr('Ledger', ", new frontier: ") + f"{datetime.utcfromtimestamp(self.current['timestamp']).strftime('%d/%m/%Y %H:%M:%S')}")
        self.updateBalancesView()
        self.updateHoldingsView()

    def showRebuildDialog(self, parent):
        rebuild_dialog = RebuildDialog(parent, self.getCurrentFrontier())
        if rebuild_dialog.exec_():
            self.rebuild(from_timestamp=rebuild_dialog.getTimestamp(),
                         fast_and_dirty=rebuild_dialog.isFastAndDirt(), silent=False)

    @Slot()
    def estimateRussianTax(self, position):
        model = self.holdings_index.model()
        account_id = get_account_id(self.db, model.data(model.index(self.holdings_index.row(), 3), Qt.DisplayRole))
        asset_id = get_asset_id(self.db, model.data(model.index(self.holdings_index.row(), 4), Qt.DisplayRole))
        asset_qty = model.data(model.index(self.holdings_index.row(), 6), Qt.DisplayRole)
        self.estimator = TaxEstimator(self.db, account_id, asset_id, asset_qty, position)
        if self.estimator.ready:
            self.estimator.open()
