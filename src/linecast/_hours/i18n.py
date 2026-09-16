"""The names the traditional hours go by, in each language.

The zmanim are transliterated in every language, as the Hebrew months
are, with the Hebrew itself kept for `--json`. Latin is Latin
everywhere. The Edo hours keep their kanji in Japanese and take the
bell count and the animal's hour elsewhere. The prayer names are
transliterated, with Indonesian's own spellings, as the Hijri months
have theirs.

Each mark has a short name for the line under the chart and a full
name for `--json` and the help. Names that are the same in every
language live in the English table and fall through `lookup`.
"""

from linecast._i18n import lang_of, lookup

# key → (short, full, hebrew)
_ZMANIM = {
    "alot": ("alot", "alot hashachar", "עלות השחר"),
    "misheyakir": ("misheyakir", "misheyakir", "משיכיר"),
    "sunrise": ("sunrise", "sunrise", "הנץ החמה"),
    "shema": ("Shema", "sof zman Shema", "סוף זמן קריאת שמע"),
    "tefillah": ("Tefillah", "sof zman Tefillah", "סוף זמן תפילה"),
    "chatzot": ("chatzot", "chatzot", "חצות"),
    "mincha_gedola": ("mincha gedola", "mincha gedola", "מנחה גדולה"),
    "mincha_ketana": ("mincha ketana", "mincha ketana", "מנחה קטנה"),
    "plag": ("plag", "plag hamincha", "פלג המנחה"),
    "candles": ("candles", "candle lighting", "הדלקת נרות"),
    "sunset": ("sunset", "sunset", "שקיעה"),
    "tzeit": ("tzeit", "tzeit hakochavim", "צאת הכוכבים"),
    "chatzot_halayla": ("chatzot halayla", "chatzot halayla", "חצות הלילה"),
}

# The Roman marks: key → (short, full). Latin in every language.
_ROMAN = {
    "hora_tertia": ("tertia", "hora tertia"),
    "hora_sexta": ("sexta", "hora sexta"),
    "hora_nona": ("nona", "hora nona"),
    "vigilia_secunda": ("vigilia II", "vigilia secunda"),
    "vigilia_tertia": ("vigilia III", "vigilia tertia"),
    "vigilia_quarta": ("vigilia IV", "vigilia quarta"),
}

# The Edo koku: key → (Japanese, English short, English full). The
# Japanese name stands in every language but the ones with their own
# column; the animal's hour is the branch's, as the wall calendars
# still print the 子の刻.
_EDO = {
    "ake_mutsu": ("明六つ", "dawn six", "dawn six, the hour of the Rabbit"),
    "asa_itsutsu": ("朝五つ", "morning five", "morning five, the hour of the Dragon"),
    "asa_yotsu": ("朝四つ", "morning four", "morning four, the hour of the Snake"),
    "hiru_kokonotsu": ("昼九つ", "noon nine", "noon nine, the hour of the Horse"),
    "hiru_yatsu": ("昼八つ", "day eight", "day eight, the hour of the Goat"),
    "yuu_nanatsu": ("夕七つ", "evening seven", "evening seven, the hour of the Monkey"),
    "kure_mutsu": ("暮六つ", "dusk six", "dusk six, the hour of the Rooster"),
    "yoru_itsutsu": ("夜五つ", "night five", "night five, the hour of the Dog"),
    "yoru_yotsu": ("夜四つ", "night four", "night four, the hour of the Pig"),
    "yoru_kokonotsu": ("夜九つ", "midnight nine", "midnight nine, the hour of the Rat"),
    "yoru_yatsu": ("夜八つ", "night eight", "night eight, the hour of the Ox"),
    "akatsuki_nanatsu": ("暁七つ", "daybreak seven", "daybreak seven, the hour of the Tiger"),
}

# The strings the hours line and the corner need beyond the names:
# "night" for the night hours, "in {dur}" for the countdown, and the
# unit the corner measures, "1h = 62m", where a system has its own.
_HOURS_STRINGS = {
    "en": {"night": "night", "in_time": "in {dur}", "koku": "1 koku"},
    "fr": {"night": "nuit", "in_time": "dans {dur}"},
    "es": {"night": "noche", "in_time": "en {dur}"},
    "de": {"night": "Nacht", "in_time": "in {dur}"},
    "it": {"night": "notte", "in_time": "tra {dur}"},
    "pt": {"night": "noite", "in_time": "em {dur}"},
    "nl": {"night": "nacht", "in_time": "over {dur}"},
    "pl": {"night": "noc", "in_time": "za {dur}"},
    "no": {"night": "natt", "in_time": "om {dur}"},
    "sv": {"night": "natt", "in_time": "om {dur}"},
    "is": {"night": "nótt", "in_time": "eftir {dur}"},
    "da": {"night": "nat", "in_time": "om {dur}"},
    "fi": {"night": "yö", "in_time": "{dur} kuluttua"},
    "ja": {"night": "夜", "in_time": "{dur}後", "koku": "1刻"},
    "ko": {"night": "밤", "in_time": "{dur} 후"},
    "zh": {"night": "夜", "in_time": "{dur}后"},
    "th": {"night": "กลางคืน", "in_time": "อีก {dur}"},
    "id": {"night": "malam", "in_time": "dalam {dur}"},
    "uk": {"night": "ніч", "in_time": "через {dur}"},
    "vi": {"night": "đêm", "in_time": "còn {dur}"},
}

# The sunrise and sunset marks read in the language's own words, since
# the line above the marks names them too; the rest are names.
_SUN_KEYS = {"sunrise": "sunrise", "sunset": "sunset"}


def hs(key, runtime, **kwargs):
    """A string of the hours line's own."""
    return lookup(_HOURS_STRINGS, key, lang_of(runtime), **kwargs)


def mark_name(system, key, runtime, short=False):
    """The name of a mark in the display language."""
    if key in _SUN_KEYS:
        from linecast._sunshine_i18n import sky_event
        return sky_event(_SUN_KEYS[key], runtime)
    if system == "halachic":
        short_name, full, _hebrew = _ZMANIM[key]
        return short_name if short else full
    if system == "roman":
        short_name, full = _ROMAN[key]
        return short_name if short else full
    if system == "japanese":
        japanese, short_name, full = _EDO[key]
        if lang_of(runtime) == "ja":
            return japanese
        return short_name if short else full
    return key


def mark_native(system, key):
    """The name in the tradition's own script, for `--json`: the Hebrew
    of a zman. None where the display name already is it."""
    if system == "halachic":
        return _ZMANIM[key][2]
    if system == "japanese":
        return _EDO[key][0]
    return None


def unit_name(system, runtime, night=False):
    """What the corner calls one of the system's hours: '1h', '1刻', or
    at Rome by night '1 vigilia'."""
    if system == "japanese":
        return hs("koku", runtime)
    if system == "roman" and night:
        return "1 vigilia"
    return "1h"


def reading_name(system, r, runtime):
    """The reading of a moment in the system's own terms: '4:20' of the
    halachic hours, 'night 4:20' after sunset; 'hora quarta'; '昼四つ半'."""
    if system == "roman":
        from linecast._hours.roman import hour_name
        return hour_name(r, runtime)
    if system == "japanese":
        from linecast._hours.wadokei import koku_name
        return koku_name(r, runtime)
    clock = f"{r.index}:{int(r.fraction * 60):02d}"
    return f"{hs('night', runtime)} {clock}" if r.night else clock


def variant_name(system, variant):
    """What the table's opinion or method is called."""
    if system == "halachic":
        from linecast._hours.zmanim import OPINION_NAMES
        return OPINION_NAMES.get(variant)
    return variant
