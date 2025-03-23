from pathlib import Path
import sqlite3
import re

import dotenv
from flask import (Flask, redirect, render_template, request)
from flask import g


CUR_FILE_DIR: Path = Path(__file__).parent
# Set up for database
DB = CUR_FILE_DIR / 'college_dev.db'

RowFactories = list[sqlite3.Row]

# Set up website
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config.update(
    TEMPLATES_AUTO_RELOAD=True,
    SECRET_KEY=dotenv.get_key(CUR_FILE_DIR / '.env', 'SECRET_KEY')
)


def get_db() -> sqlite3.Connection:
    """Create database connection."""
    conn = sqlite3.connect(
        DB,
        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    return conn


@app.teardown_appcontext
def close_connection(exception) -> None:
    """Close database."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
    return None


def query_db(query: str, args: tuple = (), one: bool = False) -> list:
    """Query database."""
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return (rows[0] if rows else None) if one else rows


class Field:
    def __set_name__(self, owner, name):
        self.fetch = f'SELECT {name} FROM {owner.table} WHERE {owner.key}=?;'
        self.store = f'UPDATE {owner.table} SET {name}=? WHERE {owner.key}=?;'

    def __get__(self, obj, objtype=None):
        return query_db(self.fetch, [obj.key], True)[0]

    def __set__(self, obj, value):
        conn = get_db()
        conn.execute(self.store, [value, obj.key])
        conn.commit()
        conn.close()


# Course Catalog Tables for Querying
class CoursePrefix:
    table = 'course_prefixes'
    key = 'prefix'
    subject = Field()
    rowid = Field()

    def __init__(self, key):
        self.key = key


class CoursePrefixByID:
    table = 'course_prefixes'
    key = 'rowid'
    subject = Field()
    prefix = Field()
    rowid = Field()

    def __init__(self, key):
        self.key = key


class CourseCatalog:
    table = 'course_catalog'
    key = 'uid'
    course_prefix_id = Field()
    course_number = Field()
    title = Field()
    credits = Field()
    prereq = Field()
    description = Field()
    rowid = Field()
    pattern = re.compile(r'^([A-Za-z]{2,3})(-)?([0-9]{3}[A-Za-z]?)$')

    def __init__(self, key):
        if isinstance(key, str):
            match = self.pattern.match(key)
            if match:
                key = f'{CoursePrefix(match.group(1)).rowid}-{match.group(3)}'
        self.key = key

    @property
    def prefix(self):
        return CoursePrefixByID(self.course_prefix_id).prefix

    @property
    def catalog_code(self):
        return f'{self.prefix}-{self.course_number}'

    def __repr__(self):
        return (
            f"CourseCatalog('{self.course_prefix_id}, {self.course_number}')")

    def __str__(self):
        return f'{self.prefix}-{self.course_number}: {self.title}'


class CourseCatalogByID:
    table = 'course_catalog'
    key = 'rowid'
    course_prefix_id = Field()
    course_number = Field()
    title = Field()
    credits = Field()
    prereq = Field()
    description = Field()
    uid = Field()

    def __init__(self, key):
        self.key = key

    @property
    def prefix(self):
        return CoursePrefixByID(self.course_prefix_id).prefix

    @property
    def catalog_code(self):
        return f'{self.prefix}-{self.course_number}'

    def __repr__(self):
        return (
            f"CourseCatalog('{self.course_prefix_id}, {self.course_number}')")

    def __str__(self):
        return f'{self.prefix}-{self.course_number}: {self.title}'


# Personal Courses Tables for Querying
class Term:
    table = 'terms'
    key = 'start_date'
    rowid = Field()

    def __init__(self, key):
        self.key = key


class TermByID:
    table = 'terms'
    key = 'rowid'
    start_date = Field()
    rowid = Field()

    def __init__(self, key):
        self.key = key


class CourseTaken:
    table = 'courses_taken'
    key = 'uid'
    term_id = Field()
    course_catalog_id = Field()
    grade = Field()
    rowid = Field()

    def __init__(self, key):
        self.key = key
        course = CourseCatalogByID(self.course_catalog_id)
        self.catalog_code = course.catalog_code
        self.title = course.title
        self.description = course.description
        self.prereqs = course.prereq
        self.credits = course.credits
        self.term_start = TermByID(self.term_id).start_date

    def to_dict(self):
        return {
            'term': self.term_start,
            'catalog_code': self.catalog_code,
            'title': self.title,
            'credits': self.credits,
            'prereqs': self.prereqs,
            'description': self.description,
            'grade': self.grade,
            'rowid': self.rowid
        }


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        term = request.form.get('term_start')
        catalog_code = request.form.get('catalog_code')
        grade = request.form.get('grade')

        conn = get_db()
        # Add term to database unless already in database.
        conn.execute('INSERT OR IGNORE INTO terms VALUES(?);', [term.strip()])
        conn.commit()
        # Obtain term ID.
        term_rowid = query_db(
            'SELECT rowid FROM terms WHERE start_date=date(?);',
            [term.strip()], True)[0]

        course_to_add = CourseCatalog(catalog_code)
        if not grade:
            conn.execute('''INSERT INTO courses_taken(
                            term_id, course_catalog_id, grade) VALUES(?, ?, ?)
                            ;''', [term_rowid, course_to_add.rowid, None])
        else:
            course_to_update = CourseTaken(
                f'{term_rowid}-{course_to_add.rowid}')
            if grade:
                course_to_update.grade = grade
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        # Display courses data.
        courses_taken = query_db('SELECT uid FROM courses_taken;')
        courses = []
        cur_courses = []
        past_courses = []
        for course in courses_taken:
            course = course[0]
            courses.append(CourseTaken(course))
        for course in courses:
            if course.grade is None:
                cur_courses.append(course)
            else:
                past_courses.append(course)
        return render_template('index.html', courses=courses,
                               cur_courses=cur_courses,
                               past_courses=past_courses)


@app.route('/syllabus/<course>', methods=['GET', 'POST'])
def syllabus(course):
    if request.method == 'POST':
        return NotImplemented
    else:
        course_code = CourseCatalog(course.split('=')[1]).rowid
        matching_course = query_db(
            '''Select uid FROM courses_taken WHERE course_catalog_id=?;''',
            [course_code], one=True)[0]
        courses_taken = query_db('SELECT uid FROM courses_taken;')
        courses = []
        cur_courses = []
        past_courses = []
        for course in courses_taken:
            course = course[0]
            courses.append(CourseTaken(course))
        for course in courses:
            if course.grade is None:
                cur_courses.append(course)
            else:
                past_courses.append(course)
        course = CourseTaken(matching_course)
        return render_template('syllabus.html',
                               course=course,
                               courses=courses,
                               cur_courses=cur_courses,
                               past_courses=past_courses,
                               syllabus=None)


@app.route('/edit', methods=['GET', 'POST'])
def edit_course():
    if request.method == 'POST':
        return NotImplemented
    else:
        # Display courses data.
        courses_taken = query_db('SELECT uid FROM courses_taken;')
        courses = []
        cur_courses = []
        past_courses = []
        for course in courses_taken:
            course = course[0]
            courses.append(CourseTaken(course))
        for course in courses:
            if course.grade is None:
                cur_courses.append(course)
            else:
                past_courses.append(course)
        return render_template('edit.html', courses=courses,
                               cur_courses=cur_courses,
                               past_courses=past_courses)


@app.route('/degreeaudit', methods=['GET', 'POST'])
def degreeaudit():
    if request.method == 'POST':
        return NotImplemented
    else:
        degree_pursuing = 'BS Computer Science'
        # Display courses data.
        courses_taken = query_db('SELECT uid FROM courses_taken;')
        courses = []
        cur_courses = []
        past_courses = []
        for course in courses_taken:
            course = course[0]
            courses.append(CourseTaken(course))
        return render_template('degreeaudit.html', courses=courses,
                               cur_courses=cur_courses,
                               past_courses=past_courses,
                               degree_pursuing=degree_pursuing)


@app.route('/details/<course>', methods=['GET', 'POST'])
def details(course):
    if request.method == 'POST':
        return NotImplemented
    else:
        print(course)
        course = CourseCatalog(course.split('=')[1])
        courses_taken = query_db('SELECT uid FROM courses_taken;')
        courses = []
        cur_courses = []
        past_courses = []
        for i in courses_taken:
            i = i[0]
            courses.append(CourseTaken(i))
        return render_template('details.html',
                               course=course,
                               courses=courses,
                               cur_courses=cur_courses,
                               past_courses=past_courses)
