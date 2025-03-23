-- Create database for My Classes Website.
PRAGMA foreign_keys = ON;

-- course_prefixes
-- Course catalog prefixes. For example, if course catalog code is
-- CS### for a Computer Science class, prefix is CS and subject is
-- Computer Science.
CREATE TABLE IF NOT EXISTS course_prefixes (
    PRIMARY KEY (prefix),
    prefix  TEXT    NOT NULL    UNIQUE ON CONFLICT FAIL,
    subject TEXT    NOT NULL    UNIQUE ON CONFLICT FAIL
);
CREATE UNIQUE INDEX IF NOT EXISTS prefix ON course_prefixes(prefix);

-- course_catalog
-- Table representing the college's course catalog.
CREATE TABLE IF NOT EXISTS course_catalog (
    PRIMARY KEY (course_code),
    course_prefix  TEXT    NOT NULL,  -- Foreign Key to course_prefix
    course_number  INTEGER NOT NULL,  -- The course number
    title          TEXT    NOT NULL,  -- Course title
    credits        INTEGER NOT NULL,  -- Number of quarter credits for class
    description    TEXT,              -- The course description
    course_code    TEXT    GENERATE ALWAYS AS  -- Ensure unique course code
                                     (   CAST(course_prefix_id AS TEXT)
                                      || CAST (course_number AS TEXT)) STORED
                             UNIQUE ON CONFLICT FAIL,
    FOREIGN KEY (course_prefix_id) REFERENCES course_prefixes(rowid)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS course_code ON course_catalog(course_prefix_id, course_number);

-- prerequisite
-- Table representing course prerequisites
CREATE TABLE IF NOT EXISTS prerequisite(
    course_code  TEXT  NOT NULL,
    prerequisite TEXT,
    FOREIGN KEY (course_code)  REFERENCES course_catalog(course_code)
    FOREIGN KEY (prerequisite) REFERENCES course_catalog(course_code)
)
