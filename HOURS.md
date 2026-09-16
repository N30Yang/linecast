# The sun's hours

`linecast sunshine` can read the day in a tradition's hours beside the civil clock. This page says what each system shows, how linecast computes it, and what it was checked against.

## Choosing one

`linecast sunshine --hours halachic` reads the day in one for a single run, and `linecast hours halachic` saves it for every run. `linecast hours none` turns it off and `linecast hours auto` clears the setting. No language brings a system of hours with it, so `auto` and `none` read the same. The names are `halachic`, `halachic-mga`, `roman`, `japanese`, and `islamic`, with a convention or a school after a hyphen for the last: `islamic-isna`, `islamic-hanafi`.

With a system on, the day view's top-left corner reads the shown moment in that system's terms, with the length of the hour in force beside it, and a line under the sunrise and sunset lists the day's marks in order. The marks already past are dim, the next is in the text colour with a countdown, and the rest are muted. The line keeps as many marks as fit the window, the next first; sunrise and sunset go last, since the line above names them. Scrolling the day with the wheel moves both. `--json` carries the same facts in an `hours` block, with each mark's name in the tradition's own script where it has one, and `--oneline` ends with the reading.

## What they have in common

Every one of these systems is the same shape. A day has two edges set by the Sun, the time between them is divided into a fixed number of equal parts, and named marks fall along it. The night, from one day's end to the next day's start, is divided the same way. Only the edges, the count, and the names differ. The moment the Sun reaches a given depression below the horizon, rising or setting, is found by bisection over the same ephemeris the moon and the sky use, and sunrise and sunset are the Sun's upper limb, refracted, 0.833° below the horizon, at sea level, as the published tables keep them.

## Halachic

`halachic` reads the day in sha'ot zmaniyot, the proportional hours of halacha: a twelfth of the day, sunrise to sunset, by the Gr"a, the Vilna Gaon. `halachic-mga` reads it by the Magen Avraham, whose day runs from alot hashachar to tzeit hakochavim, dawn to nightfall, taken as seventy-two minutes before sunrise and after sunset, the time to walk four mil. The night is twelve hours the same way, sunset to sunrise. The corner reads "4:20" for four hours and twenty sixtieths into the day, or "night 4:20" after sunset, with the hour's length beside it: 43 minutes in a December night, 74 on a June day.

The marks are fractions of that day: the latest Shema at three hours, the latest Tefillah at four, chatzot at six, mincha gedola at six and a half, mincha ketana at nine and a half, plag hamincha at ten and three quarters. Around them sit the moments read off the Sun's depression: alot hashachar at 16.1°, misheyakir at 11.5°, tzeit at 8.5°, the three small stars, and candle lighting eighteen minutes before sunset on Friday. Chatzot halayla, the middle of the night, is listed on the date it falls on. Where the Sun never gets 16.1° down, as at 60° north in June, alot, misheyakir, and tzeit are left out and the day's fractions stand.

