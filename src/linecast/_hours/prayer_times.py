"""The Islamic prayer times: Fajr to Isha, and the fast in Ramadan.

Not hours but marks. Fajr is the dawn prayer, at a depression of the
Sun that varies by convention; sunrise ends it. Dhuhr is the Sun's
transit. Asr is when a shadow has grown by the length of its object,
or twice that by the Hanafi school. Maghrib is sunset, and Isha is
nightfall at another depression, or a fixed interval after Maghrib
where the convention says so. The depressions are the conventions the
prayer-time apps offer, each named for the body that published it:
the Muslim World League's 18° and 17°, ISNA's 15° and 15°, Egypt's
19.5° and 17.5°, Umm al-Qura's 18.5° and ninety minutes, a hundred
and twenty in Ramadan, and the rest of the table below. The method
follows the country of the place shown by default, as the week's
first day does, and the frame names it.

Where the Sun never reaches the angle, as in a Nordic June, the
angle-based rule stands in: Fajr is as far before sunrise, and Isha
as far after sunset, as the angle's share of a sixty-degree night,
the rule PrayTimes and Aladhan apply by default. Imsak is ten minutes
before Fajr and is listed in Ramadan, when the fast from Fajr to
Maghrib is the day's shape and the corner counts it.

The tests check eight places on four dates against the Aladhan API
with the matching method, to the minute; the Umm al-Qura method
against its own Makkah timetable is the check still to add. A mosque's
card can differ by a minute or two: many publishers round Fajr down
and Maghrib up for caution.
"""

import math
from datetime import timedelta
from functools import lru_cache

from linecast._ephemeris import sun_declination, sun_depression_utc, sun_transit_utc
from linecast._hours import DayHours, Mark, elapsed, shift

HORIZON_DEG = 0.833
IMSAK_MINUTES = 10
RAMADAN = 9

# key → (name, fajr depression, isha: depression or ("min", after
# Maghrib, in Ramadan), maghrib depression)
METHODS = {
    "mwl": ("Muslim World League", 18.0, 17.0, HORIZON_DEG),
    "isna": ("Islamic Society of North America", 15.0, 15.0, HORIZON_DEG),
    "egypt": ("Egyptian General Authority of Survey", 19.5, 17.5, HORIZON_DEG),
    "makkah": ("Umm al-Qura University, Makkah", 18.5, ("min", 90, 120), HORIZON_DEG),
    "karachi": ("University of Islamic Sciences, Karachi", 18.0, 18.0, HORIZON_DEG),
    "tehran": ("Institute of Geophysics, University of Tehran", 17.7, 14.0, 4.5),
    "turkey": ("Diyanet İşleri Başkanlığı", 18.0, 17.0, HORIZON_DEG),
    "singapore": ("Majlis Ugama Islam Singapura", 20.0, 18.0, HORIZON_DEG),
    "jakim": ("Jabatan Kemajuan Islam Malaysia", 20.0, 18.0, HORIZON_DEG),
    "kemenag": ("Kementerian Agama Republik Indonesia", 20.0, 18.0, HORIZON_DEG),
    "france": ("Union des Organisations Islamiques de France", 12.0, 12.0, HORIZON_DEG),
    "russia": ("Spiritual Administration of Muslims of Russia", 16.0, 15.0, HORIZON_DEG),
}
METHOD_SHORT = {
    "mwl": "MWL", "isna": "ISNA", "egypt": "Egypt", "makkah": "Umm al-Qura",
    "karachi": "Karachi", "tehran": "Tehran", "turkey": "Diyanet",
    "singapore": "MUIS", "jakim": "JAKIM", "kemenag": "Kemenag",
    "france": "UOIF", "russia": "Russia",
}
SCHOOLS = ("shafii", "hanafi")

# Minutes a convention adds to its computed times for caution, the
# temkin the Diyanet prints into every Turkish timetable: sunrise
# earlier, the rest later.
_OFFSETS = {
    "turkey": {"sunrise": -7, "dhuhr": 5, "asr": 4, "maghrib": 7},
}

# The method a country's own authority publishes, or the one its
# mosques mostly print; the Muslim World League's angles elsewhere.
_COUNTRY_METHOD = {
    "US": "isna", "CA": "isna",
    "EG": "egypt", "SD": "egypt", "LY": "egypt", "SY": "egypt", "IQ": "egypt",
    "LB": "egypt", "JO": "egypt", "PS": "egypt",
    "SA": "makkah", "YE": "makkah", "BH": "makkah", "KW": "makkah",
    "QA": "makkah", "AE": "makkah", "OM": "makkah",
    "PK": "karachi", "IN": "karachi", "BD": "karachi", "AF": "karachi",
    "IR": "tehran",
    "TR": "turkey",
    "SG": "singapore",
    "MY": "jakim",
    "ID": "kemenag",
    "FR": "france",
    "RU": "russia",
}
# Where the Hanafi school's later Asr is the one printed.
_HANAFI_COUNTRIES = {"TR", "PK", "IN", "BD", "AF", "UZ", "KZ", "KG", "TJ",
                     "TM", "BA", "AL", "XK", "MK", "RU", "CN"}


