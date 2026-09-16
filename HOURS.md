# The sun's hours

`linecast sunshine` can read the day in a tradition's hours beside the civil clock. This page says what each system shows, how linecast computes it, and what it was checked against.

## Choosing one

`linecast sunshine --hours halachic` reads the day in one for a single run, and `linecast hours halachic` saves it for every run. `linecast hours none` turns it off and `linecast hours auto` clears the setting. No language brings a system of hours with it, so `auto` and `none` read the same. The names are `halachic`, `halachic-mga`, `roman`, `japanese`, and `islamic`.

With a system on, the day view's top-left corner reads the shown moment in that system's terms, with the length of the hour in force beside it, and a line under the sunrise and sunset lists the day's marks in order. The marks already past are dim, the next is in the text colour with a countdown, and the rest are muted. The line keeps as many marks as fit the window, the next first; sunrise and sunset go last, since the line above names them. Scrolling the day with the wheel moves both. `--json` carries the same facts in an `hours` block, with each mark's name in the tradition's own script where it has one, and `--oneline` ends with the reading.

## What they have in common

Every one of these systems is the same shape. A day has two edges set by the Sun, the time between them is divided into a fixed number of equal parts, and named marks fall along it. The night, from one day's end to the next day's start, is divided the same way. Only the edges, the count, and the names differ. The moment the Sun reaches a given depression below the horizon, rising or setting, is found by bisection over the same ephemeris the moon and the sky use, and sunrise and sunset are the Sun's upper limb, refracted, 0.833° below the horizon, at sea level, as the published tables keep them.

## Halachic

`halachic` reads the day in sha'ot zmaniyot, the proportional hours of halacha: a twelfth of the day, sunrise to sunset, by the Gr"a, the Vilna Gaon. `halachic-mga` reads it by the Magen Avraham, whose day runs from alot hashachar to tzeit hakochavim, dawn to nightfall, taken as seventy-two minutes before sunrise and after sunset, the time to walk four mil. The night is twelve hours the same way, sunset to sunrise. The corner reads "4:20" for four hours and twenty sixtieths into the day, or "night 4:20" after sunset, with the hour's length beside it: 43 minutes in a December night, 74 on a June day.

The marks are fractions of that day: the latest Shema at three hours, the latest Tefillah at four, chatzot at six, mincha gedola at six and a half, mincha ketana at nine and a half, plag hamincha at ten and three quarters. Around them sit the moments read off the Sun's depression: alot hashachar at 16.1°, misheyakir at 11.5°, tzeit at 8.5°, the three small stars, and candle lighting eighteen minutes before sunset on Friday. Chatzot halayla, the middle of the night, is listed on the date it falls on. Where the Sun never gets 16.1° down, as at 60° north in June, alot, misheyakir, and tzeit are left out and the day's fractions stand.

The angles are the ones [Hebcal](https://www.hebcal.com/) and the [KosherJava](https://kosherjava.com/) library publish. The tests pin four places on four dates of 2026 against Hebcal's zmanim API, read to the second: Jerusalem, Brooklyn, Helsinki, and Melbourne on the March equinox week, both solstices, and mid-September. Every zman lands within half a minute, most within five seconds. Hebcal's output is licensed CC BY 4.0. The names are transliterated in every language, as the Hebrew months are in the moon's calendar, and `--json` adds each in Hebrew letters.

Customs differ in the angles and the minutes, and a community's own luach is the authority. This is the common reckoning, offered as the printed tables offer it.

## Roman, Japanese, and Islamic

These are the next tables over the same engine, and are not in this build yet: the twelve horae and four vigiliae of the Roman day, the six koku of the Edo day and night with their edges at the Sun 7°21′40″ below the horizon, and the prayer times from Fajr to Isha with the fast in Ramadan. Each will have its section here when it lands.
