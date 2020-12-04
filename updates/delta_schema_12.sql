BEGIN TRANSACTION;
--------------------------------------------------------------------------------
-- Modify trades table to drop 'corp_action_id' column

PRAGMA foreign_keys = 0;

CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                          FROM trades;

DROP TABLE trades;

CREATE TABLE trades (
    id         INTEGER   PRIMARY KEY
                         UNIQUE
                         NOT NULL,
    timestamp  INTEGER   NOT NULL,
    settlement INTEGER   DEFAULT (0),
    number     TEXT (32) DEFAULT (''),
    account_id INTEGER   REFERENCES accounts (id) ON DELETE CASCADE
                                                  ON UPDATE CASCADE
                         NOT NULL,
    asset_id   INTEGER   REFERENCES assets (id) ON DELETE RESTRICT
                                                ON UPDATE CASCADE
                         NOT NULL,
    qty        REAL      NOT NULL
                         DEFAULT (0),
    price      REAL      NOT NULL
                         DEFAULT (0),
    coupon     REAL      DEFAULT (0),
    fee        REAL      DEFAULT (0)
);

INSERT INTO trades (
                       id,
                       timestamp,
                       settlement,
                       number,
                       account_id,
                       asset_id,
                       qty,
                       price,
                       coupon,
                       fee
                   )
                   SELECT id,
                          timestamp,
                          settlement,
                          number,
                          account_id,
                          asset_id,
                          qty,
                          price,
                          coupon,
                          fee
                     FROM sqlitestudio_temp_table;

DROP TABLE sqlitestudio_temp_table;

CREATE TRIGGER trades_after_delete
         AFTER DELETE
            ON trades
      FOR EACH ROW
          WHEN (
    SELECT value
      FROM settings
     WHERE id = 1
)
BEGIN
    DELETE FROM ledger
          WHERE timestamp >= OLD.timestamp;
    DELETE FROM sequence
          WHERE timestamp >= OLD.timestamp;
    DELETE FROM ledger_sums
          WHERE timestamp >= OLD.timestamp;
END;

CREATE TRIGGER trades_after_insert
         AFTER INSERT
            ON trades
      FOR EACH ROW
          WHEN (
    SELECT value
      FROM settings
     WHERE id = 1
)
BEGIN
    DELETE FROM ledger
          WHERE timestamp >= NEW.timestamp;
    DELETE FROM sequence
          WHERE timestamp >= NEW.timestamp;
    DELETE FROM ledger_sums
          WHERE timestamp >= NEW.timestamp;
END;

CREATE TRIGGER trades_after_update
         AFTER UPDATE OF timestamp,
                         account_id,
                         asset_id,
                         qty,
                         price,
                         coupon,
                         fee
            ON trades
      FOR EACH ROW
          WHEN (
    SELECT value
      FROM settings
     WHERE id = 1
)
BEGIN
    DELETE FROM ledger
          WHERE timestamp >= OLD.timestamp OR
                timestamp >= NEW.timestamp;
    DELETE FROM sequence
          WHERE timestamp >= OLD.timestamp OR
                timestamp >= NEW.timestamp;
    DELETE FROM ledger_sums
          WHERE timestamp >= OLD.timestamp OR
                timestamp >= NEW.timestamp;
END;

PRAGMA foreign_keys = 1;

--------------------------------------------------------------------------------
-- Re-create corp_actions table with different usage and structure
DROP TABLE corp_actions;

CREATE TABLE corp_actions (
    id           INTEGER     PRIMARY KEY
                             UNIQUE
                             NOT NULL,
    timestamp    INTEGER     NOT NULL,
    number       TEXT (32)   DEFAULT (''),
    account_id   INTEGER     NOT NULL
                             REFERENCES accounts (id) ON DELETE CASCADE
                                                      ON UPDATE CASCADE,
    type         INTEGER     NOT NULL,
    asset_id     INTEGER     NOT NULL
                             REFERENCES assets (id) ON DELETE RESTRICT
                                                    ON UPDATE CASCADE,
    qty          REAL        NOT NULL,
    asset_id_new INTEGER     REFERENCES assets (id) ON DELETE RESTRICT
                                                    ON UPDATE CASCADE
                             NOT NULL,
    qty_new      REAL        NOT NULL,
    note         TEXT (1024)
);

