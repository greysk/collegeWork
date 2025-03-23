import datetime
from create_tree import Term, DueDays, Course
from dates import Year, Month, Day, Date, Weekday
from pathlib import Path, WindowsPath


class TestMonth:
    def test_month(self):
        for i in range(1, 13):
            assert Month(i) .month == i

    def test_from_date(self):
        assert Month.from_date(datetime.date(2022, 2, 15)) == Month.FEBRUARY

    def test_month_loop(self):
        dec = [0, 12, 24, 36, 48, 60, 120]
        for j in dec:
            assert Month.monthloop(j) == Month(12)

    def test_dates_days(self):
        for i in range(1, 13):
            month = Month(i)
            for yr in range(2000, 2005):
                islp = Year(yr).isleap
                assert len(month.dates(yr)) == month.days_in(islp)

    def test_days(self):
        three1 = [1, 3, 5, 7, 8, 10, 12]
        three0 = [4, 6, 9, 11]
        for i in three1:
            assert 31 == Month(i).days_in(True) == Month(i).days_in()
        for i in three0:
            assert 30 == Month(i).days_in(True) == Month(i).days_in()
        assert 29 == Month(2).days_in(True) and 28 == Month(2).days_in()

    def test_evaluate(self):
        month = Month(5)
        assert (1 < month and Month(1) < month
                and 1 <= month and Month(1) <= month
                and 1 != month and Month(1) != month)
        assert (10 > month and Month(10) > month
                and 10 >= month and Month(10) >= month
                and 10 != month and Month(10) != month)
        assert (5 == month and Month(5) == month
                and 5 >= month and Month(5) >= month
                and 5 <= month and Month(5) <= month)


class TestDates:
    mar15 = Date(2022, 3, 15)
    lstfeb = Date(2020, 2, 29)
    lastdec = Date(2022, 12, 31)
    term = Date(2022, 1, 12)
    feb_dates = [datetime.date(2020, 2, i) for i in range(1, 30)]

    def test_MONTH(self):
        assert self.mar15.MONTH == 3

    def test_MONTH_dates(self):
        assert self.lstfeb.MONTH_dates == self.feb_dates

    def test_copy(self):
        assert (self.mar15.copy() == self.mar15
                and self.mar15.copy() is not self.mar15)

    def test_to_dt_date(self):
        assert self.mar15.to_dt_date == datetime.date(2022, 3, 15)

    def test_to_datetime(self):
        assert (self.mar15.to_datetime(1, 0, 0)
                == datetime.datetime(2022, 3, 15, 1, 0, 0))

    def test_add_yrs(self):
        assert self.lstfeb.add_yrs(5) == Date(2025, 2, 28)

    def test_add_mths(self):
        assert self.lastdec.add_mths(2) == Date(2023, 2, 28)

    def test_add_days(self):
        assert self.term.add_days(56) == Date(2022, 3, 9)

    def test_add_weeks(self):
        assert self.term.add_wks(8) == Date(2022, 3, 9)

    def test_add(self):
        assert self.term.add(months=1, weeks=3, days=4) == Date(2022, 3, 9)

    def test_equal(self):
        assert (self.term == datetime.date(2022, 1, 12)
                and self.term == Date(2022, 1, 12))


class TestTerm:
    term1 = Term(datetime.date(2022, 1, 12), 1, 8)
    dates_in1 = term1.dates_in
    jan = [datetime.date(2022, 1, i) for i in range(12, 32)]
    feb = [datetime.date(2022, 2, i) for i in range(1, 29)]
    mar = [datetime.date(2022, 3, i) for i in range(1, 10)]
    act_dates_in1 = jan + feb + mar

    def test_stop(self):
        assert self.act_dates_in1[-1] == self.term1.stop

    def test_match_len(self):
        assert len(self.dates_in1) == len(self.act_dates_in1)

    def test_dates_in(self):
        for termdt, actdate in zip(self.dates_in1, self.act_dates_in1):
            assert termdt == actdate

    def test_dirname(self):
        assert self.term1.dirname == 'Term1'

    def test_markdown_filename(self):
        assert self.term1.markdown_filename == 'Term1-DueDates.md'


