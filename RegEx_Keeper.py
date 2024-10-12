import re

country_list = [
    "Germany",
    "Russia",
    "Ukrain",
    "France",
    "Turkey",
    "Czech",
    "Belarus",
    "Latvia",
    "Moldova",
    "Slovakia",
    "Canada",
    "Georgia",
    "Bosnia",
    "Serbia",
    "Macedonia",
    "Polska",
    "Bulgaria",
    "Romania",
    "Belgium",
    "Special",
    "Austria",
    "Algeria",
    "Azerbaijan",
    "Luxembourg",
    "Uzbekistan",
    "Lithuania",
    "Denmark",
    "Hungary",
    "Estonia",
    "United_Kingdom",
    "Netherlands",
    "Spain",
    "Sweden",
]

country_configuration = {
    "Germany": "Doitch",
    "Russia": "Russian",
    "Kazakhstan": "Russian",
    "Ukrain": "Russian",
    "France": "English",
    "Turkey": "Turkish",
    "Czech": "Russian",
    "Belarus": "Russian",
    "Latvia": "English",
    "Moldova": "Russian",
    "Slovakia": "English",
    "Serbia": "English",
    "Bosnia": "English",
    "Polska": "English",
    "Macedonia": "English",
    "Canada": "English",
    "Georgia": "English",
    "Bulgaria": "English",
    "Romania": "English",
    "Belgium": "English",
    "Special": "Special",
    "Austria": "English",
    "Algeria": "English",
    "Azerbaijan": "Russian",
    "Luxembourg": "Doitch",
    "Uzbekistan": "Russian",
    "Lithuania": "English",
    "Denmark": "Russian",
    "Hungary": "English",
    "Estonia": "English",
    "United_Kingdom": "English",
    "Netherlands": "English",
    "Spain": "English",
    "Sweden": "English",
}
num_checker = re.compile(
    r"""
        (?P<Germany>\+49)\s*(?:\((\d{3})\)\s*|\d{1,4}\s*)\d{1,8}(?:[\s-]\d{1,8})* |
        (?P<Russia>\+7)\s*?(\d{3})\s*?(\d{3})(\d{2})(\d{2}) |
        (?P<Ukrain>\+380)(\d{2})(\d{3})(\d{2})(\d{2}) |
        (?P<France>\+33)(\d{1})(\d{1,2})(\d{1,2})(\d{2})(\d{2})(\d{2}) |
        (?P<Turkey>\+90)(\d{3})(\d{3})(\d{2})(\d{2}) |
        (?P<Czech>\+420)(\d{3})(\d{3})(\d{3}) |
        (?P<Belarus>\+375)(\d{1,2})(\d{6,7}) |
        (?P<Latvia>\+371)(\d{1,3})(\d{5}) |
        (?P<Moldova>\+373)(\d{2})(\d{5,7}) |
        (?P<Slovakia>\+421)(\d{3})(\d{3})(\d{3}) |
        (?P<Canada>\+1)(\d{3})(\d{3})(\d{4}) |
        (?P<Georgia>\+995)(\d{2,3})(\d{6}) |
        (?P<Bosnia>\+387)(\d{2})(\d{6}) |
        (?P<Serbia>\+381)(\d{2})(\d{7}) |
        (?P<Macedonia>\+389)(\d{1,2})(\d{6}) |
        (?P<Polska>\+48)(\d{2,3})(\d{6}) |
        (?P<Bulgaria>\+359)(\d{1,2})(\d{6,7}) |
        (?P<Romania>\+40)(\d{2,3})(\d{6,7}) |
        (?P<Belgium>\+32)(\d{1,3})(\d{6,7}) |
        (?P<Special>\+7)\s*?(\d{3})\s*?(\d{3})(\d{2})(\d{2})[special] |
        (?P<Austria>\+43)(\d{1,3})(\d{3,4})(\d{3,4}) |
        (?P<Algeria>\+213)(\d{3})(\d{2})(\d{2})(\d{2}) |
        (?P<Azerbaijan>\+994)(\d{2})(\d{6,7}) |
        (?P<Luxembourg>\+352)(\d{4})(\d{4,5}) |
        (?P<Uzbekistan>\+998)(90)(\d{3})(\d{2})(\d{2}) |
        (?P<Lithuania>\+370)(6)(\d{2})(\d{3})(\d{2}) |
        (?P<Denmark>\+45)(\d{2})(\d{2})(\d{2})(\d{2}) |
        (?P<Hungary>\+36)(1|20|30)(\d{3,4})(\d{4,5}) |
        (?P<Estonia>\+372)(\d{2}|\d{3})(\d{3})(\d{3}) |
        (?P<United_Kingdom>\+44)(\d{1,2})(\d{4})(\d{4}) |
        (?P<Netherlands>\+31)(6|20)(\d{7,8}) |
        (?P<Spain>\+34)(\d{2,3})(\d{3})(\d{3}) |
        (?P<Sweden>\+46)(\d{2})(\d{3})(\d{2})(\d{2})
        """,
    re.X | re.I,
)