--------------------------------------------------------------------------------
-- UPDATE TRIGGERS
DROP TRIGGER IF EXISTS corp_after_delete;
CREATE TRIGGER corp_after_delete
         AFTER DELETE
            ON corp_actions
      FOR EACH ROW
BEGIN
    DELETE FROM ledger
          WHERE timestamp >= OLD.timestamp;
    DELETE FROM sequence
          WHERE timestamp >= OLD.timestamp;
    DELETE FROM ledger_sums
          WHERE timestamp >= OLD.timestamp;
END;

DROP TRIGGER IF EXISTS corp_after_insert;
CREATE TRIGGER corp_after_insert
         AFTER INSERT
            ON corp_actions
      FOR EACH ROW
BEGIN
    DELETE FROM ledger
          WHERE timestamp >= NEW.timestamp;
    DELETE FROM sequence
          WHERE timestamp >= NEW.timestamp;
    DELETE FROM ledger_sums
          WHERE timestamp >= NEW.timestamp;
END;

DROP TRIGGER IF EXISTS corp_after_update;
CREATE TRIGGER corp_after_update
         AFTER UPDATE OF timestamp,
                         account_id,
                         type,
                         asset_id,
                         qty,
                         asset_id_new,
                         qty_new
            ON corp_actions
      FOR EACH ROW
BEGIN
    DELETE FROM ledger
          WHERE timestamp >= OLD.timestamp OR
                timestamp >= NEW.timestamp;
    DELETE FROM sequence
          WHERE timestamp >= OLD.timestamp OR
                timestamp >= NEW.timestamp;
    DELETE FROM ledger_sums
          WHERE timestamp >= OLD.timestamp OR
                timestamp >= NEW.timestamp;
END;

--------------------------------------------------------------------------------
-- Update other triggers to remove conditions
DROP TRIGGER IF EXISTS keep_predefined_categories;
CREATE TRIGGER keep_predefined_categories
        BEFORE DELETE
            ON categories
      FOR EACH ROW
          WHEN OLD.special = 1
BEGIN
    SELECT RAISE(ABORT, "Can't delete predefinded category");
END;

DROP TRIGGER IF EXISTS actions_after_delete;
CREATE TRIGGER actions_after_delete
         AFTER DELETE
            ON actions
      FOR EACH ROW
BEGIN
    DELETE FROM action_details
          WHERE pid = OLD.id;
    DELETE FROM ledger
          WHERE timestamp >= OLD.timestamp;
    DELETE FROM sequence
          WHERE timestamp >= OLD.timestamp;
    DELETE FROM ledger_sums
          WHERE timestamp >= OLD.timestamp;
END;

DROP TRIGGER IF EXISTS actions_after_insert;
CREATE TRIGGER actions_after_insert
         AFTER INSERT
            ON actions
      FOR EACH ROW
BEGIN
    DELETE FROM ledger
          WHERE timestamp >= NEW.timestamp;
    DELETE FROM sequence
          WHERE timestamp >= NEW.timestamp;
    DELETE FROM ledger_sums
          WHERE timestamp >= NEW.timestamp;
END;

DROP TRIGGER IF EXISTS actions_after_update;
CREATE TRIGGER actions_after_update
         AFTER UPDATE OF timestamp,
                         account_id,
                         peer_id
            ON actions
      FOR EACH ROW
BEGIN
    DELETE FROM ledger
          WHERE timestamp >= OLD.timestamp OR
                timestamp >= NEW.timestamp;
    DELETE FROM sequence
          WHERE timestamp >= OLD.timestamp OR
                timestamp >= NEW.timestamp;
    DELETE FROM ledger_sums
          WHERE timestamp >= OLD.timestamp OR
                timestamp >= NEW.timestamp;
END;

