"""Module for performing date arithmetic and comparison."""
from enum import Enum
from pathlib import Path
import datetime
from calendar import Calendar


def dropdates(dates_list: list, before: datetime.date = None,
              after: datetime.date = None
              ) -> list:
    """Modifies dates so it contains only dates from before to after.

    If neither before nor after are provided, dates list is unchanged.
    Written to drop dates from the generator returned by
    calendar.Calendar.itermonthdates() to aid in subtracting and adding dates.

    Args:
        dates (list): A list of datetime.dates
        before (datetime.date, optional): Drop dates before this date.
            Defaults to None.
        after (datetime.date, optional): Drop dates after this date.
            Defaults to None.

    Returns:
        list: Containing the dates from before to after.
    """
    if not before and not after:
        print(f'No dates dropped, because {before = !r} and {after = !r}.')
        return dates_list
    # Dates must be chronological.  If before is provided, program drops dates
    # until it reaches a date that is equal to or greater than before.  If
    # after is provided, program stores dates in monthdates until reaching a
    # date that is greater than after.
    dates_list.sort()
    monthdates = []
    for day in dates_list:
        if before and before > day:
            continue
        elif not before or before <= day:
            if after and after < day:
                break
            if day not in monthdates:
                monthdates.append(day)
    return monthdates


class Validator:

    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.set_obj_name(obj)
        if isinstance(value, getattr(obj, '__class__')):
            value = value._value
        self.validate(obj, value)
        setattr(obj, self.private_name, value)

    def set_obj_name(self, obj: object) -> None:
        """Obtain the name of the object whose value is being validated.

        Args:
            obj (object): The object whose value is being tested.
        """
        if '_name' in dir(obj):
            self._obj_name = obj._name
        else:  # Needed for Enum subtype dates
            self._obj_name = str(obj.__class__).split("'")[1]

    def validate(self, obj, value) -> None:
        """Reject non-integer value.

        Args:
            obj (object): The object whose value is being tested.
            value (int): The value being tested.

        Raises:
            TypeError: If value is not an integer.
        """
        if not isinstance(value, int):
            raise TypeError(f'{self._obj_name} value cannot be {type(value)}.')
        if not (self._obj_name == 'Weekday' or self._obj_name == 'Month'):
            self.validate_int(value)

    def validate_int(self, value: int) -> None:
        """Reject value less than 1 and Day.value greater than 31.

        Args:
            obj (object): The object whose value is being tested.
            value (int): The value being tested.

        Raises:
            ValueError: If value is less than 1 or a Day object value
                is greater than 31.
        """
        if value < 1:
            raise ValueError(f'The value of {self._obj_name} cannot be less'
                             f' than 1. Value provided: {value}.')
        # Ensure integer value provided for a Day object is less than 32.
        if self._obj_name == 'Day' and value > 31:
            raise ValueError(f'The value of {self._obj_name} cannot be greater'
                             f' than 31. Value provided: {value}.')


class DateParts:
    _module = Path(__file__).stem
    value = Validator()
    _name = 'DatePart'

    def __init__(self, name, value: int = 0) -> None:
        self._name = name
        self.value = value

    def evaluate(self, __o: object, operator: str):
        """Used with dunder operators to reduce repetition.

        Args:
            __o (object): The object being 'operated' to self
            operator (str): The operator ('+', '-', etc.)

        Returns:
            Any: The evaluation of self {operator} Other.
        """
        if isinstance(__o, int):
            return eval(f'{self._value} {operator} {__o}')
        if isinstance(__o, self.__class__):
            return eval(f'{self._value} {operator} {__o._value}')
        if isinstance(__o, str):
            if str.isdecimal():
                return eval(f'{self._value} {operator} {int(__o)}')
        return NotImplemented

    def __repr__(self) -> str:
        return f'{self._module}.{self._name}({self._value})'

    def __str__(self) -> str:
        if isinstance(self, (Weekday, Month)):
            return f'{self.name.title()}'
        return f'{self._value}'

    def __add__(self, __o: object) -> int:
        return self.evaluate(__o, '+')

    def __sub__(self, __o: object) -> int:
        return self.evaluate(__o, '-')

    def __truediv__(self, __o: object) -> float:
        return self.evaluate(__o, '/')

    def __floordiv__(self, __o: object) -> int:
        return self.evaluate(__o, '//')

    def __mod__(self, __o: object) -> int:
        return self.evaluate(__o, '%')

    def __lt__(self, __o: object) -> bool:
        return self.evaluate(__o, '<')

    def __le__(self, __o: object) -> bool:
        return self.evaluate(__o, '<=')

    def __eq__(self, __o: object) -> bool:
        return self.evaluate(__o, '==')

    def __ne__(self, __o: object) -> bool:
        return self.evaluate(__o, '!=')

    def __gt__(self, __o: object) -> bool:
        return self.evaluate(__o, '>')

    def __ge__(self, __o: object) -> bool:
        return self.evaluate(__o, '>=')


