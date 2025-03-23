"""
inits.py
Author: Graeson Thomas
Last modified: 2022-01-19

Contains interfaces to college.db for use with app.py.

Overall goal is to create a student planner to track classes
and course work.
"""
# [ ] Update database classes to be more useful.
#           Currently, are mostly for 1 row item.
import datetime
from enum import Enum, unique
import json
from pathlib import Path
import re
import sqlite3

FILE_DIR: Path = Path(__file__).parent


def _get_db() -> sqlite3.Connection:
    """Create database connection."""
    conn = sqlite3.connect(
        FILE_DIR / 'dev_college.db',
        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    return conn


def query_db(query: str, args: tuple = (), one: bool = False
             ) -> list[sqlite3.Row]:
    """Query database."""
    cur = _get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return (rows[0] if rows else None) if one else rows


def init_db(script: str | Path) -> None:
    """Create database from sql scripts."""
    with _get_db() as conn:
        with open(script, mode='r') as f:
            conn.executescript(f.read())
        conn.commit()
    conn.close()
    return None


for database in Path(FILE_DIR / 'sql_scripts').iterdir():
    init_db(database)


def get_catalog_pg(file: str | Path):
    """Create dictionaries for each course on a json catalog page.

    This script was written to parse a json file that was created
    from a course catalog pdf using PyMuPDF.
        (https://pymupdf.readthedocs.io/en/latest/index.html)


    Args:
        file (str | Path): The path to a json file of one catalog page.

    General structure of JSON file:

        `page['blocks'] -> list[dict]`
            : Each list item is a block on the page.
            : Each page has multiple blocks.
        `block['lines'] -> list[dict]`
            : Each list item is a line in a block.
            : Some blocks have multiple lines.
        `line['spans'] -> list[dict]`
            : Each list item is a span in a line.
            : Some lines have multiple spans.
        `span['text'] -> list[dict]`
            : Contains text from the page. The data extracted by this function.
            : Each span contains one text.

    Algorithm:
    1. Skip blocks[0] and blocks[1] containing the page title, headers/footers.
    2. Loop over the remaining blocks 2 at a time until the end of the page.
    3. If the first block of the pair has a first line with only 1 span in it,
       skip this pair and go to step 2. (This pair contains a note on the
       page.) Otherwise, go to step 4.
    4. From the first block in the pair, obtain the course code, title and
       credits.
    3. From the second block of the pair, get the course pre-requisites and
       description.
    4. Repeat steps 3 - 4 until there are no more blocks remaining.
    """
    # Load page into memory from JSON file.
    with open(file, 'r') as f:
        page = json.loads(f.read().strip())

    # Declare variable to hold a dictionary for each course's details.
    catalog_page: list[dict] = []

    # Obtain all but the first two page blocks.
    blocks: list = page['blocks'][2:]

    # Loop over the remaining blocks in the page two at a time.
    for i in range(2, len(blocks), 2):
        # Obtain the lines for blockA and B of the pair.
        blockA_lines: list[dict] = blocks[i]['lines']
        # If page contains a note, there will be an uneven number of blocks.
        try:
            blockB_lines: list[dict] = blocks[i+1]['lines']
        except IndexError:
            # Skip the note and go to the next block if any remain.
            continue

        # Get the course title and credits. If the title is long, it will
        # affect the location of the course credits.
        if len(blockA_lines) < 3:  # Title is only 1 span long.
            # Get title from the first line's second span.
            title = blockA_lines[0]['spans'][1]['text'].strip()
            # Get credits from the second line's only span.
            credits = blockA_lines[1]['spans'][0]['text'].replace('CREDITS', ''
                                                                  ).strip()
        else:  # Title is 2 spans long.
            # Get title from the first line's second span of first line and
            # from the second line's only span.
            title = ' '.join([blockA_lines[0]['spans'][1]['text'].strip(),
                              blockA_lines[1]['spans'][0]['text'].strip()])
            # Get the credits from the third line's only span.
            credits = int(blockA_lines[2]['spans'][0]['text'].replace(
                            'CREDITS', '').strip())

        # Add a dictionary of the course details to the catalog_page list.
        catalog_page.append(
            {
                'code': blockA_lines[0]['spans'][0]['text'].strip(),
                'title': title,
                'credits': int(credits),
                # Pre-requisites are in the first line of the blockB.
                'prereqs': blockB_lines[0]['spans'][0]['text'].replace(
                                'PREREQUISITES: ', '').replace(
                                    'AND', '&').replace('OR', '|').strip(),
                # Description is in the rest of lines in blockB.
                'description': ' '.join([line['spans'][0]['text'].strip()
                                         for line in blockB_lines[1:]])
            })
    return catalog_page


def add_courses_to_catalog():
    "Add all course catalog pages to database."

    files = tuple((FILE_DIR / 'course_catalog').iterdir())
    pattern = re.compile(r'(\w?\w\w)(\d\d\d\w?)')

    conn = _get_db()
    cur = conn.cursor()

    for file in files:
        catalog_page = get_catalog_pg(file)
        for course in catalog_page:
            course_details = list(course.values())
            cat_code = course_details[0]
            match = pattern.match(course_details.pop(0))
            if not match:
                conn.commit()
                conn.close
                print(f'No course prefix found in. {cat_code}')
                return None
            cur.execute('SELECT rowid FROM course_prefixes WHERE prefix=?;',
                        [match.group(1)])
            prefix_id = cur.fetchone()
            if prefix_id is None:
                conn.commit()
                conn.close
                print(f'No prefix id match for {match.group(1)}')
                return None
            course_details.insert(0, prefix_id[0])
            course_details.insert(1, match.group(2))
            cur.execute('''INSERT OR IGNORE INTO course_catalog(
                                course_prefix_id, course_number,
                                title, credits, pre_req, description
                            )
                            VALUES(?, ?, ?, ?, ?, ?)''', course_details)
            conn.commit()
    conn.close()


class CoursePrefix():
    def __init__(self, course_prefix: str, subject: str = None) -> None:
        self.prefix = course_prefix
        self.subject = subject
        if subject:
            try:
                self._insert
            except sqlite3.IntegrityError:
                pass

    @property
    def _insert(self) -> None:
        # Insert new subject into subjects table in database.
        with _get_db() as conn:
            conn.execute(
                'INSERT INTO course_prefixes (prefix, subject) VALUES (?, ?);',
                [self.prefix, self.subject])
        conn.close()

    @property
    def rowid(self) -> int:
        """Obtain a subject's id from database."""
        with _get_db() as conn:
            cur = conn.cursor()
            cur.execute(
                '''SELECT rowid FROM course_prefixes WHERE prefix=?;''',
                [self.prefix])
            prefix_id: list = cur.fetchone()
        conn.close()
        return prefix_id[0]


class Term():
    def __init__(self, start_date: datetime.date = None,
                 *, year: int = None, month: int = None, day: int = None,
                 ) -> None:
        # Check arguments and convert keyword arguments to datetime.date.
        date_parts = (year, month, day)
        if start_date:
            self.date = start_date
        elif all(date_parts):
            self.date = datetime.date(*date_parts)
        else:
            raise Exception('Either start_date must be provided,'
                            ' or year, month, and day must be provided.')
        # Insert term into table if not already in table.
        try:
            self._insert
        except sqlite3.IntegrityError:
            pass

    @property
    def _insert(self) -> None:
        """Add term start date to terms table."""
        # Insert new term into terms table.
        with _get_db() as conn:
            conn.execute(
                'INSERT INTO terms(start_date) VALUES (?);',
                [self.date])
        conn.close()
        return None

    @property
    def rowid(self) -> int:
        """Obtain the rowid for the term matching start_date."""
        with _get_db() as conn:
            cur = conn.cursor()
            cur.execute('SELECT rowid FROM terms WHERE start_date=date(?);',
                        [self.date])
            term_id: list = cur.fetchone()
        conn.close()
        return term_id[0]


class GradeCategory():
    def __init__(self, category: str) -> None:
        self.category = category
        try:
            self._insert
        except sqlite3.IntegrityError:
            pass

    @property
    def _insert(self) -> None:
        with _get_db() as conn:
            conn.execute(
                '''INSERT INTO grade_categories(category) VALUES(?);''',
                [self.category])
        conn.close()

    @property
    def rowid(self) -> int:
        with _get_db() as conn:
            cur = conn.cursor()
            cur.execute(
                'SELECT rowid FROM grade_categories WHERE category=?;',
                [self.category])
            id = cur.fetchone()
        conn.close()
        return id[0]


@unique
class ActionOptions(Enum):
    """Actions related to actions table"""
    READ = 1
    WATCH = 2
    STUDY = 4
    SUBMIT = 5
    WRITE = 6
    TAKE = 7


class Action():
    table = query_db('SELECT * FROM actions;')

    def __init__(self, action: ActionOptions) -> None:
        self.id = action.value
        self.action = action.name
        # Insert item into table if not already in table.
        try:
            self._insert
        except sqlite3.IntegrityError:
            pass
        # Add all ActionOptions to table.
        for ActionOption in ActionOptions:
            Action(ActionOption)

    @property
    def _insert(self) -> None:
        with _get_db() as conn:
            conn.execute(
                '''INSERT INTO actions(id, action) VALUES(?, ?);''',
                [self.id, self.action])
        conn.close()

    @property
    def rowid(self) -> int:
        """Added to mirror other table classes - can just use ActionOptions."""
        with _get_db() as conn:
            cur = conn.cursor()
            cur.execute(
                '''SELECT id FROM actions WHERE action=?;''', [self.action])
            id = cur.fetchone()
        conn.close()
        return id[0]

    @classmethod
    def fromid(cls, rowid):
        idrow = [(row['id'], row['action']) for row in cls.table if row['id']
                 == rowid]
        return idrow


class CourseCatalog():
    def __init__(self, catalog_code: str, course_title: str = None,
                 course_credits: int = None) -> None:
        match = re.match(r'^(\w+)(\d+)', catalog_code)
        assert match is not None
        self.catalog_code: tuple = (CoursePrefix(match.group(1)).rowid,
                                    match.group(2))
        assert self.catalog_code[0] is not None
        self.title = course_title
        self.credits = course_credits
        if self.title and self.credits:
            try:
                self._insert
            except sqlite3.IntegrityError:
                pass

    @property
    def _insert(self) -> None:
        with _get_db() as conn:
            conn.execute(
                '''INSERT INTO course_catalog(
                        prefix_id, course_number, title, credits)
                    VALUES(?, ?, ?, ?);''', [*self.catalog_code,
                                             self.title, self.credits])
        conn.close()

    @property
    def rowid(self) -> int:
        with _get_db() as conn:
            cur = conn.cursor()
            cur.execute(
                '''SELECT rowid FROM course_catalog
                    WHERE prefix_id=? AND course_number=?;''',
                [*self.catalog_code])
            id = cur.fetchone()
        conn.close()
        return id[0]


class CourseTaken():
    def __init__(self, start_date: datetime.date, catalog_code: str) -> None:
        self.course_catalog_id = CourseCatalog(catalog_code)
        self.term_id = Term(start_date).rowid
        try:
            self._insert
        except sqlite3.IntegrityError:
            pass

    @property
    def _insert(self) -> None:
        with _get_db() as conn:
            conn.execute(
                '''INSERT INTO courses_taken(term_id, course_catalog_id)
                    VALUES(?, ?);''', [self.term_id, self.course_catalog_id])
        conn.close()

    @property
    def rowid(self) -> int:
        with _get_db() as conn:
            cur = conn.cursor()
            cur.execute(
                '''SELECT rowid FROM courses_taken
                    WHERE term_id=? AND course_catalog_id=?;''',
                [self.term_id, self.course_catalog_id])
            id = cur.fetchone()
        conn.close()
        return id[0]

    def record_grade(self, grade: str) -> None:
        with _get_db() as conn:
            conn.execute(
                '''UPDATE OR FAIL courses_taken SET grade=?
                    WHERE rowid=?;''',
                [grade, self.rowid])
        conn.close()


class CourseRubric():
    def __init__(self, course_taken_id: int, grade_category: str,
                 percent_of_grade: float) -> None:
        self.course_taken_id = course_taken_id
        self.grade_category_id = GradeCategory(grade_category)
        self.percent = percent_of_grade
        if percent_of_grade:
            try:
                self._insert
            except sqlite3.IntegrityError:
                pass

    @property
    def _insert(self) -> None:
        with _get_db() as conn:
            conn.execute(
                '''INSERT INTO course_rubrics(
                        course_taken_id, grade_category_id, percent)
                    VALUES(?, ?, ?);''',
                [self.course_taken_id, self.grade_category_id, self.percent])
        conn.close()

    @property
    def rowid(self) -> int:
        with _get_db() as conn:
            cur = conn.cursor()
            cur.execute(
                '''SELECT rowid FROM course_rubrics
                    WHERE course_taken_id=? AND grade_category_id=?;''',
                [self.course_taken_id, self.grade_category_id])
            id = cur.fetchone()
        conn.close()
        return id[0]


class Weeks():
    def __init__(self, course_taken_id: int, week: int, topic: str) -> None:
        self.course_taken_id = course_taken_id
        self.week = week
        self.topic = topic
        if topic:
            try:
                self._insert
            except sqlite3.IntegrityError:
                pass

    @property
    def _insert(self) -> None:
        with _get_db() as conn:
            conn.execute(
                '''INSERT INTO weeks(
                        course_taken_id, week, topic)
                    VALUES(?, ?, ?);''',
                [self.course_taken_id, self.week, self.topic])
        conn.close()

    @property
    def rowid(self) -> int:
        with _get_db() as conn:
            cur = conn.cursor()
            cur.execute(
                '''SELECT rowid FROM weeks
                    WHERE course_taken_id=? AND week=?;''',
                [self.course_taken_id, self.week])
            id = cur.fetchone()
        conn.close()
        return id[0]


class Tasks():
    def __init__(self, syllabus_id: int, task: str, details: str = ''
                 ) -> None:
        self.syllabus_id = syllabus_id
        self.task = task
        self.details = details
        # Insert task item into table unless already in table.
        try:
            self._insert
        except sqlite3.IntegrityError:
            pass

    @property
    def _insert(self) -> None:
        with _get_db() as conn:
            conn.execute(
                '''INSERT INTO tasks(
                        syllabus_id, task, details)
                    VALUES(?, ?, ?);''',
                [self.syllabus_id, self.task, self.details])
        conn.close()

    @property
    def rowid(self) -> int:
        with _get_db() as conn:
            cur = conn.cursor()
            cur.execute(
                '''SELECT rowid FROM tasks WHERE syllabus_id=? AND task=?;''',
                [self.syllabus_id, self.task])
            id = cur.fetchone()
        conn.close()
        return id[0]

    def update_details(self, details: str) -> None:
        with _get_db() as conn:
            conn.execute(
                '''UPDATE OR FAIL tasks SET details=? WHERE rowid=?;''',
                [details, self.rowid])
        conn.close()

    def mark_complete(self,
                      done_date: datetime.date = datetime.datetime.now()
                      ) -> None:
        with _get_db() as conn:
            conn.execute(
                '''UPDATE OR FAIL tasks SET is_done=1, done_date=?
                    WHERE rowid=?;''',
                [done_date, self.rowid])
        conn.close()


class ToDo():
    def __init__(self, week_num: int, grade_rubric_id: int,
                 action: ActionOptions, what_to_do: str,
                 due_date: datetime.date = None) -> None:
        self.course_rubric_id = grade_rubric_id
        # Items that are graded must have a due date.
        if self.course_rubric_id != 1 and due_date is None:
            # AssertionError used to match other table classes.
            raise AssertionError
        self.week_num = week_num
        self.action_id = action.value
        self.what = what_to_do
        self.due_date = due_date
        # Insert syllabus item into table unless already in table.
        try:
            self._insert
        except sqlite3.IntegrityError:
            pass

    @property
    def _insert(self) -> None:
        with _get_db() as conn:
            conn.execute(
                '''INSERT INTO syllabus(
                        week_num, course_rubric_id, action_id, what, due_date)
                    VALUES(?, ?, ?, ?, ?);''',
                [self.week_num, self.course_rubric_id, self.action_id,
                 self.what, self.due_date])
        conn.close()

    @property
    def rowid(self) -> int:
        with _get_db() as conn:
            cur = conn.cursor()
            cur.execute(
                '''SELECT rowid FROM syllabus WHERE
                    week_num=? AND course_rubric_id=?
                        AND action_id=? AND what=?;''',
                [self.week_num, self.course_rubric_id, self.action_id,
                 self.what])
            id = cur.fetchone()
        conn.close()
        return id[0]

    def update_due_date(self, due_date: datetime.date) -> None:
        with _get_db() as conn:
            conn.execute(
                '''UPDATE OR FAIL syllabus SET due_date=?
                    WHERE rowid=?;''',
                [due_date, self.rowid])
        conn.close()

    def mark_complete(self,
                      done_date: datetime.date = datetime.datetime.now()
                      ) -> None:
        with _get_db() as conn:
            conn.execute(
                '''UPDATE OR FAIL syllabus SET is_done=1, done_date=?
                    WHERE rowid=?;''',
                [done_date, self.rowid])
        conn.close()

    def record_grade(self, grade: str) -> None:
        with _get_db() as conn:
            conn.execute(
                '''UPDATE OR FAIL syllabus SET grade=?
                    WHERE rowid=?;''',
                [grade, self.rowid])
        conn.close()

    def get_tasks(self, done: bool = None) -> list:
        if done is None:
            tasks = query_db('SELECT * FROM tasks WHERE syllabus_id=?;',
                             [self.rowid])
        else:
            done = 0 if done == 0 else 1
            tasks = query_db('''SELECT * FROM tasks
                                    WHERE syllabus_id=? AND is_done=?''',
                             [self.rowid, done])
        return tasks

    @property
    def get_status(self) -> list[int]:
        num_tasks = len(self.get_tasks())
        complete = len(self.get_tasks(True))
        return (num_tasks, complete)


_get_db().close()