DROP TRIGGER IF EXISTS dividends_after_delete;
CREATE TRIGGER dividends_after_delete
         AFTER DELETE
            ON dividends
      FOR EACH ROW
BEGIN
    DELETE FROM ledger
          WHERE timestamp >= OLD.timestamp;
    DELETE FROM sequence
          WHERE timestamp >= OLD.timestamp;
    DELETE FROM ledger_sums
          WHERE timestamp >= OLD.timestamp;
END;

DROP TRIGGER IF EXISTS dividends_after_insert;
CREATE TRIGGER dividends_after_insert
         AFTER INSERT
            ON dividends
      FOR EACH ROW
BEGIN
    DELETE FROM ledger
          WHERE timestamp >= NEW.timestamp;
    DELETE FROM sequence
          WHERE timestamp >= NEW.timestamp;
    DELETE FROM ledger_sums
          WHERE timestamp >= NEW.timestamp;
END;

DROP TRIGGER IF EXISTS dividends_after_update;
CREATE TRIGGER dividends_after_update
         AFTER UPDATE OF timestamp,
                         account_id,
                         asset_id,
                         sum,
                         sum_tax
            ON dividends
      FOR EACH ROW
BEGIN
    DELETE FROM ledger
          WHERE timestamp >= OLD.timestamp OR
                timestamp >= NEW.timestamp;
    DELETE FROM sequence
          WHERE timestamp >= OLD.timestamp OR
                timestamp >= NEW.timestamp;
    DELETE FROM ledger_sums
          WHERE timestamp >= OLD.timestamp OR
                timestamp >= NEW.timestamp;
END;

DROP TRIGGER IF EXISTS trades_after_delete;
CREATE TRIGGER trades_after_delete
         AFTER DELETE
            ON trades
      FOR EACH ROW
BEGIN
    DELETE FROM ledger
          WHERE timestamp >= OLD.timestamp;
    DELETE FROM sequence
          WHERE timestamp >= OLD.timestamp;
    DELETE FROM ledger_sums
          WHERE timestamp >= OLD.timestamp;
END;

DROP TRIGGER IF EXISTS trades_after_insert;
CREATE TRIGGER trades_after_insert
         AFTER INSERT
            ON trades
      FOR EACH ROW
BEGIN
    DELETE FROM ledger
          WHERE timestamp >= NEW.timestamp;
    DELETE FROM sequence
          WHERE timestamp >= NEW.timestamp;
    DELETE FROM ledger_sums
          WHERE timestamp >= NEW.timestamp;
END;

DROP TRIGGER IF EXISTS trades_after_update;
CREATE TRIGGER trades_after_update
         AFTER UPDATE OF timestamp,
                         account_id,
                         asset_id,
                         qty,
                         price,
                         coupon,
                         fee
            ON trades
      FOR EACH ROW
BEGIN
    DELETE FROM ledger
          WHERE timestamp >= OLD.timestamp OR
                timestamp >= NEW.timestamp;
    DELETE FROM sequence
          WHERE timestamp >= OLD.timestamp OR
                timestamp >= NEW.timestamp;
    DELETE FROM ledger_sums
          WHERE timestamp >= OLD.timestamp OR
                timestamp >= NEW.timestamp;
END;

DROP TRIGGER IF EXISTS transfers_after_delete;
CREATE TRIGGER transfers_after_delete
         AFTER DELETE
            ON transfers
      FOR EACH ROW
BEGIN
    DELETE FROM ledger
          WHERE timestamp >= OLD.timestamp;
    DELETE FROM sequence
          WHERE timestamp >= OLD.timestamp;
    DELETE FROM ledger_sums
          WHERE timestamp >= OLD.timestamp;
END;

DROP TRIGGER IF EXISTS transfers_after_insert;
CREATE TRIGGER transfers_after_insert
         AFTER INSERT
            ON transfers
      FOR EACH ROW
BEGIN
    DELETE FROM ledger
          WHERE timestamp >= NEW.timestamp;
    DELETE FROM sequence
          WHERE timestamp >= NEW.timestamp;
    DELETE FROM ledger_sums
          WHERE timestamp >= NEW.timestamp;
