from jal.constants import Setup
import sqlite3
import pandas as pd
import math
import logging

from PySide2.QtWidgets import QFileDialog, QMessageBox
from jal.ui_custom.helpers import g_tr

# ------------------------------------------------------------------------------
class JalBackup:
    backup_list = ["settings", "tags", "categories", "agents", "assets", "accounts", "countries", "corp_actions",
                   "dividends", "trades", "actions", "action_details", "transfers", "transfer_notes", "quotes",
                   "map_peer", "map_category"]

    def __init__(self, parent, db_file):
        self.parent = parent
        self.file = db_file

    def clean_db(self):
        db = sqlite3.connect(self.file)
        cursor = db.cursor()

        cursor.executescript("DELETE FROM ledger;"
                             "DELETE FROM ledger_sums;"
                             "DELETE FROM sequence;")
        db.commit()

        cursor.execute("DROP TRIGGER IF EXISTS keep_predefined_categories")
        for table in JalBackup.backup_list:
            cursor.execute(f"DELETE FROM {table}")
        db.commit()

        logging.info(g_tr('', "DB cleanup was completed"))
        db.close()

    def create(self):
        backup_directory = QFileDialog.getExistingDirectory(self.parent,
                                                            g_tr('JalBackup', "Select directory to save backup"))
        if not backup_directory:
            return

        db = sqlite3.connect(self.file)

        for table in JalBackup.backup_list:
            data = pd.read_sql_query(f"SELECT * FROM {table}", db)
            data.to_csv(f"{backup_directory}/{table}.csv", sep="|", header=True, index=False)

        db.close()
        logging.info(g_tr('', "Backup saved in: ") + backup_directory)

    def restore(self):
        restore_directory = QFileDialog.getExistingDirectory(self.parent,
                                                             g_tr('JalBackup', "Select directory to restore from"))
        if not restore_directory:
            return
        self.parent.closeDatabase()
        self.clean_db()

        db = sqlite3.connect(self.file)
        cursor = db.cursor()
        for table in JalBackup.backup_list:
            data = pd.read_csv(f"{restore_directory}/{table}.csv", sep='|', keep_default_na=False)
            for column in data:
                if data[column].dtype == 'float64':  # Correct possible mistakes due to float data type
                    if table == 'transfers' and column == 'rate':  # But rate is calculated value with arbitrary precision
                        continue
                    data[column] = data[column].round(int(-math.log10(Setup.CALC_TOLERANCE)))
            data.to_sql(name=table, con=db, if_exists='append', index=False, chunksize=100)

        cursor.execute("CREATE TRIGGER keep_predefined_categories "
                       "BEFORE DELETE ON categories FOR EACH ROW WHEN OLD.special = 1 "
                       "BEGIN SELECT RAISE(ABORT, \"Can't delete predefined category\"); END;")
        db.commit()
        db.close()
        logging.info(g_tr('', "Backup restored from: ") + restore_directory + g_tr('', " into ") + self.file)

        QMessageBox().information(self.parent, g_tr('JalBackup', "Data restored"),
                                  g_tr('JalBackup', "Database was loaded from the backup.\n") +
                                  g_tr('JalBackup', "You should restart application to apply changes\n"
                                                    "Application will be terminated now"),
                                  QMessageBox.Ok)
        self.parent.close()