The angles are the ones [Hebcal](https://www.hebcal.com/) and the [KosherJava](https://kosherjava.com/) library publish. The tests pin four places on four dates of 2026 against Hebcal's zmanim API, read to the second: Jerusalem, Brooklyn, Helsinki, and Melbourne on the March equinox week, both solstices, and mid-September. Every zman lands within half a minute, most within five seconds. Hebcal's output is licensed CC BY 4.0. The names are transliterated in every language, as the Hebrew months are in the moon's calendar, and `--json` adds each in Hebrew letters.

Customs differ in the angles and the minutes, and a community's own luach is the authority. This is the common reckoning, offered as the printed tables offer it.

## Roman

`roman` reads the day as Rome did: twelve horae from sunrise to sunset, and four vigiliae, the watches, from sunset to sunrise. An hour in Rome runs about forty-five minutes at the December solstice and seventy-five at the June one, and a watch about three hours the year round. The hours count from sunrise, so hora sexta ends at noon and hora nona is mid-afternoon, and the church's terce, sext, and none took their names from the third, sixth, and ninth. The corner reads "hora quarta" by day and "vigilia secunda" by night, with the length of the hour or the watch beside it.

The marks are the ones a Roman named: sunrise, hora tertia, hora sexta, hora nona, sunset, and the second, third, and fourth watches, the third opening at media nox, the middle of the night. Latin is Latin in every language. There is nothing to check this against but the arithmetic; the tests confirm the forty-five and seventy-five minute hours at Rome's latitude.

## Japanese

`japanese` reads the day by 不定時法, the hours Japan kept until 1873 and the wadokei were built to strike: six koku from dawn to dusk and six from dusk to dawn, each named by its bells and the earthly branch of its hour. The count runs 明六つ, 朝五つ, 朝四つ, 昼九つ at noon, 昼八つ, 夕七つ, then 暮六つ at dusk, 夜五つ, 夜四つ, 夜九つ at midnight, 夜八つ, and 暁七つ. Nine was the auspicious number and each bell after it dropped one. The corner reads the koku and its half, 昼四つ半, with the koku's length beside it: over two and a half hours on a June day in Tokyo, under two in December.

The day's edges are not sunrise and sunset but 明六つ and 暮六つ, dawn and dusk. The Jōkyō calendar fixed them at two and a half koku, thirty-six minutes, either side of sunrise and sunset; the Kansei calendar of 1798 replaced that with the Sun's centre 7°21′40″ below the horizon, the depression reached at Kyoto thirty-six minutes before sunrise at the equinoxes, and the Tenpō calendar kept it. The [National Astronomical Observatory](https://eco.mtk.nao.ac.jp/koyomi/wiki/C7F6CCC02FCCEBCCC0A4C8C6FCCAEB.html) still prints 夜明 and 日暮 by that angle, with a note that they answer to the old 明六つ and 暮六つ, and the tests check Tokyo's dawn and dusk on the equinox and both solstices against its calculator, which prints whole minutes; every one is within a minute.

Japanese keeps its own words. The other languages get the count and the time of day, "morning four", with the animal's hour in the full name, and `--json` carries the kanji beside them.

## Islamic

`islamic` reads the day by the prayer times: Fajr at dawn, sunrise, Dhuhr at the Sun's transit, Asr when a shadow has grown by the length of its object, Maghrib at sunset, and Isha at nightfall. There are no equal hours in it, so the corner names the prayer just past and the one to come with its countdown, "Asr · Maghrib in 1h 12m", and in Ramadan, while the fast runs, how far into it the moment is and how long to iftar. Imsak, ten minutes before Fajr, is listed in Ramadan.

Fajr and Isha are read off the Sun's depression, and the angle varies by convention. The conventions are the ones the prayer-time apps offer, each named for the body that published it, and the method follows the country of the place shown, as the week's first day does: ISNA's 15° and 15° in the United States and Canada, the Egyptian General Authority's 19.5° and 17.5° in Egypt and its neighbours, Umm al-Qura's 18.5° and ninety minutes after Maghrib, a hundred and twenty in Ramadan, in Saudi Arabia and the Gulf, the University of Islamic Sciences' 18° and 18° in Pakistan, India, Bangladesh, and Afghanistan, the University of Tehran's in Iran, the Diyanet's in Turkey with the minutes of caution it prints, MUIS's in Singapore, JAKIM's in Malaysia, Kemenag's in Indonesia, the UOIF's 12° and 12° in France, the Spiritual Administration's in Russia, and the Muslim World League's 18° and 17° everywhere else. `linecast hours islamic-isna`, or any of `-mwl`, `-egypt`, `-makkah`, `-karachi`, `-tehran`, `-turkey`, `-singapore`, `-jakim`, `-kemenag`, `-france`, and `-russia`, pins a convention wherever you are. The frame names the one in force.

Asr follows the school. Most print the shadow of one length; the Hanafi school waits for two, and that is the Asr listed in Turkey, South and Central Asia, the Balkans, Russia, and China. `islamic-hanafi` and `islamic-shafii` choose the school and keep the country's method.

Where the Sun never reaches the angle, as in a Nordic June, the angle-based rule stands in, the one PrayTimes and Aladhan apply by default: Fajr is as far before sunrise, and Isha as far after sunset, as the angle's share of a sixty-degree night.

The tests check eight places on four dates of 2026 against the [Aladhan](https://aladhan.com/prayer-times-api) API, each by its own country's method: Makkah, Cairo, Dearborn, London, Karachi with the Hanafi Asr, Jakarta, Istanbul, and Oslo. Fajr, sunrise, Dhuhr, Maghrib, and Isha land within a minute. Asr is held to four: Aladhan's port of the PrayTimes formula drifts two or three minutes at high latitude near the equinoxes, and PrayTimes' own formula and this table agree within twenty seconds. The names are transliterated in every language, with Indonesian's own spellings, Subuh, Zuhur, Asar, Magrib, Isya, as the Hijri months have theirs, and `--json` adds the Arabic.

A mosque's card is the authority, and can differ from these by a minute or two: many publishers round Fajr down and Maghrib up for caution, and a country's own authority may publish angles the apps do not.