END;

DROP TRIGGER IF EXISTS transfers_after_update;
CREATE TRIGGER transfers_after_update
         AFTER UPDATE OF timestamp,
                         type,
                         account_id,
                         amount
            ON transfers
      FOR EACH ROW
BEGIN
    DELETE FROM ledger
          WHERE timestamp >= OLD.timestamp OR
                timestamp >= NEW.timestamp;
    DELETE FROM sequence
          WHERE timestamp >= OLD.timestamp OR
                timestamp >= NEW.timestamp;
    DELETE FROM ledger_sums
          WHERE timestamp >= OLD.timestamp OR
                timestamp >= NEW.timestamp;
END;
--------------------------------------------------------------------------------
-- UPDATE VIEWS
DROP VIEW all_operations;

CREATE VIEW all_operations AS
    SELECT m.type,
           m.id,
           m.timestamp,
           m.account_id,
           a.name AS account,
           m.num_peer,
           m.asset_id,
           s.name AS asset,
           s.full_name AS asset_name,
           m.note,
           m.note2,
           m.amount,
           m.qty_trid,
           m.price,
           m.fee_tax,
           coalesce(money.sum_amount, 0) + coalesce(debt.sum_amount, 0) AS t_amount,
           m.t_qty,
           c.name AS currency,
           CASE WHEN m.timestamp <= a.reconciled_on THEN 1 ELSE 0 END AS reconciled
      FROM (
               SELECT 1 AS type,
                      o.id,
                      timestamp,
                      p.name AS num_peer,
                      account_id,
                      sum(d.sum) AS amount,
                      o.alt_currency_id AS asset_id,
                      NULL AS qty_trid,
                      sum(d.alt_sum) AS price,
                      NULL AS fee_tax,
                      NULL AS t_qty,
                      NULL AS note,
                      NULL AS note2,
                      o.id AS operation_id
                 FROM actions AS o
                      LEFT JOIN
                      agents AS p ON o.peer_id = p.id
                      LEFT JOIN
                      action_details AS d ON o.id = d.pid
                GROUP BY o.id
               UNION ALL
               SELECT 2 AS type,
                      d.id,
                      d.timestamp,
                      d.number AS num_peer,
                      d.account_id,
                      d.sum AS amount,
                      d.asset_id,
                      SUM(coalesce(l.amount, 0) ) AS qty_trid,
                      NULL AS price,
                      d.sum_tax AS fee_tax,
                      NULL AS t_qty,
                      d.note AS note,
                      c.name AS note2,
                      d.id AS operation_id
                 FROM dividends AS d
                      LEFT JOIN
                      ledger AS l ON d.asset_id = l.asset_id AND
                                     d.account_id = l.account_id AND
                                     l.book_account = 4 AND
                                     l.timestamp <= d.timestamp
                      LEFT JOIN
                      countries AS c ON d.tax_country_id = c.id
                GROUP BY d.id
               UNION ALL
               SELECT 3 AS type,
                      t.id,
                      t.timestamp,
                      t.number AS num_peer,
                      t.account_id,
-                     (t.price * t.qty) AS amount,
                      t.asset_id,
                      t.qty AS qty_trid,
                      t.price AS price,
                      t.fee AS fee_tax,
                      l.sum_amount AS t_qty,
                      NULL AS note,
                      NULL AS note2,
                      t.id AS operation_id
                 FROM trades AS t
                      LEFT JOIN
                      sequence AS q ON q.type = 3 AND
                                       t.id = q.operation_id
                      LEFT JOIN
                      ledger_sums AS l ON l.sid = q.id AND
                                          l.book_account = 4
               UNION ALL
               SELECT 4 AS type,
                      r.tid,
                      r.timestamp,
                      c.name AS num_peer,
                      r.account_id,
                      r.amount,
                      NULL AS asset_id,
                      r.type AS qty_trid,
                      r.rate AS price,
                      NULL AS fee_tax,
                      NULL AS t_qty,
                      n.note,
                      a.name AS note2,
                      r.id AS operation_id
                 FROM transfers AS r
                      LEFT JOIN
                      transfer_notes AS n ON r.tid = n.tid
                      LEFT JOIN
                      transfers AS tr ON r.tid = tr.tid AND
                                         r.type = -tr.type
                      LEFT JOIN
                      accounts AS a ON a.id = tr.account_id
                      LEFT JOIN
                      assets AS c ON c.id = a.currency_id
               UNION ALL
               SELECT 5 AS type,
                      ca.id,
                      ca.timestamp,
                      ca.number AS num_peer,
                      ca.account_id,
                      ca.qty AS amount,
                      ca.asset_id,
                      ca.qty_new AS qty_trid,
                      NULL AS price,
                      ca.type AS fee_tax,
                      NULL AS t_qty,
                      a.name AS note,
                      a.full_name AS note2,
                      ca.id AS operation_id
                 FROM corp_actions AS ca
                      LEFT JOIN assets AS a ON ca.asset_id_new=a.id
               ORDER BY timestamp
           )
           AS m
           LEFT JOIN
           accounts AS a ON m.account_id = a.id
           LEFT JOIN
           assets AS s ON m.asset_id = s.id
           LEFT JOIN
           assets AS c ON a.currency_id = c.id
           LEFT JOIN
           sequence AS q ON m.type = q.type AND
                            m.operation_id = q.operation_id
           LEFT JOIN
           ledger_sums AS money ON money.sid = q.id AND
                                   money.book_account = 3
           LEFT JOIN
           ledger_sums AS debt ON debt.sid = q.id AND
                                  debt.book_account = 5;


