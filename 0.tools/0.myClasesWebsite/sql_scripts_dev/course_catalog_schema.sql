-- Create database for My Classes Website.
PRAGMA foreign_keys = ON;

-- course_prefixes
-- Course catalog prefixes. For example, if course catalog code is
-- CS### for a Computer Science class, prefix is CS and subject is
-- Computer Science.
CREATE TABLE IF NOT EXISTS course_prefixes(
    prefix TEXT NOT NULL UNIQUE ON CONFLICT FAIL,
    subject TEXT NOT NULL UNIQUE ON CONFLICT FAIL
);
CREATE UNIQUE INDEX IF NOT EXISTS prefix ON course_prefixes(prefix);

-- Add all course prefixes to the course_prefix table
INSERT OR IGNORE INTO course_prefixes(prefix, subject)
VALUES ('ACC','Accounting'),
       ('AH','Allied Heath'),
       ('AR','Art'),
       ('BIO','Biological Science'),
       ('BMA','Business Math'),
       ('BUS','Business'),
       ('CA', 'College of Hummanities and Social Sciences'),
       ('CH','Chemistry'),
       ('CJ','Criminal Justice'),
       ('CO','Communication'),
       ('CS','Computer Science'),
       ('CT','Computer Engineering Technology'),
       ('ECN','Economics'),
       ('EL','Elective'),
       ('EMT','Engineering Management Technology'),
       ('EN','English'),
       ('ENT','Entrepreneurship'),
       ('ET','Electronics Engineering'),
       ('ETH','Ethnics'),
       ('FIN','Finance'),
       ('GP','Government and Politics'),
       ('GS','General Science'),
       ('GU','Grantham University'),
       ('HP','Health Professionals'),
       ('HRM','Human Resource Management/HPI'),
       ('HS','History'),
       ('HSN','Nursing and Health Professionals'),
       ('HU','Humanities'),
       ('ID','Interdisciplinary'),
       ('IS','Information Systems'),
       ('INT','International/Global'),
       ('IT','Information Technology'),
       ('LAW','Law'),
       ('LD','Leadership'),
       ('LOG','Logistics'),
       ('MA','Mathematics'),
       ('MGT','Management/HRM/HPI'),
       ('MIL','Military'),
       ('MKG','Marketing'),
       ('NUR','Nursing'),
       ('PA','Public Adminstration'),
       ('PH','Physics'),
       ('PL','Philosophy'),
       ('PLS','Paralegal Studies'),
       ('PRJ','Project Management'),
       ('PS','Psychology'),
       ('RCH','Quantitative/Qualitative/Research'),
       ('SO','Sociology'),
       ('SS','Social Science');

-- course_catalog
-- Table representing the college's course catalog.
CREATE TABLE IF NOT EXISTS course_catalog(
    course_prefix_id INTEGER NOT NULL,  -- Foreign Key to course_prefix
    course_number INTEGER NOT NULL,  -- The course number
    title TEXT NOT NULL,  -- Course title
    credits INTEGER NOT NULL,  -- Number of quarter credits for class
    prereq TEXT,  -- Any pre-requisite classes
    description TEXT,  -- The course description
    uid TEXT GENERATE ALWAYS AS  -- Ensure unique course prefix and course id
        (CAST(course_prefix_id AS TEXT) ||"-"|| CAST (course_number AS TEXT)) STORED
            UNIQUE ON CONFLICT FAIL,
    FOREIGN KEY (course_prefix_id) REFERENCES course_prefixes(rowid)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS course_code ON course_catalog(course_prefix_id, course_number);
