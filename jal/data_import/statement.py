import json
import sys
import logging
from datetime import datetime

from jal.widgets.helpers import g_tr
from jal.constants import Setup, MarketDataFeed, PredefinedAsset, DividendSubtype, CorporateAction
from jal.db.update import JalDB
if "pytest" not in sys.modules:
    from PySide2.QtCore import Slot
    from PySide2.QtWidgets import QApplication, QDialog, QMessageBox
    from jal.ui.ui_select_account_dlg import Ui_SelectAccountDlg


# -----------------------------------------------------------------------------------------------------------------------
# FIXME - this class is duplicated in statements.py
# Remove old definition and adopt if for better usage with pytest framework
if "pytest" not in sys.modules:
    class SelectAccountDialog(QDialog, Ui_SelectAccountDlg):
        def __init__(self, description, current_account, recent_account=None):
            QDialog.__init__(self)
            self.setupUi(self)
            self.account_id = recent_account
            self.current_account = current_account

            self.DescriptionLbl.setText(description)
            if self.account_id:
                self.AccountWidget.selected_id = self.account_id

            # center dialog with respect to main application window
            parent = None
            for widget in QApplication.topLevelWidgets():
                if widget.objectName() == Setup.MAIN_WND_NAME:
                    parent = widget
            if parent:
                x = parent.x() + parent.width() / 2 - self.width() / 2
                y = parent.y() + parent.height() / 2 - self.height() / 2
                self.setGeometry(x, y, self.width(), self.height())

        @Slot()
        def closeEvent(self, event):
            self.account_id = self.AccountWidget.selected_id
            if self.AccountWidget.selected_id == 0:
                QMessageBox().warning(None, g_tr('ReferenceDataDialog', "No selection"),
                                      g_tr('ReferenceDataDialog', "Invalid account selected"),
                                      QMessageBox.Ok)
                event.ignore()
                return

            if self.AccountWidget.selected_id == self.current_account:
                QMessageBox().warning(None, g_tr('ReferenceDataDialog', "No selection"),
                                      g_tr('ReferenceDataDialog', "Please select different account"),
                                      QMessageBox.Ok)
                event.ignore()
                return

            self.setResult(QDialog.Accepted)
            event.accept()


class FOF:
    PERIOD = "period"

    ACCOUNTS = "accounts"
    ASSETS = "assets"
    TRADES = "trades"
    TRANSFERS = "transfers"
    CORP_ACTIONS = "corporate_actions"
    ASSET_PAYMENTS = "asset_payments"
    INCOME_SPENDING = "income_spending"

    ASSET_MONEY = "money"
    ASSET_STOCK = "stock"
    ASSET_ADR = "adr"
    ASSET_ETF = "etf"
    ASSET_BOND = "bond"
    ASSET_FUTURES = "futures"
    ASSET_OPTION = "option"
    ASSET_WARRANT = "warrant"

    ACTION_MERGER = "merger"
    ACTION_SPLIT = "split"
    ACTION_SPINOFF = "spin-off"
    ACTION_SYMBOL_CHANGE = "symbol_change"
    ACTION_STOCK_DIVIDEND = "stock_dividend"

    PAYMENT_DIVIDEND = "dividend"
    PAYMENT_INTEREST = "interest"


class Statement_ImportError(Exception):
    pass


