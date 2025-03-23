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

-- terms
-- Course start dates/the start date of the course's term.
CREATE TABLE IF NOT EXISTS terms(
    start_date date NOT NULL UNIQUE ON CONFLICT FAIL
);
CREATE UNIQUE INDEX IF NOT EXISTS term ON terms(start_date);

-- grade_categories
-- Grading categories for courses.
CREATE TABLE IF NOT EXISTS grade_categories(
    category TEXT UNIQUE NOT NULL ON CONFLICT FAIL
);
CREATE UNIQUE INDEX IF NOT EXISTS category ON grade_categories(category);

-- actions
-- Actions for ToDos. Ex. Write, Read, Submit, Take, etc.
CREATE TABLE IF NOT EXISTS actions(
    action TEXT NOT NULL UNIQUE ON CONFLICT FAIL
);
CREATE UNIQUE INDEX IF NOT EXISTS action ON actions(action);

-- course_catalog
-- Table representing the college's course catalog.
CREATE TABLE IF NOT EXISTS course_catalog(
    course_prefix_id INTEGER NOT NULL,
    course_number INTEGER NOT NULL,
    title TEXT NOT NULL,
    credits INTEGER NOT NULL,
    pre_req TEXT,
    description TEXT,
    uid TEXT GENERATE ALWAYS AS
        (CAST(course_prefix_id AS TEXT) ||"-"|| CAST (course_number AS TEXT)) STORED
            UNIQUE ON CONFLICT FAIL,
    FOREIGN KEY (course_prefix_id) REFERENCES course_prefixes(rowid)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS course_code ON course_catalog(course_prefix_id, course_number);

-- courses_taken
-- Table containing classes taken by website user.
CREATE TABLE IF NOT EXISTS courses_taken(
    term_id INTEGER NOT NULL,
    course_catalog_id INTEGER NOT NULL,
    grade TEXT,
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

-- week
-- Table of weeks
CREATE TABLE IF NOT EXISTS weeks(
    course_taken_id INTEGER NOT NULL,
    week INTEGER(1) NOT NULL,
    topic TEXT,
    uid TEXT GENERATE ALWAYS AS
        (CAST(course_taken_id AS TEXT) ||"-"|| CAST (week AS TEXT)) STORED
            UNIQUE ON CONFLICT FAIL,
    FOREIGN KEY (course_taken_id) REFERENCES courses_taken(rowid)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS course_week ON weeks(uid);

-- Course Rubrics
CREATE TABLE IF NOT EXISTS course_rubrics(
    course_taken_id INTEGER NOT NULL,
    grade_category_id INTEGER NOT NULL,
    percent REAL NOT NULL,
    uid TEXT GENERATE ALWAYS AS
        (CAST(course_taken_id AS TEXT) ||"-"|| CAST (grade_category_id AS TEXT)) STORED
            UNIQUE ON CONFLICT FAIL,
    FOREIGN KEY (course_taken_id) REFERENCES courses_taken(rowid)
        ON UPDATE CASCADE
        ON DELETE SET NULL
    FOREIGN KEY (grade_category_id) REFERENCES grade_categories(rowid)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS course_grade_cat ON course_rubrics(uid);

-- ToDos
CREATE TABLE IF NOT EXISTS ToDos (
    week_id INTEGER NOT NULL,
    course_rubric_id INTEGER NOT NULL,
    action_id INTEGER NOT NULL,
    what TEXT NOT NULL,
    due_date TEXT,
    is_done INTEGER DEFAULT 0,
    done_date TEXT,
    grade TEXT,
    uid TEXT GENERATE ALWAYS AS
        (CAST(week_id AS TEXT) ||"-"|| CAST (course_rubric_id AS TEXT)
         ||"-"|| CAST (action_id AS TEXT) ||"-"|| what) STORED
            UNIQUE ON CONFLICT FAIL,
    FOREIGN KEY (course_rubric_id) REFERENCES course_rubrics(rowid)
        ON UPDATE CASCADE
        ON DELETE SET NULL
    FOREIGN KEY (action_id) REFERENCES actions(rowid)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS todo ON ToDos(uid);

-- Tasks
CREATE TABLE IF NOT EXISTS tasks(
    todo_id INTEGER NOT NULL,
    task TEXT NOT NULL,
    details TEXT,
    is_done INTEGER DEFAULT 0,
    done_date TEXT,
    uid TEXT GENERATE ALWAYS AS
        (CAST(todo_id AS TEXT) ||"-"|| task) STORED
            UNIQUE ON CONFLICT FAIL,
    CONSTRAINT uid UNIQUE (todo_id, task)
        ON CONFLICT FAIL,
    FOREIGN KEY (todo_id) REFERENCES ToDos(rowid)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS todo_task ON tasks(todo_id);


CREATE VIEW IF NOT EXISTS syllabus AS
    SELECT
        actions.action,
        ToDos.rowid,
        ToDos.what,
        ToDos.due_date,
        ToDos.is_done,
        ToDos.done_date,
        ToDos.grade,
        course_rubrics.percent,
        weeks.week,
        weeks.topic,
        terms.start_date,
        course_prefixes.prefix,
        course_catalog.course_number,
        course_catalog.title,
        course_catalog.credits,
        grade_categories.category
    FROM
        ToDos
    LEFT JOIN actions
        ON actions.rowid = ToDos.action_id
    LEFT JOIN course_rubrics
        ON course_rubrics.rowid = ToDos.course_rubric_id
    LEFT JOIN weeks
        ON weeks.rowid = ToDos.week_id
    LEFT JOIN courses_taken
        ON courses_taken.rowid = weeks.course_taken_id
    LEFT JOIN terms
        ON terms.rowid = courses_taken.term_id
    LEFT JOIN  course_catalog
        ON course_catalog.rowid = courses_taken.course_catalog_id
    LEFT JOIN course_prefixes
        ON course_prefixes.rowid = course_catalog.course_prefix_id
    LEFT JOIN grade_categories
        ON grade_categories.rowid = course_rubrics.grade_category_id
    ORDER BY terms.start_date;
