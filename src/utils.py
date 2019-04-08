TIERS = [
    1,
    2,
    3
]

CHAR_TIERS = {
    'Jon Snow': 3,
    'Danaerys Targaryan': 3,
    'Hot Pie': 1
}

CHAR_NAMES = {
    tier: sorted([
        char_name for char_name in CHAR_TIERS
        if CHAR_TIERS[char_name] == tier
    ])
    for tier in TIERS
}