# -----------------------------------------------------------------------------------------------------------------------
class Statement:
    _asset_types = {
        FOF.ASSET_MONEY: PredefinedAsset.Money,
        FOF.ASSET_STOCK: PredefinedAsset.Stock,
        FOF.ASSET_ADR: PredefinedAsset.Stock,
        FOF.ASSET_ETF: PredefinedAsset.ETF,
        FOF.ASSET_BOND: PredefinedAsset.Bond,
        FOF.ASSET_FUTURES: PredefinedAsset.Derivative,
        FOF.ASSET_OPTION: PredefinedAsset.Derivative,
        FOF.ASSET_WARRANT: PredefinedAsset.Derivative,
    }
    _corp_actions = {
        FOF.ACTION_MERGER: CorporateAction.Merger,
        FOF.ACTION_SPLIT: CorporateAction.Split,
        FOF.ACTION_SPINOFF: CorporateAction.SpinOff,
        FOF.ACTION_SYMBOL_CHANGE: CorporateAction.SymbolChange,
        FOF.ACTION_STOCK_DIVIDEND: CorporateAction.StockDividend
    }
    _sources = {
        'NYSE': MarketDataFeed.US,
        'ARCA': MarketDataFeed.US,
        'NASDAQ': MarketDataFeed.US,
        'TSE': MarketDataFeed.CA,
        'SBF': MarketDataFeed.EU,
        'AMEX': MarketDataFeed.US
    }
    
    def __init__(self):
        self._data = {}
        self._last_selected_account = None

    # Loads JSON statement format from file defined by 'filename'
    def load(self, filename: str) -> None:
        self._data = {}
        try:
            with open(filename, 'r') as exchange_file:
                try:
                    self._data = json.load(exchange_file)
                except json.JSONDecodeError:
                    logging.error(g_tr('Statement', "Failed to read JSON from file: ") + filename)
        except Exception as err:
            logging.error(g_tr('Statement', "Failed to read file: ") + str(err))

    # check are assets and accounts from self._data present in database
    # replace IDs in self._data with IDs from database (DB IDs will be negative, initial IDs will be positive)
    def match_db_ids(self, verbal=True):
        self._match_asset_ids(verbal)
        self._match_account_ids()

    # Check and replace IDs for Assets
    def _match_asset_ids(self, verbal):
        for asset in self._data[FOF.ASSETS]:
            isin = asset['isin'] if 'isin' in asset else ''
            reg_code = asset['reg_code'] if 'reg_code' in asset else ''
            name = asset['name'] if 'name' in asset else ''     # FIXME: update isin/reg_code/country in DB if different
            asset_id = JalDB().get_asset_id(asset['symbol'], isin=isin, reg_code=reg_code, name=name, dialog_new=verbal)
            if asset_id:
                old_id, asset['id'] = asset['id'], -asset_id
                self._update_id("asset", old_id, asset_id)
                if asset['type'] == FOF.ASSET_MONEY:
                    self._update_id("currency", old_id, asset_id)

    # Check and replace IDs for Accounts
    def _match_account_ids(self):
        for account in self._data[FOF.ACCOUNTS]:
            account_id = JalDB().find_account(account['number'], -account['currency'])
            if account_id:
                old_id, account['id'] = account['id'], -account_id
                self._update_id("account", old_id, account_id)

    # Replace 'old_value' with 'new_value' in keys 'tag_name' of self._data
    def _update_id(self, tag_name, old_value, new_value):
        for section in self._data:
            if type(self._data[section]) != list:
                continue
            if section == FOF.PERIOD:
                continue   # FIXME Here should be a list of supported sections instead of not supported
            for element in self._data[section]:
                for tag in element:
                    if tag == tag_name:
                        if type(element[tag]) == list:
                            element[tag] = [-new_value if x==old_value else x for x in element[tag]]
                        else:
                            element[tag] = -new_value if element[tag] == old_value else element[tag]

    def import_into_db(self):
        sections = {
            FOF.ASSETS: self._import_assets,
            FOF.ACCOUNTS: self._import_accounts,
            FOF.INCOME_SPENDING: self._import_imcomes_and_spendings,
            FOF.TRANSFERS: self._import_transfers,
            FOF.TRADES: self._import_trades,
            FOF.ASSET_PAYMENTS: self._import_asset_payments,
            FOF.CORP_ACTIONS: self._import_corporate_actions
        }
        
        for section in sections:
            if section in self._data and sections[section]:
                sections[section](self._data[section])
        for section in self._data:
            if section not in sections:
                logging.warning(g_tr("Statement", "Section is not supported: ") + section)  # FIXME here should be a list of sessions to load

        # FIXME This display should be outside of this method
        for account in self._data[FOF.ACCOUNTS]:
            if 'cash_end' in account:
                logging.info(g_tr('Statement', 'Planned cash: ') + f"{account['cash_end']:.2f} " +
                             f"{JalDB().get_asset_name(JalDB().get_account_currency(-account['currency']))}")

    def _import_assets(self, assets):
        for asset in assets:
            if asset['id'] < 0:
                continue
            isin = asset['isin'] if 'isin' in asset else ''
            reg_code = asset['reg_code'] if 'reg_code' in asset else ''
            name = asset['name'] if 'name' in asset else ''
            country_code = asset['country'] if 'country' in asset else ''
            try:
                source = self._sources[asset['exchange']]
            except KeyError:
                source = MarketDataFeed.NA
            asset_id = JalDB().add_asset(asset['symbol'], name, self._asset_types[asset['type']], isin,
                                         data_source=source, reg_code=reg_code, country_code=country_code)
            if asset_id:
                old_id, asset['id'] = asset['id'], -asset_id
                self._update_id("asset", old_id, asset_id)
                if asset['type'] == FOF.ASSET_MONEY:
                    self._update_id("currency", old_id, asset_id)
            else:
                raise Statement_ImportError(g_tr('Statement', "Can't create asset: ") + f"{asset}")
    
    def _import_accounts(self, accounts):
        for account in accounts:
            if account['id'] < 0:
                continue
            if account['currency'] > 0:
                raise Statement_ImportError(g_tr('Statement', "Unmatched currency for account: ") + f"{account}")
            account_id = JalDB().add_account(account['number'], -account['currency'])
            if account_id:
                old_id, account['id'] = account['id'], -account_id
                self._update_id("account", old_id, account_id)
            else:
                raise Statement_ImportError(g_tr('Statement', "Can't create account: ") + f"{account}")
    
    def _import_imcomes_and_spendings(self, actions):
        for action in actions:
            if action['account'] > 0:
                raise Statement_ImportError(g_tr('Statement', "Unmatched account for income/spending: ") + f"{action}")
            if action['peer'] > 0:
                raise Statement_ImportError(g_tr('Statement', "Unmatched peer for income/spending: ") + f"{action}")
            peer = JalDB().get_account_bank(-action['account']) if action['peer'] == 0 else -action['peer']
            if len(action['lines']) != 1:   # FIXME - need support for multilines here
                raise Statement_ImportError(g_tr('Statement', "Unsupported income/spending: ") + f"{action}")
            amount = action['lines'][0]['amount']
            category = -action['lines'][0]['category']
            if category <= 0:
                raise Statement_ImportError(g_tr('Statement', "Unmatched category for income/spending: ") + f"{action}")
            description = action['lines'][0]['description']
            JalDB().add_cash_transaction(-action['account'], peer, action['timestamp'], amount, category, description)
    
    def _import_transfers(self, transfers):
        for transfer in transfers:
            for account in transfer['account']:
                if account > 0:
                    raise Statement_ImportError(g_tr('Statement', "Unmatched account for transfer: ") + f"{transfer}")
            for asset in transfer['asset']:
                if asset > 0:
                    raise Statement_ImportError(g_tr('Statement', "Unmatched asset for transfer: ") + f"{transfer}")
            if transfer['account'][0] == 0 or transfer['account'][1] == 0:
                text = ''
                pair_account = 1
                if transfer['account'][0] == 0:  # Deposit
                    text = g_tr('Statement', "Deposit of ") + f"{transfer['deposit']:.2f} " + \
                           f"{JalDB().get_asset_name(-transfer['asset'][1])} " + \
                           f"@{datetime.utcfromtimestamp(transfer['timestamp']).strftime('%d.%m.%Y')}\n" + \
                           g_tr('Statement', "Select account to withdraw from:")
                    pair_account = transfer['account'][1]
                if transfer['account'][1] == 0:  # Withdrawal
                    text = g_tr('Statement', "Withdrawal of ") + f"{transfer['withdrawal']:.2f} " + \
                           f"{JalDB().get_asset_name(-transfer['asset'][0])} " + \
                           f"@{datetime.utcfromtimestamp(transfer['timestamp']).strftime('%d.%m.%Y')}\n" + \
                           g_tr('Statement', "Select account to deposit to:")
                    pair_account = transfer['account'][0]
                pair_account = self.select_account(text, pair_account, self._last_selected_account)
                if pair_account == 0:
                    raise Statement_ImportError(g_tr('Statement', "Account not selected"))
                self._last_selected_account = pair_account
                if transfer['account'][0] == 0:
                    transfer['account'][0] = -pair_account
                if transfer['account'][1] == 0:
                    transfer['account'][1] = -pair_account

            description = transfer['description'] if 'description' in transfer else ''
            JalDB().add_transfer(transfer['timestamp'], -transfer['account'][0], transfer['withdrawal'],
                                 -transfer['account'][1], transfer['deposit'],
                                 -transfer['account'][2], transfer['fee'], description)

    def _import_trades(self, trades):
        for trade in trades:
            if trade['account'] > 0:
                raise Statement_ImportError(g_tr('Statement', "Unmatched account for trade: ") + f"{trade}")
            if trade['asset'] > 0:
                raise Statement_ImportError(g_tr('Statement', "Unmatched asset for trade: ") + f"{trade}")
            note = trade['note'] if 'note' in trade else ''
            if 'cancelled' in trade and trade['cancelled']:
                JalDB().del_trade(-trade['account'], -trade['asset'], trade['timestamp'], trade['settlement'],
                                  trade['number'], trade['quantity'], trade['price'], trade['fee'])
                continue
            JalDB().add_trade(-trade['account'], -trade['asset'], trade['timestamp'], trade['settlement'],
                              trade['number'], trade['quantity'], trade['price'], trade['fee'], note)

    def _import_asset_payments(self, payments):
        for payment in payments:
            if payment['account'] > 0:
                raise Statement_ImportError(g_tr('Statement', "Unmatched account for payment: ") + f"{payment}")
            if payment['asset'] > 0:
                raise Statement_ImportError(g_tr('Statement', "Unmatched asset for payment: ") + f"{payment}")
            tax = payment['tax'] if 'tax' in payment else 0
            if payment['type'] == FOF.PAYMENT_DIVIDEND:
                if payment['id'] > 0:  # New dividend
                    JalDB().add_dividend(DividendSubtype.Dividend, payment['timestamp'], -payment['account'],
                                         -payment['asset'], payment['amount'], payment['description'], tax=tax)
                else:  # Dividend exists, only tax to be updated
                    JalDB().update_dividend_tax(-payment['id'], payment['tax'])
            elif payment['type'] == FOF.PAYMENT_INTEREST:
                JalDB().add_dividend(DividendSubtype.BondInterest, payment['timestamp'], -payment['account'],
                                     -payment['asset'], payment['amount'], payment['description'], payment['number'],
                                     tax=tax)
            else:
                raise Statement_ImportError(g_tr('Statement', "Unsupported payment type: ") + f"{payment}")

    def _import_corporate_actions(self, actions):
        for action in actions:
            if action['account'] > 0:
                raise Statement_ImportError(g_tr('Statement', "Unmatched account for corporate action: ") + f"{action}")
            if type(action['asset']) == list:
                asset_old = -action['asset'][0]
                asset_new = -action['asset'][1]
            else:
                asset_old = asset_new = -action['asset']
            if asset_old < 0 or asset_new < 0:
                raise Statement_ImportError(g_tr('Statement', "Unmatched asset for corporate action: ") + f"{action}")
            if type(action['quantity']) == list:
                qty_old = action['quantity'][0]
                qty_new = action['quantity'][1]
            else:
                qty_old = -1
                qty_new = action['quantity']
            try:
                action_type = self._corp_actions[action['type']]
            except KeyError:
                raise Statement_ImportError(g_tr('Statement', "Unsupported corporate action: ") + f"{action}")
            JalDB().add_corporate_action(-action['account'], action_type, action['timestamp'], action['number'],
                                         asset_old, qty_old, asset_new, qty_new,
                                         action['cost_basis'], action['description'])

    def select_account(self, text, account_id, recent_account_id=0):
        if "pytest" in sys.modules:
            return 1    # Always return 1st account if we are in testing mode
        else:
            dialog = SelectAccountDialog(text, account_id, recent_account=recent_account_id)
            if dialog.exec_() != QDialog.Accepted:
                return 0
            else:
                return dialog.account_id