def default_method(country):
    return _COUNTRY_METHOD.get((country or "").upper(), "mwl")


def default_school(country):
    return "hanafi" if (country or "").upper() in _HANAFI_COUNTRIES else "shafii"


def _local(dt_utc, tzinfo):
    if dt_utc is None:
        return None
    return dt_utc.astimezone(tzinfo) if tzinfo else dt_utc.astimezone()


def _asr_altitude_deg(lat, decl, factor):
    """The Sun's altitude when a shadow is *factor* object-lengths
    longer than at noon: cot(alt) = factor + tan|lat - decl|."""
    return math.degrees(math.atan(1.0 / (factor + math.tan(math.radians(abs(lat - decl))))))


def _angle_based(at, base, angle, night, before):
    """The angle-based rule for high latitudes: when the Sun never
    reaches the angle, or the moment lies further from sunrise or
    sunset than the angle's share of a sixty-degree night, take that
    share instead."""
    if night is None or base is None:
        return at
    portion = night * (angle / 60.0)
    if at is None or abs(elapsed(base, at)) > portion:
        return shift(base, -portion if before else portion)
    return at


def is_ramadan(local_date):
    from linecast._calendars.hijri import hijri_date
    return hijri_date(local_date)[1] == RAMADAN


@lru_cache(maxsize=64)
def prayer_times(local_date, lat, lng, tzinfo=None, method=None, country=None):
    """The day's prayer times at a place.

    *method* is a key of METHODS, or a school ('hanafi', 'shafii') to
    keep the country's method and change the Asr; None takes both from
    the country.
    """
    school = method if method in SCHOOLS else default_school(country)
    method = method if method in METHODS else default_method(country)
    _name, fajr_deg, isha_rule, maghrib_deg = METHODS[method]
    day = timedelta(days=1)

    def depression(date_, deg, evening):
        return _local(sun_depression_utc(date_, lat, lng, deg, evening, tzinfo), tzinfo)

    sunrise = depression(local_date, HORIZON_DEG, False)
    sunset = depression(local_date, HORIZON_DEG, True)
    next_sunrise = depression(local_date + day, HORIZON_DEG, False)
    prev_sunset = depression(local_date - day, HORIZON_DEG, True)
    night_before = elapsed(prev_sunset, sunrise) if sunrise and prev_sunset else None
    night_after = elapsed(sunset, next_sunrise) if next_sunrise and sunset else None

    transit = sun_transit_utc(local_date, lng, tzinfo)
    dhuhr = _local(transit, tzinfo)
    fajr = _angle_based(depression(local_date, fajr_deg, False), sunrise, fajr_deg,
                        night_before, before=True)
    maghrib = depression(local_date, maghrib_deg, True)
    ramadan = is_ramadan(local_date)
    if isinstance(isha_rule, tuple):
        _min, after, after_ramadan = isha_rule
        isha = (shift(maghrib, timedelta(minutes=after_ramadan if ramadan else after))
                if maghrib else None)
    else:
        isha = _angle_based(depression(local_date, isha_rule, True), sunset, isha_rule,
                            night_after, before=False)
    decl = sun_declination(transit)
    asr = depression(local_date, -_asr_altitude_deg(lat, decl, 2 if school == "hanafi" else 1),
                     True)

    offsets = _OFFSETS.get(method, {})
    imsak = shift(fajr, -timedelta(minutes=IMSAK_MINUTES)) if fajr and ramadan else None
    marks = []
    for key, at in (("imsak", imsak), ("fajr", fajr), ("sunrise", sunrise),
                    ("dhuhr", dhuhr), ("asr", asr), ("maghrib", maghrib),
                    ("isha", isha)):
        if at is not None:
            marks.append(Mark(key, shift(at, timedelta(minutes=offsets.get(key, 0)))))
    if "maghrib" in offsets and maghrib:
        maghrib = shift(maghrib, timedelta(minutes=offsets["maghrib"]))
    marks.sort(key=lambda m: m.at)
    variant = method if school == default_school(country) else f"{method}-{school}"
    return DayHours("islamic", local_date, fajr, maghrib, prev_sunset, next_sunrise,
                    None, marks, variant,
                    fast=(fajr, maghrib) if ramadan and fajr and maghrib else None)
