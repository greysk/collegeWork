from pathlib import Path
import datetime

import dates

FILECWD = Path(__file__).parent
COURSEWORK_DIR = Path.home() / 'OneDrive/coursework'
today = datetime.date.today()


# [ ] Incorporate portions from .tools/scrape_syllabus.py to write files' body

def getdates_in_months(from_date: dates.Date | datetime.date,
                       additional_months: int = 0, stop_date=None
                       ) -> list(datetime.dates):
    """Obtain all dates fromfrom_date through (start_date + additional_months).

    If given, the last date will be stop_date.

    Args:
        `start_date` (dates.Date | datetime.date): The start date.
        `additional_months` (int, optional): Defaults to 0. The number of
            months for which to get additional dates.
        `stop_date` (dates.Date | datetime.date, optional): Defaults to None.
            The last date to include.

    Raises:
        `NotImplementedError`: If additional_months is a negative number.

    Returns:
        `list[datetime.date]`: All dates from start_month to the last day of
            the month that is additional_months after start_month.
    """
    # Guard clause on additional_months to ensure its value is not negative.
    if additional_months < 0:
        raise NotImplementedError('additional_months cannot be negative'
                                  f' ({additional_months = !r}).')

    # Guard clause on from_date to ensure it's the correct data type.
    if not isinstance(from_date, (datetime.date, dates.Date)):
        raise NotImplementedError

    # Convert datetime.date to dates.Date
    if not isinstance(from_date, datetime.date):
        from_date = dates.Date(from_date.year, from_date.month,
                               from_date.day)

    # Get all dates in the same month as from_date
    dates_in_months = [*from_date.month_dates]

    # Obtain dates for the additional months.
    for i in range(1, additional_months + 1):
        next_month = from_date.add_mths(i)
        dates_in_months.extend(next_month.month_dates)

    # Return dates from from_date through the last day of the last month or,
    # if given, through stop_date.
    return dates.dropdates(dates_in_months, from_date, stop_date)


