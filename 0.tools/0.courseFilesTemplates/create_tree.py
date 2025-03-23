from pathlib import Path
import datetime

import dates

FILECWD = Path(__file__).parent
COURSEWORK_DIR = Path.home() / 'OneDrive/coursework'
today = datetime.date.today()


def getdates_in_months(start_date: dates.Date | datetime.date,
                       additional_months: int = 0, stop_date=None):
    """Obtain all dates from start_month to start_month + additional_months.

    Args:
        start_month (dates.Date | datetime.date): The start date.
        additional_months (int, optional): The number of additional months for
            which tog et dates. Defaults to 0.

    Raises:
        NotImplementedError: If additional_months is a negative number.

    Returns:
        list[datetime.date]: All dates from start_month to the last day of
            the month that is additional_months after start_month.
    """
    # Make sure data type is correct.
    if isinstance(start_date, datetime.date):
        start_date = dates.Date(start_date.year, start_date.month,
                                start_date.day)
    elif not isinstance(start_date, dates.Date):
        raise NotImplementedError

    dates_in_months = [*start_date.month_dates]
    # Make sure additional_months is not a negative value. If 0, return dates.
    if additional_months == 0:
        # Drop any dates that are before start_date
        return dates.dropdates(dates_in_months, start_date, stop_date)
    elif additional_months < 0:
        raise NotImplementedError('additional_months cannot be negative'
                                  f' ({additional_months=!r}).')
    # Obtain dates for the additional months.
    for i in range(1, additional_months + 1):
        next_month = start_date.add_mths(i)
        dates_in_months.extend(next_month.month_dates)
    return dates.dropdates(dates_in_months, start_date, stop_date)


class Term:
    def __init__(self, start_date: dates.Date, term_num: int,
                 num_weeks: int = 8) -> None:
        """Represents a Term of College including dates and due dates.

        Args:
            start_date (dates.Date): The start date for the term.
            term_num (int): Term number in relation to order taken/attended.
            num_weeks (int, optional): The number of weeks in the term.
                Defaults to 8.
        """
        self.num = term_num
        # Ex. '/Documents/Term1/'
        self.dir = COURSEWORK_DIR / f'Term{term_num}'
        # Ex. '/Documents/Term1/Term1-DueDates.md
        self.mrkdwn_file = self.dir / f'Term{term_num}-DueDates.md'
        self.num_weeks = num_weeks
        self.start = start_date
        self.start.add_days(num_weeks * 7)
        self.stop = self.start.add_wks(num_weeks)
        self.dates_in = self.start.dates_to_added_days
        self.weekly_due = [dates.Weekday.SUNDAY, dates.Weekday.TUESDAY]
        self._wklyduedays = {
            'SUNDAY': 'Initial Discussion Post',
            'TUESDAY': 'Remaining Assignments'}
        self.num_duedates = len(self.wklyduedays) * num_weeks

    @property
    def wklyduedays(self) -> dict:
        """The weekday deadlines for graded work.
        """
        return self._wklyduedays

    @wklyduedays.setter
    def wklyduedays(self, assigndue: dict) -> None:
        """Sets the weekday deadlines for graded work.
        """
        self._wklyduedays = assigndue

    @property
    def duedates(self) -> list:
        """All the due dates in the Term.
        """
        months = self.dates_in
        total_due_dates = self.num_duedates
        weeklyduedays = frozenset(self.wklyduedays.keys())
        due_dates = []

        for date in months:
            # Convert from datetime.date to Date.
            if len(due_dates) >= total_due_dates:
                return due_dates
            if dates.Weekday(date.weekday()).name in weeklyduedays:
                due_dates.append(date)

    def duedates_by_week(self) -> dict:
        dates_by_week = {}
        for i, due_date in enumerate(self.duedates):
            due_date = dates.Date(due_date.year, due_date.month, due_date.day)
            weeknum = f'W{i // 2 + 1}'
            if weeknum not in dates_by_week:
                dates_by_week.setdefault(weeknum, [due_date])
            else:
                dates_by_week[weeknum].append(due_date)
        return dates_by_week

    def duedates_mrkdwn(self) -> list[str]:
        """The text for a markdown file listing all due dates in the Term.

        Returns:
            list[str]: The markdown text including header and due dates table.
        """
        start_date = self.start.to_dt_date
        file_text = [
            f'# Term {self.num} - Due Dates\n',
            f'Start date: {self.start} ({start_date.strftime("%a")})\n',
            '| W#  | Day (WkD)   | What                    |',
            '| --- | ----------- | ----------------------- |'
            ]

        for i, due_date in enumerate(self.duedates):
            weeknum = i // 2 + 1
            strft_date: str = due_date.strftime('%m/%d (%a)')
            assignment = self.wklyduedays.get(
                dates.Weekday(due_date.weekday()).name)
            file_text.append(
                f'| W{weeknum}  | {strft_date} | {assignment:23} |')
        file_text.append('')
        return file_text

    def write_mrkdwn(self, test: bool = True) -> None:
        """Write the markdown file using duedates_mrkdown text.

        Args:
            test (bool, optional): If True, markdown text is printed and
                no file is written. Defaults to True.
        """
        # Ex. '/Documents/Term1/Term1-DueDates.md'
        duedates_md: Path = self.dir / f'Term{self.num}-DueDates.md'
        file_text = self.duedates_mrkdwn()
        if test:
            for i in file_text:
                print(i)
        else:
            if not self.dir.is_dir():
                self.dir.mkdir(parents=True)
            if not duedates_md.is_file():
                duedates_md.touch()
            else:  # Ask user whether to overwrite. If no, cancel.
                print(f'{duedates_md} already exists.', end=' ')
                confirm_overwrite = input('Overwrite file (Y): ')
                if not confirm_overwrite == 'Y':
                    print('Operation canceled.')
                    return None
            duedates_md.write_text('\n'.join(file_text), newline='\n')
        return None


