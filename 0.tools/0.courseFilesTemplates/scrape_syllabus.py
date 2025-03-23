from pathlib import Path
import re

from bs4 import BeautifulSoup

TOPDIR = Path.home() / 'OneDrive/coursework/0.tools/0.templates/'


def makeSoup(url: str | Path) -> BeautifulSoup:
    if isinstance(url, Path):
        with open(url, encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'lxml')
    else:
        raise NotImplementedError
        # headers = {
        #     'User-Agent':
        #     ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        #      '(KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36')
        # }
        # r = requests.get(url, headers=headers)
        # soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def clean_text(s: str) -> str:
    """
    Removes non-ascii/garbage text from HTML text.

    Args:
        s (str): String to clean

    Returns:
        str: Cleaned string
    """
    s = s.strip()
    s = s.replace('“', '"')
    s = s.replace('”', '"')
    s = s.replace('&nbsp;', ' ')
    s = s.replace('\xa0', ' ')
    s = s.replace('\n', ' ')
    s = re.sub(r'[ ]{2,}', ' ', s)
    s = s.replace('·', '- [ ]')
    s = re.sub(r'^o ', '  - [ ] ', s)
    return s


def get_week_tasks(soup: BeautifulSoup) -> dict[str]:
    week_tasks = {}
    pattern = re.compile(r'(Tentative )?(Course )?(Schedule|Activities)')
    week_table = soup.find(string=pattern).find_next('table')
    table_rows = week_table.find_all_next('tr')[1:9]  # Just assignment table

    for row in table_rows:
        tasks = []  # For all tasks in row
        task_parts = []  # For joining split tasks
        cols = row.find_all('td')  # Get cells in row
        week_label: str = clean_text(cols[0].text)  # E.g. "Week 1 ..."
        # assignments = cols[1]  # Soup of week's assignment cell contents
        # Collect all the tasks for the week.
        assignments = map(clean_text, [assign.text for assign in cols[1]
                          if not re.match(r'\s', assign.text)])

        for assign in assignments:
            # Build task list
            match = re.match(r'\s*-', assign)

            if task_parts and match:  # Split tasks
                tasks.append(' '.join(task_parts))
                if re.search(r'Discussion', tasks[-1]):
                    tasks.append('  - [ ] Initial')
                task_parts[:] = []
            # Collect multiline tasks
            task_parts.append(assign)
        tasks.append(' '.join(task_parts))  # Add final task
        week_tasks.setdefault(week_label, tasks)  # Build tasks by week
    return week_tasks


def get_course_title(soup: BeautifulSoup) -> str:
    # Second <h1><span>TITLE<o:p></o:p></h1>
    titles = list(soup.find_all('h1'))
    if len(titles) > 1:
        title = clean_text(soup.find_all('h1')[1].text)
    elif len(titles) == 1:
        title = clean_text(soup.find_all('h1')[0].text)
    else:
        title = ''
    return title


def get_textbooks(soup: BeautifulSoup) -> str:
    books = []
    # [ ] Fix
    nav = soup.p
    while True:
        if nav and nav.text == 'Required Text':
            nav = nav.find_next('p')
            break
        else:
            nav = nav.find_next('p')

    while nav and nav.text != "Course Description":
        t = clean_text(nav.text)
        if t and not (t.startswith('<!--') or t.startswith('<!')):
            books.append(t)
        nav = nav.find_next('h2')
    return ' '.join(books)


if __name__ == '__main__':
    # For text added into output file
    yr = '2024'
    mth = 'May'

    course = 'CS499'
    url = 'https://content.grantham.edu/academics/GU_CS499/syllabus1.htm'

    # Create soup from copied HTML syllabus
    soup = makeSoup(TOPDIR / f'html_syllabi/{course.lower()}.html')
    # soup = makeSoup(url)

    course_title = get_course_title(soup)
    textbooks = get_textbooks(soup)

    # Make output link
    outfile = TOPDIR / f'{course.lower()}-assignments.md'

    # Get weekly tasks
    tasks = get_week_tasks(soup)

    # # Write syllabus tasks
    with open(outfile, 'w', newline='\n') as f:
        h1 = f'# {yr} {mth} Syllabus - {course.upper()}: {course_title}\n\n'
        link = f'[Syllabus Weblink]({url})\n\n'

        textbook = '## Book(s)\n\n'

        h2s = '\n\n## Schedule\n'

        filestart = [h1, link, textbook, textbooks, h2s]

        f.writelines(filestart)

        for key, value in tasks.items():
            week = f'\n### {key}\n\n'
            # print(week, end='')
            f.write(week)
            task_list = [f'{task}\n' for task in value if task != '']
            f.writelines(task_list)
