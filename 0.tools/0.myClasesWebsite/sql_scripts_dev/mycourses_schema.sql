-- Create database for My Classes Website.
PRAGMA foreign_keys = ON;

-- terms
-- Course start dates/the start date of the course's term.
CREATE TABLE IF NOT EXISTS terms(
    start_date date NOT NULL UNIQUE ON CONFLICT FAIL
);
CREATE UNIQUE INDEX IF NOT EXISTS start_date ON terms(start_date);

-- Add base/start term
INSERT INTO terms VALUES('2022-01-12');
INSERT INTO terms VALUES('2022-03-09');

-- courses_taken
-- Table containing classes taken by website user.
CREATE TABLE IF NOT EXISTS courses_taken(
    term_id INTEGER NOT NULL,  -- Foreign key to terms
    course_catalog_id INTEGER NOT NULL, -- Foreign key to course_catalog
    grade TEXT,  -- Grade
    uid TEXT GENERATE ALWAYS AS
        (CAST(term_id AS TEXT) ||"-"|| CAST (course_catalog_id AS TEXT)) STORED
            UNIQUE ON CONFLICT FAIL,
    FOREIGN KEY (term_id) REFERENCES terms(rowid)
        ON UPDATE CASCADE
        ON DELETE SET NULL
    FOREIGN KEY (course_catalog_id) REFERENCES course_catalog(rowid)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS course_term ON courses_taken(uid);
