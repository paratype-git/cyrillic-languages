# Cyrillic languages — language-tag table

All 79 languages declared in `cyrillic-languages/library/cyrillic/cyrillic_library.json`, with the identifier fields we know today and placeholders for the external tag systems we have not yet filled in. Re-generated from [`tools/generate_language_tags.py`](tools/generate_language_tags.py).

**Columns:**

- **name_eng / name_rus** — from `cyrillic_library.json`.
- **code_pt** — Paratype's internal per-language identifier.
- **enable** — whether the language is currently compiled by the pipeline.
- **local** — OT `locl` tag used as the source file's default (blank = inherits script default, which is `ru` for this library).
- **iso639_1 / iso639_3 / bcp47 / ot_lang** — external tag systems. Values come from `tools/language_tags_enrichment.json`; `null`/`—` means the system has no code for this language.
- **confidence** — `high` = standard well-known codes; `medium` / `low` flag rows where the pick involved a judgement call (macrolanguages, dialect variants, provisional codes). See the `note` field in the JSON for per-row rationale.

| # | name_eng | name_rus | code_pt | enable | local | iso639_1 | iso639_3 | bcp47 | ot_lang | conf |
| ---: | --- | --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | Abazin | Абазинский | 1 | yes | ru | — | abq | abq | `ABA ` | high |
| 2 | Abkhazian | Абхазский | 90 | yes | ru | ab | abk | ab | `ABK ` | high |
| 3 | Avar | Аварский | 5 | yes | ru | av | ava | av | `AVR ` | high |
| 4 | Aghul | Агульский | 147 | yes | ru | — | agx | agx | `AGU ` | high |
| 5 | Adyge | Адыгейский | 2 | yes | ru | — | ady | ady | `ADY ` | high |
| 6 | Azeri | Азербайджанский | 6 | yes | ru | az | aze | az | `AZE ` | high |
| 7 | Altaic (Oirot) | Алтайский | 92 | yes | ru | — | alt | alt | `ALT ` | high |
| 8 | Bashkir | Башкирский | 8 | yes | ba | ba | bak | ba | `BSH ` | high |
| 9 | Belarusian | Белорусский | 9 | yes | ru | be | bel | be | `BEL ` | high |
| 10 | Bulgarian | Болгарский | 11 | yes | bg | bg | bul | bg | `BGR ` | high |
| 11 | Buryat | Бурятский | 12 | yes | ru | — | bua | bua | `BUR ` | medium |
| 12 | Gagauz | Гагаузский | 105 | yes | ru | — | gag | gag | `GAG ` | high |
| 13 | Dargwa | Даргинский | 18 | yes | ru | — | dar | dar | `DAR ` | high |
| 14 | Dolgan | Долганский | 148 | yes | ru | — | dlg | dlg | `—` | high |
| 15 | Dungan | Дунганский | 20 | yes | ru | — | dng | dng | `—` | high |
| 16 | Ingush | Ингушский | 34 | yes | ru | — | inh | inh | `ING ` | high |
| 17 | Itelmen | Ительменский | 146 | yes | ru | — | itl | itl | `—` | high |
| 18 | Kabardino-Cirkassian | Кабардино-Черкесский | 37 | yes | ru | — | kbd | kbd | `KAB ` | medium |
| 19 | Kabardian | Кабардинский | 136 | yes | ru | — | kbd | kbd | `KAB ` | high |
| 20 | Kazakh | Казахский | 40 | yes | ru | kk | kaz | kk | `KAZ ` | high |
| 21 | Kaitag | Кайтагский | 161 | yes | ru | — | xdq | xdq | `—` | low |
| 22 | Kalmyk | Калмыцкий | 38 | yes | ru | — | xal | xal | `KLM ` | high |
| 23 | Karakalpak | Каракалпакский | 39 | yes | ru | — | kaa | kaa | `KRK ` | high |
| 24 | Karachay-Balkar | Карачаево-Балкарский | 114 | yes | ru | — | krc | krc | `KAR ` | high |
| 25 | Saami Kildin | Кильдинский | 116 | yes | ru | — | sjd | sjd | `KSM ` | high |
| 26 | Kirghiz | Киргизский | 41 | yes | ru | ky | kir | ky | `KIR ` | high |
| 27 | Komi-Zyrian | Коми-зырянский | 112 | yes | ru | — | kpv | kpv | `KOZ ` | high |
| 28 | Komi-Permyak | Коми-пермяцкий | 111 | yes | ru | — | koi | koi | `KOP ` | high |
| 29 | Koryak | Корякский | 113 | yes | ru | — | kpy | kpy | `—` | high |
| 30 | Kryashen Tatar | Кряшенский | 135 | yes | ru | — | tat | tat | `TAT ` | low |
| 31 | Kumyk | Кумыкский | 42 | yes | ru | — | kum | kum | `KUM ` | high |
| 32 | Kurdish | Курдский | 142 | yes | ru | ku | kur | ku | `KUR ` | medium |
| 33 | Lak | Лакский | 44 | yes | ru | — | lbe | lbe | `LAK ` | high |
| 34 | Lezgin | Лезгинский | 46 | yes | ru | — | lez | lez | `LEZ ` | high |
| 35 | Macedonian | Македонский | 48 | yes | sr | mk | mkd | mk | `MKD ` | high |
| 36 | Manci | Мансийский | 121 | yes | ru | — | mns | mns | `MAN ` | high |
| 37 | Mari-high | Марийский (горный) | 122 | yes | ru | — | mrj | mrj | `HMA ` | high |
| 38 | Mari-low | Марийский (луговой) | 118 | yes | ru | — | mhr | mhr | `LMA ` | high |
| 39 | Moldavian | Молдавский | 50 | yes | ru | ro | ron | ro-MD | `MOL ` | high |
| 40 | Mongolian | Монгольский | 51 | yes | ru | mn | mon | mn | `MNG ` | high |
| 41 | Mordvin-Moksha | Мордовско-Мокшанский | 53 | yes | ru | — | mdf | mdf | `MOK ` | high |
| 42 | Mordvin-Erzya | Мордовско-Эрзянский | 52 | yes | ru | — | myv | myv | `ERZ ` | high |
| 43 | Nanai | Нанайский | 54 | yes | ru | — | gld | gld | `—` | high |
| 44 | Nganasan | Нганасанский | 149 | yes | ru | — | nio | nio | `—` | high |
| 45 | Negidal | Негидальский | 159 | yes | ru | — | neg | neg | `—` | high |
| 46 | Nenets (Yurak) | Ненецкий | 55 | yes | ru | — | yrk | yrk | `—` | high |
| 47 | Nivkh | Нивхский | 56 | yes | ru | — | niv | niv | `—` | high |
| 48 | Nogai | Ногайский | 57 | yes | ru | — | nog | nog | `NOG ` | high |
| 49 | Ossetic | Осетинский | 123 | yes | ru | os | oss | os | `OSS ` | high |
| 50 | Russian | Русский | 64 | yes | ru | ru | rus | ru | `RUS ` | high |
| 51 | Rutul | Рутульский | 151 | yes | ru | — | rut | rut | `—` | high |
| 52 | Selkup | Селькупский | 65 | yes | ru | — | sel | sel | `—` | high |
| 53 | Serbian | Сербский | 66 | yes | sr | sr | srp | sr | `SRB ` | high |
| 54 | Tabasaran | Табасаранский | 73 | yes | ru | — | tab | tab | `TAB ` | high |
| 55 | Tadzhik | Таджикский | 85 | yes | ru | tg | tgk | tg | `TAJ ` | high |
| 56 | Talysh | Талышский | 137 | yes | ru | — | tly | tly | `—` | high |
| 57 | Tatar | Татарский | 74 | yes | ru | tt | tat | tt | `TAT ` | high |
| 58 | Tat | Татский | 144 | yes | ru | — | ttt | ttt | `—` | medium |
| 59 | Tofalar | Тофаларский | 134 | yes | ru | — | kim | kim | `—` | medium |
| 60 | Touva (Soyot) | Тувинский | 77 | yes | ru | — | tyv | tyv | `TUV ` | high |
| 61 | Turkmen | Туркменский | 76 | yes | ru | tk | tuk | tk | `TKM ` | high |
| 62 | Udmurt | Удмуртский | 129 | yes | ru | — | udm | udm | `UDM ` | high |
| 63 | Uzbek | Узбекский | 81 | yes | ru | uz | uzb | uz | `UZB ` | high |
| 64 | Uighur | Уйгурский | 78 | yes | ru | ug | uig | ug | `UYG ` | high |
| 65 | Ukrainian | Украинский | 79 | yes | ru | uk | ukr | uk | `UKR ` | high |
| 66 | Ulch | Ульчский | 160 | yes | ru | — | ulc | ulc | `—` | high |
| 67 | Khakass | Хакасский | 110 | yes | ru | — | kjh | kjh | `KHK ` | medium |
| 68 | Khanty | Хантыйский | 109 | yes | ru | — | kca | kca | `—` | low |
| 69 | Tsakhur | Цахурский | 152 | yes | ru | — | tkr | tkr | `—` | high |
| 70 | Chechen | Чеченский | 14 | yes | ru | ce | che | ce | `CHE ` | high |
| 71 | Chuvash | Чувашский | 97 | yes | cv | cv | chv | cv | `CHU ` | high |
| 72 | Chukchi | Чукотский | 98 | yes | ru | — | ckt | ckt | `CHK ` | medium |
| 73 | Shor | Шорский | 133 | yes | ru | — | cjs | cjs | `—` | high |
| 74 | Evenki (Tungus) | Эвенкийский | 102 | yes | ru | — | evn | evn | `EVK ` | high |
| 75 | Even (Lamut) | Эвенский | 101 | yes | ru | — | eve | eve | `EVN ` | high |
| 76 | Enets | Энецкий | 150 | yes | ru | — | enf | enf | `—` | medium |
| 77 | Eskimo (Yupik) | Эскимосский | 100 | yes | ru | — | ess | ess | `—` | high |
| 78 | Yukagir | Юкагирский | 158 | yes | ru | — | ykg | ykg | `—` | medium |
| 79 | Yakut | Якутский | 130 | yes | ru | — | sah | sah | `YAK ` | high |