class Term:
    def __init__(self, start_date: dates.Date, term_num: int,
                 num_weeks: int = 8) -> None:
        """Represent a term in college including dates and due dates.

        Args:
            start_date (dates.Date): The start date for the term.
            term_num (int): Term number in relation to order taken/attended.
            num_weeks (int, optional): The number of weeks in the term.
                Defaults to 8.
        """
        self.num = term_num
        # E.g., '/Documents/Term1/'
        self.dir = COURSEWORK_DIR / f'Term{term_num}'
        # E.g., '/Documents/Term1/Term1-DueDates.md
        self.mrkdwn_file = self.dir / f'Term{term_num}-DueDates.md'
        self.num_weeks = num_weeks
        self.start = start_date
        self.stop = self.start.add_wks(num_weeks)
        self.dates_in = self.start.dates_to_added_days  # All dates in term.
        self.weekly_due = [dates.Weekday.SUNDAY, dates.Weekday.TUESDAY]
        self._wklyduedays = {
            'SUNDAY': 'Initial Discussion Post',
            'TUESDAY': 'Remaining Assignments'}
        self.num_duedates = len(self.wklyduedays) * num_weeks

    def __repr__(self) -> str:
        return f"Term({self.start}, {self.num}, {self.num_weeks})"

    @property
    def wklyduedays(self) -> dict:
        """The weekday deadlines for graded work.
        """
        return self._wklyduedays

    @wklyduedays.setter
    def wklyduedays(self, assigndue: dict) -> None:
        """Set the weekday deadlines for graded work.
        """
        self._wklyduedays = assigndue

    @property
    def duedates(self) -> list:
        """All the due dates in the Term based on day of the week.

        Returns:
            `list`: A list of due dates in the term.
        """
        months = self.dates_in
        total_due_dates = self.num_duedates
        weeklyduedays = frozenset(self.wklyduedays.keys())
        due_dates = []

        for date in months:
            # Guard clause to stop loop if all due_dates are found.
            if len(due_dates) >= total_due_dates:
                break
            # Accumulate due dates.
            if dates.Weekday(date.weekday()).name in weeklyduedays:
                due_dates.append(date)
        return due_dates

    def duedates_by_week(self) -> dict:
        """All due dates mapped to week numbers ('W#').

        Returns:
            `dict`: Key is the week number in 'W#' format. Value is a list
                containing that week number's due dates in datetime.date
                format.
        """
        dates_by_week = {}
        for i, due_date in enumerate(self.duedates):
            due_date = dates.Date(due_date.year, due_date.month,
                                  due_date.day)
            weeknum = f'W{i // 2 + 1}'
            if weeknum not in dates_by_week:
                dates_by_week.setdefault(weeknum, [due_date])
            else:
                dates_by_week[weeknum].append(due_date)
        return dates_by_week

    def duedates_mrkdwn(self) -> list[str]:
        """The text for a markdown file listing all due dates in the Term.

        Returns:
            `list[str]`: Text that can be used to write a markdown file.
                Includes header and due dates table. Each element in the list
                is a separate line of text.
        """
        start_date = self.start.to_dt_date  # Convert to datetime.date
        # Start the file_text with the text and table headers.
        file_text = [
            f'# Term {self.num} - Due Dates\n',
            f'Start date: {self.start} ({start_date.strftime("%a")})\n',
            '|W#| Day (WkD) |What                   |',
            '|--|-----------|-----------------------|'
            ]

        for i, due_date in enumerate(self.duedates):
            weeknum = i // 2 + 1
            strft_date: str = due_date.strftime('%m/%d (%a)')
            assignment = self.wklyduedays.get(dates.Weekday(
                                              due_date.weekday()).name)
            file_text.append(f'|W{weeknum}|{strft_date}|{assignment}|')
        # Last line is a newline.
        # file_text.append('\n')

        return file_text

    def write_mrkdwn(self, test: bool = True) -> None:
        """Write the markdown file using duedates_mrkdown text.

        Creates parent folders, if necessary.

        Args:
            `test` (bool, optional): If `True`, markdown text is printed
                and no file is written. Defaults to `True`.
        """
        # E.g., '/Documents/Term1/Term1-DueDates.md'
        duedates_md: Path = self.dir / f'Term{self.num}-DueDates.md'
        file_text = self.duedates_mrkdwn()

        if test:  # Print text and exit
            for i in file_text:
                print(i)
            return None

        if not self.dir.is_dir():  # Create parent folders.
            self.dir.mkdir(parents=True)

        if not duedates_md.is_file():  # Create duedates markdown file
            duedates_md.touch()
        else:  # Ask user whether to overwrite. If no, cancel.
            print(f'{duedates_md} already exists.', end=' ')
            confirm_overwrite = input('Overwrite file (Y): ')
            if not confirm_overwrite == 'Y':
                # Cancel operation.
                print('Operation canceled.')
        duedates_md.write_text('\n'.join(file_text), newline='\n')

        return None