--------------------------------------------------------------------------------
DROP VIEW all_transactions;

CREATE VIEW all_transactions AS
    SELECT at.*,
           a.currency_id AS currency
      FROM (
               SELECT 1 AS type,
                      a.id,
                      a.timestamp,
                      CASE WHEN SUM(d.sum) < 0 THEN COUNT(d.sum) ELSE -COUNT(d.sum) END AS subtype,
                      a.account_id AS account,
                      NULL AS asset,
                      SUM(d.sum) AS amount,
                      d.category_id AS price_category,
                      a.peer_id AS coupon_peer,
                      d.tag_id AS fee_tax_tag
                 FROM actions AS a
                      LEFT JOIN
                      action_details AS d ON a.id = d.pid
                GROUP BY a.id
               UNION ALL
               SELECT 2 AS type,
                      id,
                      timestamp,
                      0 AS subtype,
                      account_id AS account,
                      asset_id AS asset,
                      sum AS amount,
                      NULL AS price_category,
                      NULL AS coupon_peer,
                      sum_tax AS fee_tax_tag
                 FROM dividends
               UNION ALL
               SELECT 4 AS type,
                      id,
                      timestamp,
                      type AS subtype,
                      account_id AS account,
                      NULL AS asset,
                      amount,
                      NULL AS price_category,
                      NULL AS coupon_peer,
                      NULL AS fee_tax_tag
                 FROM transfers
               UNION ALL
               SELECT 3 AS type,
                      t.id,
                      t.timestamp,
                      iif(t.qty < 0, -1, 1) AS subtype,
                      t.account_id AS account,
                      t.asset_id AS asset,
                      t.qty AS amount,
                      t.price AS price_category,
                      t.coupon AS coupon_peer,
                      t.fee AS fee_tax_tag
                 FROM trades AS t
               UNION ALL
               SELECT 5 AS type,
                      a.id,
                      a.timestamp,
                      a.type AS subtype,
                      a.account_id AS account,
                      a.asset_id AS asset,
                      a.qty AS amount,
                      a.qty_new AS price_category,
                      a.asset_id_new AS coupon_peer,
                      NULL AS fee_tax_tag
                  FROM corp_actions AS a
               ORDER BY timestamp,
                        type,
                        subtype
           )
           AS at
           LEFT JOIN
           accounts AS a ON at.account = a.id;
--------------------------------------------------------------------------------
-- Set new DB schema version
UPDATE settings SET value=12 WHERE name='SchemaVersion';

COMMIT;
