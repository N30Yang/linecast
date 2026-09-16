"""The day read in a tradition's hours: the frame the tables fill in.

The moon reads the Moon through a tradition's calendar; sunshine reads
the Sun through a tradition's hours. Every system worth having is one
shape. A day has two edges set by the Sun, the time between them is
divided into a fixed number of equal parts, and named marks fall along
it. The night, from one day's end to the next day's start, is divided
the same way. Only the edges, the count, and the names differ:

- halachic (zmanim): twelve sha'ot zmaniyot, sunrise to sunset by
  the Gr"a, seventy-two minutes either side by the Magen Avraham;
- roman (roman): twelve horae by day, four vigiliae by night;
- japanese (wadokei): six koku each, the edges at the Sun 7°21′40″
  below the horizon;
- islamic (prayer_times): no equal hours at all, only the marks, by
  a method that follows the country, and the fast in Ramadan.

Each tradition is a module beside this one, and answers `day_hours`
for a civil date at a place with a DayHours: the edges, the count, and
the marks. This module holds the model, the reading of a moment
against it (which hour, how far in, how long the hour is), and the
resolver that picks a system from the flag or the saved setting.
"""

from dataclasses import dataclass, field
from datetime import date, datetime

HOURS_SYSTEMS = ("halachic", "roman", "japanese", "islamic")


@dataclass(frozen=True)
class Mark:
    """A named moment of the day: alot hashachar, hora tertia, Asr."""
    key: str
    at: datetime          # aware, in the place's own zone


@dataclass
class DayHours:
    """One civil date read in one system.

    The edges are aware local datetimes, or None where the Sun never
    gets there: a polar season at the horizon, a Nordic June at 16.1°.
    `divisions` is the number of equal hours between the day's edges,
    or None for a system that keeps marks only; the night has its own
    count, `night_divisions`, where it differs (Rome's four vigiliae
    against twelve horae). `variant` names the opinion or method the
    table used. `fast` is (start, end) on a day of fasting, Fajr to
    Maghrib in Ramadan, or None.
    """
    system: str
    date: date
    day_start: datetime | None
    day_end: datetime | None
    prev_day_end: datetime | None     # yesterday's, for the night before
    next_day_start: datetime | None   # tomorrow's, for the night after
    divisions: int | None
    marks: list = field(default_factory=list)
    variant: str | None = None
    night_divisions: int | None = None
    fast: tuple | None = None

    def __post_init__(self):
        if self.night_divisions is None:
            self.night_divisions = self.divisions


@dataclass(frozen=True)
class Reading:
    """Where a moment falls: hour *index* (from 0) of the day or the
    night, *fraction* of the way through it, and the hour's length."""
    night: bool
    index: int
    fraction: float
    hour_seconds: float
    start: datetime
    end: datetime


def resolve_hours(flag):
    """(system, variant) in force: the --hours flag, else the saved
    setting, else (None, None). `auto` is none: the calendars follow
    the language because their readers know the Moon through them,
    and no system of hours follows a language that way. A hyphen in
    the name separates the tradition from an opinion or method within
    it: halachic-mga is the halachic hours by the Magen Avraham."""
    name = flag
    if name is None:
        from linecast._config import saved_hours
        name = saved_hours()
    if name is None or name == "none":
        return None, None
    system, _hyphen, variant = name.partition("-")
    return system, (variant or None)


def _aware(now, tzinfo):
    """*now* as an aware datetime, in *tzinfo* or the machine's zone."""
    if now.tzinfo is None:
        return now.astimezone(tzinfo) if tzinfo else now.astimezone()
    return now


def day_hours(system, local_date, lat, lng, tzinfo=None, variant=None,
              country=None):
    """The table's answer for a civil date at a place, or None for a
    system this build does not know."""
    if system == "halachic":
        from linecast._hours.zmanim import zmanim
        return zmanim(local_date, lat, lng, tzinfo, opinion=variant)
    if system == "roman":
        from linecast._hours.roman import roman_hours
        return roman_hours(local_date, lat, lng, tzinfo)
    if system == "japanese":
        from linecast._hours.wadokei import wadokei
        return wadokei(local_date, lat, lng, tzinfo)
    if system == "islamic":
        from linecast._hours.prayer_times import prayer_times
        return prayer_times(local_date, lat, lng, tzinfo, method=variant,
                            country=country)
    return None


def hours_now(system, now, lat, lng, tzinfo=None, variant=None, country=None):
    """The DayHours for the civil date of *now*, and *now* made aware."""
    now = _aware(now, tzinfo)
    return day_hours(system, now.date(), lat, lng, tzinfo, variant, country), now


def reading(hours, now):
    """Where *now* falls in the system's hours, or None when the system
    keeps no hours or the Sun never made the edges that day."""
    if hours is None or not hours.divisions:
        return None
    now = _aware(now, hours.day_start.tzinfo if hours.day_start else None)
    spans = (
        (False, hours.day_start, hours.day_end),
        (True, hours.day_end, hours.next_day_start),
        (True, hours.prev_day_end, hours.day_start),
    )
    for night, start, end in spans:
        if start is None or end is None or not start <= now < end:
            continue
        count = hours.night_divisions if night else hours.divisions
        hour = (end - start) / count
        elapsed = (now - start) / hour
        index = min(count - 1, int(elapsed))
        return Reading(night, index, elapsed - index, hour.total_seconds(),
                       start, end)
    return None


def next_mark(hours, now):
    """The first mark still to come, or None once the day's are past."""
    if hours is None:
        return None
    now = _aware(now, hours.day_start.tzinfo if hours.day_start else None)
    for mark in hours.marks:
        if mark.at > now:
            return mark
    return None


def fmt_duration(seconds):
    """'1h 12m', '22m', '1h': the plain form the countdowns use."""
    minutes = int(round(seconds / 60))
    h, m = divmod(minutes, 60)
    if h and m:
        return f"{h}h {m:02d}m"
    if h:
        return f"{h}h"
    return f"{m}m"


def last_mark(hours, now):
    """The latest mark already past, or None before the day's first."""
    if hours is None:
        return None
    now = _aware(now, hours.day_start.tzinfo if hours.day_start else None)
    passed = [m for m in hours.marks if m.at <= now]
    return passed[-1] if passed else None