class TestDueDates:
    term = Term(datetime.date(2022, 1, 12), 1, 8)
    duedate = DueDays(term)
    due_dates = [datetime.date(2022, 1, 16), datetime.date(2022, 1, 18),
                 datetime.date(2022, 1, 23), datetime.date(2022, 1, 25),
                 datetime.date(2022, 1, 30), datetime.date(2022, 2, 1),
                 datetime.date(2022, 2, 6), datetime.date(2022, 2, 8),
                 datetime.date(2022, 2, 13), datetime.date(2022, 2, 15),
                 datetime.date(2022, 2, 20), datetime.date(2022, 2, 22),
                 datetime.date(2022, 2, 27), datetime.date(2022, 3, 1),
                 datetime.date(2022, 3, 6), datetime.date(2022, 3, 8)]

    def test_dates(self):
        assert self.duedate.dates == self.due_dates


class TestCourse:
    term2 = Term(datetime.date(2022, 3, 9), 2, 8)
    course = Course('CS197', 'Programming in HTML', term2)
    path = [WindowsPath('C:/Users/Graes/OneDrive/coursework/Term2/'
                        'CS197-Programming_in_HTML/W1-CS197/Discussions'),
            WindowsPath('C:/Users/Graes/OneDrive/coursework/Term2/'
                        'CS197-Programming_in_HTML/W1-CS197/Assignments'),
            WindowsPath('C:/Users/Graes/OneDrive/coursework/Term2/'
                        'CS197-Programming_in_HTML/W2-CS197/Discussions'),
            WindowsPath('C:/Users/Graes/OneDrive/coursework/Term2/'
                        'CS197-Programming_in_HTML/W2-CS197/Assignments'),
            WindowsPath('C:/Users/Graes/OneDrive/coursework/Term2/'
                        'CS197-Programming_in_HTML/W3-CS197/Discussions'),
            WindowsPath('C:/Users/Graes/OneDrive/coursework/Term2/'
                        'CS197-Programming_in_HTML/W3-CS197/Assignments'),
            WindowsPath('C:/Users/Graes/OneDrive/coursework/Term2/'
                        'CS197-Programming_in_HTML/W4-CS197/Discussions'),
            WindowsPath('C:/Users/Graes/OneDrive/coursework/Term2/'
                        'CS197-Programming_in_HTML/W4-CS197/Assignments'),
            WindowsPath('C:/Users/Graes/OneDrive/coursework/Term2/'
                        'CS197-Programming_in_HTML/W5-CS197/Discussions'),
            WindowsPath('C:/Users/Graes/OneDrive/coursework/Term2/'
                        'CS197-Programming_in_HTML/W5-CS197/Assignments'),
            WindowsPath('C:/Users/Graes/OneDrive/coursework/Term2/'
                        'CS197-Programming_in_HTML/W6-CS197/Discussions'),
            WindowsPath('C:/Users/Graes/OneDrive/coursework/Term2/'
                        'CS197-Programming_in_HTML/W6-CS197/Assignments'),
            WindowsPath('C:/Users/Graes/OneDrive/coursework/Term2/'
                        'CS197-Programming_in_HTML/W7-CS197/Discussions'),
            WindowsPath('C:/Users/Graes/OneDrive/coursework/Term2/'
                        'CS197-Programming_in_HTML/W7-CS197/Assignments'),
            WindowsPath('C:/Users/Graes/OneDrive/coursework/Term2/'
                        'CS197-Programming_in_HTML/W8-CS197/Discussions'),
            WindowsPath('C:/Users/Graes/OneDrive/coursework/Term2/'
                        'CS197-Programming_in_HTML/W8-CS197/Assignments')]

    def test_folders(self):
        assert (self.course.create_folders(Path.home() / 'OneDrive/coursework')
                == self.path)
