CREATE TABLE IF NOT EXISTS req_categories(
    category TEXT    NOT NULL UNIQUE ON CONFLICT FAIL,
    credits  INTEGER NOT NULL
);

INSERT OR IGNORE INTO req_categories
VALUES ("general education", 41),
       ("core", 50),
       ("electives", 29);

CREATE TABLE IF NOT EXISTS gened_categories(
    category         TEXT    NOT NULL UNIQUE ON CONFLICT FAIL,
    credits_required INTEGER NOT NULL,
    req_category_id  INTEGER NOT NULL,
    FOREIGN KEY (req_category_id)
     REFERENCES req_categories(rowid)
      ON UPDATE CASCADE
      ON DELETE SET NULL
);

INSERT OR IGNORE INTO gened_categories
VALUES ("english", 6, 1),
       ("communication", 3, 1),
       ("computer science", 6, 1),
       ("math", 13, 1),
       ("natural/physical science", 4, 1),
       ("humanities and fine arts", 3, 1),
       ("social sciences/behavioral sciences", 6, 1);

CREATE TABLE IF NOT EXISTS elective_categories(
    category         TEXT    NOT NULL,
    level            INTEGER NOT NULL,
    credits_required INTEGER NOT NULL,
    req_category_id  INTEGER NOT NULL,
    uid TEXT GENERATE ALWAYS AS (category || CAST (level AS TEXT)) STORED
      UNIQUE ON CONFLICT FAIL
    FOREIGN KEY (req_category_id)
     REFERENCES req_categories(rowid)
      ON UPDATE CASCADE
      ON DELETE SET NULL
);

INSERT OR IGNORE INTO elective_categories
VALUES ("gened", 0, 3, 1),
       ("CS", 3, 4, 2),
       ("open", 1, 15, 3),
       ("open", 3, 3, 3);


CREATE TABLE IF NOT EXISTS compsci_bs_courses(
    req_categories_id INTEGER NOT NULL,
    sub_category_id   INTEGER NOT NULL,
);
