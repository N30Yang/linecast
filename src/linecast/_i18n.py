"""The lookup shared by the per-command string tables.

Each command keeps its own table, {lang: {key: text}}; this module holds
the one way of reading them, so the fallback order lives in one place.
"""

import re

# The languages linecast speaks, as (code, English name), in the order the
# README lists them. Every per-command table has an entry for each; the
# `linecast language` command and the help page take their list from here.
LANGUAGES = (
    ("en", "English"), ("fr", "French"), ("es", "Spanish"), ("de", "German"),
    ("it", "Italian"), ("pt", "Portuguese"), ("nl", "Dutch"), ("pl", "Polish"),
    ("no", "Norwegian"), ("sv", "Swedish"), ("is", "Icelandic"), ("da", "Danish"),
    ("fi", "Finnish"), ("ja", "Japanese"), ("ko", "Korean"),
    ("zh", "Simplified Chinese"), ("zh-Hant", "Traditional Chinese"),
    ("th", "Thai"), ("id", "Indonesian"), ("uk", "Ukrainian"),
    ("vi", "Vietnamese"), ("eo", "Esperanto"), ("tr", "Turkish"),
)
LANGUAGE_CODES = tuple(code for code, _name in LANGUAGES)
LANGUAGE_NAMES = dict(LANGUAGES)

# Codes that name a language above by another name, lower-cased.  A
# Norwegian machine's locale is nb_NO or nn_NO (glibc has no no_NO), and
# the strings are Bokmål, so both read as "no".  Chinese is two scripts:
# Taiwan, Hong Kong, and Macau write the traditional characters, so their
# locales name zh-Hant, and the mainland's and Singapore's the simplified.
LANGUAGE_ALIASES = {
    "nb": "no", "nn": "no",
    "zh-hant": "zh-Hant", "zh-tw": "zh-Hant", "zh-hk": "zh-Hant", "zh-mo": "zh-Hant",
    "zh-hans": "zh", "zh-cn": "zh", "zh-sg": "zh",
}

# A language whose strings are another's in a different script: the moon's
# Chinese calendar and the Chinese sky come with zh-Hant as they do with zh.
SCRIPT_OF = {"zh-Hant": "zh"}


def canonical_language(code):
    """`code` as the tables know it: an alias resolved, else unchanged."""
    return LANGUAGE_ALIASES.get(code.lower(), code)


def is_language_code(value):
    """A language code linecast could act on, whether or not it has strings
    for it: two letters, two letters and a script (zh-Hant), or an alias
    of one.  An unlisted code leaves the app in English and still reaches
    the providers that publish in it, as India's alerts do."""
    if not isinstance(value, str) or not value.isascii():
        return False
    return (re.fullmatch(r"[A-Za-z]{2}(-[A-Za-z]{4})?", value) is not None
            or value.lower() in LANGUAGE_ALIASES)


# What the geocoders call a language, where it is not linecast's code.
# Open-Meteo's index knows the traditional script by Taiwan's tag and
# answers "zh-Hant" in English; Nominatim reads an Accept-Language list,
# so it gets the script, the regions that write it, and Chinese at all.
_GEOCODER_LANG = {"zh-Hant": "zh-TW"}
_ACCEPT_LANGUAGE = {"zh-Hant": "zh-Hant,zh-TW,zh-HK,zh"}


def geocoder_language(lang):
    """`lang` as the Open-Meteo geocoder's `language` parameter."""
    return _GEOCODER_LANG.get(lang, lang)


def accept_language(lang):
    """`lang` as an Accept-Language value for Nominatim."""
    return _ACCEPT_LANGUAGE.get(lang, lang)


def same_language(lang, other):
    """Whether `lang` is `other` or `other` in another script: zh-Hant
    reads as Chinese wherever the code, not the strings, decides."""
    return lang == other or SCRIPT_OF.get(lang) == other


def lang_of(runtime):
    """The runtime's language, or English when there is no runtime."""
    return getattr(runtime, "lang", "en") if runtime else "en"


# Languages that write the percent sign before the number: %40.
PERCENT_FIRST = frozenset({"tr"})


def fmt_percent(value, runtime):
    """`value` as a whole-number percentage the display language's way:
    "40%", or "%40" in Turkish."""
    text = f"{value:.0f}"
    return f"%{text}" if lang_of(runtime) in PERCENT_FIRST else f"{text}%"


def lookup(table, key, lang, **kwargs):
    """The text for `key` in `lang`, falling back to English and then to
    the key itself.  Formatted with kwargs only when some are given, so a
    text with literal braces survives a plain lookup."""
    english = table["en"]
    text = table.get(lang, english).get(key, english.get(key, key))
    return text.format(**kwargs) if kwargs else text
