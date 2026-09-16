"""Swahili time, saa za Kiswahili: twelve hours of day and twelve of night.

Swahili counts the hours of the day from its start and the hours of
the night from theirs. Seven in the morning is saa moja asubuhi, the
first hour of the day, and seven in the evening saa moja usiku, the
first of the night; noon and midnight are saa sita, the sixth. It is
how the time is told in Swahili now, in speech and in print: the
newspapers write "saa 4:00 asubuhi" for ten in the morning.

The count began at sunrise, and near the equator sunrise hardly moves:
in Dar es Salaam, Mombasa, and Nairobi it comes between about 05:55
and 06:45 all year. So the day's edges are the clock's six o'clock, as
everyone who keeps Swahili time keeps them, not the Sun's, and each
hour is an hour of the clock. The reading follows the wall clock of
the place shown, so a clock change moves it as it moves the digits.

The word after the hour says which part of the day it is, and the
parts are the ones CLDR records for Swahili and the textbooks teach:
alfajiri from four to seven in the morning, asubuhi to noon, mchana
to four, jioni to seven, and usiku through the night. The written form
is the newspapers': the Swahili hour, the minutes in two digits, and
the part of the day.
"""

from datetime import datetime, time, timedelta

from linecast._hours import DayHours

# (from hour, name), in order through the civil day: CLDR's dayPeriods
# for sw, which the University of Kansas lesson on saa agrees with hour
# for hour.
PERIODS = ((0, "usiku"), (4, "alfajiri"), (7, "asubuhi"),
           (12, "mchana"), (16, "jioni"), (19, "usiku"))


def _at(local_date, hour, tzinfo):
    dt = datetime.combine(local_date, time(hour))
    return dt.replace(tzinfo=tzinfo) if tzinfo else dt.astimezone()


def swahili_hours(local_date, tzinfo=None):
    """The day from six in the morning to six in the evening, on the
    clock, twelve hours each way. There are no marks: the hours are
    the clock's own, and the line above has sunrise and sunset."""
    day = timedelta(days=1)
    return DayHours("swahili", local_date,
                    _at(local_date, 6, tzinfo), _at(local_date, 18, tzinfo),
                    _at(local_date - day, 18, tzinfo), _at(local_date + day, 6, tzinfo),
                    12, [], None, wall_clock=True)


def period(hour):
    """The part of the day a civil hour falls in: 'asubuhi' at nine."""
    name = PERIODS[0][1]
    for start, word in PERIODS:
        if hour >= start:
            name = word
    return name


def saa(local):
    """A local wall-clock time in Swahili time: 'saa 7:13 usiku' at
    01:13, 'saa 12:14 alfajiri' at 06:14, 'saa 6:00 mchana' at noon."""
    hour = (local.hour - 6) % 12 or 12
    return f"saa {hour}:{local.minute:02d} {period(local.hour)}"
