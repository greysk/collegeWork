CREATE TABLE users (
    PRIMARY KEY(id)
    id       INTEGER,
    username TEXT    NOT NULL,
    hash     TEXT    NOT NULL,
    cash     NUMERIC NOT NULL   DEFAULT 10000.00,
);
CREATE UNIQUE INDEX username ON users (username);