class Year(DateParts):

    def __init__(self, value) -> None:
        """Object representing a calendar year. Effectively an integer.

        Args:
            value (int): The year. e.g., 1948

        Raises:
            TypeError: Raised if argument provided for value is not an int
            or Year.

        Examples
        >>> Year(2021)
        dates.Year(2021)
        >>> Year(Year(2021))
        dates.Year(2021)
        """
        super().__init__('Year', value)

    @property
    def isleap(self) -> bool:
        """True if Year is a leap year. Otherwise False.

        Examples:
        >>> Year(2020).isleap
        True
        >>> Year (2021).isleap
        False
        """
        return self._value % 4 == 0 and (self._value % 100 != 0
                                         or self._value % 400 == 0)


class Month(DateParts, Enum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12

    def __init__(self, value: int) -> None:
        """Object representing a calendar month.

        Args:
            value (int): The month number. e.g., 4

        Raises:
            TypeError: Raised if argument provided for value is not an int or
            Month.

        Examples:
        >>> Month(10)
        dates.Month(10)
        >>> Month(Month(10))
        dates.Month(10)
        >>> Month(10).name
        'OCTOBER'
        >>> Month(10).value
        10
        """
        # self._name = 'Month'
        super().__init__('Month', value)
        self.year = 0
        self.years = 0

    def set_missing_yr(self, year: int = None) -> None:
        if year is not None:
            self.year = year
        if self.year <= 0:
            self.year = input('Please provide a year: ')
            print('To avoid this prompt, set the year with'
                  f' Month({self.value}).year = {self.year}.')

    @classmethod
    def from_date(cls, date: datetime.date):
        """Obtain a Month representing the month of date.

        Sets month.year.

        Args:
            date (datetime.date): A date

        Returns:
            Self: A new Month representing date's month.

        Examples:
        >>> amonth = Month.from_date(datetime.date(2021, 10, 2))
        >>> amonth
        dates.Month(10)
        >>> amonth.year
        2021
        >>> amonth = Month.from_date(Date(2020, 5, 3))
        >>> amonth
        dates.Month(5)
        >>> amonth.year
        2020
        """
        new_month = cls(date.month)
        new_month.year = date.year
        return new_month

    @classmethod
    def monthloop(cls, to_convert: int):
        """Converts to_convert to a Month, setting years as needed.

        Args:
            to_convert (int): A number to convert to a Month and years

        Raises:
            TypeError: If to_convert is not an integer.
            NotImplementedError: If to_convert is less than 1.

        Returns:
            Month: A Month object with years set.

        Examples:
        >>> amonth = Month.monthloop(36)
        >>> amonth
        dates.Month(12)
        >>> amonth.years
        2
        >>> amonth = Month.monthloop(37)
        >>> amonth
        dates.Month(1)
        >>> amonth.years
        3
        """
        # [ ] Implement when to_convert is less than 1.
        if not isinstance(to_convert, int):
            raise TypeError('to_convert must be an int not a'
                            f' {type(to_convert)}')
        if to_convert < 1:
            raise NotImplementedError('to_convert must be greater than 0.')
        if to_convert <= 12:
            month = to_convert
            years = 0
        else:
            month = 12 if to_convert % 12 == 0 else to_convert % 12
            years = (to_convert // 12 - 1 if to_convert % 12 == 0
                     else to_convert // 12)
        new_month = Month(month)
        new_month.years = years
        return new_month

    def maxdays(self) -> int:
        """Returns the last number day in the Month.

        Examples:
        >>> Month(10).maxdays()
        31
        >>> Month(4).maxdays()
        30
        """
        month_name = self.name
        if month_name in {'APRIL', 'JUNE', 'SEPTEMBER', 'NOVEMBER'}:
            return 30
        if not month_name == 'FEBRUARY':
            return 31
        return self.maxdays_feb()

    def maxdays_feb(self, year: int = None) -> int:
        """Returns the last number day in the Month of Feb in year.

        Examples:
        >>> Month(2).maxdays_feb(2020)
        29
        >>> Month(2).maxdays_feb(2021)
        28
        """
        self.set_missing_yr(year)
        _Year = Year(self.year)
        if _Year.isleap:
            return 29
        return 28

    def dates_in(self, year: int = None) -> list[datetime.date]:
        # [ ] Fix to be similar to maxdays_feb
        """Obtain datetime.date objects for all days in the Month in year.

        Sets Month.year if it needs to do so.

        Args:
            year (Year | int): The year for the month. February necessitates.

        Returns:
            list[datetime.date]: A list of all dates in the Month in year.
        """
        # [ ] Get rid to datetime.date when implement lt,etc. in Date.
        month = self.value
        if month != 2:
            self.set_missing_yr(year)
        year = self.year
        max_days = self.maxdays()
        dates = list(Calendar().itermonthdates(year, month))
        before = datetime.date(year, month, 1)
        after = datetime.date(year, month, max_days)
        return dropdates(dates, before, after)


class Day(DateParts):

    def __init__(self, value: int = 0) -> None:
        """Returns an object representing a calendar day.

        Args:
            value (int): The day number.

        Examples:
        >>> Day(5)
        dates.Day(5)
        >>> Day(Day(5))
        dates.Day(5)
        """
        super().__init__('Day', value)


class Weekday(DateParts, Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    def __init__(self, value: int = 0) -> None:
        """Returns an object representing a day of the week (Mon - Sun).

        Args:
            value (int): The number value for the day of the week.
                Week starts on Monday (0), and ends on Sunday (6).

        Examples:
        >>> Weekday(5)
        dates.Weekday(5)
        >>> Weekday(Weekday(5))
        dates.Weekday(5)
        >>> Weekday(5).name
        'SATURDAY'
        >>> Weekday(0).name
        'MONDAY'
        """
        super().__init__('Weekday', value)
        self.weeks = 0

    @classmethod
    def weekloop(cls, to_convert: int):
        # [ ] Unclear how this helps anything/is useful.
        """Obtains a new Weekday and, as needed, sets weeks.

        Week start is 0 aka Monday. to_covert is Monday-relative.

        Args:
            to_convert (int): The number to be converted to a Weekday.

        Returns:
            A new Weekday whose attribute weeks is set to the number of weeks
            representing to_convert.

        Examples:
        >>> aweekday = Weekday.weekloop(14)
        >>> aweekday
        dates.Weekday(0)
        >>> aweekday.weeks
        2
        >>> aweekday = Weekday.weekloop(15)
        >>> aweekday
        dates.Weekday(1)
        >>> aweekday.weeks
        2
        """
        weekday = to_convert % 7
        weeks = to_convert // 7
        new_weekday = Weekday(weekday)
        new_weekday.weeks = weeks
        return new_weekday


class Date:
    _Year = Year(1970)
    _Month = Month(1)
    _Day = Day(1)
    _Weekday = Weekday(3)
    _name = 'Date'

    def __init__(self, year: int = datetime.date.today().year,
                 month: int = 1, day: int = 1
                 ) -> None:
        """An object representing a date. Similar to datetime.date.

        Args:
            year (int, optional): The date's calendar year.
                Defaults to datetime.date.today().year.
            month (int, optional): The date's calendar month. Defaults to 1.
            day (int, optional): The dates calendar day. Defaults to 1.

        Examples:
        >>> Date(2020, 2, 10)
        dates.Date(2020, 2, 10)
        >>> Date(1984, 6, 30)
        dates.Date(1984, 6, 30)
        """
        self.year = year
        self.month = month
        self.day = day
        self.weekday = self.to_dt_date.weekday()
        self.dates_to_added_days = None

    def __repr__(self) -> str:
        return f'dates.Date({self.year}, {self.month}, {self.day})'

    def __str__(self) -> str:
        return f'{self._Month.name.capitalize()} {self.day}, {self.year}'

    def validate_day(self):
        if self.day > self.maxday:
            raise ValueError(f'{self.day = !r} higher than the number of days'
                             f' in {self._Month.name} ({self.maxday}).')

    @property
    def year(self) -> int:
        """The year value.

        Examples:
        >>> Date(2010, 1, 7).year
        2010
        >>> Date(1984, 1, 6).year
        1984
        """
        return self._Year.value

    @year.setter
    def year(self, value: int) -> None:
        """Set the value of year.

        Examples:
        >>> adate = Date(2010, 1, 7)
        >>> adate.year = 2011
        >>> adate.year
        2011
        """
        self._Year = Year(value)

    @property
    def month(self) -> int:
        """The month value.

        Examples:
        >>> Date(2010, 1, 7).month
        1
        >>> Date(1984, 2, 6).month
        2
        """
        return self._Month.value

    @month.setter
    def month(self, value: int) -> None:
        """Set the value of month.

        Examples:
        >>> adate = Date(2010, 1, 7)
        >>> adate.month = 5
        >>> adate
        dates.Date(2010, 1, 5)
        >>> adate = Date(2010, 3, 31)
        >>> adate.month = 2
        >>> adate
        dates.Date(2010, 2, 28)
        >>> adate.day
        28
        """
        # date_month = Month(value)
        # date_month.year = self.year
        date_month = Month(value)
        date_month.year = self.year
        self._Month = date_month
        self.day = self.day

    @property
    def maxday(self) -> int:
        """The last day of the month of Date's month.

        Examples:
        >>> Date(2020, 2, 1).maxday
        29
        >>> Date(2021, 2, 1).maxday
        28
        >>> Date(2020, 4, 5).maxday
        30
        >>> Date(2020, 3, 2).maxday
        31
        """
        if self.month == 2:
            return self._Month.maxdays_feb(self.year)
        return self._Month.maxdays()

    @property
    def month_dates(self) -> list[datetime.date]:
        """Obtain datetime.date objs for every day in Date's month.

        Returns:
            list[datetime.date]: All the dates in Date's month.
        """
        return self._Month.dates_in(self.year)

    @property
    def day(self) -> int:
        """The day value.

        Examples:
        >>> Date(2010, 1, 7).day
        7
        >>> Date(1984, 2, 25).day
        25
        """
        return self._Day.value

    @day.setter
    def day(self, value: int) -> None:
        """Set the value of day.

        Examples:
        >>> adate = Date(2010, 1, 7)
        >>> adate.day = 5
        >>> adate
        dates.Date(2010, 1, 5)
        >>> adate = Date(2010, 3, 31)
        >>> adate.day= 2
        >>> adate
        dates.Date(2010, 3, 2)
        >>> adate.day
        2
        """
        self.validate_day()
        self._Day = Day(value)

    @property
    def weekday(self) -> int:
        return self._Weekday.value

    @weekday.setter
    def weekday(self, value: int) -> None:
        self._Weekday = Weekday(value)

    @property
    def to_dt_date(self) -> datetime.date:
        """Convert the Date to a datetime.date object."""
        return datetime.date(self.year, self.month, self.day)

    def to_datetime(self, hour: int, minute: int, second: int):
        """Convert the Date to a datetime.datetime object.

        Args:
            hour: the hour part of a time of day.
            minute: the minute part of a time of day.
            second: the second part of a time of day.
        """
        return datetime(self.year, self.month, self.day,
                        hour=hour, minute=minute, second=second)

    def copy(self):
        """Return a new Date that is a copy of Date."""
        return Date(self.year, self.month, self.day)

    def add_yrs(self, years: int = 0):
        """Obtain a new Date that is years number of years after the Date.

        Args:
            years (int, optional): The number of years to add to the Date.
                Defaults to 0.

        Returns:
            Date: A new Date that is years number of years after the Date.
        """
        return Date(self.year + years, self.month, self.day)

    def add_mths(self, months: int = 0):
        """Obtain a new Date that is months number of months after the Date.

        Args:
            months (int, optional): The number of months to add to the Date.
                Defaults to 0.

        Returns:
            Date: A new Date that is months number of months after the Date.
        """
        new_month = Month.monthloop(self._Month + months)
        if new_month.years:
            return Date(self.year + new_month.years, new_month, self.day)
        return Date(self.year, new_month, self.day)

    def add_days(self, days: int = 0):
        # [ ] Create a more memory efficient way to do this...
        """Obtain a new Date that is days number of days after the Date.

        Calculates by obtaining all of the dates from Date to the end of the
        month, and then all the dates of subsequent months until the number
        of dates collected are equal or greater to days.

        Args:
            days (int, optional): The number of days to add to the Date.
                Defaults to 0.

        Returns:
            Date: A new Date that is days number of days after the Date.
        """
        if isinstance(days, Day):
            days = days.value
        # Obtain all dates in Date's month from Date to the end of the month.
        dates = dropdates(self.month_dates, before=self)
        rolling_mth_date = self.copy()
        # Calculates by obtaining all of the dates from Date to the end of the
        # month, and then all the dates of subsequent months until the number
        # of dates collected are equal or greater to days.
        while len(dates) < days:
            rolling_mth_date = rolling_mth_date.add_mths(1)
            dates.extend(rolling_mth_date.month_dates)
        # The result of adding days to Date is in the dates list at an index
        # that is equal to days. (Similar to looking at a calendar and
        # manually counting up to a date)
        last_date = dates[days]
        self.dates_to_added_days = dropdates(dates, self, last_date)
        # Convert the datetime.date to Date.
        return Date(last_date.year, last_date.month, last_date.day)

    def add_wks(self, weeks: int = 0):
        """Obtain a new Date that is weeks number of weeks after the Date.

        Obtained by using add_days(weeks * 7)

        Args:
            weeks (int, optional): The number of weeks to add to the Date.
                Defaults to 0.

        Returns:
            Date: A new Date that is days number of days after the Date.
        """
        if isinstance(weeks, Weekday):
            weeks = weeks.value
        return self.add_days(weeks * 7)

    def add(self, *, years: int = 0, months: int = 0, weeks: int = 0,
            days: int = 0):
        """Add the given number of years, months, weeks, and/or days to Date.

        A interface to add_yrs, add_mths, add_wks, and add_days allowing all
        to be used in one method rather.

        Args:
            years (int, optional): Number of years to add to Date.
                Defaults to 0.
            months (int, optional): Number of months to add to Date.
                Defaults to 0.
            weeks (int, optional): Number of weeks to add to Date.
                Defaults to 0.
            days (int, optional): Number of days to add to Date.
                Defaults to 0.

        Returns:
            Date: A new date occuring the given number of years, months,
                weeks, and/or days after the Date.
        """
        # [ ]: Test the resulting day of the month. I want this to keep the
        # day of the month the same as much as possible.  Main concern: if
        # adding from 31 and one step is a month with < 31 days, but final
        # result has 31 days, then result should be the 31st day of the month.
        day_after = {'days': 0, 'weeks': 0, 'months': 0, 'year': 0}
        # new_date updates with each step to ensure all are added together.
        new_date = None
        # Addition starts from the top which is intended to retain Date's day
        # of the month if possible.
        if years:
            if new_date:
                new_date = new_date.add_yrs(years)
            else:
                new_date = self.add_yrs(years)
            day_after['year'] = new_date.day
        if months:
            if new_date:
                new_date = new_date.add_mths(months)
            else:
                new_date = self.add_mths(months)
            day_after['months'] = new_date.day
        if weeks:
            if new_date:
                new_date = new_date.add_wks(weeks)
            else:
                new_date = self.add_wks(weeks)
            day_after['weeks'] = new_date.day
        if days:
            if new_date:
                new_date = new_date.add_days(days)
            else:
                new_date = self.add_days(days)
            day_after['days'] = new_date.day
        return new_date

    def __add__(self, __o: datetime.date | Year | Month | Weekday | Day):
        """Operator + version of add, add_yrs, add_mths, add_wkds, add_days."""
        # [ ] Adjust. It's not intuitive to allow adding Month, Day, or Weekday
        if isinstance(__o, datetime.date | Date):
            return self.add(years=__o.year, months=__o.month, days=__o.day)
        if isinstance(__o, Year):
            raise TypeError(
                f'Use Date.add_yrs({__o.value}) or Dates.add(years='
                f'{__o.value}) to add years to a Date.')
        if isinstance(__o, Month):
            raise TypeError(
                f'Use Date.add_mths({__o.value}) or Dates.add(months='
                f'{__o.value}) to add months to a Date.')
        if isinstance(__o, Weekday):
            raise TypeError(
                f'Use Date.add_wks({__o.value}) or Dates.add(weeks='
                f'{__o.value}) to add weeks to a Date.')
        if isinstance(__o, Day):
            raise TypeError(
                f'Use Date.add_days({__o.value}) or Dates.add(days='
                f'{__o.value}) to add weeks to a Date.')
        raise NotImplementedError(
            'Can only add datetime.date and dates.Date to dates.Date.')

    def __lt__(self, __o: datetime.date) -> bool:
        if not isinstance(__o, datetime.date | Date):
            raise NotImplementedError(
                'Can only compare datetime.date or dates.Date to dates.Date.')
        if self.year > __o.year:
            return False
        elif self.year < __o.year:
            return True

        if self.month > __o.month:
            return False
        elif self.month < __o.month:
            return True

        if self.day >= __o.day:
            return False
        elif self.day < __o.day:
            return True

    def __le__(self, __o: datetime.date) -> bool:
        if not isinstance(__o, datetime.date | Date):
            raise NotImplementedError(
                'Can only compare datetime.date or dates.Date to dates.Date.')
        if self.year > __o.year:
            return False
        elif self.year < __o.year:
            return True

        if self.month > __o.month:
            return False
        elif self.month < __o.month:
            return True

        if self.day > __o.day:
            return False
        elif self.day <= __o.day:
            return True

    def __eq__(self, __o: object):
        if not isinstance(__o, datetime.date | Date):
            raise NotImplementedError(
                'Can only compare datetime.date or dates.Date to dates.Date.')
        if isinstance(__o, datetime.date | Date):
            return (self.year == __o.year and self.month == __o.month
                    and self.day == __o.day)

    def __ne__(self, __o: object):
        if not isinstance(__o, datetime.date | Date):
            raise NotImplementedError(
                'Can only compare datetime.date or dates.Date to dates.Date.')
        return not self.__eq__(__o)

    def __gt__(self, __o: datetime.date):
        if not isinstance(__o, datetime.date | Date):
            raise NotImplementedError(
                'Can only compare datetime.date or dates.Date to dates.Date.')
        if self.year < __o.year:
            return False
        elif self.year > __o.year:
            return True

        if self.month < __o.month:
            return False
        elif self.month > __o.month:
            return True

        if self.day <= __o.day:
            return False
        elif self.day > __o.day:
            return True

    def __ge__(self, __o: datetime.date):
        if not isinstance(__o, datetime.date | Date):
            raise NotImplementedError(
                'Can only compare datetime.date or dates.Date to dates.Date.')
        if self.year < __o.year:
            return False
        elif self.year > __o.year:
            return True

        if self.month < __o.month:
            return False
        elif self.month > __o.month:
            return True

        if self.day < __o.day:
            return False
        elif self.day >= __o.day:
            return True


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    def tests(item):
        print(item)
        print(f'\t{item = !r}')
        print(f'\t{item._name = !r}')
        if isinstance(item, (Weekday, Month)):
            print(f'\t{item.name = !r}')
            print(f'\t{item.value = !r}')

        item + 2
        item - 2
        item / 1
        item // 2
        item % 2
        item < 2
        item > 2
        item <= 2
        item >= 2
        item == 2
        item != 2

    def testDates(item):
        today = datetime.date.today()
        print(item)
        print(f'\t{item = !r}')
        print(f'\t{item._name = !r}')
        # item.add(months=2)
        # item.add(days=5)
        # item.add(weeks=5)
        # item + Month(2)
        item < Date(today.year, today.month, today.day)
        item > Date(today.year, today.month, today.day)
        item <= Date(today.year, today.month, today.day)
        item >= Date(today.year, today.month, today.day)
        item == Date(today.year, today.month, today.day)
        item != Date(today.year, today.month, today.day)
        item < today
        item > today
        item <= today
        item >= today
        item == today
        item != today

    # tests(Year(Year(1988)))
    # for i in range(1, 13):
    #     tests(Month(i))
    # for i in range(1, 32):
    #     tests(Day(i))
    # for i in range(7):
    #     tests(Weekday(i))

    # for i in range(1, 13):
    #     for j in range(2, 22, 10):
    #         testDates(Date(2020, j, i))
    #         testDates(Date(2021, j, i))
