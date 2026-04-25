# Cyrillic languages — language-tag table

All 79 languages declared in `cyrillic-languages/library/cyrillic/cyrillic_library.json`, with the identifier fields we know today and placeholders for the external tag systems we have not yet filled in. Re-generated from [`tools/generate_language_tags.py`](tools/generate_language_tags.py).

**Columns:**

- **name_eng / name_rus** — from `cyrillic_library.json`.
- **enable** — whether the language is currently compiled by the pipeline.
- **local** — OT `locl` tag used as the source file's default (blank = inherits script default, which is `ru` for this library).
- **iso639_1 / iso639_3 / bcp47 / ot_lang** — external tag systems. Values come from `tools/language_tags_enrichment.json`; `null`/`—` means the system has no code for this language.
- **confidence** — `high` = standard well-known codes; `medium` / `low` flag rows where the pick involved a judgement call (macrolanguages, dialect variants, provisional codes). See the `note` field in the JSON for per-row rationale.

| # | name_eng | name_rus | enable | local | iso639_1 | iso639_3 | bcp47 | ot_lang | conf |
| ---: | --- | --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | Abazin | Абазинский | yes | ru | — | abq | abq | `ABA ` | high |
| 2 | Abkhazian | Абхазский | yes | ru | ab | abk | ab | `ABK ` | high |
| 3 | Avar | Аварский | yes | ru | av | ava | av | `AVR ` | high |
| 4 | Aghul | Агульский | yes | ru | — | agx | agx | `AGU ` | high |
| 5 | Adyge | Адыгейский | yes | ru | — | ady | ady | `ADY ` | high |
| 6 | Azeri | Азербайджанский | yes | ru | az | aze | az | `AZE ` | high |
| 7 | Altaic (Oirot) | Алтайский | yes | ru | — | alt | alt | `ALT ` | high |
| 8 | Bashkir | Башкирский | yes | ba | ba | bak | ba | `BSH ` | high |
| 9 | Belarusian | Белорусский | yes | ru | be | bel | be | `BEL ` | high |
| 10 | Bulgarian | Болгарский | yes | bg | bg | bul | bg | `BGR ` | high |
| 11 | Buryat | Бурятский | yes | ru | — | bua | bua | `BUR ` | medium |
| 12 | Gagauz | Гагаузский | yes | ru | — | gag | gag | `GAG ` | high |
| 13 | Dargwa | Даргинский | yes | ru | — | dar | dar | `DAR ` | high |
| 14 | Dolgan | Долганский | yes | ru | — | dlg | dlg | `—` | high |
| 15 | Dungan | Дунганский | yes | ru | — | dng | dng | `—` | high |
| 16 | Ingush | Ингушский | yes | ru | — | inh | inh | `ING ` | high |
| 17 | Itelmen | Ительменский | yes | ru | — | itl | itl | `—` | high |
| 18 | Kabardino-Cirkassian | Кабардино-Черкесский | yes | ru | — | kbd | kbd | `KAB ` | medium |
| 19 | Kabardian | Кабардинский | yes | ru | — | kbd | kbd | `KAB ` | high |
| 20 | Kazakh | Казахский | yes | ru | kk | kaz | kk | `KAZ ` | high |
| 21 | Kaitag | Кайтагский | yes | ru | — | xdq | xdq | `—` | low |
| 22 | Kalmyk | Калмыцкий | yes | ru | — | xal | xal | `KLM ` | high |
| 23 | Karakalpak | Каракалпакский | yes | ru | — | kaa | kaa | `KRK ` | high |
| 24 | Karachay-Balkar | Карачаево-Балкарский | yes | ru | — | krc | krc | `KAR ` | high |
| 25 | Saami Kildin | Кильдинский | yes | ru | — | sjd | sjd | `KSM ` | high |
| 26 | Kirghiz | Киргизский | yes | ru | ky | kir | ky | `KIR ` | high |
| 27 | Komi-Zyrian | Коми-зырянский | yes | ru | — | kpv | kpv | `KOZ ` | high |
| 28 | Komi-Permyak | Коми-пермяцкий | yes | ru | — | koi | koi | `KOP ` | high |
| 29 | Koryak | Корякский | yes | ru | — | kpy | kpy | `—` | high |
| 30 | Kryashen Tatar | Кряшенский | yes | ru | — | tat | tat | `TAT ` | low |
| 31 | Kumyk | Кумыкский | yes | ru | — | kum | kum | `KUM ` | high |
| 32 | Kurdish | Курдский | yes | ru | ku | kur | ku | `KUR ` | medium |
| 33 | Lak | Лакский | yes | ru | — | lbe | lbe | `LAK ` | high |
| 34 | Lezgin | Лезгинский | yes | ru | — | lez | lez | `LEZ ` | high |
| 35 | Macedonian | Македонский | yes | sr | mk | mkd | mk | `MKD ` | high |
| 36 | Manci | Мансийский | yes | ru | — | mns | mns | `MAN ` | high |
| 37 | Mari-high | Марийский (горный) | yes | ru | — | mrj | mrj | `HMA ` | high |
| 38 | Mari-low | Марийский (луговой) | yes | ru | — | mhr | mhr | `LMA ` | high |
| 39 | Moldavian | Молдавский | yes | ru | ro | ron | ro-MD | `MOL ` | high |
| 40 | Mongolian | Монгольский | yes | ru | mn | mon | mn | `MNG ` | high |
| 41 | Mordvin-Moksha | Мордовско-Мокшанский | yes | ru | — | mdf | mdf | `MOK ` | high |
| 42 | Mordvin-Erzya | Мордовско-Эрзянский | yes | ru | — | myv | myv | `ERZ ` | high |
| 43 | Nanai | Нанайский | yes | ru | — | gld | gld | `—` | high |
| 44 | Nganasan | Нганасанский | yes | ru | — | nio | nio | `—` | high |
| 45 | Negidal | Негидальский | yes | ru | — | neg | neg | `—` | high |
| 46 | Nenets (Yurak) | Ненецкий | yes | ru | — | yrk | yrk | `—` | high |
| 47 | Nivkh | Нивхский | yes | ru | — | niv | niv | `—` | high |
| 48 | Nogai | Ногайский | yes | ru | — | nog | nog | `NOG ` | high |
| 49 | Ossetic | Осетинский | yes | ru | os | oss | os | `OSS ` | high |
| 50 | Russian | Русский | yes | ru | ru | rus | ru | `RUS ` | high |
| 51 | Rutul | Рутульский | yes | ru | — | rut | rut | `—` | high |
| 52 | Selkup | Селькупский | yes | ru | — | sel | sel | `—` | high |
| 53 | Serbian | Сербский | yes | sr | sr | srp | sr | `SRB ` | high |
| 54 | Tabasaran | Табасаранский | yes | ru | — | tab | tab | `TAB ` | high |
| 55 | Tadzhik | Таджикский | yes | ru | tg | tgk | tg | `TAJ ` | high |
| 56 | Talysh | Талышский | yes | ru | — | tly | tly | `—` | high |
| 57 | Tatar | Татарский | yes | ru | tt | tat | tt | `TAT ` | high |
| 58 | Tat | Татский | yes | ru | — | ttt | ttt | `—` | medium |
| 59 | Tofalar | Тофаларский | yes | ru | — | kim | kim | `—` | medium |
| 60 | Touva (Soyot) | Тувинский | yes | ru | — | tyv | tyv | `TUV ` | high |
| 61 | Turkmen | Туркменский | yes | ru | tk | tuk | tk | `TKM ` | high |
| 62 | Udmurt | Удмуртский | yes | ru | — | udm | udm | `UDM ` | high |
| 63 | Uzbek | Узбекский | yes | ru | uz | uzb | uz | `UZB ` | high |
| 64 | Uighur | Уйгурский | yes | ru | ug | uig | ug | `UYG ` | high |
| 65 | Ukrainian | Украинский | yes | ru | uk | ukr | uk | `UKR ` | high |
| 66 | Ulch | Ульчский | yes | ru | — | ulc | ulc | `—` | high |
| 67 | Khakass | Хакасский | yes | ru | — | kjh | kjh | `KHK ` | medium |
| 68 | Khanty | Хантыйский | yes | ru | — | kca | kca | `—` | low |
| 69 | Tsakhur | Цахурский | yes | ru | — | tkr | tkr | `—` | high |
| 70 | Chechen | Чеченский | yes | ru | ce | che | ce | `CHE ` | high |
| 71 | Chuvash | Чувашский | yes | cv | cv | chv | cv | `CHU ` | high |
| 72 | Chukchi | Чукотский | yes | ru | — | ckt | ckt | `CHK ` | medium |
| 73 | Shor | Шорский | yes | ru | — | cjs | cjs | `—` | high |
| 74 | Evenki (Tungus) | Эвенкийский | yes | ru | — | evn | evn | `EVK ` | high |
| 75 | Even (Lamut) | Эвенский | yes | ru | — | eve | eve | `EVN ` | high |
| 76 | Enets | Энецкий | yes | ru | — | enf | enf | `—` | medium |
| 77 | Eskimo (Yupik) | Эскимосский | yes | ru | — | ess | ess | `—` | high |
| 78 | Yukagir | Юкагирский | yes | ru | — | ykg | ykg | `—` | medium |
| 79 | Yakut | Якутский | yes | ru | — | sah | sah | `YAK ` | high |