class Course:
    def __init__(self, course_code: str, course_name: str, github_num: int,
                 term: Term) -> None:
        """Represents a college course from which to create a directory tree.

        Args:
            course_code (str): The college catalog course code for the Course.
            course_name (str): The course's name/title.
            term (Term): The term in which the course is being taken.
        """
        self.code = course_code
        self.name = course_name
        self.gitnum = github_num
        self.term = term
        self._pathname = self.name.replace(' ', '_')
        self.dir = term.dir / f'{course_code}-{self._pathname}'
        self._subweekly_folders = ['Discussions', 'Assignments']
        self._weekly_files = {
            'W?-Discussions': {
                '0.W?-DiscussPrompt-$.md': FILECWD / 'tmp_discussprompt.txt',
                '$_W?DiscussPost.md': FILECWD / 'tmp_discusspost.txt'},
            'W?-Assignments': {'0.W?-AssignPrompt-$.md':
                               FILECWD / 'tmp_assign.txt'}
            }

    @property
    def subweekly_folders(self) -> list[str]:
        """The folders that go inside each weekly folder for the course.
        """
        return self._subweekly_folders

    @subweekly_folders.setter
    def subweekly_folders(self, folders: list[str]) -> None:
        """The folders that go inside each weekly folder for the course.
        """
        self._subweekly_folders = folders

    @property
    def week_dirs(self) -> list[Path]:
        """The path to the folders for each week of the Course.
        """
        # Ex. '/Documents/Term1/CS192-Programming_Essentials/W1-CS192/'
        return [self.dir / f'W{i}-{self.code}'
                for i in range(1, self.term.num_weeks + 1)]

    @property
    def subweek_dirs(self) -> list[Path]:
        """The path to the weekly folders for the Course.
        """
        # Ex. '/Documents/Term1/CS192-Programming_Essentials/W1-CS192/Notes/'
        return [week_dir / subweekly_folder for week_dir in self.week_dirs
                for subweekly_folder in self.subweekly_folders]

    @property
    def weekly_files(self) -> dict:
        """The weekly files for the course.
        """
        return self._weekly_files

    @weekly_files.setter
    def weekly_files(self, folder_files: dict) -> None:
        """Set the weekly folders for the Course.

        Args:
            folder_files (dict): The weekly folders, subfolders, and
            templates for the Course's weekly files.
        """
        self._weekly_files = folder_files

    @property
    def weekly_files_path(self) -> list:
        """The path to the weekly files for the course."""
        wklyddt = self.term.duedates_by_week()
        filepaths = []
        for i, weekdir in enumerate(self.week_dirs, 1):
            weeknum = f'W{i}'
            for subweek_dir, file_info in self.weekly_files.items():
                subweek = weekdir / subweek_dir.replace('?', str(i))
                for key, value in file_info.items():
                    filename = key.replace('?', str(i)).replace('$',
                                                                self.code)
                    template_text = []
                    with open(value, 'r') as f:
                        for line in f.readlines():
                            line = line.replace('$', self.code)
                            line = line.replace('?', str(i))
                            line = line.replace('&', str(self.gitnum))
                            line = line.replace(
                                '!',
                                str(wklyddt[weeknum][0]))
                            line = line.replace(
                                '%',
                                str(wklyddt[weeknum][1]))
                            template_text.append(line)
                    filepaths.append((subweek / filename, template_text))
        return filepaths

    def create_folders(self, test: bool = True) -> None:
        """Create directory tree for the Course."""
        folder_tree = self.subweek_dirs
        print('Creating new course folders...')
        for folder in folder_tree:
            print(f'\t{folder}')
            if not test:
                folder.mkdir(parents=True, exist_ok=True)

    def write_week_files(self, test: bool = True, overwrite: bool = False
                         ) -> None:
        """Write the weekly files for the Course.
        """
        print('Creating new course files...')
        for filepath, template in self.weekly_files_path:
            print(f'\t{filepath}')
            if not test:
                filepath.parent.mkdir(parents=True, exist_ok=True)
                if filepath.is_file() and not overwrite:
                    overwrite = input(f'{filepath} exists. Overwrite? (Y): ')
                    if not overwrite.upper() == 'Y':
                        return None
                filepath.touch()
                with open(filepath, 'w', newline='\n') as f:
                    f.write(''.join(template))
        return None


if __name__ == '__main__':
    start = Path.home() / 'OneDrive/coursework'
    term = Term(dates.Date(2024, 7, 10), term_num=16)
    # course = Course('CS499', 'Computer Science Capstone', github_num=40,
    #                  term=term)
    course = Course('IS450', 'Security Trends and Legal Issues', 41, term)
    term.write_mrkdwn(test=False)
    course.write_week_files(False, True)

    # Future Ideas - Write headers and due dates for Assignments (Word)