class Course:
    def __init__(self, course_code: str, course_name: str, github_num: int,
                 term: Term) -> None:
        """Represents a college course from which to create a directory tree.

        Args:
            `course_code` (str): The college catalog code for the Course.
            `course_name` (str): The course's name/title.
            `term` (Term): The term in which the course is being taken.
        """
        self.code = course_code   # E.g., 'EN261'
        self.name = course_name   # E.g., 'Technical Writing'
        self.gitnum = github_num  # E.g., 13
        self.term = term  # E.g., Term(dates.Date(2022, 07, 13), 4, 8)
        # E.g., '/Documents/Term1/EN261-Technical_Writing/'
        self.dir = term.dir / f'{course_code}-{self.name.replace(" ", "_")}'
        self._subweekly_folders = ['Discussions', 'Assignments']
        self._wklyddt = self.term.duedates_by_week()

    def weekly_file_template(self, week_num):
        """The path to discussion and assignment templates for week_num.

        Args:
            `week_num` (int): The week number.

        Returns:
            `dict[dict[str]]`: A dict containing files for the week's
                discussion and assignments.
        """
        template = {
            'W?-Discussions': {
                f'.W{week_num}-DiscussPrompt-{self.code}.md':
                    FILECWD / 'tmp_discussprompt.txt',
                f'{self.code}_W{week_num}DiscussPost.md':
                    FILECWD / 'tmp_discusspost.txt'
            },
            'W?-Assignments': {
                f'.W{week_num}-AssignPrompt-{self.code}.md':
                    FILECWD / 'tmp_assign.txt'
            }
        }
        return template

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
        # E.g., '/Documents/Term1/CS192-Programming_Essentials/W1-CS192/'
        return [self.dir / f'W{i}-{self.code}'
                for i in range(1, self.term.num_weeks + 1)]

    # def weekly_files(self) -> list[Path]:
    #     for i, week_dir in enumerate(self.week_dirs):
    #         for item in self.subweekly_folders:
    #             if item == "Assignments":

    @property
    def subweek_dirs(self) -> list[Path]:
        """The path to the weekly homework folders for the Course.
        """
        # E.g., '/Documents/Term1/CS192-Programming_Essentials/W1-CS192/Notes/'
        return [week_dir / subweekly_folder for week_dir in self.week_dirs
                for subweekly_folder in self.subweekly_folders]

    def assignment_prompt_template(self, week_num: int = 0,
                                   title: str = '&',
                                   instructions: list = ['- [ ] Add'],
                                   direction_link: str = None,
                                   rubric_link: str = None) -> list[str]:
        """Obtain a completed assignment prompt template in markdown format.

        Args:
            `week_num` (int, optional): The week number. Defaults to 0.
            `title` (str, optional): The prompt title. Defaults to '&'.
            `instructions` (list, optional): The assignment instructions with
                each element being a separate paragraph.
                Defaults to ['- [ ] Add'].
            `direction_link` (str, optional): A link to the directions for the
                assignment. Defaults to None.
            `rubric_link` (str, optional): A link to the rubric for the
                assignment. Defaults to None.

        Returns:
            list[str]: _description_
        """
        weeknum = f'W{week_num}'

        if direction_link is None:
            directions = '## Directions\n'
        else:
            directions = f'## [Directions]({direction_link}\n'

        template = [
            f'# {self.code} - {weeknum} - Assignment: {title}\n',
            (f'**Due**: {self._wklyddt[weeknum][1]}'
             ' [#' f'{self.gitnum}]'
             f'(https://github.com/greysk/coursework/issues/{self.gitnum})\n'),
            directions
        ]
        for p in instructions:
            template.append(f'{p}\n')

        if rubric_link is not None:
            template.append(f'## [Rubric]({rubric_link}\n')

        return template

    def discussion_prompt_template(self, week_num: int = 0,
                                   general_week_instruct: str = None,
                                   title: str = '',
                                   initial_instruct: list = ['- [ ] Add'],
                                   response_instruct: list = None
                                   ):
        weeknum = f'W{week_num}'

        if general_week_instruct is None:
            general_week_instruct = (
                'Your initial post should be 75-150 words in length, and is'
                ' due on Sunday. By Tuesday, you should respond to two'
                ' additional posts from your peers.')

        template = [
            f'# {self.code} - {weeknum} - Discussion Prompt\n',
            f'{general_week_instruct}\n',
            f'## Initial Prompt - {title}\n',
            (f'**Due**: {self._wklyddt[weeknum][0]}'
             ' [#' f'{self.gitnum}]'
             f'(https://github.com/greysk/coursework/issues/{self.gitnum})\n')
        ]

        for p in initial_instruct:
            template.append(f'{p}\n')

        template.extend(['## Responses\n',
                         f'**Due**: {self.weeklyddt[weeknum][1]}'])

        if response_instruct is not None:
            for p in response_instruct:
                template.append(f'{p}\n')

        return template

    def discussion_post_template(self, week_num: int = 0):
        template = [
            f'# {self.code} - W{week_num} - Discussion Prompt\n',
            '## Initial Post\n', '## Response 1', '## Response 2'
        ]
        return template

    @property
    def weekly_files_path(self) -> list:
        """The path to the weekly files for the course."""
        wklyddt = self.term.duedates_by_week()
        filepaths = []
        for i, weekdir in enumerate(self.week_dirs, 1):
            weeknum = f'W{i}'
            for subweek_dir in self.subweek_dirs:
                subweek = weekdir / subweek_dir.replace('?', str(i))
                for key, value in file_info.items():
                    filename = key.replace('?', str(i))
                    template_text = []
                    with open(value, 'r') as f:
                        for line in f.readlines():
                            line = line.replace('$', str(i))
                            line = line.replace(
                                '!',
                                str(wklyddt[weeknum][0]))
                            line = line.replace(
                                '@',
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
    # start = Path.home() / 'OneDrive/coursework'
    # term = Term(dates.Date(2022, 9, 14), 4)
    # course1 = Course('IS216', 'Computer Networks', 12, term)
    # course2 = Course('PH220', 'Physics', 13, term)
    # term.write_mrkdwn(test=False)
    # course1.write_week_files(False, True)
    # course2.write_week_files(False, True)

    print(getdates_in_months(today, 0))

    # Future Ideas - Write headers and due dates for files
