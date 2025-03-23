-- purchases
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    share TEXT NOT NULL,
    share_count INTEGER NOT NULL,
    share_price REAL NOT NULL,
    dt TEXT NOT NULL,
    uid TEXT GENERATE ALWAYS AS
        (CAST(user_id AS TEXT) ||"-"|| dt) STORED
            UNIQUE ON CONFLICT FAIL
    );
CREATE UNIQUE INDEX IF NOT EXISTS uid ON transactions(uid);
CREATE INDEX IF NOT EXISTS user_id ON transactions(user_id);
CREATE INDEX IF NOT EXISTS share ON transactions(share);
