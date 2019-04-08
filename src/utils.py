TIERS = [
    1,
    2,
    3,
    4
]

CHAR_TIERS = {
    'Hot Pie': 4,
    'Jon Snow': 3,
    'Sansa Stark': 3,
    'Arya Stark': 3,
    'Bran Stark': 3,
    'Cersei Lannister': 3,
    'Jaime Lannister': 3,
    'Tyrion Lannister': 3,
    'Daenerys Targaryen': 3,
    'Night King': 3,
    'Yara Greyjoy': 2,
    'Theon Greyjoy': 2,
    'Melisandre': 2,
    'Jorah Mormont': 2,
    'The Hound': 2,
    'The Mountain': 2,
    'Samwell Tarly': 2,
    'Varys': 2,
    'Brienne of Tarth': 2,
    'Davos Seaworth': 2,
    'Tormund Giantsbane': 2,
    'Grey Worm': 2,
    'Missandei': 2,
    'Euron Greyjoy': 2,
    'Drogon': 2,
    'Rheagal': 2,
    'Gendry': 2,
    'Qyburn': 1,
    'Gilly': 1,
    'Sam (child)': 1,
    'Bronn': 1,
    'Podrick Payne': 1,
    'Beric Dondarrion': 1,
    'Ghost': 1,
    'Lyanna Mormont': 1,
    'Eddison Tollet': 1,
    'Edmure Tully': 1,
    'Meera Reed': 1,
    'Nymeria': 1,
    'Robin Arryn': 1
}

CHAR_NAMES = {
    tier: sorted([
        char_name for char_name in CHAR_TIERS
        if CHAR_TIERS[char_name] == tier
    ])
    for tier in TIERS
}
